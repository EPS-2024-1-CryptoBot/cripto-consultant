import logging

import binance_futures
import bitmex
from fastapi import FastAPI
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

@app.get("/")
def read_root():
    """
    This is the root path of the API
    """
    return {"ConsultantAPI": "CryptoBot_UnB_2024.1"}

@app.get("/cryptobot/contracts/list/bitmex")
def get_contracts_list_bitmex():
    """
    Get all the active contracts from Bitmex
    """
    return bitmex.get_contracts()

@app.get("/cryptobot/contracts/list/binance")
def get_contracts_list_binance():
    """
    Get all the contracts from Binance Futures
    """
    return binance_futures.get_contracts()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="info")

