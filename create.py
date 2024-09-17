import pandas as pd
import numpy as np
import random

# Set the seed for reproducibility
np.random.seed(42)

# Generate date range
dates = pd.date_range(start="2023-01-01", end="2024-01-01", freq='D')

# Generate random closing prices
prices = np.random.normal(loc=100, scale=10, size=len(dates))
prices = np.cumsum(prices - prices.mean()) + 100  # to get some trend in the data

# Create a DataFrame
data = pd.DataFrame({
    'Date': dates,
    'Close': prices
})

# Save to CSV
data.to_csv('sample_data.csv', index=False)

print("Sample data created and saved as 'sample_data.csv'.")
