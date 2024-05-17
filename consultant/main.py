from fastapi import FastAPI
from mangum import Mangum
import coin_gecko

app = FastAPI()

handler = Mangum(app)

@app.get("/")
def read_root():
    """
    This is the root path of the API
    """
    return {"ConsultantAPI": "CryptoBot_UnB_2024.1"}

@app.get("/crypto_currency/info")
def get_crypto_currency_api_info():
    """
    Path to get the CoinGecko API information
    """
    return coin_gecko.get_coin_gecko_health()

@app.get("/crypto_currency/coins/list")
def get_crypto_currency_coins_list():
    """
    Path to get the list of coins ids from CoinGecko
    CoinGecko spreadsheet in case you want to check the list of 
    coins without calling the API: https://docs.google.com/spreadsheets/d/1wTTuxXt8n9q7C4NDXqQpI3wpKu1_5bGVmP9Xz0XGSyU/edit#gid=0
    """
    return coin_gecko.get_coins_list()

@app.get("/crypto_currency/coins/{coin_id}")
def get_crypto_currency_coin(coin_id: str):
    """
    Path to get the information of a specific coin from CoinGecko
    """
    return coin_gecko.get_coin_simple_price(coin_id)

@app.get("/crypto_currency/coins/{coin_id}/chart")
def get_crypto_currency_coin_chart(coin_id: str):
    """
    Path to get the chart data of a specific coin from CoinGecko
    """
    return coin_gecko.get_coin_chart_data_with_timestamp(coin_id)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="info")