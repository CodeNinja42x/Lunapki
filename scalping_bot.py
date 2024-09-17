import os
import logging
import time
import numpy as np
import talib
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceOrderException
from logging.handlers import RotatingFileHandler
import requests.exceptions  # For handling specific network errors

# Secure API Key Management
api_key = os.getenv('BINANCE_API_KEY')
api_secret = os.getenv('BINANCE_API_SECRET')
binance_client = Client(api_key, api_secret)

# Setup logging with rotation
log_dir = os.path.expanduser('~/crypto_bot_logs')
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

log_file = os.path.join(log_dir, 'bot_log.log')
handler = RotatingFileHandler(log_file, maxBytes=5*1024*1024, backupCount=3)
logging.basicConfig(
    handlers=[handler],
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('CryptoBot')

# Add a console handler for real-time output
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(console_formatter)
logger.addHandler(console_handler)

# Initialize active positions
active_positions = [{'symbol': 'BTCUSDT', 'entry_price': None}, {'symbol': 'ETHUSDT', 'entry_price': None}, {'symbol': 'BNBUSDT', 'entry_price': None}, {'symbol': 'PEPEUSDT', 'entry_price': None}]

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
    'trailing_stop_loss': 0.005  # 0.5% trailing stop-loss
}

def calculate_indicators(symbol):
    try:
        klines = binance_client.get_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_5MINUTE, limit=50)
        highs, lows, closes = [np.array([float(k[i]) for k in klines]) for i in (2, 3, 4)]
        min_len = min(len(highs), len(lows), len(closes))
        highs, lows, closes = highs[:min_len], lows[:min_len], closes[:min_len]

        rsi = talib.RSI(closes, timeperiod=7)
        ma_short = talib.SMA(closes, timeperiod=strategy_params['ma_short_period'])
        ma_long = talib.SMA(closes, timeperiod=strategy_params['ma_long_period'])
        upper_band = talib.BBANDS(closes, timeperiod=10, nbdevup=1.5, nbdevdn=1.5)[0]
        atr = talib.ATR(highs, lows, closes, timeperiod=7)

        mask = ~np.isnan(rsi) & ~np.isnan(ma_short) & ~np.isnan(ma_long) & ~np.isnan(upper_band) & ~np.isnan(atr)
        rsi, ma_short, ma_long, upper_band, atr = rsi[mask], ma_short[mask], ma_long[mask], upper_band[mask], atr[mask]

        if len(rsi) < 3:
            logger.error(f"Indicator calculation skipped: Not enough valid data points.")
            return None, None, None, None, None

        return rsi[-1], ma_short[-1], ma_long[-1], closes[-1], atr[-1]

    except (requests.exceptions.RequestException, BinanceAPIException) as e:
        logger.error(f"Error in indicator calculation for {symbol}: {e}")
        return None, None, None, None, None

def adjust_strategy_based_on_volatility(atr):
    if atr > strategy_params['volatility_threshold_high']:
        logger.info("Market is volatile, adjusting for caution.")
        strategy_params['rsi_buy_threshold'] = 35
        strategy_params['rsi_sell_threshold'] = 65
    elif atr < strategy_params['volatility_threshold_low']:
        logger.info("Market is calm, adjusting for opportunity.")
        strategy_params['rsi_buy_threshold'] = 45
        strategy_params['rsi_sell_threshold'] = 55
    else:
        logger.info("Market volatility normal, keeping default strategy.")

def should_buy(symbol):
    rsi, ma_short, ma_long, close, atr = calculate_indicators(symbol)
    if rsi is not None:
        adjust_strategy_based_on_volatility(atr)
        logger.info(f"Analyzing {symbol}: RSI = {rsi:.2f}, MA Short = {ma_short:.2f}, MA Long = {ma_long:.2f}, Close = {close:.2f}, ATR = {atr:.2f}")
        if rsi < strategy_params['rsi_buy_threshold'] and ma_short > ma_long and close < ma_short:
            logger.info(f"Buying signal for {symbol}: RSI is below threshold, short MA is above long MA, and price is below short MA.")
            return True
    return False

def should_sell(symbol, entry_price):
    _, _, _, current_price, _ = calculate_indicators(symbol)
    if current_price is None:
        return False
    
    unrealized_pnl = (current_price - entry_price) / entry_price * 100
    logger.info(f"{symbol}: Current Price = {current_price:.2f}, Entry Price = {entry_price:.2f}, Unrealized PnL = {unrealized_pnl:.2f}%")
    
    if current_price >= entry_price * (1 + strategy_params['take_profit']):
        logger.info(f"Take-profit reached for {symbol}. Unrealized PnL: {unrealized_pnl:.2f}%. Preparing to sell.")
        return True
    elif current_price <= entry_price * (1 - strategy_params['stop_loss']):
        logger.info(f"Stop-loss hit for {symbol}. Unrealized PnL: {unrealized_pnl:.2f}%. Preparing to sell.")
        return True
    elif current_price >= entry_price * (1 + strategy_params['trailing_stop_loss']):
        logger.info(f"Trailing stop-loss hit for {symbol}. Unrealized PnL: {unrealized_pnl:.2f}%. Preparing to sell.")
        return True
    return False

def calculate_quantity(symbol, usdt_balance):
    try:
        info = binance_client.get_symbol_info(symbol)
        step_size = float([f for f in info['filters'] if f['filterType'] == 'LOT_SIZE'][0]['stepSize'])
        price = float(binance_client.get_symbol_ticker(symbol=symbol)['price'])
        quantity = usdt_balance / price
        quantity = round(quantity - (quantity % step_size), 8)
        logger.info(f"Calculated quantity for {symbol}: {quantity:.8f} at price {price:.2f}, total notional value = {quantity * price:.2f} USDT.")
        return quantity, quantity * price
    except BinanceAPIException as e:
        logger.error(f"Binance said 'No': {e}")
        return 0, 0
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return 0, 0

def place_order(symbol, quantity):
    try:
        order = binance_client.order_market_buy(symbol=symbol, quantity=quantity)
        logger.info(f"Order placed for {symbol}: {order}")
        return order['fills'][0]['price']
    except (BinanceAPIException, BinanceOrderException) as e:
        logger.error(f"Order failed for {symbol}: {e}")
    except Exception as e:
        logger.error(f"Order exception for {symbol}: {e}")
    return None

def sell_all(symbol, reason):
    try:
        quantity = binance_client.get_asset_balance(asset=symbol.replace('USDT', ''))['free']
        if float(quantity) > 0:
            order = binance_client.order_market_sell(symbol=symbol, quantity=quantity)
            logger.info(f"{reason} - Sold all {symbol}. Order: {order}")
    except Exception as e:
        logger.error(f"Failed to sell {symbol}: {e}")

def run_bot():
    logger.info("Starlight Theorem Plus bot is now active!")
    symbols = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT']

    while True:
        try:
            usdt_balance = 0  # Set to zero or a minimal value if there's no money for actual trading
            logger.info(f"Our digital wallet boasts {usdt_balance} USDT. Analyzing opportunities...")

            for position in active_positions:
                symbol = position['symbol']
                if position['entry_price'] is None:
                    if should_buy(symbol):
                        quantity, notional = calculate_quantity(symbol, usdt_balance * 0.05)  # Smaller position sizes for scalping
                        if quantity > 0 and notional >= 10:
                            entry_price = place_order(symbol, quantity)
                            if entry_price:
                                position['entry_price'] = float(entry_price)
                        else:
                            logger.info(f"{symbol} isn't worth our coin today, or the amount is too small.")
                    else:
                        logger.info(f"No buying signal for {symbol} at the moment.")
                else:
                    if should_sell(symbol, position['entry_price']):
                        sell_all(symbol, "Exiting position based on take-profit or stop-loss.")
                        position['entry_price'] = None  # Reset entry price after selling

            logger.info("Cycle complete. Taking a strategic pause for 30 seconds.")  # Reduced pause for faster scalping
            time.sleep(30)

        except (requests.exceptions.RequestException, BinanceAPIException) as e:
            logger.error(f"API or network error: {e}. Retrying after a brief pause.")
            time.sleep(60)
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
            time.sleep(60)

if __name__ == "__main__":
    run_bot()
