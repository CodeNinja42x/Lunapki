# Re-running the code since the previous execution state was reset.

import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib
import optuna

# Step 1: Integrate with Real Data
# Fetch Bitcoin data
btc = yf.Ticker("BTC-USD")
hist = btc.history(period="max")
hist.to_csv('/mnt/data/btc_data.csv')  # Save the fetched data to CSV

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
df = pd.read_csv('/mnt/data/btc_data.csv')
df = add_technical_indicators(df)
df.to_csv('/mnt/data/btc_data_with_indicators.csv', index=False)  # Save the enhanced data

# Step 3: Optimize the Model using Optuna
# Prepare the data for modeling
X = df[['SMA_20', 'SMA_50', 'RSI', 'Bollinger_Upper', 'Bollinger_Lower']].dropna()
y = np.where(df['Close'].shift(-1) > df['Close'], 1, 0)[:-1]

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

best_params = study.best_params
best_params
