from fastapi import APIRouter, HTTPException
from trades import StrategyType, PlatformType, TimeFrameType
from postgres_conn import PostgresConnector
from pydantic import BaseModel
import hashlib
import json
from fastapi.responses import JSONResponse


router = APIRouter()
psql = PostgresConnector()
schema = "trades."

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

    def dict(self):
        return {
            "api_key": f"'{self.api_key}'",
            "secret_key": f"'{self.secret_key}'",
            "platform": f"'{self.platform.value.upper()}'",
            "strategy": f"'{self.strategy.value.upper()}'",
            "coin": f"'{self.coin}'",
            "timeframe": f"'{self.timeframe.value.upper()}'",
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
    trades = psql.select_query(f"SELECT * FROM {schema}trades")
    return trades

@router.delete("/trades/{trade_id}", tags=["Trades Database"])
def delete_trade(trade_id):
    query = f"""
        DELETE FROM trades WHERE id = '{trade_id}'
    """
    result = psql.select_query(f"SELECT * FROM {schema}trades WHERE id = '{trade_id}'")
    if len(result) == 0:
        return JSONResponse(content={"message": "Trade not found"}, status_code=404)
    status, msg = psql.execute_query(query)
    if status == 1:
        return JSONResponse(content={"message": "Trade deleted successfully", "trade_id": trade_id}, status_code=200)
    else:
        return JSONResponse(content={"message": "Failed to delete trade", "error": str(msg)}, status_code=400)

@router.put("/trades", tags=["Trades Database"])
def create_trade(trade: TradeBase):
    columns = [str(x) for x in trade.__dict__.keys()]
    values = [str(x) for x in trade.dict().values()]
    query = f"""
        INSERT INTO {schema}trades (id,{','.join(columns)}) VALUES ('{hash(values)}',{','.join(values)})
    """
    status, msg = psql.execute_query(query)
    if status == 1:
        return JSONResponse(content={"message": "Trade created successfully", "trade": trade.dict()}, status_code=200)
    else:
        return JSONResponse(content={"message": "Failed to create trade", "error": str(msg)}, status_code=400)

@router.post("/trades/{trade_id}", tags=["Trades Database"])
def update_trade(trade_id, trade: TradeBase):
    columns = [str(x) for x in trade.__dict__.keys()]
    values = [str(x) for x in trade.dict().values()]
    query = f"""
        UPDATE trades SET {','.join([f"{columns[i]}={values[i]}" for i in range(len(columns))])} WHERE id = '{trade_id}'
    """
    result = psql.select_query(f"SELECT * FROM {schema}trades WHERE id = '{trade_id}'")
    if len(result) == 0:
        return JSONResponse(content={"message": "Trade not found"}, status_code=404)


    status, msg = psql.execute_query(query)
    if status == 1:
        return JSONResponse(content={"message": "Trade updated successfully", "trade": trade.dict()}, status_code=200)
    else:
        return JSONResponse(content={"message": "Failed to update trade", "error": str(msg)}, status_code=400)