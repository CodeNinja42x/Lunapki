import os
import ccxt
from dotenv import load_dotenv

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

# Attempt to fetch balance
try:
    balance = exchange.fetch_balance()
    print("Balance fetched successfully:", balance)
except Exception as e:
    print("Error fetching balance:", str(e))
