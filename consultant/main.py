import logging
import os

from binance import BinanceClient
from bitmex import BitmexClient
from crypto_currency import router as crypto_router
from fastapi import FastAPI, HTTPException
from fastapi.responses import PlainTextResponse
from mangum import Mangum

app = FastAPI()
handler = Mangum(app)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

stream_handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(levelname)s :: %(message)s')
stream_handler.setFormatter(formatter)
stream_handler.setLevel(logging.INFO)

file_handler = logging.FileHandler('/tmp/info.log')
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

################################################################################ API Keys

@app.get("/get_keys_binance", tags=["Binance"])
def get_keys_binance(api_key: str, secret_key: str):
    binance_keys = {"api_key": api_key, "secret_key": secret_key}
    return binance_keys

@app.get("/get_keys_bitmex", tags=["Bitmex"])
def get_keys_bitmex(api_key: str, secret_key: str):
    bitmex_keys = {"api_key": api_key, "secret_key": secret_key}
    return bitmex_keys

################################################################################# Endpoints do CoinGecko

app.include_router(crypto_router)

################################################################################# Endpoints para Funcionamento do CryptoBot
@app.get("/get_strategy", tags=["CryptoBot"])
def get_strategy(strategy_id: str):
    return

@app.post("/add_strategy", tags=["CryptoBot"])
def add_strategy(api_key: str, secret_key: str, exchange: str, strategy_name: str, contract_symbol: str, 
                timeframe: str, balance_pct: float, take_profit: float, stop_loss: float):

    return

@app.delete("/delete_strategy", tags=["CryptoBot"])
def delete_strategy(strategy_id: str):
    return

@app.put("/edit_strategy", tags=["CryptoBot"])
def edit_strategy(api_key: str, secret_key: str, exchange: str, strategy_id: str, ):
    return

################################################################################# Endpoints para Bitmex
@app.get("/cryptobot/contracts/bitmex", tags=["Bitmex"])
def get_contracts_list_bitmex(api_key: str, secret_key: str):
    """
    Get all the active contracts from Bitmex
    """
    bitmex = BitmexClient(api_key, secret_key, True)

    contracts = bitmex.get_contracts()
    if contracts is None:
        raise HTTPException(status_code=500, detail="Failed to fetch contracts from Bitmex.")
    return contracts

@app.get("/cryptobot/get_balance/bitmex", tags=["Bitmex"])
def get_balances_bitmex(api_key: str, secret_key: str):
    """
    Get the balance from Bitmex
    """
    bitmex = BitmexClient(api_key, secret_key, True)

    balance = bitmex.get_balances()
    if balance is None:
        raise HTTPException(status_code=500, detail="Failed to get balances from Bitmex.")
    return balance

@app.get("/cryptobot/candlesticks/bitmex", tags=["Bitmex"])
def get_historical_candles_bitmex(api_key: str, secret_key: str, symbol: str, interval: str):
    """
    Get the historical candlesticks from Bitmex of a symbol in an interval.
    """
    bitmex = BitmexClient(api_key, secret_key, True)

    candles = bitmex.get_historical_candles(symbol, interval)
    if candles is None:
        raise HTTPException(status_code=500, detail="Failed to fetch historical candlesticks.")
    return candles

@app.get("/cryptobot/price/bitmex", tags=["Bitmex"])
def get_bid_ask_bitmex(api_key: str, secret_key: str, symbol: str):
    """
    Get the price of the Bid and Ask from a symbol in Bitmex. Ex.: (BTCUSD)
    """
    bitmex = BitmexClient(api_key, secret_key, True)
    
    bid_ask = bitmex.get_bid_ask(symbol)
    if bid_ask is None:
        raise HTTPException(status_code=500, detail="Failed to fetch bid/ask prices.")
    return bid_ask

@app.post("/cryptobot/place_order/bitmex", tags=["Bitmex"])
def place_order_bitmex(api_key: str, secret_key: str, symbol: str, side: str, quantity: float, order_type: str, price: float, tif: str):
    """
    Place an order in Bitmex
    """
    bitmex = BitmexClient(api_key, secret_key, True)

    order = bitmex.place_order(symbol, side, quantity, order_type, price, tif)
    if order is None:
        raise HTTPException(status_code=500, detail="Failed to place order.")
    return order

@app.delete("/cryptobot/cancel_order/bitmex", tags=["Bitmex"])
def cancel_order_bitmex(api_key: str, secret_key: str, symbol: str, order_id: str):
    """
    Cancel an order in Bitmex
    """
    bitmex = BitmexClient(api_key, secret_key, True)

    canceled_order = bitmex.cancel_order(order_id)
    if canceled_order is None:
        raise HTTPException(status_code=500, detail=f"Failed to cancel the order {order_id}.")
    return canceled_order

@app.get("/cryptobot/order_status/bitmex", tags=["Bitmex"])
def get_order_status_bitmex(api_key: str, secret_key: str, symbol: str, order_id: str):
    """
    Get the order status in Bitmex
    """
    bitmex = BitmexClient(api_key, secret_key, True)

    order_status = bitmex.get_order_status(symbol, order_id)
    if order_status is None:
        raise HTTPException(status_code=500, detail=f"Failed to get the order {order_id} status.")
    return order_status

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

@app.get("/logs", tags=["Logs"], response_class=PlainTextResponse)
def get_logs():
    """
    Retrieve the logs from the info.log file
    """
    log_file_path = '/tmp/info.log'
    if os.path.exists(log_file_path):
        with open(log_file_path, 'r') as file:
            logs = file.read()
        return logs
    else:
        raise HTTPException(status_code=404, detail="Log file not found.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="info")
