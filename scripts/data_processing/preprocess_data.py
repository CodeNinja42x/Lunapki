import pandas as pd
import logging
import os

# Set up logging
logging.basicConfig(filename='/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/Bot_Logs/logs/data_preprocessing.log', level=logging.DEBUG, format='%(asctime)s %(message)s')

# Load data
try:
    data_path = '/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/Bot_Logs/fetches/fetched_data.csv'
    data = pd.read_csv(data_path)
    logging.info(f"Loaded data from {data_path}")
except Exception as e:
    logging.error(f"Error loading data: {e}")
    data = pd.DataFrame()

# Convert 'Open time' to datetime
try:
    data['Open time'] = pd.to_datetime(data['Open time'], format='%Y-%m-%d %H:%M:%S')
    logging.info("Converted 'Open time' to datetime")
except Exception as e:
    logging.error(f"Error converting 'Open time' to datetime: {e}")

# Convert other columns to numeric
try:
    cols_to_convert = ['Open', 'High', 'Low', 'Close', 'Volume']
    data[cols_to_convert] = data[cols_to_convert].apply(pd.to_numeric, errors='coerce')
    logging.info("Converted columns to numeric")
except Exception as e:
    logging.error(f"Error converting columns to numeric: {e}")

# Feature engineering
try:
    data['Price_Change'] = (data['Close'] - data['Open']) / data['Open']
    data['Volatility'] = (data['High'] - data['Low']) / data['Open']
    data['SMA_5'] = data['Close'].rolling(window=5).mean()
    data['SMA_10'] = data['Close'].rolling(window=10).mean()
    data['EMA_5'] = data['Close'].ewm(span=5).mean()
    data['EMA_10'] = data['Close'].ewm(span=10).mean()

    def compute_rsi(data, window=14):
        delta = data.diff(1)
        gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi

    data['RSI_14'] = compute_rsi(data['Close'])

    data['EMA_12'] = data['Close'].ewm(span=12).mean()
    data['EMA_26'] = data['Close'].ewm(span=26).mean()
    data['MACD'] = data['EMA_12'] - data['EMA_26']

    data['BB_upper'] = data['SMA_10'] + (data['Close'].rolling(window=10).std() * 2)
    data['BB_lower'] = data['SMA_10'] - (data['Close'].rolling(window=10).std() * 2)

    data.dropna(inplace=True)
    logging.info("Feature engineering completed successfully")

    # Add target column for training (assuming binary classification)
    data['Target'] = (data['Close'].shift(-1) > data['Close']).astype(int)

    preprocessed_data_path = '/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/Bot_Logs/fetches/preprocessed_data.csv'
    data.to_csv(preprocessed_data_path, index=False)
    logging.info(f"Preprocessed data saved to {preprocessed_data_path}")
except Exception as e:
    logging.error(f"Error in feature engineering: {e}")
