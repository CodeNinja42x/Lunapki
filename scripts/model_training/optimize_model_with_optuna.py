import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import optuna

# Load data
data_path = '/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/data/btc_data_with_indicators.csv'

# Check if the file exists
if not os.path.exists(data_path):
    raise FileNotFoundError(f"File not found: {data_path}")

df = pd.read_csv(data_path)

# Prepare the data for modeling
X = df[['SMA_20', 'SMA_50', 'RSI', 'Bollinger_Upper', 'Bollinger_Lower']].dropna()

# Create the target variable 'y' ensuring it matches the length of 'X'
y = np.where(df['Close'].shift(-1) > df['Close'], 1, 0)

# Align lengths of X and y by removing the last row in y
X = X.iloc[:-1]  # Remove the last row from X to match y's length
y = y[:len(X)]  # Ensure y is the same length as X

# Check for consistent lengths
assert len(X) == len(y), "Lengths of X and y must match."

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

def objective(trial):
    params = {
        'n_estimators': trial.suggest_int('n_estimators', 10, 200),
        'max_depth': trial.suggest_int('max_depth', 3, 10),
        'min_samples_split': trial.suggest_int('min_samples_split', 2, 10),
        'min_samples_leaf': trial.suggest_int('min_samples_leaf', 1, 4),
    }
    model = RandomForestClassifier(**params)
    model.fit(X_train, y_train)
    return model.score(X_test, y_test)

study = optuna.create_study(direction='maximize')
study.optimize(objective, n_trials=100)

print(f"Best parameters: {study.best_params}")
