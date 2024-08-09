import pandas as pd
import joblib

# Load the latest data
data = pd.read_csv('/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/latest_data.csv')

# Load the model
model = joblib.load('/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/models/ensemble_model.pkl')

# Make predictions
X = data.drop(columns=['Close'])
predictions = model.predict(X)
predictions = (predictions > 0.5).astype(int)

# Output predictions
data['Predictions'] = predictions
print(data[['Close', 'Predictions']].head())

# Save predictions to CSV
data.to_csv('/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/predictions.csv', index=False)
