import os
import logging
import numpy as np
import talib
from binance.client import Client
import joblib
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Logger setup
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('BacktestLogger')

# Load the model
model_path = '/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/crypto_model.pkl'
if not os.path.exists(model_path):
    logger.error(f"Model file {model_path} not found. Exiting...")
    exit(1)
model = joblib.load(model_path)
logger.info(f"Model loaded successfully from {model_path}")

# Binance API Setup
binance_api_key = os.getenv("BINANCE_API_KEY")
binance_api_secret = os.getenv("BINANCE_API_SECRET")
binance_client = Client(binance_api_key, binance_api_secret)

# Updated strategy parameters
strategy_params = {
    'rsi_buy_threshold': 50,  # Still using 50 to generate more buy signals
    'stop_loss_atr_multiplier': 0.3,  # Tighter stop-loss to reduce large losses
    'take_profit_atr_multiplier': 1.0,  # More conservative take-profit
    'confidence_threshold': 0.7,  # Increased to reduce low-confidence trades
    'volatility_threshold': 0.02  # Threshold for market volatility
}

# Risk management and dynamic position sizing with reduced risk per trade
def calculate_position_size(account_balance, atr, risk_per_trade=0.005):  # Reduced to 0.5% risk per trade
    return (account_balance * risk_per_trade) / atr

# Simulate trades with stop loss, take profit, and transaction costs
def simulate_trade(symbol, data, entry_price, stop_loss_level, take_profit_level, fee_rate=0.001):
    for i, row in data.iterrows():
        current_price = row['close']
        pnl = current_price - entry_price - (current_price + entry_price) * fee_rate / 2
        if current_price <= entry_price * (1 - stop_loss_level):
            logger.info(f"Trade exited at stop-loss for {symbol}. Entry: {entry_price}, Exit: {current_price}, PnL: {pnl}")
            return pnl
        elif current_price >= entry_price * (1 + take_profit_level):
            logger.info(f"Trade exited at take-profit for {symbol}. Entry: {entry_price}, Exit: {current_price}, PnL: {pnl}")
            return pnl
    final_price = data['close'].iloc[-1]
    pnl = final_price - entry_price - (final_price + entry_price) * fee_rate / 2
    logger.info(f"Trade exited at end of data for {symbol}. Entry: {entry_price}, Exit: {final_price}, PnL: {pnl}")
    return pnl

# Plot trade distribution
def plot_trade_distribution(returns):
    plt.figure(figsize=(10, 6))
    plt.hist(returns, bins=50)
    plt.title('Distribution of Trade Returns')
    plt.xlabel('PnL')
    plt.ylabel('Frequency')
    plt.show()

# Sharpe Ratio Calculation
def calculate_sharpe_ratio(returns, risk_free_rate=0.02, annualization_factor=252):
    excess_returns = np.array(returns) - risk_free_rate
    return np.sqrt(annualization_factor) * (np.mean(excess_returns) / np.std(excess_returns))

# Get historical data
def get_historical_data(symbol, interval, days=180):  # Extend period for better testing
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(days=days)
    try:
        klines = binance_client.get_historical_klines(symbol, interval, start_time.strftime("%d %b %Y %H:%M:%S"), end_time.strftime("%d %b %Y %H:%M:%S"))
        data = pd.DataFrame(klines, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])
        data['timestamp'] = pd.to_datetime(data['timestamp'], unit='ms')
        data['close'] = data['close'].astype(float)
        data['high'] = data['high'].astype(float)
        data['low'] = data['low'].astype(float)
        return data
    except Exception as e:
        logger.error(f"Error fetching data for {symbol}: {e}")
        return None

# Technical indicators calculation
def calculate_indicators(data):
    close = data['close'].values
    high = data['high'].values
    low = data['low'].values

    data['rsi'] = talib.RSI(close, timeperiod=14)
    data['ma_short'] = talib.SMA(close, timeperiod=20)
    data['ma_long'] = talib.SMA(close, timeperiod=50)
    macd, signal, _ = talib.MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)
    data['macd'] = macd
    data['atr'] = talib.ATR(high, low, close, timeperiod=14)
    
    # Add additional features
    data['momentum'] = data['close'].pct_change()
    data['bb_upper'], data['bb_middle'], data['bb_lower'] = talib.BBANDS(close, timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)
    data['bb_width'] = (data['bb_upper'] - data['bb_lower']) / data['bb_middle']
    
    return data

# Backtest strategy
def backtest_strategy(symbol, account_balance):
    data = get_historical_data(symbol, Client.KLINE_INTERVAL_5MINUTE, days=180)
    if data is None or data.isnull().values.any():
        logger.error(f"Data integrity issues detected for {symbol}. Skipping...")
        return 0
    
    data = calculate_indicators(data)
    total_pnl = 0
    for i in range(len(data) - 1):
        row = data.iloc[i]
        # Use only the original 4 features: RSI, MA short, MA long, and MACD
        features = np.array([row['rsi'], row['ma_short'], row['ma_long'], row['macd']]).reshape(1, -1)
        
        # Log important indicators and predictions
        logger.info(f"RSI: {row['rsi']}, MACD: {row['macd']}, ATR: {row['atr']}")

        try:
            model_prediction = model.predict(features)[0]
            model_prediction = np.clip(model_prediction, 0, 1)
            logger.info(f"Model Prediction: {model_prediction}")
        except Exception as e:
            logger.error(f"Error in model prediction for {symbol}: {e}")
            continue

        # Apply confidence threshold
        if model_prediction > strategy_params['confidence_threshold'] and row['rsi'] < strategy_params['rsi_buy_threshold']:
            entry_price = row['close']
            atr = row['atr']
            stop_loss_level = atr * strategy_params['stop_loss_atr_multiplier'] / entry_price
            take_profit_level = atr * strategy_params['take_profit_atr_multiplier'] / entry_price

            if atr > strategy_params['volatility_threshold']:
                stop_loss_level *= 0.5  # Tighter stop-loss for volatile markets

            position_size = calculate_position_size(account_balance, atr)
            pnl = simulate_trade(symbol, data.iloc[i+1:], entry_price, stop_loss_level, take_profit_level)
            total_pnl += pnl * position_size

    return total_pnl

# Backtest runner
def run_backtest():
    account_balance = 10000  # Starting balance
    symbols = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT']
    total_pnl = 0
    for symbol in symbols:
        logger.info(f"Running backtest on {symbol}")
        pnl = backtest_strategy(symbol, account_balance)
        logger.info(f"{symbol} - Total PnL: {pnl}")
        total_pnl += pnl

    logger.info(f"Total PnL for all symbols: {total_pnl}")

# Run the backtest
if __name__ == "__main__":
    run_backtest()
