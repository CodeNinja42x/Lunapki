import json
import lightgbm as lgb
import pandas as pd
from sklearn.model_selection import train_test_split

# Load the processed data
data = pd.read_csv('/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/Bot/processed_data.csv')

# Split the data into features and target
X = data.drop(columns=['target'])
y = data['target']

# Split the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Load the best parameters
with open('/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/Bot/best_params.json', 'r') as f:
    best_params = json.load(f)

# Create a LightGBM dataset
train_data = lgb.Dataset(X_train, label=y_train)
test_data = lgb.Dataset(X_test, label=y_test, reference=train_data)

# Train the final model
final_model = lgb.train(best_params, train_data, valid_sets=[test_data], verbose_eval=False)

# Save the final model
final_model.save_model('/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/Bot/final_model.txt')

print("Final model training completed and saved.")
