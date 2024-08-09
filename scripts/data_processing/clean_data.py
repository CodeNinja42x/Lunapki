import pandas as pd

# Load data
data_path = '/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/data/features.csv'
data = pd.read_csv(data_path, index_col=0)

# Check for NaN values and remove them
data_cleaned = data.dropna()

# Save cleaned data
cleaned_data_path = '/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/data/features_cleaned.csv'
data_cleaned.to_csv(cleaned_data_path)

print("Data cleaned and saved successfully.")
