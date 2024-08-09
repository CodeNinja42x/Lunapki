import pandas as pd
import numpy as np
import ta
import os
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO, filename='/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/real_time_data.log', filemode='a', 
                    format='%(asctime)s - %(levelname)s - %(message)s')

logging.info("Started real-time data script")

# Define paths
data_dir = '/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/data'
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

# Function to get real-time data (dummy example here, replace with actual data fetching logic)
def get_real_time_data():
    # Dummy data generation
    date_range = pd.date_range(start='1/1/2020', periods=100, freq='h')
    data = pd.DataFrame({
        'Date': date_range,
        'Open': np.random.rand(100),
        'High': np.random.rand(100),
        'Low': np.random.rand(100),
        'Close': np.random.rand(100),
        'Volume': np.random.rand(100)
    })
    data[['Open', 'High', 'Low', 'Close', 'Volume']] = data[['Open', 'High', 'Low', 'Close', 'Volume']].astype(float)
    return data

data = get_real_time_data()
data.to_csv(os.path.join(data_dir, 'real_time_data.csv'), index=False)
logging.info("Saved real-time data")

# Splitting data into training and test sets
train_size = int(len(data) * 0.8)
train_data = data[:train_size]
test_data = data[train_size:]

# Save the datasets
train_data.to_csv(os.path.join(data_dir, 'X_train.csv'), index=False)
test_data.to_csv(os.path.join(data_dir, 'X_test.csv'), index=False)

logging.info("Saved training and test datasets")
print("Real-time data script completed and datasets saved.")
