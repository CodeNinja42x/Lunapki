import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import ta
from scipy.optimize import minimize
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Function to fetch stock data
def fetch_stock_data(ticker, start_date, end_date):
    logger.info(f"Fetching data for {ticker} from {start_date} to {end_date}")
    return yf.download(ticker, start=start_date, end=end_date)

# Add technical indicators
def add_technical_indicators(df):
    logger.info("Adding technical indicators...")
    df['RSI'] = ta.momentum.RSIIndicator(df['Close']).rsi()
    df['MACD'] = ta.trend.MACD(df['Close']).macd()
    df['MACD_Signal'] = ta.trend.MACD(df['Close']).macd_signal()
    df['ATR'] = ta.volatility.AverageTrueRange(df['High'], df['Low'], df['Close']).average_true_range()
    df['SMA_50'] = df['Close'].rolling(window=50).mean()
    df['SMA_200'] = df['Close'].rolling(window=200).mean()
    df['Volatility'] = df['Close'].rolling(window=20).std()  # Volatility as a simple rolling standard deviation
    logger.info("Technical indicators added.")
    return df

# Generate trading signals
def generate_signals(df, rsi_low, rsi_high, macd_diff):
    logger.info("Generating trading signals...")
    df['Signal'] = np.where((df['RSI'] < rsi_low) & 
                            (df['MACD'] - df['MACD_Signal'] > macd_diff) &
                            (df['Close'] > df['SMA_50']), 1, 0)
    df['Signal'] = np.where((df['RSI'] > rsi_high) | 
                            (df['MACD'] - df['MACD_Signal'] < -macd_diff) | 
                            (df['Close'] < df['SMA_50']), -1, df['Signal'])
    logger.info("Signals generated.")
    return df

# Backtest the strategy
def backtest_strategy(df):
    logger.info("Backtesting strategy with transaction costs...")
    df['Strategy_Returns'] = df['Signal'].shift(1) * df['Close'].pct_change() - 0.001  # Transaction costs
    df['Cumulative_Returns'] = (1 + df['Strategy_Returns']).cumprod()
    
    final_portfolio_value = df['Cumulative_Returns'].iloc[-1]
    total_returns = df['Strategy_Returns'].sum()
    sharpe_ratio = np.sqrt(252) * df['Strategy_Returns'].mean() / df['Strategy_Returns'].std()
    
    logger.info(f"Sharpe Ratio: {sharpe_ratio}")
    logger.info(f"Final Portfolio Value: {final_portfolio_value}")
    logger.info(f"Total Returns: {total_returns}")
    
    return df, sharpe_ratio, final_portfolio_value, total_returns

# Optimize strategy parameters
def optimize_strategy(params, df):
    rsi_low, rsi_high, macd_diff = params
    df = generate_signals(df, rsi_low, rsi_high, macd_diff)
    df, sharpe_ratio, _, _ = backtest_strategy(df)
    return -sharpe_ratio  # Minimize negative Sharpe Ratio

# Visualize data and signals
def visualize_data(df, ticker):
    logger.info(f"Visualizing data for {ticker}...")
    plt.figure(figsize=(14, 7))
    plt.plot(df.index, df['Close'], label=f'{ticker} Close Price')
    plt.plot(df[df['Signal'] == 1].index, df['Close'][df['Signal'] == 1], '^', markersize=10, color='g', label='Buy Signal')
    plt.plot(df[df['Signal'] == -1].index, df['Close'][df['Signal'] == -1], 'v', markersize=10, color='r', label='Sell Signal')
    plt.legend()
    plt.title(f'{ticker} Trading Signals')
    plt.show()
    
    # Plot cumulative returns
    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df['Cumulative_Returns'], label='Strategy Cumulative Returns')
    plt.plot(df.index, (df['Close'] / df['Close'].iloc[0]), label='Buy and Hold')
    plt.legend()
    plt.title(f'{ticker} Strategy vs Buy and Hold')
    plt.show()

# Save data to CSV
def save_data_to_csv(df, ticker):
    df.to_csv(f'{ticker}_data_with_indicators.csv')
    logger.info(f"Data saved to {ticker}_data_with_indicators.csv")

# Main function to run the script
def main():
    ticker = 'AAPL'  # Example ticker
    start_date = '2020-01-01'
    end_date = '2023-01-01'
    
    # Fetch stock data
    df = fetch_stock_data(ticker, start_date, end_date)
    
    # Add technical indicators
    df = add_technical_indicators(df)
    
    # Set initial parameters for optimization
    initial_params = [30, 70, 0.01]
    
    # Optimize strategy parameters
    result = minimize(optimize_strategy, initial_params, args=(df,), method='Nelder-Mead')
    optimized_params = result.x
    logger.info(f"Optimized Parameters: RSI Low={optimized_params[0]}, RSI High={optimized_params[1]}, MACD Diff={optimized_params[2]}")
    
    # Generate signals with optimized parameters
    df = generate_signals(df, optimized_params[0], optimized_params[1], optimized_params[2])
    
    # Backtest the strategy
    df, sharpe_ratio, final_portfolio_value, total_returns = backtest_strategy(df)
    
    # Visualize data and save the results
    visualize_data(df, ticker)
    save_data_to_csv(df, ticker)

if __name__ == "__main__":
    main()
