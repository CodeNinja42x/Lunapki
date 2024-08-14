import time
import json
import logging
from binance.client import Client
from datetime import datetime

# Set up logging
logging.basicConfig(filename='trading_log.log', level=logging.INFO,
                    format='%(asctime)s - %(message)s')
logger = logging.getLogger()

# Load API keys from .env or hardcode them
api_key = 'your_api_key_here'
api_secret = 'your_api_secret_here'

client = Client(api_key, api_secret)

symbol = 'BTCUSDT'
portfolio_value = 10000.00  # Initial portfolio value
btc_amount = 0.0
state_file = 'portfolio_state.json'

# Function to save state
def save_state(portfolio_value, btc_amount):
    state = {
        'portfolio_value': portfolio_value,
        'btc_amount': btc_amount,
    }
    with open(state_file, 'w') as f:
        json.dump(state, f)

# Function to load state
def load_state():
    try:
        with open(state_file, 'r') as f:
            state = json.load(f)
            return state['portfolio_value'], state['btc_amount']
    except FileNotFoundError:
        return 10000.00, 0.0  # Default values if state file doesn't exist

# Load the saved state
portfolio_value, btc_amount = load_state()

def buy_btc(amount, price):
    global portfolio_value, btc_amount
    btc_amount += amount
    portfolio_value -= amount * price
    logger.info(f"Bought {amount} BTC at price {price:.2f}")

def sell_btc(amount, price):
    global portfolio_value, btc_amount
    btc_amount -= amount
    portfolio_value += amount * price
    logger.info(f"Sold {amount} BTC at price {price:.2f}")

while True:
    try:
        price = float(client.get_symbol_ticker(symbol=symbol)['price'])
        logger.info(f"Real-time price of {symbol}: {price:.2f}")
        
        # Example trading logic
        if price < 60000 and portfolio_value > 1000:  # Simple buy condition
            buy_btc(0.1, price)
        elif price > 61000 and btc_amount > 0.1:  # Simple sell condition
            sell_btc(0.1, price)
        
        logger.info(f"Current portfolio value: ${portfolio_value:.2f}")
        save_state(portfolio_value, btc_amount)  # Save state after each update
        
        time.sleep(60)  # Wait for 60 seconds before the next check
        
    except Exception as e:
        logger.error(f"Error occurred: {e}")
        time.sleep(60)  # Wait for a minute before retrying
