from imblearn.over_sampling import SMOTE
import pandas as pd

# Load data
data = pd.read_csv('data/processed_data/your_processed_data.csv')
X = data.drop('target_column', axis=1)
y = data['target_column']

# Apply SMOTE
smote = SMOTE(sampling_strategy='minority')
X_res, y_res = smote.fit_resample(X, y)

# Save the augmented data
augmented_data = pd.concat([X_res, y_res], axis=1)
augmented_data.to_csv('data/processed_data/augmented_data.csv', index=False)
