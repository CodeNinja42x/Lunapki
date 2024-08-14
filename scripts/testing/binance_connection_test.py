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

# Test connection
status = client.get_system_status()
print("Binance System Status:", status)
