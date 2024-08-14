import pandas as pd
import talib as ta

# Load your data
data = pd.read_csv('/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/data/processed_data/processed_data.csv')

# Rolling window features
data['rolling_mean_20'] = data['close'].rolling(window=20).mean()
data['rolling_std_20'] = data['close'].rolling(window=20).std()

# Additional technical indicators
data['RSI'] = ta.RSI(data['close'], timeperiod=14)
data['MACD'], data['MACD_signal'], data['MACD_hist'] = ta.MACD(data['close'], fastperiod=12, slowperiod=26, signalperiod=9)
data['upper_band'], data['middle_band'], data['lower_band'] = ta.BBANDS(data['close'], timeperiod=20)

# Time-based features
data['day_of_week'] = pd.to_datetime(data['date']).dt.dayofweek

# Save the enhanced dataset
output_path = '/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/data/enhanced_data_v2.csv'
data.to_csv(output_path, index=False)

print(f"Enhanced feature engineering completed and saved to {output_path}")
