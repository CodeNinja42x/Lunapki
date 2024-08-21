import yfinance as yf

# Fetch Bitcoin data
btc = yf.Ticker("BTC-USD")
hist = btc.history(period="max")

# Save the fetched data to CSV for further processing
hist.to_csv('/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/data/btc_data.csv')
