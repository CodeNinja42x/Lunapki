from your_backtesting_library import backtest_model  # Replace with your actual backtesting function
import pandas as pd

# Load the enhanced data
df = pd.read_csv('/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/data/btc_data_with_indicators.csv')

# Load the trained model
import joblib
loaded_model = joblib.load('/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/models/best_model.pkl')

# Run backtest on a larger scale
backtest_result = backtest_model(loaded_model, df['2020':], window_size=20)
print(backtest_result)
