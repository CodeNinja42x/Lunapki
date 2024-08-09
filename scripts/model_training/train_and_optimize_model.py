import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score, train_test_split
import optuna
import joblib
import numpy as np

# Load selected features
data_path = '/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/data/selected_features.csv'
data = pd.read_csv(data_path, index_col=0)

# Load target
target_path = '/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/data/features_cleaned.csv'
target = pd.read_csv(target_path, index_col=0)['target']

# Define features and target
X = data
y = target

# Check for NaN values in target
if y.isna().sum() > 0:
    raise ValueError("Target variable contains NaN values.")

# Define objective function for hyperparameter tuning
def objective(trial):
    n_estimators = trial.suggest_int('n_estimators', 100, 1000)
    max_depth = trial.suggest_int('max_depth', 2, 20)
    min_samples_split = trial.suggest_int('min_samples_split', 2, 10)
    
    model = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth, min_samples_split=min_samples_split, random_state=42)
    scores = cross_val_score(model, X, y, cv=5, scoring='f1')
    return np.mean(scores)

# Optimize hyperparameters using Optuna
study = optuna.create_study(direction='maximize', sampler=optuna.samplers.TPESampler())
study.optimize(objective, n_trials=50)

# Train final model with best hyperparameters
best_params = study.best_params
model = RandomForestClassifier(**best_params, random_state=42)
model.fit(X, y)

# Evaluate model
accuracy = cross_val_score(model, X, y, cv=5, scoring='accuracy').mean()
precision = cross_val_score(model, X, y, cv=5, scoring='precision').mean()
recall = cross_val_score(model, X, y, cv=5, scoring='recall').mean()
f1 = cross_val_score(model, X, y, cv=5, scoring='f1').mean()

# Save model
joblib.dump(model, '/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/Bot/final_model.pkl')
print(f"Model saved successfully. Accuracy: {accuracy}, Precision: {precision}, Recall: {recall}, F1 Score: {f1}")
