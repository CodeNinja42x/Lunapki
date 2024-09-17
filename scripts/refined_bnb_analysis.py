import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from ta.volatility import BollingerBands

def refined_bnb_analysis(data_path):
    df = pd.read_csv(data_path)
    
    # Ensure column names are lowercase for consistency
    df.columns = df.columns.str.lower()
    
    close_col = 'close'  # Assuming 'close' is the column name for closing prices

    # Bollinger Bands based on close price
    bb = BollingerBands(close=df[close_col], window=20, window_dev=2)
    df['bb_upper'] = bb.bollinger_hband()
    df['bb_middle'] = bb.bollinger_mavg()
    df['bb_lower'] = bb.bollinger_lband()

    # Adjusted Stop-Loss based on Bollinger Bands
    df['adjusted_stop'] = df['bb_lower'] + (df['bb_upper'] - df['bb_lower']) * 0.05  # 5% of band width

    # Trailing Stop based on Close price
    df['trailing_stop'] = df[close_col].shift(1) * 0.93  # 7% trailing stop initially

    # Dynamic stop-loss based on Bollinger Band width
    df['dynamic_stop'] = df[close_col] - (df['bb_upper'] - df['bb_lower']) * 0.5  # 50% of band width

    # Example PnL calculation (replace with actual PnL if available)
    df['pnl'] = df[close_col].pct_change().fillna(0)

    # Multi-Level Profit-Taking Logic with wider targets
    for i in range(1, len(df)):
        entry_price = df[close_col].iloc[i-1]
        current_price = df[close_col].iloc[i]
        
        # First profit target at +15%
        if current_price >= entry_price * 1.15:
            df.at[i, 'pnl'] += (current_price - entry_price) * 0.33 / entry_price  # Sell 1/3
        
        # Second profit target at +25%
        if current_price >= entry_price * 1.25:
            df.at[i, 'pnl'] += (current_price - entry_price * 1.15) * 0.33 / (entry_price * 1.15)  # Sell another 1/3

        # Third profit target at +40%
        if current_price >= entry_price * 1.40:
            df.at[i, 'pnl'] += (current_price - entry_price * 1.25) * 0.34 / (entry_price * 1.25)  # Sell remaining 1/3

        # Tighten trailing stop after 10% profit
        if current_price >= entry_price * 1.10:
            df['trailing_stop'].iloc[i] = df[close_col].shift(1).iloc[i] * 0.95  # 5% trailing stop

    # Risk-adjusted position sizing
    risk_per_trade = 0.01  # Risk 1% of account balance per trade
    account_size = 10000  # Example account size

    for i in range(1, len(df)):
        entry_price = df[close_col].iloc[i-1]
        stop_price = df['dynamic_stop'].iloc[i-1]
        risk_amount = (entry_price - stop_price) / entry_price
        position_size = (risk_per_trade * account_size) / (entry_price * risk_amount)
        df.at[i, 'position_size'] = position_size

    # Metrics calculation
    total_trades = len(df)
    wins = df[df['pnl'] > 0]
    losses = df[df['pnl'] <= 0]
    
    win_rate = len(wins) / total_trades if total_trades > 0 else 0
    avg_win = wins['pnl'].mean() if len(wins) > 0 else 0
    avg_loss = losses['pnl'].mean() if len(losses) > 0 else 0

    # Calculate drawdown
    df['cumulative_returns'] = (1 + df['pnl']).cumprod()
    df['peak'] = df['cumulative_returns'].cummax()
    df['drawdown'] = (df['cumulative_returns'] - df['peak']) / df['peak']
    max_drawdown = df['drawdown'].min()

    # Print results
    print(f"Total Trades: {total_trades}")
    print(f"Win Rate: {win_rate:.2%}")
    print(f"Average Win: {avg_win:.2f}")
    print(f"Average Loss: {avg_loss:.2f}")
    print(f"Max Drawdown: {max_drawdown:.2%}")

    # Visualize performance with adjusted stops and trailing stops
    plt.figure(figsize=(14, 7))

    # Plot price with Bollinger Bands and adjusted stop-loss
    plt.subplot(2, 1, 1)
    plt.plot(df.index, df[close_col], label='Close Price')
    plt.plot(df.index, df['bb_upper'], label='BB Upper', alpha=0.5)
    plt.plot(df.index, df['bb_lower'], label='BB Lower', alpha=0.5)
    plt.plot(df.index, df['adjusted_stop'], label='Adjusted Stop', alpha=0.7, linestyle='--')
    plt.plot(df.index, df['trailing_stop'], label='Trailing Stop', alpha=0.7, linestyle='-.')
    plt.title('Price with Bollinger Bands, Adjusted Stop-Loss, and Trailing Stop')
    plt.legend()

    # Cumulative PnL and drawdown
    plt.subplot(2, 1, 2)
    plt.plot(df.index, df['pnl'].cumsum(), label='Cumulative PnL')
    plt.plot(df.index, df['peak'], label='Peak')
    plt.plot(df.index, df['drawdown'], label='Drawdown')
    plt.title('Cumulative PnL and Drawdown')
    plt.legend()

    plt.tight_layout()
    plt.show()

    return df

# Example usage:
refined_bnb_analysis('/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/data/your_historical_data.csv')
