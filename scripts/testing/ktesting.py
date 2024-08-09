import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load the processed data
data = pd.read_csv('/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/processed_data.csv')

# Define initial parameters
initial_balance = 10000
balance = initial_balance
positions = []
equity_curve = []
holdings = 0  # Tracks the number of shares held

# Sample strategy: Buy if RSI < 30, sell if RSI > 70, with stop-loss and take-profit
stop_loss = 0.05  # 5% stop loss
take_profit = 0.1  # 10% take profit

for i in range(1, len(data)):
    if data['rsi'][i] < 30 and balance >= data['Close'][i]:
        positions.append(('buy', data['Close'][i]))
        balance -= data['Close'][i]
        holdings += 1
    elif data['rsi'][i] > 70 and holdings > 0:
        positions.append(('sell', data['Close'][i]))
        balance += data['Close'][i]
        holdings -= 1
    elif holdings > 0:
        entry_price = positions[-1][1]
        if (data['Close'][i] <= entry_price * (1 - stop_loss)) or (data['Close'][i] >= entry_price * (1 + take_profit)):
            positions.append(('sell', data['Close'][i]))
            balance += data['Close'][i]
            holdings -= 1

    equity = balance + holdings * data['Close'][i]
    equity_curve.append(equity)

# Calculate final balance
final_balance = balance + holdings * data['Close'].iloc[-1]

# Calculate performance metrics
def calculate_performance_metrics(equity_curve):
    returns = np.diff(equity_curve) / equity_curve[:-1]
    annual_return = np.mean(returns) * 252
    annual_volatility = np.std(returns) * np.sqrt(252)
    sharpe_ratio = annual_return / annual_volatility
    max_drawdown = (np.min(equity_curve) - np.max(equity_curve)) / np.max(equity_curve)
    return annual_return, annual_volatility, sharpe_ratio, max_drawdown

annual_return, annual_volatility, sharpe_ratio, max_drawdown = calculate_performance_metrics(np.array(equity_curve))

print(f"Initial balance: {initial_balance}")
print(f"Final balance: {final_balance}")
print(f"Annual Return: {annual_return:.2f}")
print(f"Annual Volatility: {annual_volatility:.2f}")
print(f"Sharpe Ratio: {sharpe_ratio:.2f}")
print(f"Max Drawdown: {max_drawdown:.2f}")

# Plot equity curve
plt.figure()
plt.plot(equity_curve)
plt.title('Equity Curve')
plt.xlabel('Trade Number')
plt.ylabel('Equity')
plt.show()

# Save equity curve plot
plt.savefig('/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/models/equity_curve.png')
