from sklearn.ensemble import VotingClassifier
import xgboost as xgb
from sklearn.ensemble import RandomForestClassifier

def train_ensemble(X, y):
    model1 = xgb.XGBClassifier()
    model2 = RandomForestClassifier()

    ensemble = VotingClassifier(estimators=[('xgb', model1), ('rf', model2)], voting='soft')
    ensemble.fit(X, y)
    
    return ensemble

if __name__ == "__main__":
    df = pd.read_csv("data/engineered_data.csv")
    X = df.drop('target', axis=1)
    y = df['target']

    ensemble = train_ensemble(X, y)
    print("Ensemble model trained.")
