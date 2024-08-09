# save_required_features.py

import joblib

required_features = [
    'return_lag_3', 'return_volatility', 'volume', 'return_lag_10', 'return_lag_2',
    'return', 'volatility_lag_1', 'return_lag_1', 'diff_close_ma_50', 'momentum_lag_10',
    'volume_change', 'volatility_lag_10', 'return_lag_5', 'momentum_lag_5', 'volatility',
    'expanding_std', 'volatility_lag_2', 'volatility_lag_5', 'diff_close_ma_10',
    'rolling_std_5', 'momentum_lag_1', 'rolling_std_10', 'volatility_lag_3', 'rolling_std_20',
    'MACD', 'MACD_Diff', 'BB_Width', 'momentum_lag_2', 'RSI', 'momentum_lag_3', 'rolling_volume_10',
    'close', 'BB_High', 'MACD_Signal', 'expanding_mean', 'MACD_RSI', 'rolling_volume_50',
    'momentum_volatility', 'momentum', 'high', 'BB_Low', 'open', 'low', 'rolling_mean_10',
    'moving_avg_10', 'cumulative_return', 'rolling_mean_20', 'ema_20', 'ema_10', 'rolling_mean_5',
    'moving_avg_50'
]

# Save the required features to a file
joblib.dump(required_features, '/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/models/required_features.pkl')
