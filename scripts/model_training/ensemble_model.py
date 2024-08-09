import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from sklearn.metrics import accuracy_score

# Load data
data = pd.read_csv('data/processed_data/your_processed_data.csv')

# Define features and target
X = data.drop('target_column', axis=1)
y = data['target_column']

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train individual models
xgb_model = XGBClassifier()
lgbm_model = LGBMClassifier()
rf_model = RandomForestClassifier()

xgb_model.fit(X_train, y_train)
lgbm_model.fit(X_train, y_train)
rf_model.fit(X_train, y_train)

# Make predictions
xgb_pred = xgb_model.predict(X_test)
lgbm_pred = lgbm_model.predict(X_test)
rf_pred = rf_model.predict(X_test)

# Ensemble predictions (Simple Averaging)
ensemble_pred = np.round((xgb_pred + lgbm_pred + rf_pred) / 3)

# Evaluate ensemble model
accuracy = accuracy_score(y_test, ensemble_pred)
print(f'Ensemble Model Accuracy: {accuracy:.4f}')

# Save ensemble model
import pickle
with open('models/trained_models/ensemble_model.pkl', 'wb') as f:
    pickle.dump(ensemble_pred, f)
