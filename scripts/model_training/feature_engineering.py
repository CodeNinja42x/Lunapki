import pandas as pd

# Load your dataset
data_path = '/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/data/your_dataset.csv'
df = pd.read_csv(data_path)

# Check for missing columns
required_columns = ['Date', 'Close', 'High', 'Low']
missing_columns = [col for col in required_columns if col not in df.columns]

if missing_columns:
    print(f"Missing columns in the dataset: {missing_columns}")
    # Handle missing columns as needed (e.g., exit or fill with default values)
else:
    # Proceed with feature engineering
    # ... (Your feature engineering code here)
    
    # Save the enhanced dataset
    enhanced_data_path = '/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/data/enhanced_data_v2.csv'
    df.to_csv(enhanced_data_path, index=False)
    print(f"Feature engineering completed. Enhanced dataset saved to {enhanced_data_path}")
