import os
import logging
from fetch_data import fetch_data
from train_models import train_models
from make_decision import make_decision

# Configure logging
logging.basicConfig(filename='/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/logs/main_script.log', level=logging.INFO)

def main():
    logging.info("Starting main script...")
    
    # Fetch data
    try:
        logging.info("Starting data collection...")
        fetch_data()
        logging.info("Data collection complete.")
    except Exception as e:
        logging.error(f"Error during data collection: {e}")
        return
    
    # Train models
    try:
        logging.info("Starting model training...")
        train_models()
        logging.info("Model training complete.")
    except Exception as e:
        logging.error(f"Error during model training: {e}")
        return

    # Make trading decision
    try:
        logging.info("Making trading decision...")
        make_decision()
        logging.info("Trading decision complete.")
    except Exception as e:
        logging.error(f"Error making decision: {e}")

if __name__ == '__main__':
    main()
