import os
import logging
import time
import numpy as np
import talib
from binance.client import Client
from binance.exceptions import BinanceAPIException
import joblib
from logging.handlers import RotatingFileHandler
import random

# Secure API Key Management
api_key = os.getenv('BINANCE_API_KEY')
api_secret = os.getenv('BINANCE_API_SECRET')
binance_client = Client(api_key, api_secret)

# Setup logging
log_dir = os.path.expanduser('~/crypto_bot_logs')
if not os.path.exists(log_dir):
    os.makedirs(log_dir)
log_file = os.path.join(log_dir, 'bot_log.log')
handler = RotatingFileHandler(log_file, maxBytes=5*1024*1024, backupCount=3)
logging.basicConfig(handlers=[handler], level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('CryptoBot')

# Console handler for real-time output
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(console_formatter)
logger.addHandler(console_handler)

# Load the trained ML model
model = joblib.load('crypto_model.pkl')  # Path to your ML model

# Strategy Parameters
strategy_params = {
    'rsi_buy_threshold': 35,
    'rsi_sell_threshold': 65,
    'ma_short_period': 9,
    'ma_long_period': 21,
    'atr_period': 14,
    'stop_loss_atr_multiplier': 1.5,
    'take_profit_atr_multiplier': 2,
    'trailing_stop_atr_multiplier': 1,
    'random_trade_chance': 50,
    'cooldown_period': 60,
    'max_drawdown': 0.2,
    'retry_attempts': 3,  # Retry mechanism
    'retry_delay': 5      # Retry delay in seconds
}

# Performance Metrics
metrics = {
    'total_trades': 0,
    'successful_trades': 0,
    'random_trades': 0,  # Track cosmic randomness
    'cosmic_fails': 0,   # Track failed cosmic coin flips
    'total_pnl': 0,
}

# Error handling retry mechanism
def retry_request(func, max_attempts, delay, *args, **kwargs):
    attempts = 0
    while attempts < max_attempts:
        try:
            return func(*args, **kwargs)
        except BinanceAPIException as e:
            logger.warning(f"Attempt {attempts + 1}/{max_attempts}: API error {e}")
            attempts += 1
            time.sleep(delay)
    logger.error(f"Max retries reached for {func.__name__}. Moving on.")
    return None

# Function to calculate indicators
def calculate_indicators(symbol):
    try:
        klines = retry_request(binance_client.get_klines, strategy_params['retry_attempts'], strategy_params['retry_delay'],
                               symbol=symbol, interval=Client.KLINE_INTERVAL_5MINUTE, limit=50)
        if klines is None:
            return None, None, None, None, None, None, None, None

        highs, lows, closes = [np.array([float(k[i]) for k in klines]) for i in (2, 3, 4)]
        rsi = talib.RSI(closes, timeperiod=7)
        ma_short = talib.SMA(closes, timeperiod=strategy_params['ma_short_period'])
        ma_long = talib.SMA(closes, timeperiod=strategy_params['ma_long_period'])
        macd, signal, _ = talib.MACD(closes, fastperiod=12, slowperiod=26, signalperiod=9)
        atr = talib.ATR(highs, lows, closes, timeperiod=strategy_params['atr_period'])

        # Prepare features for ML model
        features = np.column_stack((rsi, ma_short, ma_long, macd, signal, atr))
        ml_prediction = model.predict(features[-1:])[0]
        ml_confidence = model.predict_proba(features[-1:])[0][ml_prediction]

        return rsi[-1], ma_short[-1], ma_long[-1], macd[-1], signal[-1], atr[-1], ml_prediction, ml_confidence

    except Exception as e:
        logger.error(f"Error in indicator calculation for {symbol}: {e}")
        return None, None, None, None, None, None, None, None

# Trading logic with random chance and retry
def should_buy(symbol):
    rsi, ma_short, ma_long, macd, signal, atr, ml_prediction, ml_confidence = calculate_indicators(symbol)
    
    if rsi is None:
        return False
    
    # Cosmic random trade chance
    random_chance = random.uniform(0, 100)
    if random_chance < strategy_params['random_trade_chance']:
        metrics['random_trades'] += 1  # Track how many random trades are made
        logger.info(f"Cosmic flip! Random chance triggered with {random_chance:.2f}%.")
    else:
        metrics['cosmic_fails'] += 1  # Track failed cosmic flips
        return False

    if ml_confidence > 0.7 and rsi < strategy_params['rsi_buy_threshold'] and ma_short > ma_long and macd > signal:
        return True
    return False

# Circuit breaker for market chaos
def check_circuit_breaker(usdt_balance, portfolio_peak):
    drawdown = (portfolio_peak - usdt_balance) / portfolio_peak if portfolio_peak else 0
    if drawdown > strategy_params['max_drawdown']:
        logger.warning(f"Max drawdown of {drawdown:.2%} hit. Pausing trading.")
        return True
    return False

# Update the performance log
def update_metrics(pnl, successful_trade):
    metrics['total_trades'] += 1
    if successful_trade:
        metrics['successful_trades'] += 1
    metrics['total_pnl'] += pnl
    logger.info(f"Metrics Updated: Total Trades: {metrics['total_trades']}, Successful Trades: {metrics['successful_trades']}, PnL: {metrics['total_pnl']:.2f} USDT")

# Main bot function
def run_bot():
    global portfolio_peak
    logger.info("Starlight Theorem Plus bot is now active!")
    symbols = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT']

    while True:
        try:
            usdt_balance = float(retry_request(binance_client.get_asset_balance, strategy_params['retry_attempts'], strategy_params['retry_delay'], asset='USDT')['free'])
            portfolio_peak = max(portfolio_peak, usdt_balance) if portfolio_peak else usdt_balance

            if check_circuit_breaker(usdt_balance, portfolio_peak):
                logger.info("Circuit breaker activated. Pausing for 1 hour.")
                time.sleep(3600)
                continue

            for symbol in symbols:
                if should_buy(symbol):
                    logger.info(f"Attempting to buy {symbol}.")
                    # Buy logic, etc.

            logger.info("End of cycle, pausing for 30 seconds.")
            time.sleep(30)

        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            time.sleep(30)

if __name__ == "__main__":
    run_bot()
