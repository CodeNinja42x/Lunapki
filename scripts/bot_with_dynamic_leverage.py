import ccxt
import os
from dotenv import load_dotenv
import pandas as pd

# Load environment variables from .env file
load_dotenv()

# Fetch API keys from environment variables
api_key = os.getenv('BINANCE_API_KEY')
api_secret = os.getenv('BINANCE_API_SECRET')

# Initialize Binance exchange
exchange = ccxt.binance({
    'apiKey': api_key,
    'secret': api_secret,
    'enableRateLimit': True,
})

# Function to adjust leverage
def adjust_leverage(symbol, leverage):
    try:
        exchange.fapiPrivate_post_leverage({
            'symbol': symbol.replace('/', ''),
            'leverage': leverage
        })
        print(f"Leverage set to {leverage}x for {symbol}")
    except Exception as e:
        print(f"An error occurred while setting leverage: {e}")

# Function to place a buy or sell order
def place_order(symbol, order_type, amount, price=None):
    try:
        if order_type == 'market':
            order = exchange.create_market_sell_order(symbol, amount) if amount < 0 else exchange.create_market_buy_order(symbol, amount)
        elif order_type == 'limit' and price:
            order = exchange.create_limit_sell_order(symbol, abs(amount), price) if amount < 0 else exchange.create_limit_buy_order(symbol, abs(amount), price)
        print(f"Order placed: {order}")
        return order
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Your trade logic function (simplified)
def trade_logic(df):
    trend_slope = df['close'].diff().mean()  # Example for slope calculation
    volatility = df['close'].rolling(window=10).std().mean()  # Example for volatility calculation

    if trend_slope > 10:
        adjust_leverage('BTC/USDT', 20)  # High leverage for strong trends
    elif volatility > 50:
        adjust_leverage('BTC/USDT', 10)  # Medium leverage for volatile markets
    else:
        adjust_leverage('BTC/USDT', 2)  # Low leverage for calmer conditions

    # Example model prediction and trade action
    model_prediction = "Sell/Hold"  # Placeholder for the model's output
    if model_prediction == 'Buy':
        place_order('BTC/USDT', 'market', 0.002)  # Buy order
    elif model_prediction == 'Sell':
        place_order('BTC/USDT', 'market', -0.002)  # Sell order

# Example of fetching and preparing data
# (This should be replaced with your actual data fetching logic)
def fetch_data():
    # Example fetching of historical data
    return pd.DataFrame({
        'close': [23271.9, 23300.0, 23250.0],  # Example data
        'high': [23300.0, 23350.0, 23320.0],
        'low': [23200.0, 23250.0, 23210.0],
        'volume': [1000, 1200, 1100]
    })

# Main execution logic
df = fetch_data()
trade_logic(df)
