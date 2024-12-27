import time
import math
import os
import csv
import random
import pandas as pd
from dotenv import load_dotenv
from binance.client import Client
from binance.exceptions import BinanceAPIException

# -----------------------------------------------------------------------------
# Load Environment Variables
# -----------------------------------------------------------------------------
load_dotenv()
API_KEY = os.getenv('BINANCE_API_KEY')
API_SECRET = os.getenv('BINANCE_API_SECRET')

# -----------------------------------------------------------------------------
# Initialize Binance Client
# -----------------------------------------------------------------------------
client = Client(API_KEY, API_SECRET)

# -----------------------------------------------------------------------------
# Parameters with Configurable Defaults
# -----------------------------------------------------------------------------
DEFAULT_LEVERAGE = int(os.getenv('DEFAULT_LEVERAGE', 10))
RISK_PER_TRADE = float(os.getenv('RISK_PER_TRADE', 0.01))
ATR_MULTIPLIER = float(os.getenv('ATR_MULTIPLIER', 1.5))
RISK_REWARD_RATIO = float(os.getenv('RISK_REWARD_RATIO', 2.0))
MIN_NOTIONAL = float(os.getenv('MIN_NOTIONAL', 5))

# Funny Trade Log File Name
TRADE_LOG_FILE = f"trades_of_glory_{random.randint(1000, 9999)}.csv"
DEBUG_LOG_FILE = "super_secret_debug_log.csv"

# -----------------------------------------------------------------------------
# Utility Functions
# -----------------------------------------------------------------------------
def ensure_csv_headers(filename, headers):
    file_exists = os.path.isfile(filename)
    if not file_exists:
        with open(filename, mode='w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(headers)

def log_debug_info(symbol, balance, price, atr, size):
    ensure_csv_headers(
        DEBUG_LOG_FILE,
        ["symbol", "balance", "price", "atr", "calculated_size", "timestamp"]
    )
    try:
        with open(DEBUG_LOG_FILE, mode="a", newline='') as file:
            writer = csv.writer(file)
            writer.writerow([symbol, balance, price, atr, size, time.time()])
    except Exception as e:
        print(f"Error logging debug information: {e}")

# -----------------------------------------------------------------------------
# Fetch Account Balance
# -----------------------------------------------------------------------------
def get_balance() -> float:
    try:
        balance = client.futures_account_balance()
        usdt_balance = next((item for item in balance if item["asset"] == "USDT"), None)
        if usdt_balance:
            return float(usdt_balance["balance"])
        else:
            print("Could not find USDT balance in futures account.")
            return 0.0
    except BinanceAPIException as e:
        print(f"Error fetching balance: {e}")
        return 0.0

# -----------------------------------------------------------------------------
# Main Trading Example
# -----------------------------------------------------------------------------
def run_trading_example(symbol):
    print(f"Starting trade example for {symbol}...")

    # Fetch Account Balance
    balance = get_balance()
    print(f"Account Balance: {balance}")
    if balance <= 0:
        print("No available USDT balance to trade. Please fund your account or verify your API credentials.")
        return

    # Fetch Current Price
    try:
        ticker = client.futures_symbol_ticker(symbol=symbol)
        current_price = float(ticker["price"])
        print(f"Current Price of {symbol}: {current_price}")
    except BinanceAPIException as e:
        print(f"Error fetching price for {symbol}: {e}")
        return

    # Calculate ATR
    atr_value = calculate_atr(symbol)
    print(f"ATR Value for {symbol}: {atr_value}")

    # Calculate Position Size
    size = calculate_position_size(symbol, balance, current_price, atr_value)
    print(f"Calculated Position Size: {size}")

    # Log Debug Info
    log_debug_info(symbol, balance, current_price, atr_value, size)

    if size <= 0:
        print(
            f"Position size is too small ({size}). This could happen due to:\n"
            f"  - Insufficient account balance (Balance: {balance} USDT)\n"
            f"  - High ATR value ({atr_value}), indicating increased market volatility\n"
            f"  - Minimum notional requirement not met (Min: {MIN_NOTIONAL} USDT)\n"
            "Try increasing your account balance or adjusting risk parameters."
        )
        return

    print("Order logic here...")
    # Add order placement logic
