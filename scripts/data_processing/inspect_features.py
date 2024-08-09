# inspect_features.py
import pandas as pd
import joblib

# Load the required features list
required_features = joblib.load('/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/models/required_features.pkl')

# Load the dataset
data = pd.read_csv('/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/data/advanced_features_data_updated.csv')

# Print features in the dataset
print("Features in dataset:", list(data.columns))

# Check for missing features
missing_features = [feature for feature in required_features if feature not in data.columns]
if missing_features:
    print("Missing features:", missing_features)
else:
    print("All required features are present.")
