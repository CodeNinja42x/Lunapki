from sklearn.ensemble import GradientBoostingClassifier
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
import pandas as pd

# Load data
df = pd.read_csv('/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/data/btc_data_with_indicators.csv')
X = df[['SMA_20', 'SMA_50', 'RSI', 'Bollinger_Upper', 'Bollinger_Lower']]
y = df['Target']

# Example with Gradient Boosting
gb_model = GradientBoostingClassifier()
gb_model.fit(X_train, y_train)

# Example with LSTM
model = Sequential()
model.add(LSTM(50, activation='relu', input_shape=(X_train.shape[1], 1)))
model.add(Dense(1))
model.compile(optimizer='adam', loss='mse')
model.fit(X_train.values.reshape(-1, X_train.shape[1], 1), y_train, epochs=50)
