from sklearn.model_selection import cross_val_score
from xgboost import XGBClassifier
import pandas as pd

if __name__ == "__main__":
    df = pd.read_csv('engineered_data.csv')
    X, y = df.drop('target', axis=1), df['target']
    model = XGBClassifier()
    scores = cross_val_score(model, X, y, cv=5)
    print(f"Cross-validation scores: {scores}")
    print(f"Mean accuracy: {scores.mean():.2f}")
