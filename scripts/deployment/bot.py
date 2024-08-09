import os
import pandas as pd
import joblib
import logging
from binance.client import Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv('/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/.env')

# Configure logging
logging.basicConfig(filename='/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/logs/trading_bot.log', level=logging.INFO)

def make_decision():
    try:
        logging.info("Making trading decision...")

        api_key = os.getenv('BINANCE_API_KEY')
        api_secret = os.getenv('BINANCE_API_SECRET')

        if not api_key or not api_secret:
            raise ValueError("API Key or Secret is missing.")

        client = Client(api_key, api_secret)

        # Load data
        data_path = '/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/data/data.csv'
        data = pd.read_csv(data_path)
        X = data.drop(columns=['timestamp', 'open', 'high', 'low', 'close', 'volume']).tail(1)

        # Load scaler and transform data
        scaler_path = '/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/models/scaler.pkl'
        scaler = joblib.load(scaler_path)
        X_scaled = scaler.transform(X)

        # Load models and make predictions
        model_paths = [
            '/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/models/RandomForest_model.pkl',
            '/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/models/GradientBoosting_model.pkl',
            '/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/models/AdaBoost_model.pkl',
            '/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/models/CatBoost_model.pkl',
            '/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/models/XGBoost_model.pkl',
            '/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/models/LightGBM_model.pkl',
            '/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/models/LogisticRegression_model.pkl'
        ]

        predictions = {}
        for model_path in model_paths:
            model_name = os.path.basename(model_path).replace('_model.pkl', '')
            model = joblib.load(model_path)
            prediction = model.predict(X_scaled)[0]
            predictions[model_name] = prediction

        logging.info(f"Predictions: {predictions}")

        # Make final trading decision
        decision = round(sum(predictions.values()) / len(predictions))
        logging.info(f"Trading decision: {decision}")

        # Execute trade
        symbol = "BTCUSDT"
        if decision == 1:
            order = client.order_market_buy(
                symbol=symbol,
                quantity=0.001
            )
        else:
            order = client.order_market_sell(
                symbol=symbol,
                quantity=0.001
            )

        logging.info(f"Order executed: {order}")

    except Exception as e:
        logging.error(f"Error making decision: {e}")

if __name__ == "__main__":
    make_decision()
