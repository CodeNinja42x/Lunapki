import os
import joblib

# Path to the saved model
model_load_path = '/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/models/optimized_rf_model.pkl'

# Check if the model file exists
if not os.path.exists(model_load_path):
    raise FileNotFoundError(f"Model file not found: {model_load_path}")

# Load the trained model
model = joblib.load(model_load_path)

# Assuming you have a backtesting function defined elsewhere
# backtest_results = backtest_model(model, X_test, y_test)  # Replace with your actual backtesting function
# print(backtest_results)
