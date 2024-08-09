import os
import logging
import joblib
import pandas as pd
from binance.client import Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up Binance client
client = Client(os.getenv('BINANCE_API_KEY'), os.getenv('BINANCE_API_SECRET'))

# Configure logging
logging.basicConfig(filename='/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/Bot/cron.log', level=logging.INFO)

def make_trading_decision():
    logging.info('Making trading decision...')
    
    # Load models
    models = {
        'RandomForest': joblib.load('/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/models/RandomForest_model.pkl'),
        'GradientBoosting': joblib.load('/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/models/GradientBoosting_model.pkl'),
        'AdaBoost': joblib.load('/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/models/AdaBoost_model.pkl'),
        'CatBoost': joblib.load('/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/models/CatBoost_model.pkl'),
        'XGBoost': joblib.load('/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/models/XGBoost_model.pkl'),
        'LightGBM': joblib.load('/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/models/LightGBM_model.pkl'),
        'LogisticRegression': joblib.load('/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/models/LogisticRegression_model.pkl')
    }
    
    # Assuming you have a function to get the current market data to predict on
    # Replace this with your actual data fetching for prediction
    current_data = pd.DataFrame()  # Replace with actual current data
    
    predictions = {name: model.predict(current_data) for name, model in models.items()}
    logging.info(f'Predictions: {predictions}')
    
    # Majority voting mechanism
    decision = 'buy' if sum(predictions.values()) > len(predictions) / 2 else 'sell'
    logging.info(f'Trading decision: {decision}')
    return decision

def place_order(decision):
    logging.info('Placing order...')
    try:
        if decision == 'buy':
            order = client.order_market_buy(symbol='BTCUSDT', quantity=0.001)
        else:
            order = client.order_market_sell(symbol='BTCUSDT', quantity=0.001)
        logging.info(f'Order placed: {order}')
    except Exception as e:
        logging.error(f'Binance API Exception: {e}')

def main():
    decision = make_trading_decision()
    place_order(decision)

if __name__ == "__main__":
    main()
