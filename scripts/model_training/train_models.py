import pandas as pd
import joblib
import logging
from sklearn.model_selection import train_test_split, GridSearchCV, StratifiedKFold
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, AdaBoostClassifier, VotingClassifier
from sklearn.linear_model import LogisticRegression
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from catboost import CatBoostClassifier
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score
from imblearn.over_sampling import RandomOverSampler
from sklearn.preprocessing import Binarizer
from sklearn.exceptions import UndefinedMetricWarning
import warnings

# Set up logging
logging.basicConfig(filename='/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/logs/train_models.log', level=logging.DEBUG, format='%(asctime)s %(message)s')

# Ignore warnings related to undefined metrics
warnings.filterwarnings('ignore', category=UndefinedMetricWarning)

# Load data
try:
    data_path = '/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/data/data.csv'
    data = pd.read_csv(data_path)
    logging.info(f"Loaded data from {data_path}")
except Exception as e:
    logging.error(f"Error loading data: {e}")
    data = pd.DataFrame()

if data.empty:
    logging.error("Data is empty. Please check the data collection step.")
    raise ValueError("Data is empty. Please check the data collection step.")

# Split data into features and target
try:
    target = 'target'
    features = [col for col in data.columns if col != target and col != 'timestamp']  # Exclude 'timestamp'
    X = data[features]
    y = data[target]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Check class distribution
    class_distribution = y_train.value_counts()
    logging.info(f"Class distribution in training data:\n{class_distribution}")

    # Apply RandomOverSampler to handle class imbalance
    ros = RandomOverSampler(random_state=42)
    X_train, y_train = ros.fit_resample(X_train, y_train)
except Exception as e:
    logging.error(f"Error splitting data: {e}")
    raise e

# Determine the number of splits for cross-validation
min_samples_class = class_distribution.min()
n_splits = max(2, min(5, min_samples_class))

# Define model hyperparameter grids with adjusted parameters for LightGBM
param_grid = {
    'RandomForest': {'n_estimators': [100, 200], 'max_depth': [None, 10, 20]},
    'GradientBoosting': {'n_estimators': [100, 200], 'learning_rate': [0.01, 0.1]},
    'AdaBoost': {'n_estimators': [50, 100], 'learning_rate': [0.01, 0.1]},
    'LogisticRegression': {'C': [0.1, 1.0, 10.0]},
    'XGBoost': {'n_estimators': [100, 200], 'learning_rate': [0.01, 0.1]},
    'LightGBM': {'n_estimators': [100, 200], 'learning_rate': [0.01, 0.1], 'min_data_in_leaf': [1, 5, 10], 'num_leaves': [20, 31, 50]},
    'CatBoost': {'iterations': [100, 200], 'learning_rate': [0.01, 0.1]}
}

# Train individual models with hyperparameter tuning
try:
    models = {
        'RandomForest': RandomForestClassifier(),
        'GradientBoosting': GradientBoostingClassifier(),
        'AdaBoost': AdaBoostClassifier(),
        'LogisticRegression': LogisticRegression(),
        'XGBoost': XGBClassifier(),
        'LightGBM': LGBMClassifier(),
        'CatBoost': CatBoostClassifier()
    }

    for name, model in models.items():
        grid_search = GridSearchCV(model, param_grid[name], cv=StratifiedKFold(n_splits=n_splits))
        grid_search.fit(X_train, y_train)
        models[name] = grid_search.best_estimator_
        joblib.dump(models[name], f'/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/models/{name}_model.pkl')
        logging.info(f"{name} model trained and saved")

    # Create an ensemble model
    ensemble_model = VotingClassifier(estimators=[
        ('rf', models['RandomForest']),
        ('gb', models['GradientBoosting']),
        ('ada', models['AdaBoost']),
        ('log', models['LogisticRegression']),
        ('xgb', models['XGBoost']),
        ('lgb', models['LightGBM']),
        ('cat', models['CatBoost'])
    ], voting='soft')

    ensemble_model.fit(X_train, y_train)
    accuracy = ensemble_model.score(X_test, y_test)
    y_pred_prob = ensemble_model.predict_proba(X_test)[:, 1]

    # Adjust the decision threshold
    binarizer = Binarizer(threshold=0.5)
    y_pred = binarizer.transform(y_pred_prob.reshape(-1, 1))

    precision = precision_score(y_test, y_pred, zero_division=1)
    recall = recall_score(y_test, y_pred, zero_division=1)
    f1 = f1_score(y_test, y_pred, zero_division=1)
    accuracy = accuracy_score(y_test, y_pred)

    logging.info(f"Ensemble Model trained with accuracy: {accuracy}")
    logging.info(f"Precision: {precision}, Recall: {recall}, F1 Score: {f1}")

    # Save the ensemble model
    joblib.dump(ensemble_model, '/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/models/ensemble_model.pkl')
    logging.info("Ensemble model saved")
except Exception as e:
    logging.error(f"Error training model: {e}")
    raise e
