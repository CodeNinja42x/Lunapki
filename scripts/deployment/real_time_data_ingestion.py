import pandas as pd
import time
import os
from datetime import datetime

data_dir = '/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/data'
log_dir = '/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/logs'

# Simulate real-time data ingestion
def get_real_time_data():
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    data = {
        'Date': [current_time],
        'Open': [71030.12],
        'High': [71034.04],
        'Low': [71030.12],
        'Close': [71034.03],
        'Volume': [3.95581]
    }
    return pd.DataFrame(data)

real_time_data_path = os.path.join(data_dir, 'real_time_data.csv')
real_time_data = get_real_time_data()

if os.path.exists(real_time_data_path):
    real_time_data.to_csv(real_time_data_path, mode='a', header=False, index=False)
else:
    real_time_data.to_csv(real_time_data_path, mode='w', header=True, index=False)

print(f"Real-time data saved to {real_time_data_path}")

with open(os.path.join(log_dir, 'real_time_data_ingestion.log'), 'a') as log_file:
    log_file.write(f"{datetime.now()} - Real-time data saved to {real_time_data_path} - INFO\n")
