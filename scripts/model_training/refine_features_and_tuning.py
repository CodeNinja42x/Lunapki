from scripts.lib.trading_bot_library import load_data, refine_and_tune_model

X_train = load_data('/path/to/X_train.csv')
y_train = load_data('/path/to/y_train.csv')

best_model, best_params = refine_and_tune_model(X_train, y_train, n_splits=2)  # Reduced n_splits to 2
print("Best Model:", best_model)
print("Best Parameters:", best_params)
