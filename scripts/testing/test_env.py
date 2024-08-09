import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv('/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/.env')

api_key = os.getenv('BINANCE_API_KEY')
api_secret = os.getenv('BINANCE_SECRET_KEY')

print(f"API Key: {api_key}")
print(f"API Secret: {api_secret}")
