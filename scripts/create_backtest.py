import pandas as pd
from datetime import datetime, timedelta

# Create a date range
dates = pd.date_range(end=datetime.today(), periods=100)

# Generate random close prices
data = {
    'Date': dates,
    'Close': pd.Series([100 + x for x in range(len(dates))]) + pd.Series([0.5 - x % 2 for x in range(len(dates))])
}

# Create a DataFrame
df = pd.DataFrame(data)

# Save to CSV
df.to_csv('/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/sample_data.csv', index=False)

print("Sample data created and saved as 'sample_data.csv'.")
