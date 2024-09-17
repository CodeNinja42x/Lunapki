import pandas as pd
import numpy as np
from binance.client import Client
from sklearn.preprocessing import MinMaxScaler
import xgboost as xgb
from tensorflow.keras.models import load_model
import logging
import os
import asyncio
import websockets
import json
import talib
import tensorflow as tf

# Initialize Binance API
API_KEY = os.getenv('BINANCE_API_KEY')
API_SECRET = os.getenv('BINANCE_API_SECRET')
client = Client(API_KEY, API_SECRET)

# Setup logging
logging.basicConfig(filename='trading_bot.log',
                    level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Global Parameters
RISK_PERCENTAGE = 0.01
ACCOUNT_BALANCE = 100000  # Example account balance
SYMBOLS = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT']  # Multi-crypto support
INTERVAL = Client.KLINE_INTERVAL_1MINUTE

# Trailing stop parameters
TRAILING_PERCENT = 0.5  # 0.5% trailing stop

# Global variable to hold models
lstm_model, scaler, xgb_model = None, None, None


### 1. Load Pre-trained Models (If available) ###

def load_models():
    """Load the LSTM and XGBoost models if they exist."""
    global lstm_model, xgb_model, scaler

    if os.path.exists('lstm_model.h5') and os.path.exists('xgb_model.json'):
        logging.info("Loading pre-trained models...")
        lstm_model = load_model('lstm_model.h5')
        xgb_model = xgb.Booster()
        xgb_model.load_model('xgb_model.json')
        logging.info("Models loaded successfully!")
    else:
        logging.error("Models not found. Please train the models before continuing.")
        return False
    return True


### 2. Data Collection and Technical Indicators ###

def fetch_historical_data(symbol, interval, start_str, end_str=None):
    """Fetch historical data from Binance."""
    logging.info(f"Fetching historical data for {symbol} from {start_str}")
    klines = client.get_historical_klines(symbol, interval, start_str, end_str)
    df = pd.DataFrame(klines, columns=[
        'Open time', 'Open', 'High', 'Low', 'Close', 'Volume',
        'Close time', 'Quote asset volume', 'Number of trades',
        'Taker buy base asset volume', 'Taker buy quote asset volume', 'Ignore'
    ])
    df['Open time'] = pd.to_datetime(df['Open time'], unit='ms')
    df.set_index('Open time', inplace=True)
    df = df.astype(float)
    return df


def add_technical_indicators(df):
    """Add technical indicators to the data frame."""
    df['EMA_20'] = df['Close'].ewm(span=20).mean()
    df['RSI'] = talib.RSI(df['Close'], timeperiod=14)
    df['MACD'], df['MACD_signal'], _ = talib.MACD(df['Close'], fastperiod=12, slowperiod=26, signalperiod=9)
    df['ATR'] = talib.ATR(df['High'], df['Low'], df['Close'], timeperiod=14)
    return df


### 3. Signal Generation and Trading Execution ###

def generate_trade_signal(lstm_model, xgb_model, scaler, recent_data):
    """Generate trade signals based on LSTM and XGBoost models."""
    # Prepare data for LSTM
    lstm_input = recent_data['Close'].values[-60:]
    lstm_input_scaled = scaler.transform(lstm_input.reshape(-1, 1))
    lstm_input_scaled = np.reshape(lstm_input_scaled, (1, lstm_input_scaled.shape[0], 1))
    lstm_prediction = lstm_model.predict(lstm_input_scaled)
    lstm_prediction = scaler.inverse_transform(lstm_prediction)

    # Prepare data for XGBoost
    features = ['Close', 'Volume', 'EMA_20', 'RSI', 'MACD', 'ATR']
    xgb_input = recent_data[features].iloc[-1]
    xgb_prediction = xgb_model.predict(np.array([xgb_input]))

    # Combine predictions
    if lstm_prediction > recent_data['Close'].iloc[-1] and xgb_prediction == 1:
        return 'buy'
    elif lstm_prediction < recent_data['Close'].iloc[-1] and xgb_prediction == 0:
        return 'sell'
    else:
        return 'hold'


async def process_live_data():
    """Process live data and execute trades based on model signals."""
    global lstm_model, scaler, xgb_model

    df = pd.DataFrame()  # Initialize an empty DataFrame for live data

    for symbol in SYMBOLS:
        uri = f"wss://stream.binance.com:9443/ws/{symbol.lower()}@kline_{INTERVAL}"
        async with websockets.connect(uri) as websocket:
            while True:
                try:
                    data = await websocket.recv()
                    data_json = json.loads(data)
                    kline = data_json['k']
                    if kline['x']:  # If kline is closed
                        new_row = {
                            'Open time': pd.to_datetime(kline['t'], unit='ms'),
                            'Open': float(kline['o']),
                            'High': float(kline['h']),
                            'Low': float(kline['l']),
                            'Close': float(kline['c']),
                            'Volume': float(kline['v']),
                        }
                        df.loc[new_row['Open time']] = new_row
                        df = add_technical_indicators(df)

                        # Generate trade signal
                        signal = generate_trade_signal(lstm_model, xgb_model, scaler, df)
                        logging.info(f"Generated signal for {symbol}: {signal}")

                        # Calculate position size and execute trade (mock execution here)
                        logging.info(f"Executing {signal} signal for {symbol}")

                except Exception as e:
                    logging.error(f"Error during WebSocket data processing: {e}")


### Main Execution ###

def main():
    """Main function to initialize models and start the trading bot."""
    global lstm_model, scaler, xgb_model

    if load_models():
        logging.info("Starting real-time data processing...")
        try:
            asyncio.get_event_loop().run_until_complete(process_live_data())
        except Exception as e:
            logging.error(f"Error in main execution: {e}")

if __name__ == "__main__":
    main()
