import pandas as pd
import numpy as np
import ta  # Technical Analysis library

# Load data
data = pd.read_csv('/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/Bot/raw_data.csv')

# Calculating returns
data['return'] = data['Close'].pct_change()
data['log_return'] = np.log(data['Close'] / data['Close'].shift(1))

# Technical indicators
data['SMA'] = data['Close'].rolling(window=20).mean()
data['EMA'] = data['Close'].ewm(span=20, adjust=False).mean()
data['RSI'] = ta.momentum.RSIIndicator(close=data['Close'], window=14).rsi()
data['MACD'] = ta.trend.MACD(close=data['Close']).macd()
data['MACD_diff'] = ta.trend.MACD(close=data['Close']).macd_diff()
data['Bollinger_H'] = ta.volatility.BollingerBands(close=data['Close']).bollinger_hband()
data['Bollinger_L'] = ta.volatility.BollingerBands(close=data['Close']).bollinger_lband()

# Lagged features
for lag in range(1, 8):
    data[f'return_lag_{lag}'] = data['return'].shift(lag)
    data[f'log_return_lag_{lag}'] = data['log_return'].shift(lag)
    data[f'Close_lag_{lag}'] = data['Close'].shift(lag)

# Creating the target column (1 if next day's return is positive, 0 otherwise)
data['target'] = (data['return'].shift(-1) > 0).astype(int)

# Drop NaN values created by the lagging and target shift
data = data.dropna()

# Save the processed data
data.to_csv('/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/Bot/processed_data.csv', index=False)
