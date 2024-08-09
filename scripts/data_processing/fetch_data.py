import pandas as pd
from binance.client import Client
import logging
from datetime import datetime
import ta

# Initialize logging
logging.basicConfig(level=logging.INFO, filename='fetch_data.log', filemode='a', 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def fetch_data():
    api_key = 'binaVuWGlq8yFXYi9Uv68PYOCefAmOD9XzVWMYyafKnK9lhObrBVH3bcMPqv334aoamV'
    api_secret = 'jFcly53Oz9OmjRBkZ7o9sqWtyIYHtQdgmL7vmHd9WBAeg5fTI68qjBBLAq4VLlmM'

    client = Client(api_key, api_secret)

    symbol = "ETHUSDT"
    interval = Client.KLINE_INTERVAL_1HOUR

    # Fetch historical data
    klines = client.get_historical_klines(symbol, interval, "1 Jan, 2020", "now")
    data = pd.DataFrame(klines, columns=['Open time', 'Open', 'High', 'Low', 'Close', 'Volume', 
                                         'Close time', 'Quote asset volume', 'Number of trades', 
                                         'Taker buy base asset volume', 'Taker buy quote asset volume', 'Ignore'])

    data['Open time'] = pd.to_datetime(data['Open time'], unit='ms')
    data.set_index('Open time', inplace=True)
    data = data.astype(float)

    # Save data
    data.to_csv('/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/latest_data.csv')
    logging.info("Data fetched successfully")

def create_features():
    data = pd.read_csv('/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/latest_data.csv')

    # Ensure 'Close' column is in numeric format
    data['Close'] = pd.to_numeric(data['Close'], errors='coerce')
    data['High'] = pd.to_numeric(data['High'], errors='coerce')
    data['Low'] = pd.to_numeric(data['Low'], errors='coerce')
    data['Open'] = pd.to_numeric(data['Open'], errors='coerce')

    # Create features
    data['RSI'] = ta.momentum.RSIIndicator(data['Close']).rsi()
    data['MA20'] = data['Close'].rolling(window=20).mean()
    data['MA50'] = data['Close'].rolling(window=50).mean()
    
    bb_indicator = ta.volatility.BollingerBands(close=data['Close'], window=20, window_dev=2)
    data['BB_high'] = bb_indicator.bollinger_hband()
    data['BB_low'] = bb_indicator.bollinger_lband()
    data['BB_width'] = data['BB_high'] - data['BB_low']
    
    macd_indicator = ta.trend.MACD(close=data['Close'])
    data['MACD'] = macd_indicator.macd()
    data['MACD_signal'] = macd_indicator.macd_signal()
    data['MACD_diff'] = macd_indicator.macd_diff()
    
    data['ATR'] = ta.volatility.AverageTrueRange(high=data['High'], low=data['Low'], close=data['Close'], window=14).average_true_range()
    
    # Forward fill for any missing data
    data.fillna(method='ffill', inplace=True)
    data.dropna(inplace=True)

    # Save processed data
    data.to_csv('/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/processed_data_with_features.csv', index=False)
    logging.info("Feature engineering completed and saved.")

if __name__ == "__main__":
    fetch_data()
    create_features()
