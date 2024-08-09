# /Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/scripts/optuna_hyperparameter_tuning.py

import optuna
import lightgbm as lgb
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
import joblib

def load_data(filepath):
    return pd.read_csv(filepath)

def extract_features(data):
    features = {
        'feature1': data['some_column'] * 2,
        'feature2': data['another_column'] + 1,
        # Add other features here
    }
    return pd.DataFrame(features)

def objective(trial):
    param = {
        'objective': 'binary',
        'metric': 'accuracy',
        'verbosity': -1,
        'boosting_type': 'gbdt',
        'learning_rate': trial.suggest_loguniform('learning_rate', 1e-4, 1e-1),
        'num_leaves': trial.suggest_int('num_leaves', 10, 200),
        'max_depth': trial.suggest_int('max_depth', 3, 20),
        'min_data_in_leaf': trial.suggest_int('min_data_in_leaf', 10, 100),
        'colsample_bytree': trial.suggest_uniform('colsample_bytree', 0.5, 1.0),
        'subsample': trial.suggest_uniform('subsample', 0.5, 1.0),
        'reg_alpha': trial.suggest_loguniform('reg_alpha', 1e-3, 10.0),
        'reg_lambda': trial.suggest_loguniform('reg_lambda', 1e-3, 10.0)
    }
    
    data = load_data('/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/data/preprocessed_data.csv')
    X = extract_features(data)
    y = data['target_column']
    
    X_train, X_valid, y_train, y_valid = train_test_split(X, y, test_size=0.2, random_state=42)
    
    dtrain = lgb.Dataset(X_train, label=y_train)
    dvalid = lgb.Dataset(X_valid, label=y_valid, reference=dtrain)
    model = lgb.train(param, dtrain, valid_sets=[dvalid], early_stopping_rounds=100)
    
    scores = cross_val_score(model, X, y, cv=5, scoring='accuracy')
    trial.set_user_attr('model', model)
    return scores.mean()

if __name__ == "__main__":
    study = optuna.create_study(direction='maximize')
    study.optimize(objective, n_trials=100)
    
    print("Best hyperparameters: ", study.best_params)
    
    best_model = study.best_trial.user_attrs['model']
    model_path = '/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/models/optuna_best_model.pkl'
    joblib.dump(best_model, model_path)
    print(f"Best model saved to {model_path}")
