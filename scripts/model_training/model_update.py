# model_update.py
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
import pickle

# Load new data and retrain model
data = pd.read_csv('new_data.csv')
X = data.drop('Target', axis=1)
y = data['Target']

model = GradientBoostingClassifier()
model.fit(X, y)

# Save the updated model
with open('updated_model.pkl', 'wb') as f:
    pickle.dump(model, f)
