import os
from dotenv import load_dotenv
from binance.client import Client

# Load environment variables from .env file
load_dotenv()

# Retrieve the API key and secret from the environment
api_key = os.getenv('BINANCE_API_KEY')
api_secret = os.getenv('BINANCE_API_SECRET')

# Initialize Binance client
client = Client(api_key, api_secret)

# Fetch real-time price data
symbol = 'BTCUSDT'  # Example symbol
price = client.get_symbol_ticker(symbol=symbol)
print(f"Real-time price of {symbol}: {price['price']}")
