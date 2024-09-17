import pandas as pd

# Assuming you've already imported your data with necessary signals and indicators
# For demonstration purposes, let's say your DataFrame is called 'data'

# Backtesting
print("Backtesting strategy with transaction costs...")

initial_capital = 100000  # Starting with $100,000
position_size = 100  # Number of shares per trade
transaction_cost = 0.001  # 0.1% transaction cost per trade
cash = initial_capital
portfolio_value = cash
data['Portfolio_Value'] = 0
data['Position'] = 0
stop_loss = 0  # Initialize stop_loss to avoid NameError

for i in range(1, len(data)):
    # Buy Signal
    if data['Buy_Signal'].iloc[i] == 1 and data['Position'].iloc[i - 1] == 0:
        shares_to_buy = position_size
        entry_price = data['Close'].iloc[i]
        stop_loss = entry_price - 2 * data['ATR'].iloc[i]  # ATR-based stop-loss
        data['Position'].iloc[i] = shares_to_buy
        portfolio_value = cash - shares_to_buy * entry_price - transaction_cost * shares_to_buy * entry_price
        cash = 0  # All cash is used to buy the position
    
    # Sell Signal
    elif data['Sell_Signal'].iloc[i] == 1 and data['Position'].iloc[i - 1] > 0:
        exit_price = data['Close'].iloc[i]
        shares_to_sell = data['Position'].iloc[i - 1]
        portfolio_value = shares_to_sell * exit_price - transaction_cost * shares_to_sell * exit_price
        cash = portfolio_value  # Convert shares to cash
        data['Position'].iloc[i] = 0  # Exit the position
        stop_loss = 0  # Reset stop_loss when position is closed
    
    # Apply Stop-Loss
    elif data['Position'].iloc[i - 1] > 0 and data['Close'].iloc[i] < stop_loss:
        exit_price = data['Close'].iloc[i]
        shares_to_sell = data['Position'].iloc[i - 1]
        portfolio_value = shares_to_sell * exit_price - transaction_cost * shares_to_sell * exit_price
        cash = portfolio_value  # Convert shares to cash
        data['Position'].iloc[i] = 0  # Exit the position
        stop_loss = 0  # Reset stop_loss when position is closed
    
    # Update portfolio value
    data['Portfolio_Value'].iloc[i] = portfolio_value

# After the loop, calculate performance metrics like total return, Sharpe ratio, etc.
total_returns = (portfolio_value - initial_capital) / initial_capital
print(f"Total Returns: {total_returns * 100:.2f}%")

# You can then save your results or plot them as you were doing
data.to_csv("backtest_results.csv", index=False)
