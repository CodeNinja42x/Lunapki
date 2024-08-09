import optuna
from lightgbm import LGBMClassifier
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.datasets import load_breast_cancer  # Replace with your dataset
from sklearn.metrics import accuracy_score
import pandas as pd

# Load your dataset
# Replace this with your dataset
data = load_breast_cancer()
X = pd.DataFrame(data.data, columns=data.feature_names)
y = pd.Series(data.target)

# Split the dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

def objective(trial):
    # Define the hyperparameters to tune
    param = {
        'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.3),
        'num_leaves': trial.suggest_int('num_leaves', 20, 150),
        'max_depth': trial.suggest_int('max_depth', 3, 12),
        'min_data_in_leaf': trial.suggest_int('min_data_in_leaf', 10, 100),
        'colsample_bytree': trial.suggest_float('colsample_bytree', 0.3, 1.0),
        'subsample': trial.suggest_float('subsample', 0.3, 1.0),
        'reg_alpha': trial.suggest_float('reg_alpha', 0.0, 10.0),
        'reg_lambda': trial.suggest_float('reg_lambda', 0.0, 10.0),
    }
    
    # Create and train the model
    model = LGBMClassifier(**param)
    score = cross_val_score(model, X_train, y_train, n_jobs=-1, cv=3)
    accuracy = score.mean()
    
    return accuracy

# Create a study and optimize it
study = optuna.create_study(direction='maximize')
study.optimize(objective, n_trials=100)

# Print best hyperparameters
print("Best hyperparameters:", study.best_params)

# Train the final model with the best hyperparameters
final_model = LGBMClassifier(**study.best_params)
final_model.fit(X_train, y_train)

# Evaluate the model
y_pred = final_model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Test Accuracy: {accuracy:.2f}")
