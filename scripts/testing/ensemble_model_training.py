import pandas as pd
import xgboost as xgb
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

# Load the refined data
data = pd.read_csv('/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/data/refined_data.csv')

# Define target and features
target_column = 'close'
X = data.drop(columns=[target_column, 'date'])
y = data[target_column]

# Load the XGBoost model
xgb_model = xgb.XGBRegressor()
xgb_model.load_model('/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/models/optimized_xgb_model_refined.pkl')

# Train a RandomForest model
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X, y)

# Make predictions with both models
xgb_predictions = xgb_model.predict(X)
rf_predictions = rf_model.predict(X)

# Ensemble: Average predictions
ensemble_predictions = (xgb_predictions + rf_predictions) / 2

# Evaluate the ensemble model
mse = mean_squared_error(y, ensemble_predictions)
print(f"Ensemble Model Mean Squared Error: {mse}")
