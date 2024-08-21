import pandas as pd
from trading_bot_library import refine_and_tune_model, load_data

# Load training data
X_train_path = '/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/data/enhanced_data_v2.csv'
y_train_path = '/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/data/y_train.csv'

X_train = load_data(X_train_path)
y_train = load_data(y_train_path)

# Check data shapes
print(f"Shape of X_train: {X_train.shape}")
print(f"Shape of y_train: {y_train.shape}")

# Ensure sample sizes match
if X_train.shape[0] != y_train.shape[0]:
    raise ValueError(f"Found input variables with inconsistent numbers of samples: {X_train.shape[0]}, {y_train.shape[0]}")

# Refine and tune the model
try:
    best_model, best_params = refine_and_tune_model(X_train, y_train, n_splits=2)
    print("Model tuning completed successfully.")
except Exception as e:
    print(f"An error occurred during model tuning: {e}")
