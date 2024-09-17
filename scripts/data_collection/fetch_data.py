from binance.client import Client

def fetch_market_data(api_key, api_secret, symbol):
    client = Client(api_key, api_secret)
    trades = client.get_recent_trades(symbol=symbol)
    return trades

if __name__ == "__main__":
    api_key = 'KqH2Y2Sal3AFvmd4f1W0PMZoO7cCiRg7Cv03Mlo36PPAKXldlumQzBtHIiZUQNXK'
    api_secret = '758A75mLiN4OJjMhslQppLHNHili3A8ZFczLmZyavXJRoXO20AVzmjnhKERbbJqU'
    symbol = 'BTCUSDT'
    data = fetch_market_data(api_key, api_secret, symbol)
    print(data)
