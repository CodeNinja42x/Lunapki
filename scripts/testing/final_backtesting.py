import pandas as pd
from crypto_trading_bot.scripts.lib import trading_bot_library as tbl

# Load the best model
best_model = tbl.load_model('/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/models/best_model.pkl')

# Load the testing data
X_test = tbl.load_data('/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/data/X_test.csv')
y_test = tbl.load_data('/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/data/y_test.csv')

# Debugging: Check the loaded test data
print(f"X_test shape: {X_test.shape}")
print(f"y_test shape: {y_test.shape}")

# Perform backtesting
backtesting_results = tbl.perform_backtesting(best_model, X_test, y_test)

# Save backtesting results
tbl.save_backtesting_results(backtesting_results, '/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/results/backtesting_results.csv')

print("Backtesting completed and results saved.")
