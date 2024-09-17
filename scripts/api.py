import ccxt

# Use the provided Testnet API keys
api_key = 'h8nxVXfe6U1Ong2JRMNATRsWlCvUzfx31ILW4FejuDUJpHQjJ5Fqi15BEzKJIOpU'
secret_key = 'hIMHB0X2SNTnjKN33o8Powpj0mX5t2w6mLudfF1oIEnTMznFOUARU0VYFJsB5yah'

# Initialize Binance Testnet for Futures
binance_testnet = ccxt.binance({
    'apiKey': api_key,
    'secret': secret_key,
    'enableRateLimit': True,
})

# Enable Testnet/Sandbox mode
binance_testnet.set_sandbox_mode(True)

# Fetch and print account balance from testnet
balance = binance_testnet.fetch_balance()
print(balance)
