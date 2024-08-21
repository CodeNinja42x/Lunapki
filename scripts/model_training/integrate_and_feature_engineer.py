import os
import yfinance as yf
import pandas as pd

# Step 1: Integrate Real Data
# Fetch Bitcoin data
btc = yf.Ticker("BTC-USD")
hist = btc.history(period="max")

# Ensure the directory exists
save_dir = '/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/data'
os.makedirs(save_dir, exist_ok=True)

# Save the fetched data to CSV
btc_data_path = os.path.join(save_dir, 'btc_data.csv')
hist.to_csv(btc_data_path)

# Step 2: Enhance Feature Engineering
def add_technical_indicators(df):
    df['SMA_20'] = df['Close'].rolling(window=20).mean()
    df['SMA_50'] = df['Close'].rolling(window=50).mean()
    df['RSI'] = calculate_rsi(df['Close'], 14)
    df['Bollinger_Upper'] = df['Close'].rolling(window=20).mean() + (df['Close'].rolling(window=20).std() * 2)
    df['Bollinger_Lower'] = df['Close'].rolling(window=20).mean() - (df['Close'].rolling(window=20).std() * 2)
    return df

def calculate_rsi(data, window):
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

# Load the data and apply the indicators
df = pd.read_csv(btc_data_path)
df = add_technical_indicators(df)

# Save the enhanced data
enhanced_data_path = os.path.join(save_dir, 'btc_data_with_indicators.csv')
df.to_csv(enhanced_data_path, index=False)
