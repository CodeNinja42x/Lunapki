import yfinance as yf
import pandas as pd
import numpy as np
import ta
import matplotlib.pyplot as plt
import logging
from scipy.optimize import minimize

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Fetch stock data from Yahoo Finance
def fetch_stock_data(ticker, start_date, end_date):
    logger.info(f"Fetching data for {ticker} from {start_date} to {end_date}")
    df = yf.download(ticker, start=start_date, end=end_date)
    return df

# Add technical indicators
def add_technical_indicators(df):
    logger.info("Adding technical indicators...")
    df['RSI'] = ta.momentum.RSIIndicator(df['Close']).rsi()
    df['MACD'] = ta.trend.MACD(df['Close']).macd()
    df['MACD_Signal'] = ta.trend.MACD(df['Close']).macd_signal()
    df['BB_Upper'], df['BB_Middle'], df['BB_Lower'] = ta.volatility.BollingerBands(df['Close']).bollinger_hband(), ta.volatility.BollingerBands(df['Close']).bollinger_mavg(), ta.volatility.BollingerBands(df['Close']).bollinger_lband()
    df['ATR'] = ta.volatility.AverageTrueRange(df['High'], df['Low'], df['Close']).average_true_range()
    df['SMA_50'] = df['Close'].rolling(window=50).mean()
    df['SMA_200'] = df['Close'].rolling(window=200).mean()
    logger.info("Technical indicators added.")
    return df

# Generate signals based on technical indicators
def generate_signals(df, rsi_low, rsi_high, macd_diff):
    logger.info("Generating trading signals...")
    df['Signal'] = np.where((df['RSI'] < rsi_low) & (df['MACD'] > df['MACD_Signal'] + macd_diff) & (df['Close'] > df['SMA_50']), 1, 0)
    df['Signal'] = np.where((df['RSI'] > rsi_high) | (df['MACD'] < df['MACD_Signal'] - macd_diff) | (df['Close'] < df['SMA_50']), -1, df['Signal'])
    logger.info("Signals generated.")
    return df

# Backtesting with strategy logic
def backtest_strategy(df, transaction_cost=0.001):
    logger.info("Backtesting strategy...")
    
    df['Strategy_Returns'] = df['Signal'].shift(1) * df['Close'].pct_change()
    df['Strategy_Returns'] -= transaction_cost * np.abs(df['Signal'].diff().fillna(0))
    df['Cumulative_Returns'] = (1 + df['Strategy_Returns']).cumprod()
    
    final_portfolio_value = df['Cumulative_Returns'].iloc[-1]
    total_returns = df['Strategy_Returns'].sum()
    
    # Sharpe Ratio (assuming 252 trading days)
    sharpe_ratio = np.sqrt(252) * df['Strategy_Returns'].mean() / df['Strategy_Returns'].std()

    logger.info(f"Sharpe Ratio: {sharpe_ratio}")
    logger.info(f"Final Portfolio Value: {final_portfolio_value}")
    logger.info(f"Total Returns: {total_returns}")
    
    return df, sharpe_ratio, final_portfolio_value, total_returns

# Optimize the strategy by tuning the RSI and MACD parameters
def optimize_strategy(params, df):
    rsi_low, rsi_high, macd_diff = params
    df = generate_signals(df, rsi_low, rsi_high, macd_diff)
    df, sharpe_ratio, _, _ = backtest_strategy(df)
    return -sharpe_ratio  # Minimize the negative Sharpe Ratio

# Visualize the stock price and signals
def visualize_data(df, ticker):
    plt.figure(figsize=(14, 7))
    plt.plot(df.index, df['Close'], label=f'{ticker} Close Price')
    plt.plot(df[df['Signal'] == 1].index, df['Close'][df['Signal'] == 1], '^', markersize=10, color='g', label='Buy Signal')
    plt.plot(df[df['Signal'] == -1].index, df['Close'][df['Signal'] == -1], 'v', markersize=10, color='r', label='Sell Signal')
    plt.legend()
    plt.title(f'{ticker} Buy/Sell Signals')
    plt.show()

    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df['Cumulative_Returns'], label='Strategy Cumulative Returns')
    plt.plot(df.index, (df['Close'] / df['Close'].iloc[0]), label='Buy and Hold')
    plt.legend()
    plt.title('Strategy vs Buy and Hold Cumulative Returns')
    plt.show()

# Main function to execute the full process
def main():
    ticker = 'AAPL'  # Example stock
    start_date = '2020-01-01'
    end_date = '2023-01-01'

    # Fetch and prepare data
    df = fetch_stock_data(ticker, start_date, end_date)
    df = add_technical_indicators(df)

    # Optimize the strategy by finding the best RSI and MACD parameters
    initial_params = [30, 70, 0]  # Initial guess for RSI low, RSI high, and MACD difference
    result = minimize(optimize_strategy, initial_params, args=(df,), method='Nelder-Mead')
    optimized_params = result.x
    logger.info(f"Optimized Parameters: RSI Low={optimized_params[0]}, RSI High={optimized_params[1]}, MACD Diff={optimized_params[2]}")

    # Backtest and visualize the optimized strategy
    df = generate_signals(df, optimized_params[0], optimized_params[1], optimized_params[2])
    df, sharpe_ratio, final_portfolio_value, total_returns = backtest_strategy(df)
    visualize_data(df, ticker)

    # Save results to CSV
    df.to_csv(f'{ticker}_data_with_optimized_strategy.csv')
    logger.info(f"Data saved to {ticker}_data_with_optimized_strategy.csv")

if __name__ == "__main__":
    main()
