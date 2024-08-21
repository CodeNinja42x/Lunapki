import pandas as pd

# Creating placeholder datasets
X_train = pd.DataFrame({
    'feature1': [1, 2, 3, 4, 5],
    'feature2': [6, 7, 8, 9, 10]
})
y_train = pd.DataFrame({
    'target': [0, 1, 0, 1, 0]
})
X_test = pd.DataFrame({
    'feature1': [11, 12, 13],
    'feature2': [14, 15, 16]
})
y_test = pd.DataFrame({
    'target': [1, 0, 1]
})

# Saving to CSV
X_train.to_csv('/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/data/X_train.csv', index=False)
y_train.to_csv('/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/data/y_train.csv', index=False)
X_test.to_csv('/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/data/X_test.csv', index=False)
y_test.to_csv('/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/data/y_test.csv', index=False)

print("Placeholder datasets created and saved.")
