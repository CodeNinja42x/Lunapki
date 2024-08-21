from your_trading_library import simulate_trading, deploy_model  # Replace with your actual functions
import pandas as pd

# Load the enhanced data
df = pd.read_csv('/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/data/btc_data_with_indicators.csv')

# Load the trained model
import joblib
model = joblib.load('/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/models/best_model.pkl')

# Choose to deploy or simulate
simulate_trading(model, df['2024':])  # Or use deploy_model(model) for live deployment
