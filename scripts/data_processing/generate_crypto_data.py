import ccxt
import pandas as pd
from datetime import datetime

# Initialize the Binance exchange
exchange = ccxt.binance()

# Define the symbol and timeframe
symbol = 'BTC/USDT'
timeframe = '1d'  # Daily data

# Fetch historical data
since = exchange.parse8601('2022-01-01T00:00:00Z')
data = exchange.fetch_ohlcv(symbol, timeframe, since=since)

# Create a DataFrame
df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])

# Convert timestamp to datetime
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

# Save to CSV
data_path = '/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/data/crypto_data.csv'
df.to_csv(data_path, index=False)

print(f"Crypto data saved to {data_path}")
