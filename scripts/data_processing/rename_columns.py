import pandas as pd

# Load your dataset
data = pd.read_csv('/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/data/updated_historical_data.csv')

# Rename columns to match the expected names
data.rename(columns={
    'date': 'Date',
    'close': 'Close',
    'high': 'High',    # Assuming you have 'high' and 'low' columns under different names
    'low': 'Low'
}, inplace=True)

# Save the updated dataset
data.to_csv('/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/data/updated_historical_data.csv', index=False)

print("Columns have been renamed and dataset updated.")
