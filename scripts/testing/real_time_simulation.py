import time
import pandas as pd
import numpy as np
from xgboost import XGBRegressor

# Load the refined data
data = pd.read_csv('/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/data/refined_data.csv')

# Initialize model
model_path = '/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/models/optimized_xgb_model_refined.pkl'
model = XGBRegressor()
model.load_model(model_path)

# Initialize variables
initial_capital = 10000  # Initial capital in dollars
capital = initial_capital
position = 0
stop_loss = 0.95  # Stop loss at 95% of the purchase price
take_profit = 1.05  # Take profit at 105% of the purchase price
portfolio_values = []
trade_log = []

# Simulate real-time trading
for i in range(1, len(data)):
    if i < 2:
        continue  # Skip the first iteration as there's no previous data to compare
    
    current_data = data.iloc[:i]
    X = current_data.drop(columns=['close', 'date'])
    y = current_data['close']
    
    prediction = model.predict(X.tail(1))[0]
    
    if position == 0:
        # Buy if predicted price is higher than the previous price
        if prediction > y.iloc[-2]:
            position = capital / y.iloc[-1]
            purchase_price = y.iloc[-1]
            capital = 0
            trade_log.append(f"Buy at {purchase_price}")
    else:
        # Sell if price hits stop-loss or take-profit
        current_price = y.iloc[-1]
        if current_price <= purchase_price * stop_loss or current_price >= purchase_price * take_profit:
            capital = position * current_price
            position = 0
            trade_log.append(f"Sell at {current_price}")
    
    # Calculate portfolio value
    portfolio_value = capital + (position * y.iloc[-1])
    portfolio_values.append(portfolio_value)
    
    # Mimic real-time delay
    time.sleep(1)  # Adjust delay as needed

# Performance metrics
final_portfolio_value = portfolio_values[-1]
total_return = (final_portfolio_value - initial_capital) / initial_capital * 100

# Save results
portfolio_df = pd.DataFrame(portfolio_values, columns=['Portfolio Value'])
portfolio_df.to_csv('/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/results/simulation_results.csv', index=False)

# Log trades
with open('/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/results/trade_log.txt', 'w') as f:
    for entry in trade_log:
        f.write(entry + "\n")

print(f"Final Portfolio Value: ${final_portfolio_value:.2f}")
print(f"Total Return: {total_return:.2f}%")
