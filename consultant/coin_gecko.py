import os
import requests

"""
REFER TO THE COIN GECKO API DOCUMENTATION FOR MORE INFORMATION (V3.0.1)
https://docs.coingecko.com/v3.0.1/reference/introduction
"""

def build_gecko_request(method, endpoint, params=None):
    url = os.environ.get("COIN_GECKO_API_URL") + "/" + endpoint

    headers = {
        "accept": "application/json",
        "x-cg-demo-api-key": os.environ.get("COIN_GECKO_API_KEY")
    }

    if method == "get":
        response = requests.get(url, headers=headers, params=params)
    elif method == "post":
        response = requests.post(url, headers=headers, json=params)
    else:
        response = None

    return response



def get_coin_gecko_info():
    return {"info": "CoinGecko info", 
                "key": os.environ.get("COIN_GECKO_API_KEY"),
                "url": os.environ.get("COIN_GECKO_API_URL")
            }

def get_coin_gecko_health():
    response = build_gecko_request("get", "/ping")
    return response.json()

def get_coins_list():
    response = build_gecko_request("get", "/coins/list")
    return response.json()
    
def get_coin_simple_price(coin_id):
    """
    Get the current price of a coin in USD
    This endpoint accept array of ids in a single request, for the MVP we are going to use only one id
    """
    response = build_gecko_request("get", f"/simple/price?ids={coin_id}&vs_currencies=brl&include_market_cap=true&include_24hr_vol=true&include_24hr_change=true&include_last_updated_at=true&precision=2")
    return response.json()

def get_coin_chart_data_with_timestamp(coin_id):
    """
    Get the market chart data (price, market cap, volume) of a coin in a specific date range
    For now leaving the default range of 3 weeks
    """
    response = build_gecko_request("get", f"/coins/{coin_id}/market_chart/range?vs_currency=usd&from=1711929600&to=1712275200")
    return response.json()