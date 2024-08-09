import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from catboost import CatBoostClassifier
import joblib
import os

def generate_sample_data(num_samples=500, num_features=20):
    data = np.random.rand(num_samples, num_features)
    columns = [f'feature_{i}' for i in range(num_features)]
    return pd.DataFrame(data, columns=columns)

def train_models(X, y):
    models = {
        'RandomForest': RandomForestClassifier(n_estimators=100, random_state=42),
        'GradientBoosting': GradientBoostingClassifier(n_estimators=100, random_state=42),
        'XGBoost': XGBClassifier(n_estimators=100, random_state=42),
        'LightGBM': LGBMClassifier(n_estimators=100, random_state=42),
        'CatBoost': CatBoostClassifier(n_estimators=100, random_state=42, verbose=0)
    }
    trained_models = {}
    for name, model in models.items():
        model.fit(X, y)
        trained_models[name] = model
    return trained_models

def save_models(models, dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    for name, model in models.items():
        joblib.dump(model, os.path.join(dir_path, f'{name}_model.pkl'))

def save_feature_names(feature_names, filepath):
    joblib.dump(feature_names, filepath)

def main():
    data = generate_sample_data()
    target = np.random.randint(0, 2, size=(data.shape[0],))
    data['target'] = target
    data.to_csv('/Users/gorkemberkeyuksel/Desktop/training_data.csv', index=False)
    
    X = data.drop(columns=['target'])
    y = data['target']
    
    models = train_models(X, y)
    
    model_dir = '/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/models'
    save_models(models, model_dir)
    
    features_path = os.path.join(model_dir, 'training_feature_names.pkl')
    save_feature_names(X.columns.tolist(), features_path)
    
    print(f"Model and feature names saved successfully.\nTraining data columns: {X.columns.tolist()}")

if __name__ == "__main__":
    main()
