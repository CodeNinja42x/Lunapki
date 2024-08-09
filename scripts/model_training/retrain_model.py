import joblib
import numpy as np
from sklearn.datasets import make_classification
from sklearn.tree import DecisionTreeClassifier

# Create a synthetic dataset (replace this with your actual data loading and preprocessing steps)
X, y = make_classification(n_samples=1000, n_features=20, random_state=42)

# Train a new model (replace this with your actual model training steps)
model = DecisionTreeClassifier()
model.fit(X, y)

# Save the new model
joblib.dump(model, 'models/trained_model_resaved.pkl')
