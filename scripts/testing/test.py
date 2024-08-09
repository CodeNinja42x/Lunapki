import pandas as pd

# Load your data
data_path = '/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/latest_data.csv'
data = pd.read_csv(data_path)

# Display the first few rows of the dataframe
print(data.head())
