import pandas as pd
import optuna
import lightgbm as lgb
import xgboost as xgb
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import log_loss
from sklearn.preprocessing import StandardScaler
import shap
import matplotlib.pyplot as plt

# Load your data
data = pd.read_csv('/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/processed_data.csv')
target_column = 'Close'  # Assuming 'Close' is the target column

# Feature Engineering
def create_features(data):
    # Create lagged features
    data['lag_1'] = data['Close'].shift(1)
    data['lag_5'] = data['Close'].shift(5)
    data['lag_10'] = data['Close'].shift(10)
    
    # Create moving averages
    data['ma_10'] = data['Close'].rolling(window=10).mean()
    data['ma_20'] = data['Close'].rolling(window=20).mean()
    data['ma_50'] = data['Close'].rolling(window=50).mean()
    
    # Create rolling statistics
    data['rolling_std_10'] = data['Close'].rolling(window=10).std()
    data['rolling_std_20'] = data['Close'].rolling(window=20).std()
    
    # Create RSI
    data['rsi'] = calculate_rsi(data['Close'], 14)
    
    # Create Bollinger Bands
    data['bollinger_high'] = data['ma_20'] + (data['rolling_std_20'] * 2)
    data['bollinger_low'] = data['ma_20'] - (data['rolling_std_20'] * 2)
    
    # Create MACD
    data['ma_12'] = data['Close'].ewm(span=12, adjust=False).mean()
    data['ma_26'] = data['Close'].ewm(span=26, adjust=False).mean()
    data['macd'] = data['ma_12'] - data['ma_26']
    data['signal'] = data['macd'].ewm(span=9, adjust=False).mean()
    
    # Handle missing values by backfilling
    data.bfill(inplace=True)
    
    return data

def calculate_rsi(series, period):
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

data = create_features(data)

# Prepare data for modeling
X = data.drop(columns=[target_column, 'Open time', 'Close time'])  # Adjust as necessary
y = data[target_column]

# Scaling features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

X_train, X_val, y_train, y_val = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

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
    cv_results = lgb.cv(params, dtrain, nfold=5, stratified=False, early_stopping_rounds=100, metrics='rmse', seed=42)
    return cv_results['rmse-mean'][-1]

def objective_xgb(trial):
    params = {
        'objective': 'regression',
        'eval_metric': 'rmse',
        'verbosity': 0,
        '        learning_rate': trial.suggest_float('learning_rate', 0.01, 0.3),
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

