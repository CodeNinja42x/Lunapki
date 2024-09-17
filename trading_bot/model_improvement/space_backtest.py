import yfinance as yf
import pandas as pd
import numpy as np

# Fetch historical data
def fetch_data(ticker):
    print(f"Fetching data for {ticker}")
    data = yf.download(ticker, start="2022-01-01", end="2023-01-01")
    data['RSI'] = calculate_rsi(data['Close'], 14)
    return data

# Calculate RSI
def calculate_rsi(series, period=14):
    delta = series.diff(1)
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=period, min_periods=1).mean()
    avg_loss = loss.rolling(window=period, min_periods=1).mean()
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

# Calculate ATR for stop-loss
def calculate_atr(data, period=14):
    high_low = data['High'] - data['Low']
    high_close = np.abs(data['High'] - data['Close'].shift())
    low_close = np.abs(data['Low'] - data['Close'].shift())
    ranges = pd.concat([high_low, high_close, low_close], axis=1)
    true_range = ranges.max(axis=1)
    atr = true_range.rolling(window=period).mean()
    return atr

# Define buy/sell signals based on RSI and Moving Average
def generate_signals(data, rsi_buy=25, rsi_sell=75):
    data['Buy_Signal'] = np.where((data['RSI'] < rsi_buy) & (data['Close'] > data['50_MA']), 1, 0)
    data['Sell_Signal'] = np.where(data['RSI'] > rsi_sell, 1, 0)
    return data

# Backtest the strategy
def backtest_strategy(data, stop_loss_factor=2):
    portfolio_value = 100000  # Starting portfolio value
    position = 0
    buy_price = 0
    transaction_costs = 0
    atr = calculate_atr(data)

    for i in range(len(data)):
        if data['Buy_Signal'].iloc[i] == 1 and position == 0:
            position = portfolio_value / data['Close'].iloc[i]
            buy_price = data['Close'].iloc[i]
            print(f"Buy at {buy_price} on {data.index[i]}")
        
        if position > 0:
            stop_loss = buy_price - (stop_loss_factor * atr.iloc[i])
            if data['Low'].iloc[i] < stop_loss:
                portfolio_value = position * stop_loss
                position = 0
                print(f"Stop-Loss triggered at {stop_loss} on {data.index[i]}")
                continue
            
            if data['Sell_Signal'].iloc[i] == 1:
                portfolio_value = position * data['Close'].iloc[i]
                print(f"Sell at {data['Close'].iloc[i]} on {data.index[i]}")
                position = 0

    return portfolio_value

# Main function to run the backtest on multiple assets
def run_backtest(tickers):
    for ticker in tickers:
        data = fetch_data(ticker)
        data['50_MA'] = data['Close'].rolling(window=50).mean()  # 50-day Moving Average
        data = generate_signals(data)
        final_portfolio_value = backtest_strategy(data)
        total_returns = (final_portfolio_value - 100000) / 100000
        print(f"Final Portfolio Value for {ticker}: {final_portfolio_value}")
        print(f"Total Returns for {ticker}: {total_returns}")

# Run the backtest on AAPL, SPY, QQQ, and BTC-USD
tickers = ['AAPL', 'SPY', 'QQQ', 'BTC-USD']
run_backtest(tickers)
