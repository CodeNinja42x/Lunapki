# load_features.py

import joblib

# Load the required features from the file
required_features = joblib.load('/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/models/required_features.pkl')

# Print the required features to verify
print(required_features)
