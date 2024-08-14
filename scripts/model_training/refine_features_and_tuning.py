import pandas as pd
from crypto_trading_bot.scripts.lib import trading_bot_library as tbl

# Load the training data
X_train = tbl.load_data('/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/data/X_train.csv')
y_train = tbl.load_data('/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/data/y_train.csv')

# Debugging: Check the loaded data
print(f"X_train shape: {X_train.shape}")
print(f"y_train shape: {y_train.shape}")

# Refine features and tune the model
best_model, best_params = tbl.refine_and_tune_model(X_train, y_train)

# Save the best model and parameters
tbl.save_model(best_model, '/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/models/best_model.pkl')
tbl.save_params(best_params, '/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/models/best_params.json')

print("Model tuning completed and saved.")
