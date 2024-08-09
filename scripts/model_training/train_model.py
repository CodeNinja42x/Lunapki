import pandas as pd
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib

# Paths to your data
processed_data_path = 'data/processed_data/processed_data.csv'
model_save_path = 'models/trained_models/xgb_model.pkl'

# Load processed data
data = pd.read_csv(processed_data_path)

# Replace 'your_target_column' with the actual column name in your dataset
X = data.drop(columns=['your_target_column'])
y = data['your_target_column']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = XGBClassifier()
model.fit(X_train, y_train)

# Evaluate model
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

# Save the model
joblib.dump(model, model_save_path)

print(f"Model training completed. Test Accuracy: {accuracy:.2f}. Model saved to {model_save_path}.")
