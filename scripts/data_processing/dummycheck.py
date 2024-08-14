import os
import pandas as pd

data_directory = '/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/data/'

# Files to check
required_files = ['X_train.csv', 'X_test.csv', 'y_train.csv', 'y_test.csv']

# Dummy data for missing files
dummy_data = {
    'X_train.csv': pd.DataFrame({
        'feature1': [1, 2, 3],
        'feature2': [4, 5, 6],
        'target': [0, 1, 0]
    }),
    'X_test.csv': pd.DataFrame({
        'feature1': [2, 3, 4],
        'feature2': [5, 6, 7]
    }),
    'y_train.csv': pd.DataFrame({
        'target': [0, 1, 0]
    }),
    'y_test.csv': pd.DataFrame({
        'target': [1, 0, 1]
    })
}

# Check and create missing files
for file_name in required_files:
    file_path = os.path.join(data_directory, file_name)
    if not os.path.exists(file_path):
        dummy_data[file_name].to_csv(file_path, index=False)
        print(f"Created missing file: {file_path}")
