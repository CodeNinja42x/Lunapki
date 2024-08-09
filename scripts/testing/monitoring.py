# monitoring.py
import logging

logging.basicConfig(filename='trading_bot.log', level=logging.INFO,
                    format='%(asctime)s - %(message)s')

def log_trade(trade_details):
    logging.info(f"Trade executed: {trade_details}")

# Example usage
if __name__ == "__main__":
    trade_details = {'symbol': 'BTCUSDT', 'side': 'BUY', 'quantity': 0.001, 'price': 50000}
    log_trade(trade_details)
