from xgboost import XGBRegressor
import pandas as pd
from sklearn.metrics import mean_squared_error

# Load the enhanced data
data_path = '/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/data/processed_data_with_features.csv'
data = pd.read_csv(data_path)

# Replace 'target_column_name' with your actual target column name
target_column = 'close'  # Change this to your actual target column name
X = data.drop(columns=[target_column, 'date'])
y = data[target_column]

# Load the trained model
model_load_path = '/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/models/model_file.pkl'
model = XGBRegressor()
model.load_model(model_load_path)

# Make predictions
predictions = model.predict(X)
mse = mean_squared_error(y, predictions)
print(f"Model Testing Mean Squared Error: {mse}")

# Additional backtesting or testing logic can be added here
