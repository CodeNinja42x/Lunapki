import os

# Set the directory you want to start the search from
directory = "/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot"

# Walk through the directory and its subdirectories
for root, dirs, files in os.walk(directory):
    for file in files:
        if file.endswith(".csv"):
            print(os.path.join(root, file))
