import pandas as pd
from sklearn.preprocessing import StandardScaler
import numpy as np
import ta  # Technical Analysis library

# Load data
data_path = '/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/data/crypto_data.csv'
data = pd.read_csv(data_path)

# Convert 'timestamp' to datetime and drop it
data['timestamp'] = pd.to_datetime(data['timestamp'])
data.set_index('timestamp', inplace=True)

# Generate basic features
data['return'] = data['close'].pct_change()
data['volatility'] = data['return'].rolling(window=10).std()
data['momentum'] = data['close'] - data['close'].shift(10)
data['moving_avg_10'] = data['close'].rolling(window=10).mean()
data['moving_avg_50'] = data['close'].rolling(window=50).mean()

# Calculate RSI
data['RSI'] = ta.momentum.RSIIndicator(data['close'], window=14).rsi()

# Calculate MACD
macd = ta.trend.MACD(data['close'])
data['MACD'] = macd.macd()
data['MACD_Signal'] = macd.macd_signal()
data['MACD_Diff'] = macd.macd_diff()

# Calculate Bollinger Bands
bb = ta.volatility.BollingerBands(data['close'], window=20, window_dev=2)
data['BB_High'] = bb.bollinger_hband()
data['BB_Low'] = bb.bollinger_lband()
data['BB_Width'] = bb.bollinger_hband() - bb.bollinger_lband()

# Create lag features
lags = [1, 2, 3, 5, 10]
for lag in lags:
    data[f'return_lag_{lag}'] = data['return'].shift(lag)
    data[f'volatility_lag_{lag}'] = data['volatility'].shift(lag)
    data[f'momentum_lag_{lag}'] = data['momentum'].shift(lag)

# Interaction features
data['return_volatility'] = data['return'] * data['volatility']
data['momentum_volatility'] = data['momentum'] * data['volatility']
data['MACD_RSI'] = data['MACD'] * data['RSI']

# Rolling mean and standard deviation for different windows
windows = [5, 10, 20]
for window in windows:
    data[f'rolling_mean_{window}'] = data['close'].rolling(window=window).mean()
    data[f'rolling_std_{window}'] = data['close'].rolling(window=window).std()

# Expanding mean and standard deviation
data['expanding_mean'] = data['close'].expanding().mean()
data['expanding_std'] = data['close'].expanding().std()

# New Features: Price Differences
data['diff_close_ma_10'] = data['close'] - data['moving_avg_10']
data['diff_close_ma_50'] = data['close'] - data['moving_avg_50']

# New Feature: Cumulative Returns
data['cumulative_return'] = (1 + data['return']).cumprod() - 1

# New Feature: Exponential Moving Average (EMA)
data['ema_10'] = data['close'].ewm(span=10, adjust=False).mean()
data['ema_20'] = data['close'].ewm(span=20, adjust=False).mean()

# New Volume Features
data['volume_change'] = data['volume'].pct_change()
data['rolling_volume_10'] = data['volume'].rolling(window=10).mean()
data['rolling_volume_50'] = data['volume'].rolling(window=50).mean()

# Drop rows with NaN values created by rolling window operations
data.dropna(inplace=True)

# Define target variable
data['target'] = np.where(data['return'].shift(-1) > 0, 1, 0)

# Save the features and target
features_path = '/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/data/features.csv'
data.to_csv(features_path, index=True)

print("Features generated and saved successfully.")
