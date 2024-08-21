from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
import numpy as np
import pandas as pd

# Load data
df = pd.read_csv('/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/data/btc_data_with_indicators.csv')
X = df[['SMA_20', 'SMA_50', 'RSI', 'Bollinger_Upper', 'Bollinger_Lower']]
y = df['Target']

# Model with best parameters found from Optuna
best_params = {'n_estimators': 100, 'max_depth': 5, 'min_samples_split': 2, 'min_samples_leaf': 1}  # Replace with your best_params
model = RandomForestClassifier(**best_params)

scores = cross_val_score(model, X, y, cv=5)
print(f"Cross-validation scores: {scores}")
print(f"Mean CV score: {np.mean(scores)}")
