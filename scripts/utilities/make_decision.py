import os
import pandas as pd
import joblib
import logging
from binance.client import Client
from binance.exceptions import BinanceAPIException
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv('/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/.env')

# Configure logging
logging.basicConfig(filename='/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/logs/make_decision.log', level=logging.INFO)

def make_decision():
    try:
        logging.info("Making trading decision...")
        data = pd.read_csv('/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/data/data.csv')
        X = data.drop(columns=['target']).iloc[-1:]

        scaler = joblib.load('/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/models/scaler.pkl')
        X_scaled = scaler.transform(X)

        predictions = {}
        models_path = '/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/models'
        for model_file in os.listdir(models_path):
            if model_file == 'scaler.pkl':
                continue
            model_name = model_file.split('_')[0]
            model = joblib.load(os.path.join(models_path, model_file))
            prediction = model.predict(X_scaled)[0]
            predictions[model_name] = prediction

        logging.info(f"Predictions: {predictions}")

        decision = max(predictions.values(), key=list(predictions.values()).count)
        logging.info(f"Trading decision: {decision}")

        if decision == 1:
            place_order('buy')
        else:
            place_order('sell')
    except Exception as e:
        logging.error(f"Error making decision: {e}")

def place_order(decision):
    try:
        api_key = os.getenv('BINANCE_API_KEY')
        api_secret = os.getenv('BINANCE_SECRET_KEY')

        if not api_key or not api_secret:
            logging.error("API Key or Secret is missing.")
            return

        client = Client(api_key, api_secret)
        symbol = 'BTCUSDT'
        quantity = 0.001

        # Check account balance
        asset = symbol.replace('USDT', '')
        balance = client.get_asset_balance(asset=asset)
        available_balance = float(balance['free'])

        if decision == 'buy':
            logging.info("Placing buy order...")
            order = client.order_market_buy(symbol=symbol, quantity=quantity)
        else:
            if available_balance < quantity:
                logging.error(f"Insufficient balance to place sell order. Available balance: {available_balance}")
                return
            logging.info("Placing sell order...")
            order = client.order_market_sell(symbol=symbol, quantity=quantity)

        logging.info(f"Order response: {order}")
    except BinanceAPIException as e:
        logging.error(f"Binance API Exception: {e}")
    except Exception as e:
        logging.error(f"General Exception: {e}")

if __name__ == '__main__':
    make_decision()
