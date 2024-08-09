import pandas as pd
import numpy as np
import pickle
import logging
from binance.client import Client
import lightgbm as lgb
import xgboost as xgb
import ta
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Initialize logging
logging.basicConfig(level=logging.INFO, filename='real_time_trading.log', filemode='a', 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Load models
lgb_model = lgb.Booster(model_file='/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/models/best_lightgbm_model.txt')
xgb_model = xgb.XGBRegressor()
xgb_model.load_model('/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/models/best_xgboost_model.json')

# Load scaler
with open('/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/models/scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)

# Load feature names
with open('/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/models/feature_names.pkl', 'rb') as f:
    expected_features = pickle.load(f)

# Fetch data from Binance
def fetch_latest_data(symbol):
    api_key = os.getenv('BINANCE_API_KEY')
    api_secret = os.getenv('BINANCE_API_SECRET')
    client = Client(api_key, api_secret)
    interval = Client.KLINE_INTERVAL_1HOUR
    klines = client.get_historical_klines(symbol, interval, "1 Jan, 2020", "1 Jun, 2024")
    data = pd.DataFrame(klines, columns=['Open time', 'Open', 'High', 'Low', 'Close', 'Volume', 
                                         'Close time', 'Quote asset volume', 'Number of trades', 
                                         'Taker buy base asset volume', 'Taker buy quote asset volume', 'Ignore'])
    data['Open time'] = pd.to_datetime(data['Open time'], unit='ms')
    data.set_index('Open time', inplace=True)
    return data

def create_features(data):
    # Ensure numerical columns are correctly typed
    cols = ['Open', 'High', 'Low', 'Close', 'Volume', 'Quote asset volume', 
            'Number of trades', 'Taker buy base asset volume', 'Taker buy quote asset volume']
    data[cols] = data[cols].apply(pd.to_numeric, errors='coerce')

    data['RSI'] = ta.momentum.RSIIndicator(data['Close']).rsi()
    data['MA20'] = data['Close'].rolling(window=20).mean()
    data['MA50'] = data['Close'].rolling(window=50).mean()
    data['lag_1'] = data['Close'].shift(1)
    data['lag_5'] = data['Close'].shift(5)
    data['lag_10'] = data['Close'].shift(10)
    data['ma_10'] = data['Close'].rolling(window=10).mean()
    data['rolling_std_10'] = data['Close'].rolling(window=10).std()
    data['rolling_std_20'] = data['Close'].rolling(window=20).std()
    data['bollinger_high'] = data['MA20'] + (data['rolling_std_20'] * 2)
    data['bollinger_low'] = data['MA20'] - (data['rolling_std_20'] * 2)
    data['ma_12'] = data['Close'].ewm(span=12, adjust=False).mean()
    data['ma_26'] = data['Close'].ewm(span=26, adjust=False).mean()
    data['macd'] = data['ma_12'] - data['ma_26']
    data['signal'] = data['macd'].ewm(span=9, adjust=False).mean()
    
    data.fillna(method='ffill', inplace=True)
    return data

def main():
    while True:
        try:
            symbols = ["ETHUSDT", "BTCUSDT", "XRPUSDT", "DOGEUSDT"]
            for symbol in symbols:
                data = fetch_latest_data(symbol)
                data = create_features(data)
                
                # Ensure that all expected columns are present
                for col in expected_features:
                    if col not in data.columns:
                        data[col] = 0  # Fill missing columns with default value (e.g., 0)

                features = data[expected_features].values
                features_scaled = scaler.transform(features)
                
                # Predict using both models
                lgb_pred = lgb_model.predict(features_scaled[-1].reshape(1, -1))
                xgb_pred = xgb_model.predict(features_scaled[-1].reshape(1, -1))
                
                logging.info(f"{symbol} - LGB Prediction: {lgb_pred}, XGB Prediction: {xgb_pred}")
                print(f"{symbol} - LGB Prediction: {lgb_pred}, XGB Prediction: {xgb_pred}")
            
        except Exception as e:
            logging.error(f"Error in trading loop: {e}")

if __name__ == "__main__":
    main()
