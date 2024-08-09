import pandas as pd
import optuna
import lightgbm as lgb
import xgboost as xgb
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import log_loss
from sklearn.preprocessing import StandardScaler

# Load your data
data = pd.read_csv('path_to_your_data.csv')  # Update with your data path
target_column = 'your_target_column'  # Update with your target column name

# Feature Engineering
data['feature_1'] = data['column_1'] * data['column_2']  # Example feature
# Add more feature engineering steps here

X = data.drop(columns=[target_column])
y = data[target_column]

# Scaling features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

X_train, X_val, y_train, y_val = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Define objective functions for LightGBM and XGBoost
def objective_lgb(trial):
    params = {
        'objective': 'binary',
        'metric': 'binary_logloss',
        'verbosity': -1,
        'boosting_type': 'gbdt',
        'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.3),
        'num_leaves': trial.suggest_int('num_leaves', 20, 150),
        'max_depth': trial.suggest_int('max_depth', 3, 15),
        'min_data_in_leaf': trial.suggest_int('min_data_in_leaf', 10, 100),
        'colsample_bytree': trial.suggest_float('colsample_bytree', 0.5, 1.0),
        'subsample': trial.suggest_float('subsample', 0.5, 1.0),
        'reg_alpha': trial.suggest_float('reg_alpha', 0.0, 10.0),
        'reg_lambda': trial.suggest_float('reg_lambda', 0.0, 10.0),
    }
    dtrain = lgb.Dataset(X_train, label=y_train)
    cv_results = lgb.cv(params, dtrain, nfold=5, stratified=True, early_stopping_rounds=100, metrics='binary_logloss', seed=42)
    return cv_results['binary_logloss-mean'][-1]

def objective_xgb(trial):
    params = {
        'objective': 'binary:logistic',
        'eval_metric': 'logloss',
        'verbosity': 0,
        'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.3),
        'max_depth': trial.suggest_int('max_depth', 3, 15),
        'min_child_weight': trial.suggest_int('min_child_weight', 1, 10),
        'subsample': trial.suggest_float('subsample', 0.5, 1.0),
        'colsample_bytree': trial.suggest_float('colsample_bytree', 0.5, 1.0),
        'alpha': trial.suggest_float('alpha', 0.0, 10.0),
        'lambda': trial.suggest_float('lambda', 0.0, 10.0),
    }
    dtrain = xgb.DMatrix(X_train, label=y_train)
    cv_results = xgb.cv(params, dtrain, nfold=5, early_stopping_rounds=100, metrics='logloss', seed=42)
    return cv_results['test-logloss-mean'].min()

# Run the optimization for LightGBM
study_lgb = optuna.create_study(direction='minimize')
study_lgb.optimize(objective_lgb, n_trials=100)

# Run the optimization for XGBoost
study_xgb = optuna.create_study(direction='minimize')
study_xgb.optimize(objective_xgb, n_trials=100)

# Print best parameters
print("Best LightGBM Parameters: ", study_lgb.best_params)
print("Best XGBoost Parameters: ", study_xgb.best_params)

# Train and save the best LightGBM model
best_lgb = lgb.LGBMClassifier(**study_lgb.best_params)
best_lgb.fit(X_train, y_train)
best_lgb.save_model('best_lightgbm_model.txt')

# Train and save the best XGBoost model
best_xgb = xgb.XGBClassifier(**study_xgb.best_params)
best_xgb.fit(X_train, y_train)
best_xgb.save_model('best_xgboost_model.json')
