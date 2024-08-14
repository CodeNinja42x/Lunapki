import pandas as pd
import ta  # Import the 'ta' library for technical analysis

# Load the data
data = pd.read_csv('/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/data/enhanced_data_with_indicators.csv')

# Implement additional feature engineering
# Example: Adding Bollinger Bands
data['BB_upper'], data['BB_middle'], data['BB_lower'] = ta.volatility.BollingerBands(close=data['close']).bollinger_hband(), ta.volatility.BollingerBands(close=data['close']).bollinger_mavg(), ta.volatility.BollingerBands(close=data['close']).bollinger_lband()

# Save the enhanced data
data.to_csv('/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/data/enhanced_data_with_bands.csv', index=False)
print("Additional feature engineering completed and data saved.")
