import pandas as pd
import os
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)

# Directory paths
data_directory = '/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/data'
data_file_path = os.path.join(data_directory, 'new_data.csv')

# Create data directory if it doesn't exist
os.makedirs(data_directory, exist_ok=True)

# Generate sample data
data = {
    'Target': [1, 0, 1, 0, 1, 1, 0, 0, 1, 0] * 10,
    'Feature1': [10, 20, 30, 40, 50, 60, 70, 80, 90, 100] * 10,
    'Feature2': [0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4] * 10,
    'Feature3': [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000] * 10
}
df = pd.DataFrame(data)

# Save to CSV
df.to_csv(data_file_path, index=False)
logging.info(f"Sample data file created at {data_file_path}")
