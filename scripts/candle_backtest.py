import os
import logging
import numpy as np
import pandas as pd
import talib
from binance.client import Client
import joblib
from datetime import datetime, timedelta
from ta.volatility import BollingerBands
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Logger setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('BacktestLogger')

# Load the model
model_path = '/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/crypto_model.pkl'
model = joblib.load(model_path)
logger.info('Model loaded successfully.')

# Output model information
try:
    n_features = model.n_features_in_
    logger.info(f"Model expects {n_features} features.")
except AttributeError:
    logger.warning("Could not determine the number of features the model expects (attribute 'n_features_in_' not found).")

# Binance API Setup
binance_api_key = os.getenv("BINANCE_API_KEY")
binance_api_secret = os.getenv("BINANCE_API_SECRET")
binance_client = Client(binance_api_key, binance_api_secret)
logger.info('Binance client initialized.')

# Function to get historical data from Binance
def get_historical_data(symbol, interval, days=180):
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(days=days)
    klines = binance_client.get_historical_klines(
        symbol,
        interval,
        start_time.strftime("%d %b %Y %H:%M:%S"),
        end_time.strftime("%d %b %Y %H:%M:%S")
    )
    data = pd.DataFrame(klines, columns=[
        'timestamp', 'open', 'high', 'low', 'close', 'volume',
        'close_time', 'quote_asset_volume', 'number_of_trades',
        'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'
    ])
    data['timestamp'] = pd.to_datetime(data['timestamp'], unit='ms')
    data.set_index('timestamp', inplace=True)
    # Convert columns to float
    float_cols = ['open', 'high', 'low', 'close', 'volume']
    data[float_cols] = data[float_cols].astype(float)
    logger.info(f'Data for {symbol} fetched successfully.')
    return data

# Function to calculate indicators and prepare features
def prepare_features(df):
    # Calculate technical indicators
    df['ATR'] = talib.ATR(df['high'], df['low'], df['close'], timeperiod=14)
    df['RSI'] = talib.RSI(df['close'], timeperiod=14)
    # Bollinger Bands
    indicator_bb = BollingerBands(close=df['close'], window=20, window_dev=2)
    df['bb_upper'] = indicator_bb.bollinger_hband()
    df['bb_lower'] = indicator_bb.bollinger_lband()
    df = df.dropna()
    logger.info('Features prepared.')
    return df

# Function to prepare model features
def prepare_model_features(df):
    # Attempt to select the features that the model expects
    # First, get the feature names from the model if possible
    feature_names = None
    try:
        feature_names = model.get_booster().feature_names
    except:
        pass
    try:
        feature_names = model.feature_names_in_
    except:
        pass

    if feature_names is not None:
        logger.info(f"Model feature names: {feature_names}")
        # Ensure that all feature names are present in df
        missing_features = [feat for feat in feature_names if feat not in df.columns]
        if missing_features:
            logger.error(f"Missing features in data: {missing_features}")
        features_df = df[feature_names].copy()
    else:
        # If feature names are not available, use default feature set
        logger.warning("Could not retrieve feature names from the model. Using default feature set.")
        features_df = df[['open', 'high', 'low', 'close']].copy()

    # Output the features being used
    logger.info(f"Features provided: {features_df.columns.tolist()}")

    # Handle any missing values or preprocessing as required by your model
    features_df.replace([np.inf, -np.inf], np.nan, inplace=True)
    features_df.fillna(method='ffill', inplace=True)
    features_df.fillna(method='bfill', inplace=True)
    logger.info('Model features prepared.')
    return features_df

# Function to detect reversal signals
def detect_reversal_signals(df, model_predictions):
    signals = []
    # Adjusted parameters for less strict criteria
    rsi_overbought = 65  # Lowered from 70
    rsi_oversold = 35    # Raised from 30
    wick_atr_multiplier = 0.3  # Reduced from 0.5

    for i in range(1, len(df)):
        current = df.iloc[i]
        previous = df.iloc[i - 1]
        upper_wick = current['high'] - max(current['open'], current['close'])
        lower_wick = min(current['open'], current['close']) - current['low']
        atr = current['ATR']
        rsi = current['RSI']
        model_pred = model_predictions[i]
        date = current.name
        price = current['close']

        # Adjust model prediction encoding if necessary
        # Assuming model_pred == 1 indicates 'BUY', and model_pred == 0 indicates 'SELL'
        # If your model uses different encoding, adjust the conditions accordingly

        # Verify model prediction encoding
        if model_pred not in [0, 1]:
            logger.warning(f"Unexpected model prediction value: {model_pred} at index {i}")
            continue  # Skip this iteration if the prediction is invalid

        # Long upper wick at resistance with ATR and RSI overbought, and model predicts downward trend
        if (current['high'] >= current['bb_upper'] and
            upper_wick > wick_atr_multiplier * atr and
            rsi >= rsi_overbought and
            current['close'] < current['bb_upper'] and
            model_pred == 0):  # Assuming 0 is a 'SELL' signal
            signals.append({'Date': date, 'Signal': 'SELL', 'Price': price})
            logger.info(f"SELL signal on {date} at price {price} confirmed by model.")

        # Long lower wick at support with ATR and RSI oversold, and model predicts upward trend
        elif (current['low'] <= current['bb_lower'] and
              lower_wick > wick_atr_multiplier * atr and
              rsi <= rsi_oversold and
              current['close'] > current['bb_lower'] and
              model_pred == 1):  # Assuming 1 is a 'BUY' signal
            signals.append({'Date': date, 'Signal': 'BUY', 'Price': price})
            logger.info(f"BUY signal on {date} at price {price} confirmed by model.")
    logger.info(f'Signals detected: {len(signals)}.')
    return pd.DataFrame(signals)

# Function to detect reversal signals without model predictions
def detect_reversal_signals_without_model(df):
    signals = []
    # Adjusted parameters for less strict criteria
    rsi_overbought = 65  # Lowered from 70
    rsi_oversold = 35    # Raised from 30
    wick_atr_multiplier = 0.3  # Reduced from 0.5

    for i in range(1, len(df)):
        current = df.iloc[i]
        previous = df.iloc[i - 1]
        upper_wick = current['high'] - max(current['open'], current['close'])
        lower_wick = min(current['open'], current['close']) - current['low']
        atr = current['ATR']
        rsi = current['RSI']
        date = current.name
        price = current['close']

        # Long upper wick at resistance with ATR and RSI overbought
        if (current['high'] >= current['bb_upper'] and
            upper_wick > wick_atr_multiplier * atr and
            rsi >= rsi_overbought and
            current['close'] < current['bb_upper']):
            signals.append({'Date': date, 'Signal': 'SELL', 'Price': price})
            logger.info(f"SELL signal on {date} at price {price}.")

        # Long lower wick at support with ATR and RSI oversold
        elif (current['low'] <= current['bb_lower'] and
              lower_wick > wick_atr_multiplier * atr and
              rsi <= rsi_oversold and
              current['close'] > current['bb_lower']):
            signals.append({'Date': date, 'Signal': 'BUY', 'Price': price})
            logger.info(f"BUY signal on {date} at price {price}.")
    logger.info(f'Signals detected without model: {len(signals)}.')
    return pd.DataFrame(signals)

# Function to perform backtesting
def backtest_strategy(df, signals):
    initial_capital = 10000
    capital = initial_capital
    position = 0  # 1 for long, -1 for short, 0 for no position
    entry_price = 0
    trade_log = []
    returns = []
    capital_history = [capital]
    dates = [df.index[0]]

    for index, signal in signals.iterrows():
        date = signal['Date']
        price = signal['Price']
        signal_type = signal['Signal']

        if signal_type == 'BUY':
            if position == 0:
                position = 1
                entry_price = price
                trade_log.append(f"{date} - BUY at {price}")
                logger.info(f"BUY signal on {date} at price {price}.")
            elif position == -1:
                # Close short position
                profit = entry_price - price
                capital += profit
                returns.append(profit / entry_price)
                trade_log.append(f"{date} - CLOSE SHORT at {price} - Profit: {profit}")
                logger.info(f"CLOSE SHORT on {date} at price {price} - Profit: {profit}")
                position = 0
            # Update capital history
            capital_history.append(capital)
            dates.append(date)

        elif signal_type == 'SELL':
            if position == 0:
                position = -1
                entry_price = price
                trade_log.append(f"{date} - SELL at {price}")
                logger.info(f"SELL signal on {date} at price {price}.")
            elif position == 1:
                # Close long position
                profit = price - entry_price
                capital += profit
                returns.append(profit / entry_price)
                trade_log.append(f"{date} - CLOSE LONG at {price} - Profit: {profit}")
                logger.info(f"CLOSE LONG on {date} at price {price} - Profit: {profit}")
                position = 0
            # Update capital history
            capital_history.append(capital)
            dates.append(date)

    # Close any open positions at the end
    if position != 0:
        current_price = df['close'].iloc[-1]
        date = df.index[-1]
        if position == 1:
            profit = current_price - entry_price
            capital += profit
            returns.append(profit / entry_price)
            trade_log.append(f"{date} - CLOSE LONG at {current_price} - Profit: {profit}")
            logger.info(f"End of Data - CLOSE LONG at {current_price} - Profit: {profit}")
        elif position == -1:
            profit = entry_price - current_price
            capital += profit
            returns.append(profit / entry_price)
            trade_log.append(f"{date} - CLOSE SHORT at {current_price} - Profit: {profit}")
            logger.info(f"End of Data - CLOSE SHORT at {current_price} - Profit: {profit}")
        position = 0
        # Update capital history
        capital_history.append(capital)
        dates.append(date)

    total_return = (capital - initial_capital) / initial_capital * 100
    logger.info(f"Backtesting completed. Total Return: {total_return:.2f}%")
    # Create a DataFrame for capital history
    capital_history_df = pd.DataFrame({'Date': dates, 'Capital': capital_history}).set_index('Date')
    return total_return, returns, trade_log, capital_history_df

# Calculate maximum drawdown
def max_drawdown(capital_history):
    peak = capital_history['Capital'].cummax()
    drawdown = (capital_history['Capital'] - peak) / peak
    max_dd = drawdown.min()
    logger.info(f"Maximum Drawdown calculated: {max_dd}")
    return max_dd

# Sharpe ratio
def sharpe_ratio(returns, risk_free_rate=0):
    mean_return = np.mean(returns)
    std_return = np.std(returns)
    if std_return == 0:
        return 0
    sharpe = (mean_return - risk_free_rate) / std_return * np.sqrt(252)
    logger.info(f"Sharpe Ratio calculated: {sharpe}")
    return sharpe

# Sortino ratio
def sortino_ratio(returns, risk_free_rate=0):
    mean_return = np.mean(returns)
    negative_returns = [r for r in returns if r < 0]
    std_negative = np.std(negative_returns)
    if std_negative == 0:
        return 0
    sortino = (mean_return - risk_free_rate) / std_negative * np.sqrt(252)
    logger.info(f"Sortino Ratio calculated: {sortino}")
    return sortino

# Main execution
if __name__ == "__main__":
    account_balance = 10000
    symbols = ['BTCUSDT']  # Testing with one symbol
    total_returns = []
    all_trade_logs = []
    capital_histories = []

    for symbol in symbols:
        logger.info(f"Starting backtest for {symbol}")
        df = get_historical_data(symbol, Client.KLINE_INTERVAL_5MINUTE, days=180)
        df = prepare_features(df)
        features_df = prepare_model_features(df)

        # Output number of features
        logger.info(f"Features DataFrame shape: {features_df.shape}")
        logger.info(f"First few rows of features_df:\n{features_df.head()}")

        # Ensure that the features align with the model's expectations
        try:
            # Make predictions with the model
            model_predictions = model.predict(features_df)
            logger.info(f"Model predictions generated for {symbol}.")
            # Analyze model prediction distribution
            unique, counts = np.unique(model_predictions, return_counts=True)
            prediction_distribution = dict(zip(unique, counts))
            logger.info(f"Model prediction distribution: {prediction_distribution}")
        except ValueError as e:
            logger.error(f"Error during model prediction: {e}")
            logger.error("Check that the features provided match the model's expected input.")
            break  # Exit the loop or handle the error as needed

        # Proceed only if predictions were successful
        if 'model_predictions' in locals():
            # Detect reversal signals with model predictions
            signals = detect_reversal_signals(df, model_predictions)

            # If no signals are detected, test without model predictions
            if signals.empty:
                logger.info("No signals detected with model predictions. Testing without model predictions.")
                signals = detect_reversal_signals_without_model(df)

            # Backtest the strategy
            if not signals.empty:
                total_return, returns, trade_log, capital_history = backtest_strategy(df, signals)
                total_returns.extend(returns)
                all_trade_logs.extend(trade_log)
                capital_histories.append(capital_history)
                logger.info(f"Total Return for {symbol}: {total_return:.2f}%")
            else:
                logger.info("No signals detected even without model predictions. Skipping backtesting for this symbol.")

    # If backtesting was successful, calculate performance metrics
    if capital_histories:
        # Combine capital histories
        combined_capital_history = pd.concat(capital_histories)
        combined_capital_history.sort_index(inplace=True)
        combined_capital_history['Capital'] = combined_capital_history['Capital'].cummax()

        # Calculate performance metrics
        max_dd = max_drawdown(combined_capital_history)
        sharpe = sharpe_ratio(total_returns)
        sortino = sortino_ratio(total_returns)

        logger.info(f"Overall Max Drawdown: {max_dd}")
        logger.info(f"Overall Sharpe Ratio: {sharpe}")
        logger.info(f"Overall Sortino Ratio: {sortino}")

        # Output the results
        for log_entry in all_trade_logs:
            print(log_entry)
        print(f"Overall Total Return: {(combined_capital_history['Capital'].iloc[-1] - account_balance) / account_balance * 100:.2f}%")
        print(f"Overall Max Drawdown: {max_dd}")
        print(f"Overall Sharpe Ratio: {sharpe}")
        print(f"Overall Sortino Ratio: {sortino}")
    else:
        logger.error("Backtesting was not completed due to errors or no signals detected.")
