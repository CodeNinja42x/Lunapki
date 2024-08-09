import pandas as pd

def load_data(file_path):
    """Load raw data from the specified file path."""
    return pd.read_csv(file_path)

def clean_data(df):
    """Perform basic data cleaning tasks."""
    # Example cleaning steps
    df = df.dropna()  # Drop missing values
    df = df[df['column_name'] > 0]  # Filter based on a condition
    return df

def save_processed_data(df, file_path):
    """Save the cleaned data to the specified file path."""
    df.to_csv(file_path, index=False)

if __name__ == "__main__":
    raw_data_path = '../data/raw_data/your_raw_data.csv'
    processed_data_path = '../data/processed_data/your_processed_data.csv'

    data = load_data(raw_data_path)
    cleaned_data = clean_data(data)
    save_processed_data(cleaned_data, processed_data_path)
