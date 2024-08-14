import optuna
import pandas as pd
import xgboost as xgb
from sklearn.model_selection import cross_val_score

# Load the refined data
data = pd.read_csv('/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/data/refined_data.csv')

# Define target and features
target_column = 'close'
X = data.drop(columns=[target_column, 'date'])
y = data[target_column]

# Define objective function for Optuna
def objective(trial):
    param = {
        'tree_method': 'hist',  # Using 'hist' for CPU-based training
        'lambda': trial.suggest_float('lambda', 1e-8, 1.0, log=True),
        'alpha': trial.suggest_float('alpha', 1e-8, 1.0, log=True),
        'colsample_bytree': trial.suggest_float('colsample_bytree', 0.2, 1.0),
        'subsample': trial.suggest_float('subsample', 0.2, 1.0),
        'learning_rate': trial.suggest_float('learning_rate', 1e-8, 0.1),
        'n_estimators': trial.suggest_int('n_estimators', 100, 1000),
        'max_depth': trial.suggest_int('max_depth', 1, 9),
        'random_state': trial.suggest_int('random_state', 42, 42),
        'min_child_weight': trial.suggest_int('min_child_weight', 1, 300),
    }
    
    model = xgb.XGBRegressor(**param)
    
    # Cross-validation
    scores = cross_val_score(model, X, y, cv=5, scoring='neg_mean_squared_error')
    rmse = (-scores.mean()) ** 0.5
    return rmse

# Create a study and optimize
study = optuna.create_study(direction='minimize')
study.optimize(objective, n_trials=100)

# Output the best parameters and retrain the model
print("Best trial:")
trial = study.best_trial
print(f"  Value: {trial.value}")
print("  Params: ")
for key, value in trial.params.items():
    print(f"    {key}: {value}")

best_params = study.best_params
model = xgb.XGBRegressor(**best_params)
model.fit(X, y)

model_save_path = '/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/models/optimized_xgb_model_refined.pkl'
model.save_model(model_save_path)

print(f"Optimized model saved to {model_save_path}")
