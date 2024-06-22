from fastapi import APIRouter, Path, Body
from trades import StrategyType, PlatformType, TimeFrameType
from pydantic import BaseModel
import hashlib
import json
from fastapi.responses import JSONResponse
from trades import session, Trade
from sqlalchemy import delete, insert, update
from sqlalchemy.exc import SQLAlchemyError
from log import get_logger

log = get_logger('bot_api')
router = APIRouter()

def hash(block):
    encoded_block = json.dumps(block, sort_keys=True).encode()
    return hashlib.sha256(encoded_block).hexdigest()

class TradeBase(BaseModel):
    api_key: str
    secret_key: str
    platform: PlatformType
    strategy: StrategyType
    coin: str
    timeframe: TimeFrameType
    balance: float
    take_profit: float
    stop_loss: float
    rsi_period: float = None
    macd_fast: float = None
    macd_slow: float = None
    macd_signal: float = None
    minimum_volume: float = None

    class Config:
        schema_extra = {
            "example": {
                "api_key": "your_api_key",
                "secret_key": "your_secret_key",
                "platform": "Binance",
                "strategy": "Technical",
                "coin": "BTC",
                "timeframe": "1m",
                "balance": 1000.0,
                "take_profit": 0.02,
                "stop_loss": 0.01,
                "rsi_period": 14,
                "macd_fast": 12,
                "macd_slow": 26,
                "macd_signal": 9,
                "minimum_volume": 500.0
            }
        }

    def dict(self):
        return {
            "api_key": f"{self.api_key}",
            "secret_key": f"{self.secret_key}",
            "platform": f"{self.platform.value}",
            "strategy": f"{self.strategy.value}",
            "coin": f"{self.coin}",
            "timeframe": f"{self.timeframe.value}",
            "balance": float(self.balance),
            "take_profit": float(self.take_profit),
            "stop_loss": float(self.stop_loss),
            "rsi_period": float(self.rsi_period),
            "macd_fast": float(self.macd_fast),
            "macd_slow": float(self.macd_slow),
            "macd_signal": float(self.macd_signal),
            "minimum_volume": float(self.minimum_volume)
        }

def socket_handler(event, context):
    print(event, context)

@router.get("/trades", tags=["Trades Database"])
def get_trades():
    """
    Retrieves all trades from the session.

    Returns:
        list: A list of Trade objects representing the trades.
    """
    trades = session.query(Trade).all()
    return trades

@router.delete("/trades/{trade_id}", tags=["Trades Database"])
def delete_trade(trade_id = Path(..., description="The ID of the trade to be deleted", example="1668f12b0207f50935a4319c11cdcc76d4fc8ac4f1f5145e5117d775f80eed08")):
    """
    Deletes a trade with the given trade_id.

    Args:
        trade_id (int): The ID of the trade to be deleted.

    Returns:
        JSONResponse: A JSON response indicating the status of the deletion operation.
            If the trade is deleted successfully, the response will have a status code of 200
            and a message indicating the successful deletion. If the trade doesn't exist,
            the response will have a status code of 400 and an error message.

    """
    trade = session.query(Trade).filter(Trade.id == trade_id).first()
    if trade:
        stmt = delete(Trade).where(Trade.id == trade_id)
        session.execute(stmt)
        session.commit()
        log.info(f"Trade with id='{trade_id}' deleted successfully")
        return JSONResponse(content={"message": "Trade deleted successfully", "trade_id": trade_id}, status_code=200)
    else:
        log.error(f"Trade with id='{trade_id}' doesn't exist")
        return JSONResponse(content={"message": "Failed to delete trade", "error": f"Trade id='{trade_id}' doesn't exist"}, status_code=400)

@router.put("/trades", tags=["Trades Database"])
def create_trade(trade: TradeBase = Body(...)):
    """
    Create a new trade.

    Args:
        trade (TradeBase): The trade object to be created.

    Returns:
        JSONResponse: A JSON response containing the status of the trade creation.

    Raises:
        SQLAlchemyError: If there is an error during the trade creation process.
    """
    trade_obj = trade.dict()
    trade_obj["id"] = hash(trade_obj)
    try:
        stmt = insert(Trade).values(trade_obj)
        session.execute(stmt)
        session.commit()
        log.info(f"Trade created successfully: {trade_obj}")
        return JSONResponse(content={"message": "Trade created successfully", "trade": trade.dict()}, status_code=200)
    except SQLAlchemyError as e:
        log.error(e)
        session.rollback()
        return JSONResponse(content={"message": "Failed to create trade", "error": str(e)}, status_code=400)

@router.patch("/trades/{trade_id}", tags=["Trades Database"])
def update_trade(trade_id = Path(..., description="The ID of the trade to be deleted", example="1668f12b0207f50935a4319c11cdcc76d4fc8ac4f1f5145e5117d775f80eed08"), trade: TradeBase = Body(...)):
    """
    Update a trade with the given trade_id.

    Args:
        trade_id (int): The ID of the trade to be updated.
        trade (TradeBase): The updated trade information.

    Returns:
        JSONResponse: A JSON response indicating the status of the update operation.
            If the trade is updated successfully, the response will contain a success message
            and the updated trade information. If the trade does not exist, the response will
            indicate that the update failed due to the trade not being found. If there is an
            error during the update operation, the response will contain an error message.

    """
    original_trade = session.query(Trade).filter(Trade.id == trade_id).first()
    if original_trade:
        try:
            stmt = update(Trade).where(Trade.id == trade_id).values(trade.dict())
            session.execute(stmt)
            session.commit()
            log.info(f"Trade with id='{trade_id}' updated successfully")
            return JSONResponse(content={"message": "Trade updated successfully", "trade": trade.dict()}, status_code=200)
        except SQLAlchemyError as e:
            session.rollback()
            log.error(e)
            return JSONResponse(content={"message": "Failed to update trade", "error": str(e)}, status_code=400)
    return JSONResponse(content={"message": "Failed to update trade", "error": f"No Trade with id='{trade_id}'"}, status_code=400)