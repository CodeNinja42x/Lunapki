import os
import logging
import numpy as np
import pandas as pd
import talib
from binance.client import Client
import joblib
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Logger setup
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('BacktestLogger')

# Load the model
model_path = '/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/crypto_model.pkl'
model = joblib.load(model_path)

# Binance API Setup
binance_api_key = os.getenv("BINANCE_API_KEY")
binance_api_secret = os.getenv("BINANCE_API_SECRET")
binance_client = Client(binance_api_key, binance_api_secret)

# Historical data function
def get_historical_data(symbol, interval, days=180):
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(days=days)
    klines = binance_client.get_historical_klines(symbol, interval, start_time.strftime("%d %b %Y %H:%M:%S"), end_time.strftime("%d %b %Y %H:%M:%S"))
    data = pd.DataFrame(klines, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])
    data['timestamp'] = pd.to_datetime(data['timestamp'], unit='ms')
    data['close'] = data['close'].astype(float)
    return data

# Strategy and backtest functions (simplified for focus)
def backtest_strategy(symbol):
    data = get_historical_data(symbol, Client.KLINE_INTERVAL_5MINUTE, days=180)
    data['returns'] = data['close'].pct_change()  # Calculate daily returns
    return data['returns']

# Calculate maximum drawdown
def max_drawdown(returns):
    cum_returns = (1 + returns).cumprod()
    peak = cum_returns.cummax()
    drawdown = (cum_returns - peak) / peak
    return drawdown.min()

# Sharpe ratio
def sharpe_ratio(returns, risk_free_rate=0):
    return np.sqrt(252) * (returns.mean() - risk_free_rate) / returns.std()

# Sortino ratio
def sortino_ratio(returns, risk_free_rate=0):
    downside_returns = returns[returns < risk_free_rate]
    downside_std = np.sqrt(252) * downside_returns.std()
    return np.sqrt(252) * (returns.mean() - risk_free_rate) / downside_std

# Backtest runner
def run_backtest():
    account_balance = 10000  # Starting balance
    symbols = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT']
    total_returns = pd.Series(dtype=float)
    
    for symbol in symbols:
        returns = backtest_strategy(symbol)
        total_returns = total_returns.append(returns.dropna())

    max_dd = max_drawdown(total_returns)
    sharpe = sharpe_ratio(total_returns)
    sortino = sortino_ratio(total_returns)

    logger.info(f"Max Drawdown: {max_dd}")
    logger.info(f"Sharpe Ratio: {sharpe}")
    logger.info(f"Sortino Ratio: {sortino}")

# Run the backtest
if __name__ == "__main__":
    run_backtest()
