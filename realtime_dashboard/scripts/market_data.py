import requests

def fetch_market_data(symbol):
    response = requests.get(f'https://api.binance.com/api/v3/ticker/price?symbol={symbol}')
    return response.json()
