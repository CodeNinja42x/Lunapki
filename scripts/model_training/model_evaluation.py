import xgboost as xgb
import pandas as pd
from sklearn.metrics import classification_report, confusion_matrix

def load_model(model_path):
    """Load a trained model from the specified file path."""
    model = xgb.XGBClassifier()
    model.load_model(model_path)
    return model

def evaluate_model(model, X, y):
    """Evaluate the model's performance."""
    y_pred = model.predict(X)
    print(confusion_matrix(y, y_pred))
    print(classification_report(y, y_pred))

if __name__ == "__main__":
    model_path = '../models/trained_models/your_model.xgb'
    data_path = '../data/engineered_data/your_engineered_data.csv'
    
    model = load_model(model_path)
    data = pd.read_csv(data_path)
    
    X = data.drop('target', axis=1)
    y = data['target']
    
    evaluate_model(model, X, y)
