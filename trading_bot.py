import os
import logging
import time
import numpy as np
import talib
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceOrderException
import joblib
from logging.handlers import RotatingFileHandler

# Secure API Key Management (Update with Testnet API keys)
api_key = os.getenv('BINANCE_API_KEY')  # Testnet API key
api_secret = os.getenv('BINANCE_API_SECRET')  # Testnet API secret

# Initialize Binance client for Testnet
binance_client = Client(api_key, api_secret, testnet=True)
binance_client.API_URL = 'https://testnet.binance.vision/api'  # Use Testnet API URL for spot trading

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

# Load the trained ML model (Ensure your model is in the working directory)
model = joblib.load('crypto_model.pkl')  # Path to your ML model

# Strategy Parameters
strategy_params = {
    'rsi_buy_threshold': 40,
    'rsi_sell_threshold': 60,
    'ma_short_period': 9,
    'ma_long_period': 21,
    'volatility_threshold_high': 1.5,
    'volatility_threshold_low': 0.3,
    'stop_loss': 0.01,
    'take_profit': 0.02,
    'trailing_stop_loss': 0.005,
    'ml_confidence_threshold': 0.7
}

# Portfolio management and metrics tracking
portfolio_peak = None
max_drawdown = 0.2
total_trades = 0
successful_trades = 0
total_pnl = 0

# Dictionary to track open positions and cooldown periods (properly initialize for symbols)
open_positions = {}  # To track active trades
cooldown_periods = {}  # To track cooldown times for symbols

# Function to calculate indicators
def calculate_indicators(symbol):
    try:
        klines = binance_client.get_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_5MINUTE, limit=50)
        highs, lows, closes = [np.array([float(k[i]) for k in klines]) for i in (2, 3, 4)]
        min_len = min(len(highs), len(lows), len(closes))
        highs, lows, closes = highs[:min_len], lows[:min_len], closes[:min_len]

        rsi = talib.RSI(closes, timeperiod=7)
        ma_short = talib.SMA(closes, timeperiod=strategy_params['ma_short_period'])
        ma_long = talib.SMA(closes, timeperiod=strategy_params['ma_long_period'])
        macd, signal, _ = talib.MACD(closes)
        atr = talib.ATR(highs, lows, closes, timeperiod=14)

        # Prepare features for ML model
        features = np.column_stack((rsi, ma_short, ma_long, macd, signal, atr))
        ml_prediction = model.predict(features[-1:])[0]
        ml_confidence = model.predict_proba(features[-1:])[0][ml_prediction]

        return rsi[-1], ma_short[-1], ma_long[-1], macd[-1], signal[-1], atr[-1], ml_prediction, ml_confidence

    except Exception as e:
        logger.error(f"Error in indicator calculation for {symbol}: {e}")
        return None, None, None, None, None, None, None, None

# Dynamic Cooldown based on ATR (volatility)
def get_dynamic_cooldown(atr):
    base_cooldown = 300  # Base cooldown of 5 minutes
    volatility_factor = atr / 0.01  # Adjust the factor for desired sensitivity
    return base_cooldown * volatility_factor

# Dynamic Allocation based on ML Confidence
def dynamic_allocation(symbol, usdt_balance, ml_confidence):
    min_allocation = 0.01  # 1% allocation
    max_allocation = 0.10  # 10% allocation
    allocation_factor = min_allocation + (max_allocation - min_allocation) * ml_confidence  # Scale based on confidence
    return usdt_balance * allocation_factor

# Check for max drawdown limit
def check_drawdown(usdt_balance, portfolio_peak, max_drawdown):
    drawdown = (portfolio_peak - usdt_balance) / portfolio_peak if portfolio_peak else 0
    if drawdown > max_drawdown:
        logger.info(f"Max drawdown reached: {drawdown:.2%}. Pausing trading.")
        return True
    return False

# Update Performance Metrics
def update_metrics(pnl, trade_successful):
    global total_trades, successful_trades, total_pnl
    total_trades += 1
    if trade_successful:
        successful_trades += 1
    total_pnl += pnl
    win_rate = successful_trades / total_trades if total_trades > 0 else 0
    logger.info(f"Current win rate: {win_rate:.2%}, Total PnL: {total_pnl:.2f} USDT")

# Place a trailing stop-loss order
def place_trailing_stop_loss(symbol, quantity, trailing_stop_percentage):
    try:
        order = binance_client.create_order(
            symbol=symbol,
            side='SELL',
            type='TRAILING_STOP_MARKET',
            quantity=quantity,
            callbackRate=trailing_stop_percentage
        )
        logger.info(f"Placed trailing stop-loss for {symbol} with {trailing_stop_percentage}% trail.")
    except Exception as e:
        logger.error(f"Failed to place trailing stop-loss for {symbol}: {e}")

# Determine if we should buy, incorporating dynamic cooldown logic
def should_buy(symbol):
    rsi, ma_short, ma_long, macd, signal, atr, ml_prediction, ml_confidence = calculate_indicators(symbol)
    
    # Check cooldown for the symbol
    if symbol in cooldown_periods and time.time() - cooldown_periods[symbol] < get_dynamic_cooldown(atr):
        logger.info(f"{symbol} is still in dynamic timeout due to volatility, skipping buy.")
        return False

    if ml_confidence > strategy_params['ml_confidence_threshold']:
        if ml_prediction == 1 and rsi < strategy_params['rsi_buy_threshold'] and ma_short > ma_long and macd > signal:
            return True
    return False

# Determine if we should sell
def should_sell(symbol, entry_price):
    rsi, ma_short, ma_long, macd, signal, atr, ml_prediction, ml_confidence = calculate_indicators(symbol)
    
    if rsi is not None:
        current_price = float(binance_client.get_symbol_ticker(symbol=symbol)['price'])
        unrealized_pnl = (current_price - entry_price) / entry_price * 100
        logger.info(f"{symbol}: Current Price = {current_price:.2f}, Entry Price = {entry_price:.2f}, Unrealized PnL = {unrealized_pnl:.2f}%, ML Confidence = {ml_confidence:.2f}")

        if current_price >= entry_price * (1 + strategy_params['take_profit']) or current_price <= entry_price * (1 - strategy_params['stop_loss']):
            return True, current_price
        elif ml_confidence > strategy_params['ml_confidence_threshold'] and ml_prediction == 0:
            return True, current_price
    return False, None

# Calculate order quantity, accounting for trading fees
def calculate_quantity(symbol, usdt_balance):
    try:
        info = binance_client.get_symbol_info(symbol)
        step_size = float([f for f in info['filters'] if f['filterType'] == 'LOT_SIZE'][0]['stepSize'])
        price = float(binance_client.get_symbol_ticker(symbol=symbol)['price'])
        quantity = usdt_balance / price
        quantity = round(quantity - (quantity % step_size), 8)
        logger.info(f"Calculated quantity for {symbol}: {quantity:.8f} at price {price:.2f}.")
        return quantity, quantity * price
    except BinanceAPIException as e:
        logger.error(f"Binance API error for {symbol}: {e}")
        return 0, 0
    except Exception as e:
        logger.error(f"Error occurred: {e}")
        return 0, 0

# Place a market buy order
def place_order(symbol, quantity):
    try:
        order = binance_client.order_market_buy(symbol=symbol, quantity=quantity)
        logger.info(f"Order placed for {symbol}: {order}")
        return order['fills'][0]['price']
    except BinanceAPIException as e:
        logger.error(f"Order failed for {symbol}: {e}")
    except Exception as e:
        logger.error(f"Order exception for {symbol}: {e}")
    return None

# Sell all of the asset
def sell_all(symbol, reason):
    try:
        quantity = binance_client.get_asset_balance(asset=symbol.replace('USDT', ''))['free']
        if float(quantity) > 0:
            order = binance_client.order_market_sell(symbol=symbol, quantity=quantity)
            logger.info(f"{reason} - Sold all {symbol}. Order: {order}")
    except Exception as e:
        logger.error(f"Failed to sell {symbol}: {e}")

# The main function running the bot
def run_bot():
    global portfolio_peak
    logger.info("Starlight Theorem Plus bot is now active in paper trading mode (Testnet)!")
    symbols = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT']

    while True:
        try:
            usdt_balance = float(binance_client.get_asset_balance(asset='USDT')['free'])
            portfolio_peak = max(portfolio_peak, usdt_balance) if portfolio_peak else usdt_balance
            logger.info(f"Current USDT balance: {usdt_balance:.2f}. Searching for opportunities...")

            if check_drawdown(usdt_balance, portfolio_peak, max_drawdown):
                logger.info("Pausing trading due to max drawdown.")
                time.sleep(3600)  # Pause for an hour
                continue

            for symbol in symbols:
                if symbol in open_positions:
                    # Check if we should exit an existing position
                    entry_price = open_positions[symbol]['entry_price']
                    should_exit, exit_price = should_sell(symbol, entry_price)
                    if should_exit:
                        pnl = exit_price - entry_price  # Calculate profit or loss
                        update_metrics(pnl, pnl > 0)
                        sell_all(symbol, "Closing position based on strategy")
                        logger.info(f"Closed {symbol} at {exit_price}.")
                        del open_positions[symbol]
                        cooldown_periods[symbol] = time.time()  # Add to cooldown after selling
                else:
                    # Look for buy opportunities if no open position
                    if should_buy(symbol):
                        quantity, notional = calculate_quantity(symbol, dynamic_allocation(symbol, usdt_balance, strategy_params['ml_confidence_threshold']))
                        if quantity > 0 and notional >= 10:
                            entry_price = place_order(symbol, quantity)
                            if entry_price:
                                logger.info(f"Bought {symbol} at {entry_price}")
                                open_positions[symbol] = {'entry_price': float(entry_price)}  # Track the open position
                                place_trailing_stop_loss(symbol, quantity, strategy_params['trailing_stop_loss'] * 100)
                            else:
                                logger.info(f"Failed to buy {symbol}.")
                        else:
                            logger.info(f"{symbol} not worth our investment today.")

            logger.info("Cycle complete. Pausing for 30 seconds.")
            time.sleep(30)

        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
            time.sleep(30)

# Start the bot
if __name__ == "__main__":
    run_bot()
