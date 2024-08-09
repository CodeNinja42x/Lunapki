import pandas as pd
import joblib
import os  # Make sure to import os

file_path = '/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/data/training_data.csv'

if os.path.exists(file_path):
    data = pd.read_csv(file_path)
    X = data.drop('target', axis=1)
    training_feature_names = list(X.columns)
    joblib.dump(training_feature_names, '/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/models/training_feature_names.pkl')
    print("Training feature names saved successfully.")
else:
    print(f"File does not exist: {file_path}. Please place the training data file in the correct directory.")
