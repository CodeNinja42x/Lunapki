import pandas as pd
import numpy as np
from binance.client import Client
from sklearn.preprocessing import MinMaxScaler
import xgboost as xgb
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
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


### 1. Data Collection Module ###

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
    logging.info(f"Historical data for {symbol} fetched and processed")
    return df


### 2. Technical Indicators and Feature Engineering Module ###

def add_technical_indicators(df):
    """Add technical indicators to the data frame."""
    logging.info("Adding technical indicators")
    df['EMA_20'] = df['Close'].ewm(span=20).mean()
    df['RSI'] = talib.RSI(df['Close'], timeperiod=14)
    df['MACD'], df['MACD_signal'], _ = talib.MACD(df['Close'], fastperiod=12, slowperiod=26, signalperiod=9)
    df['ATR'] = talib.ATR(df['High'], df['Low'], df['Close'], timeperiod=14)
    logging.info("Technical indicators added")
    return df


### 3. LSTM Model for Trend Prediction ###

def train_lstm_model(df):
    """Train an LSTM model for trend prediction."""
    logging.info("Training LSTM model")
    data = df[['Close']].values
    scaler = MinMaxScaler()
    scaled_data = scaler.fit_transform(data)

    X, y = [], []
    look_back = 60
    for i in range(look_back, len(scaled_data)):
        X.append(scaled_data[i - look_back:i, 0])
        y.append(scaled_data[i, 0])
    X, y = np.array(X), np.array(y)
    X = np.reshape(X, (X.shape[0], X.shape[1], 1))

    model = Sequential()
    model.add(LSTM(50, return_sequences=True, input_shape=(X.shape[1], 1)))
    model.add(LSTM(50))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mean_squared_error')

    # Log progress per epoch
    model.fit(X, y, epochs=5, batch_size=32, callbacks=[
        tf.keras.callbacks.LambdaCallback(
            on_epoch_end=lambda epoch, logs: logging.info(f"Epoch {epoch+1} - loss: {logs['loss']}")
        )
    ])
    
    # Save model
    model.save('lstm_model.h5')
    logging.info("LSTM model training complete and saved")
    return model, scaler


### 4. XGBoost Model for Signal Classification ###

def train_xgboost_model(df):
    """Train an XGBoost classifier for trade signals."""
    logging.info("Training XGBoost model")
    df = df.dropna()
    features = ['Close', 'Volume', 'EMA_20', 'RSI', 'MACD', 'ATR']
    X = df[features]
    y = np.where(df['Close'].shift(-1) > df['Close'], 1, 0)  # 1 for up, 0 for down

    model = xgb.XGBClassifier(n_estimators=100, max_depth=5, learning_rate=0.1)
    model.fit(X[:-1], y[:-1])
    
    # Save the XGBoost model
    model.save_model('xgb_model.json')
    logging.info("XGBoost model training complete and saved")
    return model


### 5. Risk Management Module with Trailing Stop ###

def calculate_position_size(account_balance, risk_percentage, stop_loss_price, entry_price):
    """Calculate position size based on risk management strategy."""
    risk_amount = account_balance * risk_percentage
    stop_loss_distance = abs(entry_price - stop_loss_price)
    position_size = risk_amount / stop_loss_distance
    logging.info(f"Calculated position size: {position_size}")
    return position_size

def calculate_trailing_stop(entry_price, trailing_percent):
    """Calculate trailing stop based on current price and trailing percentage."""
    return entry_price * (1 - trailing_percent / 100)


### 6. Signal Generation and Trading Execution Module ###

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
    logging.info(f"LSTM prediction: {lstm_prediction}, XGBoost prediction: {xgb_prediction}")
    if lstm_prediction > recent_data['Close'].iloc[-1] and xgb_prediction == 1:
        return 'buy'
    elif lstm_prediction < recent_data['Close'].iloc[-1] and xgb_prediction == 0:
        return 'sell'
    else:
        return 'hold'

def execute_trade_with_trailing_stop(signal, symbol, quantity, entry_price, trailing_percent=0.5):
    """Execute trades with trailing stop-loss."""
    if signal == 'buy':
        order = client.order_market_buy(symbol=symbol, quantity=quantity)
        logging.info(f"Executed BUY order for {quantity} units of {symbol}")

        # Set trailing stop-loss
        trailing_stop_price = calculate_trailing_stop(entry_price, trailing_percent)
        logging.info(f"Trailing Stop set at: {trailing_stop_price}")

    elif signal == 'sell':
        order = client.order_market_sell(symbol=symbol, quantity=quantity)
        logging.info(f"Executed SELL order for {quantity} units of {symbol}")
    else:
        logging.info("No trade executed. Signal was HOLD.")


### 7. Real-Time Data Processing with WebSockets ###

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

                        # Calculate position size and execute trade
                        entry_price = new_row['Close']
                        stop_loss_price = entry_price * 0.995  # Example stop loss at 0.5% below entry
                        quantity = calculate_position_size(ACCOUNT_BALANCE, RISK_PERCENTAGE, stop_loss_price, entry_price) / entry_price

                        execute_trade_with_trailing_stop(signal, symbol, quantity, entry_price)

                except Exception as e:
                    logging.error(f"Error during WebSocket data processing: {e}")


### 8. Main Execution Loop ###

def main():
    """Main function to initialize models and start the trading bot."""
    global lstm_model, scaler, xgb_model

    try:
        # Check if models already exist
        if os.path.exists('lstm_model.h5') and os.path.exists('xgb_model.json'):
            logging.info("Loading pre-trained models...")
            lstm_model = tf.keras.models.load_model('lstm_model.h5')
            xgb_model = xgb.Booster()
            xgb_model.load_model('xgb_model.json')
        else:
            # Fetch and process historical data for training
            df = fetch_historical_data(SYMBOLS[0], INTERVAL, '1 Jan, 2021')
            df = add_technical_indicators(df)

            # Train models
            lstm_model, scaler = train_lstm_model(df)
            xgb_model = train_xgboost_model(df)

        # Start real-time data processing
        asyncio.get_event_loop().run_until_complete(process_live_data())

    except Exception as e:
        logging.error(f"Error in main execution: {e}")


if __name__ == "__main__":
    main()
