# rename_columns.py

import pandas as pd
import joblib

# Load the new data
new_data = pd.read_csv('/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/data/trading_data.csv')

# Load the required features
required_features = joblib.load('/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/models/required_features.pkl')

# Check for missing features and rename columns if necessary
missing_features = [feature for feature in required_features if feature not in new_data.columns]
print(f"Missing features: {missing_features}")

# Here you would manually rename the columns in new_data to match the required features
# Ensure all the required features are present in the new data
for feature in missing_features:
    # For demonstration, let's assume you manually rename columns to fix missing features
    if feature not in new_data.columns:
        # You need to add the logic to rename columns here
        # For example: new_data.rename(columns={'old_name': 'new_name'}, inplace=True)
        pass

# Save the updated new data
new_data.to_csv('/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/data/trading_data_updated.csv', index=False)
