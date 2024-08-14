import pandas as pd
import ta  # Make sure you have this package installed
import os

# Load the data
def load_data(file_path):
    return pd.read_csv(file_path)

# File paths
raw_data_path = '/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/data/raw_data/your_raw_data.csv'
processed_data_path = '/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/data/processed_data/processed_data.csv'
engineered_data_path = '/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/data/engineered_data/your_engineered_data.csv'

# Load raw data
data = load_data(raw_data_path)

# Feature Engineering (this is an example, modify as needed)
# Add any technical indicators or features here
data['SMA'] = ta.trend.sma_indicator(data['close'], window=20)
data['EMA'] = ta.trend.ema_indicator(data['close'], window=20)
data['RSI'] = ta.momentum.rsi(data['close'], window=14)
data['MACD'] = ta.trend.macd(data['close'])

# Save processed data
data.to_csv(processed_data_path, index=False)

# Further process if needed
# Example: Save engineered data
data.to_csv(engineered_data_path, index=False)

print("Feature engineering completed and data saved successfully.")
