import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from ta.volatility import BollingerBands, AverageTrueRange
from ta.trend import MACD
from ta.momentum import RSIIndicator

def refined_bnb_analysis(data_path):
    df = pd.read_csv(data_path)
    
    # Ensure column names are lowercase for consistency
    df.columns = df.columns.str.lower()
    
    # Verify that the necessary columns exist
    required_columns = ['high', 'low', 'close']
    if not all(col in df.columns for col in required_columns):
        raise ValueError(f"Data is missing one or more required columns: {required_columns}")

    close_col = 'close'

    # Print out a sample of the high, low, and close columns for debugging
    print(f"High prices:\n{df['high'].head()}")
    print(f"Low prices:\n{df['low'].head()}")
    print(f"Close prices:\n{df['close'].head()}")

    # Calculate Bollinger Bands
    bb = BollingerBands(close=df[close_col], window=20, window_dev=2)
    df['bb_upper'] = bb.bollinger_hband()
    df['bb_middle'] = bb.bollinger_mavg()
    df['bb_lower'] = bb.bollinger_lband()

    # Calculate MACD
    macd = MACD(close=df[close_col])
    df['macd'] = macd.macd()
    df['macd_signal'] = macd.macd_signal()
    df['macd_diff'] = macd.macd_diff()

    # Calculate Average True Range (ATR) for volatility analysis
    atr = AverageTrueRange(high=df['high'], low=df['low'], close=df[close_col])
    df['atr'] = atr.average_true_range()

    # Debug ATR values
    print(f"Average True Range (ATR) values:\n{df['atr'].head()}")

    # RSI Filter (Momentum confirmation)
    rsi = RSIIndicator(close=df[close_col], window=14)
    df['rsi'] = rsi.rsi()

    # Simplified trade signal: Use only MACD and RSI
    df['trade_signal'] = np.where((df['macd_diff'] > 0) & (df['rsi'] < 70), 1, 0)
    df['short_signal'] = np.where((df['macd_diff'] < 0) & (df['rsi'] > 30), 1, 0)

    # Initialize pnl column to 0
    df['pnl'] = 0.0

    # Adjusted Stop-Loss based on ATR
    df['adjusted_stop'] = df[close_col] - df['atr'] * 0.5  # Tighter stop using 0.5x ATR

    # Trailing Stop dynamically based on ATR
    df['trailing_stop'] = df[close_col] - df['atr'] * 0.3  # Further tighten trailing stop to 0.3x ATR

    # Simplified Multi-Level Profit-Taking Logic with smaller targets
    for i in range(1, len(df)):
        if df['trade_signal'].iloc[i] == 1:  # Only enter long trades when conditions are met
            entry_price = df[close_col].iloc[i-1]
            current_price = df[close_col].iloc[i]
            
            # Log the entry and current price for debugging
            print(f"Trade Entry at index {i}: Entry Price = {entry_price}, Current Price = {current_price}")
            
            # Profit targets at smaller intervals for better trade frequency
            if current_price >= entry_price * 1.01:  # First target at +1%
                df.at[i, 'pnl'] += (current_price - entry_price) * 0.5 / entry_price  # Sell 50%
                print(f"Hit +1% profit target at index {i}: Current Price = {current_price}, PnL = {df.at[i, 'pnl']}")
            if current_price >= entry_price * 1.02:  # Second target at +2%
                df.at[i, 'pnl'] += (current_price - entry_price * 1.01) * 0.5 / (entry_price * 1.01)  # Sell remaining 50%
                print(f"Hit +2% profit target at index {i}: Current Price = {current_price}, PnL = {df.at[i, 'pnl']}")

            # Tighten trailing stop after hitting the first profit target
            if current_price >= entry_price * 1.01:
                df['trailing_stop'].iloc[i] = df[close_col].shift(1).iloc[i] - df['atr'].iloc[i] * 0.3  # Further tighten ATR stop
                print(f"Tightened Trailing Stop at index {i}")

    # Metrics calculation
    total_trades = len(df[df['trade_signal'] == 1])  # Count only valid trades
    wins = df[(df['pnl'] > 0) & (df['trade_signal'] == 1)]
    losses = df[(df['pnl'] <= 0) & (df['trade_signal'] == 1)]
    
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

    # Save engineered data
    df.to_csv('/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/data/engineered_data.csv', index=False)

    return df

# Example usage:
df = refined_bnb_analysis('/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/data/your_historical_data.csv')
