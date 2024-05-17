import logging

from binance_futures import write_log
from fastapi import FastAPI
from mangum import Mangum

app = FastAPI()
handler = Mangum(app)

# Create and configure the logger object

logger = logging.getLogger()

logger.setLevel(logging.DEBUG)  # Overall minimum logging level

stream_handler = logging.StreamHandler()  # Configure the logging messages displayed in the Terminal
formatter = logging.Formatter('%(asctime)s %(levelname)s :: %(message)s')
stream_handler.setFormatter(formatter)
stream_handler.setLevel(logging.INFO)  # Minimum logging level for the StreamHandler

file_handler = logging.FileHandler('info.log')  # Configure the logging messages written to a file
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.DEBUG)  # Minimum logging level for the FileHandler

logger.addHandler(stream_handler)
logger.addHandler(file_handler)

write_log()

@app.get("/")
def read_root():
    """
    This is the root path of the API
    """
    return {"ConsultantAPI": "CryptoBot_UnB_2024.1"}

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="info")

