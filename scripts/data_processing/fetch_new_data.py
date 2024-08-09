import ccxt
import pandas as pd
import os
from dotenv import load_dotenv

def fetch_new_data():
    load_dotenv()  # Load environment variables from .env file
    
    api_key = os.getenv('BINANCE_API_KEY')
    api_secret = os.getenv('BINANCE_API_SECRET')
    
    exchange = ccxt.binance({
        'apiKey': api_key,
        'secret': api_secret,
    })
    symbol = 'BTC/USDT'
    timeframe = '1d'
    limit = 100  # Fetch the most recent 100 data points

    ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
    
    # Convert to DataFrame
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    
    df.to_csv('/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/data/new_data.csv', index=False)
    print("New data fetched and saved successfully.")

if __name__ == "__main__":
    fetch_new_data()
