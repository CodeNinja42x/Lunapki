import pandas as pd
import os
import pickle
from sklearn.impute import SimpleImputer
from datetime import datetime

# Set the data directory
data_dir = '/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/data'
log_dir = '/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/logs'

# Load the real-time data
real_time_data_path = os.path.join(data_dir, 'real_time_data.csv')
data = pd.read_csv(real_time_data_path)

# Perform feature engineering (example steps, adjust as needed)
data['MA_5'] = data['Close'].rolling(window=5).mean()
data['MA_10'] = data['Close'].rolling(window=10).mean()
data['STD_5'] = data['Close'].rolling(window=5).std()
data['Return'] = data['Close'].pct_change()

# Fill missing values using forward fill method
data.ffill(inplace=True)

# Ensure 'Target' column is present (for demonstration purposes, creating a dummy target)
if 'Target' not in data.columns:
    data['Target'] = (data['Close'].shift(-1) > data['Close']).astype(int)

# Drop any rows with NaN values
data.dropna(inplace=True)

# Drop columns that cannot be used as features
columns_to_drop = ['Date', 'timestamp']
data.drop(columns=[col for col in columns_to_drop if col in data.columns], inplace=True)

# Handle remaining NaN values using SimpleImputer
imputer = SimpleImputer(strategy='mean')
data_imputed = imputer.fit_transform(data)

# Create a DataFrame with the imputed data and correct column names
data = pd.DataFrame(data_imputed, columns=data.columns)

# Save the processed data
processed_data_path = os.path.join(data_dir, 'processed_data_with_features.csv')
data.to_csv(processed_data_path, index=False)

# Save feature names
feature_names_path = os.path.join(data_dir, 'feature_names.pkl')
feature_names = data.columns.tolist()
if 'Target' in feature_names:
    feature_names.remove('Target')  # Ensure Target is not included in features

with open(feature_names_path, 'wb') as f:
    pickle.dump(feature_names, f)

print(f"Feature engineering completed and saved to {processed_data_path}")

with open(os.path.join(log_dir, 'feature_engineering_improve.log'), 'a') as log_file:
    log_file.write(f"{datetime.now()} - Feature engineering completed and saved to {processed_data_path} - INFO\n")
    log_file.write(f"{datetime.now()} - Feature names saved to {feature_names_path} - INFO\n")
