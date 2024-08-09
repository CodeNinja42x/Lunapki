import pandas as pd
import joblib

# Load the dataset
data = pd.read_csv('/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/data/consistent_features_data.csv')

# Load the feature names used during training
training_feature_names = joblib.load('/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/models/training_feature_names.pkl')

# Ensure all required features are present in the data
missing_features = [feature for feature in training_feature_names if feature not in data.columns]
if missing_features:
    raise ValueError(f"Missing features in the dataset: {missing_features}")

print("All required features are present.")
