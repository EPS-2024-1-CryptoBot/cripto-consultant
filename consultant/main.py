import logging

import connectors.bitmex
from connectors.binance_futures import BinanceFuturesClient
from fastapi import FastAPI, HTTPException, Query
from mangum import Mangum

app = FastAPI()
handler = Mangum(app)
binance = BinanceFuturesClient(True)

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


@app.get("/")
def read_root():
    """
    This is the root path of the API
    """
    return {"ConsultantAPI": "CryptoBot_UnB_2024.1"}

@app.get("/cryptobot/contracts/bitmex")
def get_contracts_list_bitmex():
    """
    Get all the active contracts from Bitmex
    """
    return connectors.bitmex.get_contracts()

@app.get("/cryptobot/contracts/binance")
def get_contracts_list_binance():
    """
    Get all the contracts from Binance
    """
    return binance.get_contracts()

@app.get("/cryptobot/candlesticks/binance")
def get_historical_candles_binance(symbol: str, interval: str):
    """
    Get the historical candlesticks from Binance of a symbol in an interval. Ex.: (BTCUSDT, 1h)
    Check those possible intervals on https://github.com/luzzif/binance-api-client/blob/1e8c252/src/enums/CandlestickInterval.ts#L12
    """
    candles = binance.get_historical_candles(symbol, interval)
    if candles is None:
        raise HTTPException(status_code=500, detail="Failed to fetch historical candlesticks.")
    return candles
c
@app.get("/cryptobot/prices/binance")
def get_bid_ask_binance(symbol: str):
    """
    Get the price of the Bid and Ask from a symbol in Binance. Ex.: (BTCUSDT)
    """
    bid_ask = binance.get_bid_ask(symbol)
    if bid_ask is None:
        raise HTTPException(status_code=500, detail="Failed to fetch bid/ask prices.")
    return bid_ask

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="info")
