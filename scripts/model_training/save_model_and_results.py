from trading_bot_library import save_model

# Assuming grid_search is your trained model object
try:
    save_model(grid_search, '/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/models/grid_search_model.pkl')
    print("grid_search_model.pkl saved successfully.")
except Exception as e:
    print(f"Error saving grid_search_model.pkl: {e}")

# Assuming best_model is another trained model object
try:
    save_model(best_model, '/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/models/best_model.pkl')
    print("best_model.pkl saved successfully.")
except Exception as e:
    print(f"Error saving best_model.pkl: {e}")
