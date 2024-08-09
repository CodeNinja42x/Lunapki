import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pandas as pd

def train_model(X, y):
    """Train an XGBoost model on the provided data."""
    model = xgb.XGBClassifier()
    model.fit(X, y)
    return model

def evaluate_model(model, X_test, y_test):
    """Evaluate the model on the test data."""
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model accuracy: {accuracy}")

if __name__ == "__main__":
    data_path = '../data/engineered_data/your_engineered_data.csv'
    data = pd.read_csv(data_path)

    X = data.drop('target', axis=1)
    y = data['target']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    model = train_model(X_train, y_train)
    evaluate_model(model, X_test, y_test)
