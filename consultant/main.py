from fastapi import FastAPI
from mangum import Mangum
from crypto_currency import router as crypto_currency_router

app = FastAPI()
app.include_router(crypto_currency_router, prefix="/crypto_currency")

handler = Mangum(app)

@app.get("/", tags=["Root"])
def read_root():
    """
    This is the root path of the API
    """
    return {"ConsultantAPI": "CryptoBot_UnB_2024.1"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="info")