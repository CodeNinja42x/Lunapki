import pandas as pd
import numpy as np  # Ensure numpy is imported

def advanced_backtest(data, strategy='moving_average'):
    if strategy == 'moving_average':
        # Moving Average Crossover Strategy
        data['SMA50'] = data['Close'].rolling(window=50).mean()
        data['SMA200'] = data['Close'].rolling(window=200).mean()
        data['Signal'] = 0
        data['Signal'][50:] = np.where(data['SMA50'][50:] > data['SMA200'][50:], 1, 0)
        data['Position'] = data['Signal'].diff()

        # Calculate returns
        data['Strategy_Returns'] = data['Position'].shift(1) * data['Close'].pct_change()
        return data['Strategy_Returns'].cumsum()

    # Additional strategies can be added here
    return None
