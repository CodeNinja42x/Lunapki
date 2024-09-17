import ccxt

# Connect to multiple exchanges
exchanges = {
    'binance': ccxt.binance(),
    'kraken': ccxt.kraken(),
}

def fetch_price(exchange, symbol):
    ticker = exchanges[exchange].fetch_ticker(symbol)
    return ticker['last']

def find_arbitrage(symbol):
    binance_price = fetch_price('binance', symbol)
    kraken_price = fetch_price('kraken', symbol)
    
    price_diff = binance_price - kraken_price
    if price_diff > 0:
        print(f"Arbitrage opportunity: Buy on Kraken at {kraken_price} and sell on Binance at {binance_price}")
    else:
        print("No arbitrage opportunity found.")

if __name__ == "__main__":
    find_arbitrage('BTC/USDT')
