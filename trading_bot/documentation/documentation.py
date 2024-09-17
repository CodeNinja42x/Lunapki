def generate_documentation():
    with open('documentation.txt', 'w') as f:
        f.write("Trading Bot Project Documentation\n")
        f.write("Feature Engineering: Adds technical indicators like Bollinger Bands and MACD\n")
        f.write("Hyperparameter Tuning: Uses Optuna to optimize model parameters\n")
        f.write("Cross-Validation: Evaluates the model using k-fold CV\n")
        f.write("Backtesting: Simulates strategy returns on historical data\n")
        f.write("Performance Metrics: Sharpe Ratio, Max Drawdown, and Sortino Ratio\n")

if __name__ == "__main__":
    generate_documentation()
    print("Documentation generated.")
