import pandas as pd
import joblib
import numpy as np
from binance.client import Client
from time import sleep

# Load the model
model = joblib.load('/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/Bot/LightGBM_model.pkl')

# Initialize the Binance client
api_key = 'your_api_key'
api_secret = 'your_api_secret'
client = Client(api_key, api_secret)

# Function to fetch real-time data
def fetch_realtime_data(symbol, interval):
    klines = client.get_klines(symbol=symbol, interval=interval, limit=1)
    data = pd.DataFrame(klines, columns=['Open time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close time', 'Quote asset volume', 'Number of trades', 'Taker buy base asset volume', 'Taker buy quote asset volume', 'Ignore'])
    data['Open time'] = pd.to_datetime(data['Open time'], unit='ms')
    data.set_index('Open time', inplace=True)
    data = data[['Open', 'High', 'Low', 'Close', 'Volume']]
    data = data.astype(float)
    return data

# Function to preprocess data for prediction
def preprocess_data(data):
    data['MA_7'] = data['Close'].rolling(window=7).mean()
    data['MA_14'] = data['Close'].rolling(window=14).mean()
    data['MA_30'] = data['Close'].rolling(window=30).mean()
    data['Price_Change_1d'] = data['Close'].pct_change(1)
    data['Price_Change_7d'] = data['Close'].pct_change(7)
    data = data.dropna()
    features = ['Close', 'Volume', 'MA_7', 'MA_14', 'MA_30', 'Price_Change_1d', 'Price_Change_7d']
    return data[features].iloc[-1].values.reshape(1, -1)

# Function to place orders
def place_order(symbol, quantity, side):
    try:
        order = client.create_order(
            symbol=symbol,
            side=side,
            type='MARKET',
            quantity=quantity)
        print(f"Order placed: {order}")
    except Exception as e:
        print(f"Error placing order: {e}")

# Real-time trading logic
symbol = 'ETHUSDT'
quantity = 0.01  # Define your trading quantity
interval = Client.KLINE_INTERVAL_1MINUTE

while True:
    data = fetch_realtime_data(symbol, interval)
    if not data.empty:
        features = preprocess_data(data)
        prediction = model.predict(features)
        if prediction[0] == 1:
            place_order(symbol, quantity, 'BUY')
        else:
            place_order(symbol, quantity, 'SELL')
    sleep(60)  # Wait for 1 minute before fetching new data
