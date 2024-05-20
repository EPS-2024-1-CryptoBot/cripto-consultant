from fastapi import APIRouter, HTTPException, Request
import coin_gecko

router = APIRouter()
default_list_of_coins = ["bitcoin", "ethereum", "cardano", "solana", "binancecoin", "terra-luna", "ripple", "dogecoin", "shiba-inu"]

def is_valid_coin(coin_id):
    return coin_id in default_list_of_coins

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
    # This is a list of the most popular coins in the market - hard coded for now
    # We can use the coin gecko API to get the list of all coins in the future
    response = {
        "available_coins": default_list_of_coins
    }
    return response

@router.get("/coins/{coin_id}", tags=["Crypto Currency"])
def get_crypto_currency_coin(coin_id: str):
    """
    Path to get the information of a specific coin from CoinGecko
    """
    if not is_valid_coin(coin_id):
        raise HTTPException(status_code=404, detail="Coin not found")

    return coin_gecko.get_coin_simple_price(coin_id)

@router.get("/coins/{coin_id}/chart", tags=["Crypto Currency"])
def get_crypto_currency_coin_chart(coin_id: str):
    """
    Path to get the chart data of a specific coin from CoinGecko
    """
    if not is_valid_coin(coin_id):
        raise HTTPException(status_code=404, detail="Coin not found")
    return coin_gecko.get_coin_chart_data_with_timestamp(coin_id)