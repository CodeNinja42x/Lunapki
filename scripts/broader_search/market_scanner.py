import ccxt
import pandas as pd
import ta
import logging
import json
import time

# Setup logging
logging.basicConfig(filename='market_scanner.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

# Load configuration from a JSON file (you can modify this file for quick changes)
with open('scanner_config.json', 'r') as config_file:
    config = json.load(config_file)

# Connect to Binance (replace with your API key/secret)
exchange = ccxt.binance({
    'apiKey': 'YOUR_API_KEY',
    'secret': 'YOUR_API_SECRET',
})

coins = config["coins"]
timeframe = config["timeframe"]

def fetch_data(symbol):
    try:
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe)
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        return df
    except Exception as e:
        logging.error(f"Error fetching data for {symbol}: {e}")
        return None

def scan_markets():
    for coin in coins:
        df = fetch_data(coin)
        if df is None:
            continue
        
        try:
            # Calculate indicators
            df['rsi'] = ta.momentum.RSIIndicator(df['close']).rsi()
            df['macd'] = ta.trend.MACD(df['close']).macd_diff()
            df['bollinger_hband'] = ta.volatility.BollingerBands(df['close']).bollinger_hband()
            df['bollinger_lband'] = ta.volatility.BollingerBands(df['close']).bollinger_lband()
            
            # Strategy: Signal if RSI < 30 and price near lower Bollinger Band
            if df['rsi'].iloc[-1] < config["rsi_threshold"] and df['close'].iloc[-1] <= df['bollinger_lband'].iloc[-1]:
                logging.info(f"Buy signal for {coin} on {timeframe} timeframe!")
        except Exception as e:
            logging.error(f"Error calculating indicators for {coin}: {e}")

if __name__ == "__main__":
    while True:
        scan_markets()
        time.sleep(config["scan_interval"])  # Interval between scans (in seconds)
