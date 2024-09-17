# Perform test prediction on a sample for each model
def test_model_prediction(model, data):
    try:
        close = data['close'].values
        high = data['high'].values
        low = data['low'].values
        
        # Use only the features that were used during training
        rsi = talib.RSI(close, timeperiod=7)
        ma_short = talib.SMA(close, timeperiod=9)
        ma_long = talib.SMA(close, timeperiod=21)
        macd, signal, _ = talib.MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)

        # Adjust the feature set to match the trained model's input (assuming 4 features were used)
        features = np.column_stack((rsi, ma_short, ma_long, macd))  # Exclude any extra feature like 'signal'

        # Determine if the model is a regressor or classifier
        if hasattr(model, 'predict_proba'):  # Classifier model
            with np.warnings.catch_warnings():
                np.warnings.simplefilter('ignore', UserWarning)
                prediction = model.predict(features[-1:])[0]
                confidence = model.predict_proba(features[-1:])[0][prediction]
                logger.info(f"Model prediction: {prediction}, Confidence: {confidence}")
                return prediction, confidence
        else:  # Regressor model
            with np.warnings.catch_warnings():
                np.warnings.simplefilter('ignore', UserWarning)
                prediction = model.predict(features[-1:])[0]
                logger.info(f"Model regression prediction: {prediction}")
                return prediction, None

    except Exception as e:
        logger.error(f"Error during model prediction: {e}")
        return None, None
