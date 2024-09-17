import pandas as pd

# Load the data
data = pd.read_csv('/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/data/engineered_data.csv')

# Print all column names
print("Column Names in engineered_data.csv:")
print(data.columns)

# Print the first few rows to inspect the data structure
print("\nFirst few rows of the data:")
print(data.head())
