import pandas as pd

# Load the updated dataset
data = pd.read_csv('/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/data/updated_historical_data.csv')

# Print the columns
print("Columns in the updated dataset:")
print(data.columns)
