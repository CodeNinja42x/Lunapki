# trade_execution.py
from binance.client import Client
import os

# Load API keys from environment variables
api_key = os.getenv('BINANCE_API_KEY')
api_secret = os.getenv('BINANCE_API_SECRET')

client = Client(api_key, api_secret)

def place_order(symbol, side, quantity, order_type='MARKET'):
    try:
        order = client.create_order(
            symbol=symbol,
            side=side,
            type=order_type,
            quantity=quantity
        )
        return order
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Example usage
if __name__ == "__main__":
    symbol = 'BTCUSDT'
    side = 'BUY'
    quantity = 0.001  # Adjust quantity as needed

    order = place_order(symbol, side, quantity)
    print(order)
