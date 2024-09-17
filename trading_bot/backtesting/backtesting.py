import pandas as pd
from talib import BBANDS, MACD

def simple_strategy(data):
    data['BB_Upper'], _, data['BB_Lower'] = BBANDS(data['Close'], timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)
    data['MACD'], data['MACD_Signal'], _ = MACD(data['Close'], fastperiod=12, slowperiod=26, signalperiod=9)
    
    data['Signal'] = 0
    data.loc[(data['Close'] < data['BB_Lower']) & (data['MACD'] > data['MACD_Signal']), 'Signal'] = 1
    data.loc[(data['Close'] > data['BB_Upper']) & (data['MACD'] < data['MACD_Signal']), 'Signal'] = -1
    
    data['Returns'] = data['Close'].pct_change()
    data['Strategy_Return'] = data['Signal'].shift(1) * data['Returns']
    return data

if __name__ == "__main__":
    df = pd.read_csv('engineered_data.csv')
    df = simple_strategy(df)
    df.to_csv('backtest_results.csv', index=False)
