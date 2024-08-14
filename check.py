import pandas as pd

# Load the processed data
data = pd.read_csv('data/processed_data/processed_data.csv')

# Print the column names
print(data.columns)
