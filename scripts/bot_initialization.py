import logging
import os
import time
import pandas as pd
import requests
import math
from binance.client import Client
from dotenv import load_dotenv

# API keys directly added (Remember to keep these secure!)
api_key = "HkXPu1eLbNKFYZ6qIVn73HGsxuoBJAT6sAm6J2VNrIkEeI9972kcDfP7mH6SdCht"
api_secret = "u1wI2ghvrnTlehpXtHbxsKVBstscCBCZiN1VA2EZMhfZ6MC1ChmXqrBr3xMVFjCD"

# Initialize Binance client
client = Client(api_key, api_secret)

# Configure logging
log_directory = "/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/logs"
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

logging.basicConfig(
    filename=os.path.join(log_directory, 'bot_activity.log'),
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def fetch_data(symbol, timeframe):
    logging.info(f"Fetching data for {symbol} with timeframe {timeframe}")
    try:
        url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={timeframe}"
        response = requests.get(url)
        response.raise_for_status()
        ohlcv = response.json()

        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 
                                          'close_time', 'quote_asset_volume', 'number_of_trades',
                                          'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        logging.info("Data fetched and processed successfully")
        return df
    except Exception as e:
        logging.error(f"Error fetching data: {e}")
        return None

def process_data(df):
    logging.info("Processing data")
    try:
        df['close'] = df['close'].astype(float)
        df['MA20'] = df['close'].rolling(window=20).mean()
        logging.info("Data processed successfully")
        return df
    except Exception as e:
        logging.error(f"Error processing data: {e}")
        return None

def get_latest_price(symbol):
    try:
        ticker = client.get_symbol_ticker(symbol=symbol)
        return float(ticker['price'])
    except Exception as e:
        logging.error(f"Error fetching latest price: {e}")
        return None

def get_symbol_precision(symbol):
    try:
        info = client.get_symbol_info(symbol)
        step_size = float(info['filters'][2]['stepSize'])
        precision = int(round(-math.log(step_size, 10), 0))
        return precision
    except Exception as e:
        logging.error(f"Error fetching symbol precision: {e}")
        return 6  # Default precision if there's an error

def calculate_trade_quantity(symbol, notional_value):
    price = get_latest_price(symbol)
    if price is None:
        return None
    quantity = notional_value / price
    precision = get_symbol_precision(symbol)
    adjusted_quantity = round(quantity, precision)
    return adjusted_quantity

def execute_trade(symbol, side, notional_value=20):
    try:
        quantity = calculate_trade_quantity(symbol, notional_value)
        if quantity is None:
            logging.error(f"Failed to calculate quantity for {symbol}")
            return
        logging.info(f"Executing {side} trade for {quantity} of {symbol}")

        # Fetch symbol info to get minQty and maxQty for the symbol
        symbol_info = client.get_symbol_info(symbol)
        min_qty = float(symbol_info['filters'][2]['minQty'])
        max_qty = float(symbol_info['filters'][2]['maxQty'])

        # Ensure quantity meets the LOT_SIZE filter
        if quantity < min_qty or quantity > max_qty:
            logging.error(f"Quantity {quantity} for {symbol} does not meet LOT_SIZE requirements. minQty: {min_qty}, maxQty: {max_qty}")
            return

        order = client.order_market(
            symbol=symbol,
            side=side,
            quantity=quantity
        )
        logging.info(f"Trade executed successfully: {order}")
    except Exception as e:
        logging.error(f"Error executing trade: {e}")

def run_bot():
    logging.info("Starting bot")
    symbols = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT']
    timeframe = '1m'

    for symbol in symbols:
        logging.info(f"Processing {symbol}")
        df = fetch_data(symbol, timeframe)
        if df is not None:
            processed_df = process_data(df)
            if processed_df is not None:
                logging.info("Checking trade conditions")
                last_row = processed_df.iloc[-1]
                if last_row['close'] > last_row['MA20']:
                    execute_trade(symbol, 'BUY', 20)
                elif last_row['close'] < last_row['MA20']:
                    execute_trade(symbol, 'SELL', 20)
                else:
                    logging.info("No trade executed. Waiting for better conditions.")
            else:
                logging.warning("Data processing failed, skipping run")
        else:
            logging.warning("Data fetch failed, skipping run")
    logging.info("Bot cycle complete, sleeping for 60 seconds")

if __name__ == "__main__":
    while True:
        run_bot()
        time.sleep(60)
