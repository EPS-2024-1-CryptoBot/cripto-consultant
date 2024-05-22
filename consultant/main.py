import logging

import connectors.bitmex
from connectors.binance_futures import BinanceFuturesClient
from crypto_currency import router as crypto_currency_router
from fastapi import FastAPI, HTTPException, Query
from mangum import Mangum

app = FastAPI()
app.include_router(crypto_currency_router, prefix="/crypto_currency")

handler = Mangum(app)
binance = BinanceFuturesClient("8d0922c254c066f9325a2dc6acdb82ccbd1c108cdcd0d1fa9e2a193deef06892", 
                                "a86579e0a1ef79d25380986ba179edb44f821bf3165fd99b0dcaff5deb963e55", 
                                True)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

stream_handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(levelname)s :: %(message)s')
stream_handler.setFormatter(formatter)
stream_handler.setLevel(logging.INFO)

file_handler = logging.FileHandler('info.log')
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.DEBUG)

logger.addHandler(stream_handler)
logger.addHandler(file_handler)


@app.get("/", tags=["Root"])
def read_root():
    """
    This is the root path of the API
    """
    return {"ConsultantAPI": "CryptoBot_UnB_2024.1"}

@app.get("/cryptobot/contracts/bitmex", tags=["Bitmex"])
def get_contracts_list_bitmex():
    """
    Get all the active contracts from Bitmex
    """
    return connectors.bitmex.get_contracts()

@app.get("/cryptobot/contracts/binance", tags=["Binance"])
def get_contracts_list_binance():
    """
    Get all the contracts from Binance
    """
    return binance.get_contracts()

@app.get("/cryptobot/candlesticks/binance", tags=["Binance"])
def get_historical_candles_binance(symbol: str, interval: str):
    """
    Get the historical candlesticks from Binance of a symbol in an interval. Ex.: (BTCUSDT, 1h)
    Check those possible intervals on https://github.com/luzzif/binance-api-client/blob/1e8c252/src/enums/CandlestickInterval.ts#L12
    """
    candles = binance.get_historical_candles(symbol, interval)
    if candles is None:
        raise HTTPException(status_code=500, detail="Failed to fetch historical candlesticks.")
    return candles

@app.get("/cryptobot/price/binance", tags=["Binance"])
def get_bid_ask_binance(symbol: str):
    """
    Get the price of the Bid and Ask from a symbol in Binance. Ex.: (BTCUSDT)
    """
    bid_ask = binance.get_bid_ask(symbol)
    if bid_ask is None:
        raise HTTPException(status_code=500, detail="Failed to fetch bid/ask prices.")
    return bid_ask

@app.get("/cryptobot/get_balance/binance", tags=["Binance"])
def get_balances_binance():
    """
    Get the balance from Binance
    """
    balance = binance.get_balances()
    if balance is None:
        raise HTTPException(status_code=500, detail="Failed to get balances.")
    return balance

@app.post("/cryptobot/place_order/binance", tags=["Binance"])
def place_order_binance(symbol: str, side: str, quantity: float, order_type: str, price: float, tif: str):
    """
    Place an order in Binance
    """
    order = binance.place_order(symbol, side, quantity, order_type, price, tif)
    if order is None:
        raise HTTPException(status_code=500, detail="Failed to place order.")
    return order

@app.delete("/cryptobot/cancel_order/binance", tags=["Binance"])
def cancel_order_binance(symbol: str, order_id: str):
    """
    Cancel an order in Binance
    """
    canceled_order = binance.cancel_order(symbol, order_id)
    if canceled_order is None:
        raise HTTPException(status_code=500, detail=f"Failed to cancel the order {order_id}.")
    return canceled_order

@app.get("/cryptobot/order_status/binance", tags=["Binance"])
def get_order_status_binance(symbol, order_id):
    """
    Get the order status in Binance
    """
    order_status = binance.get_order_status(symbol, order_id)
    if order_status is None:
        raise HTTPException(status_code=500, detail=f"Failed to get the order {order_id} status.")
    return order_status


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="info")
