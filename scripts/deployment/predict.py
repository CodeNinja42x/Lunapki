import pandas as pd
import joblib

def predict(input_file):
    model = joblib.load('/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/models/best_model.pkl')
    new_data = pd.read_csv(input_file)
    features = new_data[['returns', 'volatility', 'moving_avg_5', 'moving_avg_10', 'moving_avg_20',
                         'momentum_5', 'momentum_10', 'high_low_diff', 'close_open_diff',
                         'volatility_10', 'volatility_20']]
    predictions = model.predict(features)
    print("Predictions:", predictions)

if __name__ == "__main__":
    predict('/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/data/processed_new_data.csv')
