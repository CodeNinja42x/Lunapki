# generate_missing_features.py

import pandas as pd
import numpy as np

# Load the existing data
data = pd.read_csv('/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/data/trading_data.csv')

# Check and fill missing basic features
basic_features = ['volume', 'close', 'high', 'open', 'low']
for feature in basic_features:
    if feature not in data.columns:
        print(f"Adding missing basic feature: {feature}")
        data[feature] = np.nan  # Add the column with NaN values

# Now fill the NaN values with some default logic or values
# You need to define how to handle these missing values based on your specific dataset and requirements
# For demonstration, we use forward fill and backward fill
data.fillna(method='ffill', inplace=True)
data.fillna(method='bfill', inplace=True)

# Generate the missing features
data['return'] = data['close'].pct_change()
data['return_lag_1'] = data['return'].shift(1)
data['return_lag_2'] = data['return'].shift(2)
data['return_lag_3'] = data['return'].shift(3)
data['return_lag_5'] = data['return'].shift(5)
data['return_lag_10'] = data['return'].shift(10)
data['volatility'] = data['return'].rolling(window=5).std()
data['volatility_lag_1'] = data['volatility'].shift(1)
data['volatility_lag_2'] = data['volatility'].shift(2)
data['volatility_lag_3'] = data['volatility'].shift(3)
data['volatility_lag_5'] = data['volatility'].shift(5)
data['volatility_lag_10'] = data['volatility'].shift(10)
data['expanding_std'] = data['return'].expanding().std()
data['diff_close_ma_10'] = data['close'] - data['close'].rolling(window=10).mean()
data['diff_close_ma_50'] = data['close'] - data['close'].rolling(window=50).mean()
data['momentum_lag_1'] = data['close'] - data['close'].shift(1)
data['momentum_lag_2'] = data['close'] - data['close'].shift(2)
data['momentum_lag_3'] = data['close'] - data['close'].shift(3)
data['momentum_lag_5'] = data['close'] - data['close'].shift(5)
data['momentum_lag_10'] = data['close'] - data['close'].shift(10)
data['rolling_std_5'] = data['close'].rolling(window=5).std()
data['rolling_std_10'] = data['close'].rolling(window=10).std()
data['rolling_std_20'] = data['close'].rolling(window=20).std()
data['rolling_volume_10'] = data['volume'].rolling(window=10).mean()
data['rolling_volume_50'] = data['volume'].rolling(window=50).mean()
data['cumulative_return'] = (1 + data['return']).cumprod() - 1

# Example of calculating MACD and other indicators
data['ema_12'] = data['close'].ewm(span=12, adjust=False).mean()
data['ema_26'] = data['close'].ewm(span=26, adjust=False).mean()
data['MACD'] = data['ema_12'] - data['ema_26']
data['MACD_Signal'] = data['MACD'].ewm(span=9, adjust=False).mean()
data['MACD_Diff'] = data['MACD'] - data['MACD_Signal']

# generate_missing_features.py continued

data['BB_High'] = data['close'].rolling(window=20).mean() + 2 * data['close'].rolling(window=20).std()
data['BB_Low'] = data['close'].rolling(window=20).mean() - 2 * data['close'].rolling(window=20).std()
data['BB_Width'] = data['BB_High'] - data['BB_Low']

data['RSI'] = 100 - (100 / (1 + data['close'].diff(1).apply(lambda x: np.maximum(x, 0)).rolling(window=14).mean() / data['close'].diff(1).apply(lambda x: np.abs(np.minimum(x, 0))).rolling(window=14).mean()))

# Adding the remaining missing features
data['return_volatility'] = data['return'].rolling(window=10).std()
data['volume_change'] = data['volume'].pct_change()
data['expanding_mean'] = data['close'].expanding().mean()
data['MACD_RSI'] = data['MACD'] / data['RSI']
data['momentum_volatility'] = data['momentum_lag_1'].rolling(window=5).std()
data['momentum'] = data['close'].pct_change()

# Calculate rolling means and moving averages
data['rolling_mean_10'] = data['close'].rolling(window=10).mean()
data['moving_avg_10'] = data['close'].rolling(window=10).mean()
data['rolling_mean_20'] = data['close'].rolling(window=20).mean()
data['ema_20'] = data['close'].ewm(span=20, adjust=False).mean()
data['ema_10'] = data['close'].ewm(span=10, adjust=False).mean()
data['rolling_mean_5'] = data['close'].rolling(window=5).mean()
data['moving_avg_50'] = data['close'].rolling(window=50).mean()

# Ensure 'target' column is present
if 'target' not in data.columns:
    print("Adding missing target column")
    data['target'] = np.nan  # Add the column with NaN values or define how to generate this

# Save the updated data
data.to_csv('/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/data/advanced_features_data_updated.csv', index=False)

print("Missing features generated and saved successfully.")
