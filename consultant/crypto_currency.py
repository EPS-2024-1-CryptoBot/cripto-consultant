from fastapi import APIRouter, HTTPException, Request
import coin_gecko

router = APIRouter()

@router.get("/info", tags=["Crypto Currency"])
def get_crypto_currency_api_info():
    """
    Path to get the CoinGecko API information
    """
    return coin_gecko.get_coin_gecko_health()

@router.get("/coins/list", tags=["Crypto Currency"])
def get_crypto_currency_coins_list():
    """
    Path to get the list of coins ids from CoinGecko
    CoinGecko spreadsheet in case you want to check the list of 
    coins without calling the API: https://docs.google.com/spreadsheets/d/1wTTuxXt8n9q7C4NDXqQpI3wpKu1_5bGVmP9Xz0XGSyU/edit#gid=0
    """
    return coin_gecko.get_coins_list()

@router.get("/coins/{coin_id}", tags=["Crypto Currency"])
def get_crypto_currency_coin(coin_id: str):
    """
    Path to get the information of a specific coin from CoinGecko
    """
    return coin_gecko.get_coin_simple_price(coin_id)

@router.get("/coins/{coin_id}/chart", tags=["Crypto Currency"])
def get_crypto_currency_coin_chart(coin_id: str):
    """
    Path to get the chart data of a specific coin from CoinGecko
    """
    return coin_gecko.get_coin_chart_data_with_timestamp(coin_id)