import pandas as pd
from crypto_trading_bot.scripts.lib import trading_bot_library as tbl

# Load the tuned model
grid_search = tbl.load_model('/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/models/grid_search_model.pkl')

# Load test data
X_test = tbl.load_data('/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/data/X_test.csv')
y_test = tbl.load_data('/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/data/y_test.csv')

# Debugging: Check the loaded test data
print(f"X_test shape: {X_test.shape}")
print(f"y_test shape: {y_test.shape}")

# Save the best model
tbl.save_model(grid_search.best_estimator_, '/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/models/best_model.pkl')

# Make predictions and evaluate the model
y_pred = tbl.predict(grid_search.best_estimator_, X_test)
mse = tbl.evaluate_model(y_test, y_pred)
print(f"Mean Squared Error: {mse}")
