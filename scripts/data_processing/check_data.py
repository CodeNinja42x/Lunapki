import pandas as pd

data_path = '/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/data/preprocessed_data.csv'
data = pd.read_csv(data_path)

print(data.columns)
