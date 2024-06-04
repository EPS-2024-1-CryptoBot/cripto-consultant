import logging
import os

from connectors.binance import BinanceClient
from connectors.bitmex import BitmexClient
from fastapi import FastAPI, HTTPException
from mangum import Mangum

app = FastAPI()
handler = Mangum(app)

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

@app.get("/get_keys_binance", tags=["Binance"])
def get_keys_binance(api_key: str, secret_key: str):
    keys = {"api_key": api_key, "secret_key": secret_key}
    return keys

################################################################################# Endpoints para Bitmex
# @app.get("/cryptobot/contracts/bitmex", tags=["Bitmex"])
# def get_contracts_list_bitmex():
#     """
#     Get all the active contracts from Bitmex
#     """
#     contracts = bitmex.get_contracts()
#     if contracts is None:
#         raise HTTPException(status_code=500, detail="Failed to fetch contracts from Bitmex.")
#     return contracts

# @app.get("/cryptobot/get_balance/bitmex", tags=["Bitmex"])
# def get_balances_bitmex():
#     """
#     Get the balance from Bitmex
#     """
#     balance = bitmex.get_balances()
#     if balance is None:
#         raise HTTPException(status_code=500, detail="Failed to get balances from Bitmex.")
#     return balance

# @app.get("/cryptobot/candlesticks/bitmex", tags=["Bitmex"])
# def get_historical_candles_bitmex(symbol: str, interval: str):
#     """
#     Get the historical candlesticks from Bitmex of a symbol in an interval.
#     """
#     candles = bitmex.get_historical_candles(symbol, interval)
#     if candles is None:
#         raise HTTPException(status_code=500, detail="Failed to fetch historical candlesticks.")
#     return candles

# @app.get("/cryptobot/price/bitmex", tags=["Bitmex"])
# def get_bid_ask_bitmex(symbol: str):
#     """
#     Get the price of the Bid and Ask from a symbol in Bitmex. Ex.: (BTCUSD)
#     """
#     bid_ask = bitmex.get_bid_ask(symbol)
#     if bid_ask is None:
#         raise HTTPException(status_code=500, detail="Failed to fetch bid/ask prices.")
#     return bid_ask

# @app.post("/cryptobot/place_order/bitmex", tags=["Bitmex"])
# def place_order_bitmex(symbol: str, side: str, quantity: float, order_type: str, price: float, tif: str):
#     """
#     Place an order in Bitmex
#     """
#     order = bitmex.place_order(symbol, side, quantity, order_type, price, tif)
#     if order is None:
#         raise HTTPException(status_code=500, detail="Failed to place order.")
#     return order

# @app.delete("/cryptobot/cancel_order/bitmex", tags=["Bitmex"])
# def cancel_order_bitmex(symbol: str, order_id: str):
#     """
#     Cancel an order in Bitmex
#     """
#     canceled_order = bitmex.cancel_order(symbol, order_id)
#     if canceled_order is None:
#         raise HTTPException(status_code=500, detail=f"Failed to cancel the order {order_id}.")
#     return canceled_order

# @app.get("/cryptobot/order_status/bitmex", tags=["Bitmex"])
# def get_order_status_bitmex(symbol: str, order_id: str):
#     """
#     Get the order status in Bitmex
#     """
#     order_status = bitmex.get_order_status(symbol, order_id)
#     if order_status is None:
#         raise HTTPException(status_code=500, detail=f"Failed to get the order {order_id} status.")
#     return order_status

################################################################################# Endpoints para Binance
@app.get("/cryptobot/contracts/binance", tags=["Binance"])
def get_contracts_list_binance(api_key: str, secret_key: str):
    """
    Get all the contracts from Binance
    """
    binance = BinanceClient(api_key, secret_key, True, True)

    contracts = binance.get_contracts()
    if contracts is None:
        raise HTTPException(status_code=500, detail="Failed to fetch contracts from Binance.")
    return contracts

@app.get("/cryptobot/candlesticks/binance", tags=["Binance"])
def get_historical_candles_binance(api_key: str, secret_key: str, symbol: str, interval: str):
    """
    Get the historical candlesticks from Binance of a symbol in an interval. Ex.: (BTCUSDT, 1h)
    Check those possible intervals on https://github.com/luzzif/binance-api-client/blob/1e8c252/src/enums/CandlestickInterval.ts#L12
    """
    binance = BinanceClient(api_key, secret_key, True, True)

    candles = binance.get_historical_candles(symbol, interval)
    if candles is None:
        raise HTTPException(status_code=500, detail="Failed to fetch historical candlesticks.")
    return candles

@app.get("/cryptobot/price/binance", tags=["Binance"])
def get_bid_ask_binance(api_key: str, secret_key: str, symbol: str):
    """
    Get the price of the Bid and Ask from a symbol in Binance. Ex.: (BTCUSDT)
    """
    binance = BinanceClient(api_key, secret_key, True, True)

    bid_ask = binance.get_bid_ask(symbol)
    if bid_ask is None:
        raise HTTPException(status_code=500, detail="Failed to fetch bid/ask prices.")
    return bid_ask

@app.get("/cryptobot/get_balance/binance", tags=["Binance"])
def get_balances_binance(api_key: str, secret_key: str):
    """
    Get the balance from Binance
    """
    binance = BinanceClient(api_key, secret_key, True, True)

    balance = binance.get_balances()
    if balance is None:
        raise HTTPException(status_code=500, detail="Failed to get balances from Binance.")
    return balance

@app.post("/cryptobot/place_order/binance", tags=["Binance"])
def place_order_binance(api_key: str, secret_key: str, symbol: str, side: str, quantity: float, order_type: str, price: float, tif: str):
    """
    Place an order in Binance
    """
    binance = BinanceClient(api_key, secret_key, True, True)

    order = binance.place_order(symbol, side, quantity, order_type, price, tif)
    if order is None:
        raise HTTPException(status_code=500, detail="Failed to place order.")
    return order

@app.delete("/cryptobot/cancel_order/binance", tags=["Binance"])
def cancel_order_binance(api_key: str, secret_key: str, symbol: str, order_id: str):
    """
    Cancel an order in Binance
    """
    binance = BinanceClient(api_key, secret_key, True, True)

    canceled_order = binance.cancel_order(symbol, order_id)
    if canceled_order is None:
        raise HTTPException(status_code=500, detail=f"Failed to cancel the order {order_id}.")
    return canceled_order

@app.get("/cryptobot/order_status/binance", tags=["Binance"])
def get_order_status_binance(api_key: str, secret_key: str, symbol: str, order_id: str):
    """
    Get the order status in Binance
    """
    binance = BinanceClient(api_key, secret_key, True, True)

    order_status = binance.get_order_status(symbol, order_id)
    if order_status is None:
        raise HTTPException(status_code=500, detail=f"Failed to get the order {order_id} status.")
    return order_status

################################################################################# Endpoint para logs


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="info")
