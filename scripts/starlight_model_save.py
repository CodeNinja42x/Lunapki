import os
import joblib
import xgboost as xgb  # Assuming you're working with XGBoost
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_iris  # Replace this with your actual dataset

# Path to your model
model_path = '/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/models/optimized_xgb_model_v2.pkl'

# Check if the model exists
if os.path.exists(model_path):
    try:
        print(f"Model found at {model_path}. Loading model...")
        xgb_model = joblib.load(model_path)
        print("Model loaded successfully!")
    except Exception as e:
        print(f"Error loading model: {e}")
        print("Model might be corrupted. Retraining a new model...")
        
        # Retrain the model
        data = load_iris()  # Replace with your actual dataset
        X, y = data.data, data.target
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

        # Train a new XGBoost model
        xgb_model = xgb.XGBClassifier(n_estimators=100, max_depth=3, learning_rate=0.1)
        xgb_model.fit(X_train, y_train)

        # Save the new model
        joblib.dump(xgb_model, model_path)
        print(f"New model trained and saved at {model_path}")
else:
    print(f"Model not found at {model_path}. Training a new model...")

    # Train a new model (replace with your training code)
    data = load_iris()  # Replace with your actual dataset
    X, y = data.data, data.target
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    # Train the XGBoost model (replace parameters as needed)
    xgb_model = xgb.XGBClassifier(n_estimators=100, max_depth=3, learning_rate=0.1)
    xgb_model.fit(X_train, y_train)

    # Save the new model
    joblib.dump(xgb_model, model_path)
    print(f"New model trained and saved at {model_path}")
