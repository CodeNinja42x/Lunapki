import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import SelectFromModel

# Load data
data_path = '/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/data/features.csv'
data = pd.read_csv(data_path, index_col=0)

# Define features and target
X = data.drop(columns=['target'])
y = data['target']

# Feature selection using RandomForest
selector = RandomForestClassifier(n_estimators=100, random_state=42)
selector.fit(X, y)

# Select features with importance greater than a threshold
sfm = SelectFromModel(selector, threshold=0.01)
sfm.fit(X, y)

# Transform the data to retain selected features
X_transformed = sfm.transform(X)
selected_features = X.columns[sfm.get_support()]

# Create a new DataFrame with selected features
data_selected = pd.DataFrame(X_transformed, columns=selected_features)
data_selected['target'] = y

# Save the selected features to a new CSV
selected_features_path = '/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/data/selected_features.csv'
data_selected.to_csv(selected_features_path, index=True)

print("Selected features saved successfully.")
