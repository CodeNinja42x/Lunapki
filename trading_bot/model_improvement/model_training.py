from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib

def train_model(X_file, y_file):
    # Load data
    X = pd.read_csv(X_file)
    y = pd.read_csv(y_file)

    # Split the data
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train a model (e.g., Random Forest)
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Save the model
    joblib.dump(model, 'ensemble_model.pkl')
    print("Model training completed and saved as 'ensemble_model.pkl'.")
    return model

# Train model using the processed data
model = train_model('processed_data_with_features.csv', 'y_train.csv')
