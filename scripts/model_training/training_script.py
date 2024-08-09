import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler

# Load your latest data
data = pd.read_csv('/path/to/your/latest_data.csv')

# Preprocess the data
# Assuming 'target' is your label column
X = data.drop(columns=['target'])
y = data['target']
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train the model
model = RandomForestClassifier(n_estimators=100)
model.fit(X_scaled, y)

# Save the model and scaler
joblib.dump(model, '/path/to/your/model.pkl')
joblib.dump(scaler, '/path/to/your/scaler.pkl')
