import joblib
from crypto_trading_bot.scripts.lib import trading_bot_library as tbl

# Path to the model to be deployed
model_path = '/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/models/best_model.pkl'

# Load the model
model = tbl.load_model(model_path)

# Debugging: Confirm model loading
print(f"Model loaded from: {model_path}")

# Deploy or simulate the model
tbl.deploy_or_simulate_model(model)

print("Model deployment or simulation completed.")
