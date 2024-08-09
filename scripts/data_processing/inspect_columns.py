# inspect_columns.py

import pandas as pd

# Load the dataset
data = pd.read_csv('/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/data/advanced_features_data.csv')

# Print the columns of the dataset
print(data.columns)
