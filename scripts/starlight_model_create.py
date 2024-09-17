import joblib
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_iris  # Replace with your dataset

# Load example dataset
data = load_iris()  # Replace with your actual dataset
X, y = data.data, data.target

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Train the XGBoost model
xgb_model = xgb.XGBClassifier(n_estimators=100, max_depth=3, learning_rate=0.1)
xgb_model.fit(X_train, y_train)

# Save the model as crypto_model.pkl
joblib.dump(xgb_model, 'crypto_model.pkl')
