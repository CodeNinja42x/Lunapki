import pandas as pd
import ta
import os

# Load the dataset
data_path = '/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/data/your_historical_data.csv'
data = pd.read_csv(data_path)

# Check if necessary columns are present
required_columns = ['Date', 'Close', 'High', 'Low']
missing_columns = [col for col in required_columns if col not in data.columns]

if missing_columns:
    print(f"Missing columns in the dataset: {missing_columns}")
    # Provide default values or skip processing for missing columns
    if 'Date' not in data.columns:
        data['Date'] = pd.to_datetime('today')  # Example default for 'Date'
    if 'Close' not in data.columns:
        data['Close'] = data['close']  # Use lowercase 'close' column if available
    if 'High' not in data.columns:
        data['High'] = data['Close']  # Default to 'Close' values
    if 'Low' not in data.columns:
        data['Low'] = data['Close']  # Default to 'Close' values

# Feature Engineering
data['SMA'] = ta.trend.SMAIndicator(close=data['Close'], window=14).sma_indicator()
data['EMA'] = ta.trend.EMAIndicator(close=data['Close'], window=14).ema_indicator()
data['RSI'] = ta.momentum.RSIIndicator(close=data['Close'], window=14).rsi()
data['MACD'] = ta.trend.MACD(close=data['Close']).macd()

# Save the enhanced dataset
output_path = '/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/data/enhanced_data_v2.csv'
data.to_csv(output_path, index=False)
print(f"Feature engineering completed. Enhanced dataset saved to {output_path}")
