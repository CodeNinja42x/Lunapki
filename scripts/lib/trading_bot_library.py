import joblib
import pandas as pd
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier

def load_data(filepath):
    return pd.read_csv(filepath)

def refine_and_tune_model(X_train, y_train, n_splits=2):
    param_grid = {
        'n_estimators': [50, 100, 200],
        'max_depth': [None, 10, 20],
    }
    grid_search = GridSearchCV(RandomForestClassifier(), param_grid, cv=n_splits)
    grid_search.fit(X_train, y_train)
    return grid_search.best_estimator_, grid_search.best_params_

def load_model(filepath):
    return joblib.load(filepath)

def save_model(model, filepath):
    joblib.dump(model, filepath)
