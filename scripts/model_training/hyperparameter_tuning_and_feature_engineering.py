import pandas as pd
import optuna
import lightgbm as lgb
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import pickle
import shap
import matplotlib.pyplot as plt
import ta

# Load your data
data = pd.read_csv('/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/processed_data.csv')
target_column = 'Close'

# Feature Engineering
def create_features(data):
    # Ensure numerical columns are correctly typed
    cols = ['Open', 'High', 'Low', 'Close', 'Volume', 'Quote asset volume', 
            'Number of trades', 'Taker buy base asset volume', 'Taker buy quote asset volume']
    data[cols] = data[cols].apply(pd.to_numeric, errors='coerce')
    
    data['RSI'] = ta.momentum.RSIIndicator(data['Close']).rsi()
    data['MA20'] = data['Close'].rolling(window=20).mean()
    data['MA50'] = data['Close'].rolling(window=50).mean()
    data['lag_1'] = data['Close'].shift(1)
    data['lag_5'] = data['Close'].shift(5)
    data['lag_10'] = data['Close'].shift(10)
    data['ma_10'] = data['Close'].rolling(window=10).mean()
    data['rolling_std_10'] = data['Close'].rolling(window=10).std()
    data['rolling_std_20'] = data['Close'].rolling(window=20).std()
    data['bollinger_high'] = data['MA20'] + (data['rolling_std_20'] * 2)
    data['bollinger_low'] = data['MA20'] - (data['rolling_std_20'] * 2)
    data['ma_12'] = data['Close'].ewm(span=12, adjust=False).mean()
    data['ma_26'] = data['Close'].ewm(span=26, adjust=False).mean()
    data['macd'] = data['ma_12'] - data['ma_26']
    data['signal'] = data['macd'].ewm(span=9, adjust=False).mean()
    
    data.fillna(method='ffill', inplace=True)
    return data

data = create_features(data)

# Prepare data for modeling
X = data.drop(columns=[target_column, 'Open time', 'Close time'])  # Adjust as necessary
y = data[target_column]

# Scaling features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

X_train, X_val, y_train, y_val = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Save the scaler
with open('/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/models/scaler.pkl', 'wb') as f:
    pickle.dump(scaler, f)

# Save feature names
feature_names = list(X.columns)
with open('/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/models/feature_names.pkl', 'wb') as f:
    pickle.dump(feature_names, f)

# Define objective functions for LightGBM and XGBoost
def objective_lgb(trial):
    params = {
        'objective': 'regression',
        'metric': 'rmse',
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
    cv_results = lgb.cv(params, dtrain, nfold=5, stratified=False, metrics='rmse', seed=42)
    best_iteration = len(cv_results['valid rmse-mean']) - 1
    return cv_results['valid rmse-mean'][best_iteration]

def objective_xgb(trial):
    params = {
        'objective': 'reg:squarederror',  # Corrected objective
        'eval_metric': 'rmse',
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
    cv_results = xgb.cv(params, dtrain, nfold=5, early_stopping_rounds=100, metrics='rmse', seed=42)
    return cv_results['test-rmse-mean'].min()

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
best_lgb = lgb.LGBMRegressor(**study_lgb.best_params)
best_lgb.fit(X_train, y_train)
best_lgb.booster_.save_model('/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/models/best_lightgbm_model.txt')

# Train and save the best XGBoost model
best_xgb = xgb.XGBRegressor(**study_xgb.best_params)
best_xgb.fit(X_train, y_train)
best_xgb.save_model('/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/models/best_xgboost_model.json')

# SHAP values for LightGBM
explainer_lgb = shap.Explainer(best_lgb)
shap_values_lgb = explainer_lgb(X_val)

# Plot SHAP summary
shap.summary_plot(shap_values_lgb, X_val, feature_names=X.columns)

# Save the plot
plt.savefig('/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/models/lightgbm_shap_summary.png')

# SHAP values for XGBoost
explainer_xgb = shap.Explainer(best_xgb)
shap_values_xgb = explainer_xgb(X_val)

# Plot SHAP summary
shap.summary_plot(shap_values_xgb, X_val, feature_names=X.columns)

# Save the plot
plt.savefig('/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/models/xgboost_shap_summary.png')
