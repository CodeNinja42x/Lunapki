import ccxt
import pandas as pd
import numpy as np
import talib
import matplotlib.pyplot as plt
from datetime import datetime

# Initialize Binance API (you can replace this with your own API keys if needed)
binance = ccxt.binance({
    'rateLimit': 1200,
    'enableRateLimit': True,
})

# Convert date to Unix timestamp in milliseconds
def date_to_timestamp(date_str):
    return int(datetime.strptime(date_str, '%Y-%m-%d').timestamp() * 1000)

# Fetch Historical Data for BTC/USDT (1 Day timeframe) from Binance
def get_historical_data(symbol, timeframe, start_date, end_date):
    start_timestamp = date_to_timestamp(start_date)
    end_timestamp = date_to_timestamp(end_date)
    ohlcv = binance.fetch_ohlcv(symbol, timeframe, since=start_timestamp)
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    return df[(df['timestamp'] >= pd.to_datetime(start_date)) & (df['timestamp'] <= pd.to_datetime(end_date))]

# Apply Indicators (RSI, MACD, Bollinger Bands, ATR, and Stochastic Oscillator)
def apply_indicators(df):
    df['MA50'] = talib.SMA(df['close'], timeperiod=50)
    df['MA200'] = talib.SMA(df['close'], timeperiod=200)
    df['upperband'], df['middleband'], df['lowerband'] = talib.BBANDS(df['close'], timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)
    df['rsi'] = talib.RSI(df['close'], timeperiod=14)
    df['macd'], df['macdsignal'], _ = talib.MACD(df['close'], fastperiod=12, slowperiod=26, signalperiod=9)
    df['atr'] = talib.ATR(df['high'], df['low'], df['close'], timeperiod=14)
    df['slowk'], df['slowd'] = talib.STOCH(df['high'], df['low'], df['close'], fastk_period=14, slowk_period=3, slowd_period=3)
    return df

# Define the trading strategy with logging
def trading_strategy(df, risk_per_trade=0.01, balance=10000):
    position_size = 0
    entry_price = None
    pnl = 0
    risked_amount = balance * risk_per_trade
    balance_history = [balance]

    for i in range(1, len(df)):
        # Log each step's indicators and decisions
        print(f"Index {i}: Date: {df['timestamp'][i]}")
        print(f"RSI: {df['rsi'][i]}, MACD: {df['macd'][i]}, MACD Signal: {df['macdsignal'][i]}")
        print(f"Close: {df['close'][i]}, Lower BB: {df['lowerband'][i]}, Upper BB: {df['upperband'][i]}")
        print(f"ATR: {df['atr'][i]}, Slow K: {df['slowk'][i]}, Slow D: {df['slowd'][i]}")

        # Entry conditions: RSI < 30, MACD crosses up, Price < Lower Bollinger Band, and low ATR
        if (df['rsi'][i] < 30 and df['macd'][i] > df['macdsignal'][i] and df['close'][i] < df['lowerband'][i] and df['slowk'][i] < 20 and df['atr'][i] < df['atr'].mean()):
            entry_price = df['close'][i]
            target_price = entry_price * 1.02  # 2% take profit
            stop_loss = entry_price * 0.98     # 2% stop loss
            position_size = risked_amount / (entry_price - stop_loss)
            
            print(f"*** Trade Entry at index {i}: Entry Price = {entry_price}, Target Price = {target_price}, Position Size = {position_size}")

        # Exit conditions: Price > Upper Bollinger Band or RSI > 70 or ATR spikes up
        elif entry_price is not None and position_size > 0 and (df['rsi'][i] > 70 or df['close'][i] > df['upperband'][i] or df['atr'][i] > df['atr'].mean()):
            exit_price = df['close'][i]
            pnl += (exit_price - entry_price) * position_size
            balance += pnl
            position_size = 0  # Close the position
            entry_price = None  # Reset the entry price
            
            print(f"*** Exit Trade at index {i}: Exit Price = {exit_price}, PnL = {pnl}")

        # Update balance history
        balance_history.append(balance)

    return balance_history

# Plot the results
def plot_results(df, balance_history):
    fig, ax = plt.subplots(2, figsize=(14, 8))

    # Plot price and Bollinger Bands
    ax[0].plot(df['timestamp'], df['close'], label='Close Price', color='blue')
    ax[0].plot(df['timestamp'], df['upperband'], label='Upper Bollinger Band', linestyle='--', color='red')
    ax[0].plot(df['timestamp'], df['lowerband'], label='Lower Bollinger Band', linestyle='--', color='green')
    ax[0].set_title('BTC/USDT Price with Bollinger Bands')
    ax[0].legend()

    # Plot balance history
    ax[1].plot(df['timestamp'], balance_history, label='Balance History', color='orange')
    ax[1].set_title('Balance Over Time')
    ax[1].legend()

    plt.show()

# Main execution
symbol = 'BTC/USDT'
timeframe = '1d'
start_date = '2017-01-01'
end_date = '2019-01-01'

# Fetch historical data
df = get_historical_data(symbol, timeframe, start_date, end_date)

# Apply indicators
df = apply_indicators(df)

# Run backtest with logging
balance_history = trading_strategy(df)

# Plot the results
plot_results(df, balance_history)
