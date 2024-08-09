import lightgbm as lgb
import pandas as pd
import json
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Load your processed data
data = pd.read_csv('/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/latest_data.csv')

# Check if 'target' column exists, if not create it
if 'target' not in data.columns:
    data['target'] = (data['Close'].shift(-1) > data['Close']).astype(int)

# Ensure any NaN values are handled
data.dropna(inplace=True)

X = data.drop(columns=['target'])
y = data['target']

# Split the data
X_train, X_valid, y_train, y_valid = train_test_split(X, y, test_size=0.2, random_state=42)

# Load best parameters
with open('/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/Bot/best_params.json', 'r') as f:
    best_params = json.load(f)

# Train the model
train_data = lgb.Dataset(X_train, label=y_train)
valid_data = lgb.Dataset(X_valid, label=y_valid, reference=train_data)

model = lgb.train(best_params, train_data, valid_sets=[valid_data], early_stopping_rounds=10, verbose_eval=False)

# Save the model
model.save_model('/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/Bot/model.txt')

# Make predictions
y_pred = model.predict(X_valid, num_iteration=model.best_iteration)
y_pred = [1 if pred > 0.5 else 0 for pred in y_pred]

# Evaluate the model
accuracy = accuracy_score(y_valid, y_pred)
print(f'Accuracy: {accuracy}')
