import joblib

# Load the existing model
model = joblib.load('models/trained_model.pkl')

# Re-save the model in the current environment
joblib.dump(model, 'models/trained_model_resaved.pkl')
