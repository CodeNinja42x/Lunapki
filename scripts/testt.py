import pandas as pd
import matplotlib.pyplot as plt

# ATR Calculation (Flexible period)
def calculate_atr(df, period=14):
    df['High-Low'] = df['High'] - df['Low']
    df['High-Close'] = abs(df['High'] - df['Close'].shift(1))
    df['Low-Close'] = abs(df['Low'] - df['Close'].shift(1))
    
    tr = df[['High-Low', 'High-Close', 'Low-Close']].max(axis=1)
    atr = tr.rolling(window=period).mean()
    
    return atr

# Dynamic stop-loss and take-profit with resistance levels and partial exits
def apply_trade_logic(df, atr_multiplier=2, profit_targets=[0.02, 0.05, 0.10], resistance_levels=None):
    df['ATR'] = calculate_atr(df)

    for index, row in df.iterrows():
        entry_price = row['Close']  # Assume we enter a trade at close price
        
        # Stop-loss and Take-profit levels
        stop_loss = entry_price - (row['ATR'] * atr_multiplier)
        partial_exits = []
        
        for target in profit_targets:
            take_profit = entry_price * (1 + target)
            if resistance_levels:
                take_profit = min(take_profit, resistance_levels[index])
            partial_exits.append(take_profit)
        
        # Visualize the logic or print outcomes
        if row['Close'] <= stop_loss:
            print(f"Stop-Loss hit at index {index}, closing position.")
        for i, target in enumerate(partial_exits):
            if row['Close'] >= target:
                print(f"Partial Take-Profit hit at index {index}, closing {1/len(profit_targets)} of position at {target}.")

# Backtesting and visualization
def backtest_and_visualize(df):
    apply_trade_logic(df)
    
    # Visualization
    plt.figure(figsize=(14, 7))
    plt.plot(df.index, df['Close'], label='Close Price')
    
    # Plot Stop-Loss and Take-Profit levels
    plt.scatter(df.index, df['ATR'], color='blue', label='ATR Stop-Loss')
    
    plt.legend()
    plt.show()

# Assuming your trading data is in a DataFrame
df = pd.read_csv('your_trading_data.csv')
backtest_and_visualize(df)
