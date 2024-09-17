import pandas as pd
import numpy as np
import talib as ta
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, VotingClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from xgboost import XGBClassifier

def load_data_from_csv(file_path):
    df = pd.read_csv(file_path, parse_dates=['Date'])
    print(f"Data loaded. Shape: {df.shape}")
    return df

def calculate_indicators(df):
    required_columns = ['Date', 'Close']
    for col in required_columns:
        if col not in df.columns:
            raise KeyError(f"Column '{col}' is missing from the DataFrame")

    df['MA50'] = ta.SMA(df['Close'], timeperiod=50)
    df['MA200'] = ta.SMA(df['Close'], timeperiod=200)
    df['RSI'] = ta.RSI(df['Close'], timeperiod=14)
    
    df['MACD'], df['MACDsignal'], _ = ta.MACD(df['Close'])
    df['BB_upper'], df['BB_middle'], df['BB_lower'] = ta.BBANDS(df['Close'], timeperiod=20)

    print(f"Indicators calculated. DataFrame shape: {df.shape}")
    return df

def prepare_features(df):
    df['Price_Change'] = df['Close'].pct_change()
    features = ['MA50', 'MA200', 'RSI', 'MACD', 'MACDsignal', 'Price_Change', 
                'BB_upper', 'BB_middle', 'BB_lower']
    
    # Check for NaN values
    nan_counts = df[features].isna().sum()
    print("Checking for NaNs in features:")
    print(nan_counts)

    # Drop features with excessive NaNs (e.g., more than 50%)
    features_to_drop = nan_counts[nan_counts > len(df) * 0.5].index
    df = df.drop(columns=features_to_drop)
    features = list(set(features) - set(features_to_drop))

    # Handle remaining NaNs - forward fill followed by backward fill
    df[features] = df[features].fillna(method='ffill').fillna(method='bfill')

    X = df[features].dropna()
    y = (df['Close'].shift(-1) > df['Close']).astype(int)
    
    X = X.iloc[:-1]
    y = y.iloc[:-1]

    print(f"Features prepared. X shape: {X.shape}, y shape: {y.shape}")
    return X, y

def train_model(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    rf = RandomForestClassifier(random_state=42)
    rf_param_grid = {
        'n_estimators': [100, 200, 300],
        'max_depth': [5, 10, 15],
        'min_samples_split': [2, 5, 10],
        'min_samples_leaf': [1, 2, 4]
    }
    grid_search_rf = GridSearchCV(estimator=rf, param_grid=rf_param_grid, cv=5, scoring='accuracy', n_jobs=-1)
    grid_search_rf.fit(X_train, y_train)
    best_rf = grid_search_rf.best_estimator_

    xgb = XGBClassifier(use_label_encoder=False, eval_metric='mlogloss', random_state=42)
    xgb_param_grid = {
        'n_estimators': [100, 200, 300],
        'learning_rate': [0.01, 0.1, 0.2],
        'max_depth': [3, 5, 7],
        'subsample': [0.8, 0.9, 1.0],
        'colsample_bytree': [0.8, 0.9, 1.0]
    }
    grid_search_xgb = GridSearchCV(estimator=xgb, param_grid=xgb_param_grid, cv=5, scoring='accuracy', n_jobs=-1)
    grid_search_xgb.fit(X_train, y_train)
    best_xgb = grid_search_xgb.best_estimator_

    gbc = GradientBoostingClassifier(random_state=42)
    gbc_param_grid = {
        'n_estimators': [100, 200, 300],
        'learning_rate': [0.01, 0.1, 0.2],
        'max_depth': [3, 5, 7],
        'min_samples_split': [2, 5, 10],
        'min_samples_leaf': [1, 2, 4]
    }
    grid_search_gbc = GridSearchCV(estimator=gbc, param_grid=gbc_param_grid, cv=5, scoring='accuracy', n_jobs=-1)
    grid_search_gbc.fit(X_train, y_train)
    best_gbc = grid_search_gbc.best_estimator_

    ensemble_model = VotingClassifier(estimators=[
        ('rf', best_rf),
        ('xgb', best_xgb),
        ('gbc', best_gbc)
    ], voting='soft')

    ensemble_model.fit(X_train, y_train)

    return ensemble_model

def backtest_strategy(df, model):
    X, _ = prepare_features(df)
    
    # Align the DataFrame index with the feature matrix X
    df = df.loc[X.index]

    df['ML_Prediction'] = model.predict(X)
    
    df['Signal'] = np.where((df['MA50'] > df['MA200']) & (df['RSI'] < 30) & (df['ML_Prediction'] == 1) | 
                            (df['MA50'] > df['MA200']) & (df['RSI'] > 70) & (df['ML_Prediction'] == 0), 1, 0)
    
    df['Strategy_Return'] = df['Close'].pct_change().shift(-1) * df['Signal']
    df['Strategy_Return'].fillna(0, inplace=True)
    df['Cumulative_Strategy_Return'] = (1 + df['Strategy_Return']).cumprod()

    if df['Strategy_Return'].std() == 0:
        sharpe_ratio = 0
        sortino_ratio = 0
    else:
        sharpe_ratio = np.mean(df['Strategy_Return']) / df['Strategy_Return'].std() * np.sqrt(252)
        downside_return = df.loc[df['Strategy_Return'] < 0, 'Strategy_Return']
        sortino_ratio = np.mean(df['Strategy_Return']) / downside_return.std() * np.sqrt(252) if not downside_return.empty else 0

    max_drawdown = (df['Cumulative_Strategy_Return'].cummax() - df['Cumulative_Strategy_Return']).max()

    plt.figure(figsize=(14, 7))
    plt.plot(df['Date'], df['Cumulative_Strategy_Return'], label='Strategy Returns')
    plt.plot(df['Date'], df['Close'] / df['Close'].iloc[0], label='Market Returns')
    plt.title(f'Backtest Results - Sharpe Ratio: {sharpe_ratio:.2f}, Max Drawdown: {max_drawdown:.2%}')
    plt.legend()
    plt.show()

    print(df[['Date', 'Close', 'MA50', 'MA200', 'RSI', 'Signal']].tail(20))
    print(f"Total Strategy Return: {df['Cumulative_Strategy_Return'].iloc[-1] - 1:.2%}")
    print(f"Sharpe Ratio: {sharpe_ratio:.2f}")
    print(f"Sortino Ratio: {sortino_ratio:.2f}")
    print(f"Max Drawdown: {max_drawdown:.2%}")

if __name__ == "__main__":
    file_path = '/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/sample_data.csv'
    df = load_data_from_csv(file_path)
    df = calculate_indicators(df)
    X, y = prepare_features(df)
    if X.empty:
        print("Error: Feature matrix X is empty after preprocessing. Please check your data.")
    else:
        model = train_model(X, y)
        backtest_strategy(df, model)
