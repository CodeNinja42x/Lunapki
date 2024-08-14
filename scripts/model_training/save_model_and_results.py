from scripts.lib.trading_bot_library import load_model, save_model

grid_search = load_model('/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/models/grid_search_model.pkl')
save_model(grid_search, '/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/models/final_model.pkl')
