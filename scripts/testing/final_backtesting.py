from trading_bot_library import load_model, backtest_model

# Load the best model with error handling
try:
    best_model = load_model('/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/models/best_model.pkl')
    print("best_model.pkl loaded successfully.")
except EOFError:
    print("EOFError: best_model.pkl might be empty or corrupted.")
except FileNotFoundError:
    print("FileNotFoundError: best_model.pkl does not exist.")
except Exception as e:
    print(f"An error occurred while loading best_model.pkl: {e}")

# Proceed with backtesting if the model loaded successfully
if 'best_model' in locals():
    try:
        backtest_model(best_model)
        print("Backtesting completed successfully.")
    except Exception as e:
        print(f"An error occurred during backtesting: {e}")
