# xgboost_training.py
import pandas as pd
import xgboost as xgb

# Load the feature-engineered data
data = pd.read_csv('data/engineered_data_v2.csv')
X = data.drop('target', axis=1)
y = data['target']

# Train XGBoost model
model = xgb.XGBClassifier()
model.fit(X, y)

# Save the model
model.save_model('models/xgboost_model.json')
