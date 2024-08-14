import pandas as pd
import numpy as np
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error

# Load the enhanced data
data = pd.read_csv('/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/data/enhanced_data_with_indicators.csv')

# Replace 'target_column_name' with your actual target column name
target_column = 'close'  # Change this to your actual target column name
X = data.drop(columns=[target_column, 'date'])
y = data[target_column]

# Load the optimized model
model_path = '/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/models/optimized_xgb_model.pkl'
model = XGBRegressor()
model.load_model(model_path)

# Make predictions
predictions = model.predict(X)

# Backtesting logic with stop-loss and take-profit
initial_capital = 10000  # Initial capital in dollars
capital = initial_capital
position = 0
stop_loss = 0.95  # Stop loss at 95% of the purchase price
take_profit = 1.05  # Take profit at 105% of the purchase price
portfolio_values = []

for i in range(1, len(predictions)):
    if position == 0:
        # Buy if predicted price is higher than the previous price
        if predictions[i] > predictions[i-1]:
            position = capital / data['close'].iloc[i]
            purchase_price = data['close'].iloc[i]
            capital = 0
    else:
        # Sell if price hits stop-loss or take-profit
        current_price = data['close'].iloc[i]
        if current_price <= purchase_price * stop_loss or current_price >= purchase_price * take_profit:
            capital = position * current_price
            position = 0
    
    # Calculate portfolio value
    portfolio_value = capital + (position * data['close'].iloc[i])
    portfolio_values.append(portfolio_value)

# Convert portfolio values to a DataFrame
portfolio_df = pd.DataFrame(portfolio_values, columns=['Portfolio Value'])
portfolio_df['Portfolio Value'].plot(title='Portfolio Value Over Time')

# Performance metrics
final_portfolio_value = portfolio_values[-1]
total_return = (final_portfolio_value - initial_capital) / initial_capital * 100
mse = mean_squared_error(y, predictions)

print(f"Final Portfolio Value: ${final_portfolio_value:.2f}")
print(f"Total Return: {total_return:.2f}%")
print(f"Model Mean Squared Error: {mse}")

portfolio_df.to_csv('/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/results/backtesting_results.csv', index=False)
