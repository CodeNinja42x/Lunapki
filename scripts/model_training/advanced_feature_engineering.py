import pandas as pd
import ta  # Technical Analysis library

# Load data
data = pd.read_csv('data/raw_data/your_raw_data.csv')

# Calculate RSI
data['RSI'] = ta.momentum.RSIIndicator(close=data['close'], window=14).rsi()

# Calculate Stochastic Oscillator
stoch = ta.momentum.StochasticOscillator(
    high=data['high'], low=data['low'], close=data['close'], window=14)
data['Stochastic'] = stoch.stoch()

# Save the enhanced dataset
data.to_csv('data/processed_data/advanced_features_data.csv', index=False)
