import os
import pandas as pd
import numpy as np  # Import numpy
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib

# Load the data
data_path = '/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/data/btc_data_with_indicators.csv'
df = pd.read_csv(data_path)

# Prepare the data for modeling
X = df[['SMA_20', 'SMA_50', 'RSI', 'Bollinger_Upper', 'Bollinger_Lower']].dropna()
y = np.where(df['Close'].shift(-1) > df['Close'], 1, 0)

# Align lengths of X and y by removing the last row in y
X = X.iloc[:-1]  # Remove the last row from X to match y's length
y = y[:len(X)]  # Ensure y is the same length as X

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Using the best parameters found by Optuna
best_params = {'n_estimators': 92, 'max_depth': 3, 'min_samples_split': 7, 'min_samples_leaf': 2}

# Train the model
model = RandomForestClassifier(**best_params)
model.fit(X_train, y_train)

# Ensure the directory exists for saving the model
model_save_dir = '/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/models'
os.makedirs(model_save_dir, exist_ok=True)

# Save the trained model
model_save_path = os.path.join(model_save_dir, 'optimized_rf_model.pkl')
joblib.dump(model, model_save_path)
print(f"Model saved to {model_save_path}")
