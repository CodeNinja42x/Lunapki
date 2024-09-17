import ccxt
import pandas as pd
import time

# Connect to Binance
exchange = ccxt.binance()

def fetch_data(symbol, timeframe, since):
    data = exchange.fetch_ohlcv(symbol, timeframe, since=since)
    df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    return df

if __name__ == "__main__":
    symbol = 'BTC/USDT'
    timeframe = '1h'
    since = exchange.parse8601('2023-01-01T00:00:00Z')  # Start from Jan 1st, 2023
    
    # Fetch data
    df = fetch_data(symbol, timeframe, since)

    # Save to CSV
    file_path = '/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/data/BTC_USDT_1h.csv'
    df.to_csv(file_path, index=False)
    
    print(f"Data saved to {file_path}")
