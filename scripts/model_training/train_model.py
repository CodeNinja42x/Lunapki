import pandas as pd
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib

# Load the processed data
processed_data_path = 'data/processed_data/processed_data.csv'
data = pd.read_csv(processed_data_path)

# Define target column and features
target_column = 'Close'
features = data.drop(columns=[target_column])
target = data[target_column]

# Split the data
X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

# Train the model
model = XGBClassifier(use_label_encoder=False, eval_metric='mlogloss')
model.fit(X_train, y_train)

# Evaluate the model
predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)
print(f'Test Accuracy: {accuracy}')

# Save the model
model_save_path = 'models/trained_models/xgb_model.pkl'
joblib.dump(model, model_save_path)
