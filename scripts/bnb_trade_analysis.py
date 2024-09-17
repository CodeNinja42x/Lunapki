import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from ta.volatility import BollingerBands

def refined_bnb_analysis(data_path):
    # Load the data
    df = pd.read_csv(data_path)

    # Calculate Bollinger Bands for volatility-based stop-loss adjustment
    bb = BollingerBands(high=df['High'], low=df['Low'], close=df['Close'], window=20, window_dev=2)
    df['bb_upper'], df['bb_middle'], df['bb_lower'] = bb.bollinger_hband(), bb.bollinger_mavg(), bb.bollinger_lband()
    
    # Adjust stop-loss based on Bollinger Bands
    df['adjusted_stop'] = df['bb_lower'] + (df['bb_upper'] - df['bb_lower']) * 0.2  # Adjust as needed for tighter stops

    # Example: PnL is based on percentage changes in closing prices
    df['PnL'] = df['Close'].pct_change().fillna(0)  # You can replace this with actual PnL if available

    # Calculate key metrics
    total_trades = len(df)
    wins = df[df['PnL'] > 0]
    losses = df[df['PnL'] <= 0]
    
    win_rate = len(wins) / total_trades if total_trades > 0 else 0
    avg_win = wins['PnL'].mean() if len(wins) > 0 else 0
    avg_loss = losses['PnL'].mean() if len(losses) > 0 else 0

    # Calculate drawdown
    df['cumulative_returns'] = (1 + df['PnL']).cumprod()
    df['peak'] = df['cumulative_returns'].cummax()
    df['drawdown'] = (df['cumulative_returns'] - df['peak']) / df['peak']
    max_drawdown = df['drawdown'].min()

    # Print results
    print(f"Total Trades: {total_trades}")
    print(f"Win Rate: {win_rate:.2%}")
    print(f"Average Win: {avg_win:.2f}")
    print(f"Average Loss: {avg_loss:.2f}")
    print(f"Max Drawdown: {max_drawdown:.2%}")

    # Visualize performance and adjusted stop-losses
    plt.figure(figsize=(14, 7))
    
    # Price and Bollinger Bands
    plt.subplot(2, 1, 1)
    plt.plot(df.index, df['Close'], label='Close Price')
    plt.plot(df.index, df['bb_upper'], label='BB Upper', alpha=0.5)
    plt.plot(df.index, df['bb_lower'], label='BB Lower', alpha=0.5)
    plt.plot(df.index, df['adjusted_stop'], label='Adjusted Stop', alpha=0.7, linestyle='--')
    plt.title('Price with Bollinger Bands and Adjusted Stop-Loss')
    plt.legend()
    
    # Cumulative PnL
    plt.subplot(2, 1, 2)
    plt.plot(df.index, df['PnL'].cumsum(), label='Cumulative PnL')
    plt.plot(df.index, df['peak'], label='Peak')
    plt.plot(df.index, df['drawdown'], label='Drawdown')
    plt.title('Cumulative PnL and Drawdown')
    plt.legend()

    plt.tight_layout()
    plt.show()

    return df

# Example usage:
refined_bnb_analysis('/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/data/btc_data_with_indicators.csv')
