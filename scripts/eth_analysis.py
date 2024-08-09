import pandas as pd
import matplotlib.pyplot as plt

# Load the data
data = pd.read_csv('/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/Bot_Logs/fetches/fetched_data.csv')

# Print column names and a sample of the data
print("Column names:", data.columns)
print(data.head())

# Convert timestamp to datetime for better plotting
# Adjust the column name here based on the actual column name in your data
data['timestamp'] = pd.to_datetime(data['timestamp'], unit='ms')

# Step 1: Price Trend Over Time
plt.figure(figsize=(14, 7))
plt.plot(data['timestamp'], data['close'], label='Closing Price')
plt.title('ETH Closing Prices Over Time')
plt.xlabel('Date')
plt.ylabel('Price (USD)')
plt.legend()
plt.grid(True)
plt.show()

# Step 2: Moving Averages
data['7_day_MA'] = data['close'].rolling(window=7).mean()
data['30_day_MA'] = data['close'].rolling(window=30).mean()

plt.figure(figsize=(14, 7))
plt.plot(data['timestamp'], data['close'], label='Closing Price', alpha=0.5)
plt.plot(data['timestamp'], data['7_day_MA'], label='7-Day Moving Average')
plt.plot(data['timestamp'], data['30_day_MA'], label='30-Day Moving Average')
plt.title('ETH Closing Prices with Moving Averages')
plt.xlabel('Date')
plt.ylabel('Price (USD)')
plt.legend()
plt.grid(True)
plt.show()

# Step 3: Volatility Analysis
data['daily_return'] = data['close'].pct_change()
data['volatility'] = data['daily_return'].rolling(window=30).std()

plt.figure(figsize=(14, 7))
plt.plot(data['timestamp'], data['volatility'], label='30-Day Rolling Volatility')
plt.title('ETH Price Volatility Over Time')
plt.xlabel('Date')
plt.ylabel('Volatility')
plt.legend()
plt.grid(True)
plt.show()

# Step 4: Volume Analysis
plt.figure(figsize=(14, 7))
plt.bar(data['timestamp'], data['volume'], label='Trading Volume', color='orange', alpha=0.6)
plt.title('ETH Trading Volume Over Time')
plt.xlabel('Date')
plt.ylabel('Volume')
plt.legend()
plt.grid(True)
plt.show()
