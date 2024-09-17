import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor, StackingRegressor
from sklearn.model_selection import TimeSeriesSplit, RandomizedSearchCV
from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error
import xgboost as xgb
import talib as ta
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from pmdarima import auto_arima

# Load your dataset
df = pd.read_csv('your_stock_data.csv', index_col='Date', parse_dates=True)

# Feature Engineering - Add technical indicators
df['RSI'] = ta.RSI(df['Close'], timeperiod=14)
df['MACD'], df['MACD_signal'], _ = ta.MACD(df['Close'], fastperiod=12, slowperiod=26, signalperiod=9)
df['ATR'] = ta.ATR(df['High'], df['Low'], df['Close'], timeperiod=14)
df['UpperBB'], df['MiddleBB'], df['LowerBB'] = ta.BBANDS(df['Close'], timeperiod=20)

# Fill any NaN values (important for technical indicators)
df.fillna(method='ffill', inplace=True)

# Define target and features
X = df[['RSI', 'MACD', 'MACD_signal', 'ATR', 'UpperBB', 'MiddleBB', 'LowerBB']]
y = df['Close']

# Split into training and testing
train_size = int(0.8 * len(df))
X_train, X_test = X[:train_size], X[train_size:]
y_train, y_test = y[:train_size], y[train_size:]

# Scaling the data
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Model 1: Random Forest
rf_model = RandomForestRegressor()
rf_params = {'n_estimators': [100, 200], 'max_depth': [10, 20], 'min_samples_split': [2, 5]}
rf_search = RandomizedSearchCV(rf_model, rf_params, n_iter=10, cv=TimeSeriesSplit(n_splits=5), verbose=1)
rf_search.fit(X_train_scaled, y_train)
best_rf = rf_search.best_estimator_

# Model 2: XGBoost
xgb_model = xgb.XGBRegressor()
xgb_params = {'n_estimators': [100, 200], 'max_depth': [3, 6], 'learning_rate': [0.01, 0.1]}
xgb_search = RandomizedSearchCV(xgb_model, xgb_params, n_iter=10, cv=TimeSeriesSplit(n_splits=5), verbose=1)
xgb_search.fit(X_train_scaled, y_train)
best_xgb = xgb_search.best_estimator_

# Model 3: ARIMA
arima_model = auto_arima(y_train, seasonal=False, trace=True, error_action='ignore', suppress_warnings=True)
arima_pred_train = arima_model.predict_in_sample()
arima_pred_test = arima_model.predict(n_periods=len(y_test))

# Ensemble Model: Stacking (Random Forest + XGBoost)
stacked_model = StackingRegressor(
    estimators=[('rf', best_rf), ('xgb', best_xgb)],
    final_estimator=Ridge()
)
stacked_model.fit(X_train_scaled, y_train)

# Make predictions
stacked_predictions = stacked_model.predict(X_test_scaled)
mse = mean_squared_error(y_test, stacked_predictions)
print(f"Mean Squared Error of Stacked Model: {mse}")

# Combine with ARIMA predictions (simple ensemble)
final_predictions = (stacked_predictions * 0.7) + (arima_pred_test * 0.3)
final_mse = mean_squared_error(y_test, final_predictions)
print(f"Final Ensemble MSE: {final_mse}")

# Visualize actual vs predicted prices
plt.figure(figsize=(10, 6))
plt.plot(df.index[train_size:], y_test, label="Actual")
plt.plot(df.index[train_size:], final_predictions, label="Predicted", linestyle='--')
plt.title("Actual vs Predicted Stock Prices")
plt.legend()
plt.show()

# Residuals
residuals = y_test - final_predictions
sns.scatterplot(x=np.arange(len(residuals)), y=residuals)
plt.title("Residuals of Final Ensemble Model")
plt.show()

# Autocorrelation of Residuals
from statsmodels.graphics.tsaplots import plot_acf
plot_acf(residuals)
plt.show()

# Save Models
joblib.dump(best_rf, 'random_forest_model.joblib')
joblib.dump(best_xgb, 'xgboost_model.joblib')
joblib.dump(arima_model, 'arima_model.pkl')
joblib.dump(stacked_model, 'stacked_model.joblib')
joblib.dump(scaler, 'scaler.joblib')

# Example backtesting logic
portfolio_value = 100000  # Initial capital
position_size = 100  # Number of shares to buy/sell
for i in range(len(y_test)):
    if final_predictions[i] > y_test.iloc[i]:  # Buy signal
        portfolio_value += position_size * (y_test.iloc[i] - y_test.iloc[i-1])

print(f"Final Portfolio Value: {portfolio_value}")
