import yfinance as yf
import pandas as pd
import ta
import matplotlib.pyplot as plt
import argparse
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fetch_stock_data(ticker, start_date, end_date):
    """
    Fetches stock data from Yahoo Finance for a given ticker and date range.
    """
    try:
        logger.info(f"Fetching data for {ticker} from {start_date} to {end_date}")
        df = yf.download(ticker, start=start_date, end=end_date)
        if df.empty:
            raise ValueError(f"No data found for {ticker} between {start_date} and {end_date}.")
        return df
    except Exception as e:
        logger.error(f"Error fetching data for {ticker}: {e}")
        return pd.DataFrame()

def add_indicator(df, indicator_func, name, **kwargs):
    """
    Adds a technical indicator to the dataframe.
    """
    try:
        df[name] = indicator_func(**kwargs)
        logger.info(f"Added {name} indicator to the dataframe.")
    except Exception as e:
        logger.error(f"Error adding {name} indicator: {e}")
    return df

def add_technical_indicators(df):
    """
    Adds technical indicators like RSI, MACD, Bollinger Bands, and ATR to the dataframe.
    """
    logger.info("Adding technical indicators...")
    try:
        # Relative Strength Index (RSI)
        df = add_indicator(df, ta.momentum.RSIIndicator(df['Close']).rsi, 'RSI')

        # Moving Average Convergence Divergence (MACD)
        macd = ta.trend.MACD(df['Close'])
        df['MACD'] = macd.macd()
        df['MACD_Signal'] = macd.macd_signal()

        # Bollinger Bands
        bollinger = ta.volatility.BollingerBands(df['Close'])
        df['BB_Upper'] = bollinger.bollinger_hband()
        df['BB_Lower'] = bollinger.bollinger_lband()

        # Average True Range (ATR)
        df = add_indicator(df, ta.volatility.AverageTrueRange(df['High'], df['Low'], df['Close']).average_true_range, 'ATR')

        logger.info("Technical indicators added.")
    except Exception as e:
        logger.error(f"Error adding technical indicators: {e}")
    return df

def visualize_data(df, ticker):
    """
    Visualizes the stock's closing price along with technical indicators like Bollinger Bands, RSI, and MACD.
    """
    logger.info(f"Visualizing data for {ticker}...")
    try:
        # Plotting Close Price with Bollinger Bands
        plt.figure(figsize=(14, 7))
        plt.plot(df.index, df['Close'], label=f'{ticker} Close Price', color='blue')
        plt.plot(df.index, df['BB_Upper'], label='Bollinger Upper Band', color='orange')
        plt.plot(df.index, df['BB_Lower'], label='Bollinger Lower Band', color='green')
        plt.fill_between(df.index, df['BB_Upper'], df['BB_Lower'], color='gray', alpha=0.2)
        plt.title(f'{ticker} Close Price with Bollinger Bands')
        plt.legend()
        plt.show()

        # Plotting RSI
        plt.figure(figsize=(14, 7))
        plt.plot(df.index, df['RSI'], label='RSI', color='purple')
        plt.axhline(70, color='red', linestyle='--')
        plt.axhline(30, color='green', linestyle='--')
        plt.title(f'{ticker} RSI')
        plt.legend()
        plt.show()

        # Plotting MACD and MACD Signal
        plt.figure(figsize=(14, 7))
        plt.plot(df.index, df['MACD'], label='MACD', color='blue')
        plt.plot(df.index, df['MACD_Signal'], label='MACD Signal', color='red')
        plt.title(f'{ticker} MACD and Signal')
        plt.legend()
        plt.show()

        # Plotting ATR
        plt.figure(figsize=(14, 7))
        plt.plot(df.index, df['ATR'], label='ATR', color='black')
        plt.title(f'{ticker} ATR')
        plt.legend()
        plt.show()

    except Exception as e:
        logger.error(f"Error visualizing data: {e}")

def save_data_to_csv(df, ticker):
    """
    Saves the dataframe with technical indicators to a CSV file.
    """
    try:
        filename = f"{ticker}_data_with_indicators.csv"
        df.to_csv(filename)
        logger.info(f"Data saved to {filename}")
    except Exception as e:
        logger.error(f"Error saving data to CSV: {e}")

def main():
    # Command-line argument parsing
    parser = argparse.ArgumentParser(description="Analyze stock data with technical indicators.")
    parser.add_argument('ticker', type=str, help='The stock ticker symbol')
    parser.add_argument('--start', type=str, default='2020-01-01', help='Start date for data fetch')
    parser.add_argument('--end', type=str, default='2023-01-01', help='End date for data fetch')
    args = parser.parse_args()

    # Fetch stock data
    df = fetch_stock_data(args.ticker, args.start, args.end)

    if df.empty:
        logger.error("No data to process. Exiting.")
        return

    # Add technical indicators
    df = add_technical_indicators(df)

    # Visualize the data with technical indicators
    visualize_data(df, args.ticker)

    # Save the data to CSV
    save_data_to_csv(df, args.ticker)

if __name__ == "__main__":
    main()
