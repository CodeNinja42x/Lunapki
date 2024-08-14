import pandas as pd

# Load the engineered data
data_path = '/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/data/engineered_data/your_engineered_data.csv'
data = pd.read_csv(data_path)

# Print the column names
print("Columns in the dataset:")
print(data.columns)
