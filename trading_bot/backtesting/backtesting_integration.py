def backtest_model(model_file, X_test_file, y_test_file):
    # Load test data and model
    X_test = pd.read_csv(X_test_file)
    y_test = pd.read_csv(y_test_file)
    model = joblib.load(model_file)

    # Run backtesting
    predictions = model.predict(X_test)

    # Evaluate performance
    accuracy = sum(predictions == y_test) / len(y_test)
    print(f"Backtesting Accuracy: {accuracy * 100:.2f}%")
    return accuracy

# Backtest model
backtest_model('ensemble_model.pkl', 'X_test.csv', 'y_test.csv')
