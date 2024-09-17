import pandas as pd

def map_engineered_to_train(engineered_file, output_file):
    engineered_data = pd.read_csv(engineered_file)
    
    # Select only the necessary features for training
    selected_features = ['feature1', 'feature2', 'BB_Upper', 'BB_Middle', 'BB_Lower', 'MACD', 'ATR']  # Adjust based on your needs
    X_train = engineered_data[selected_features]
    
    # Save the mapped training data
    X_train.to_csv(output_file, index=False)
    print(f"X_train with selected features saved to {output_file}")

# Example usage
map_engineered_to_train('engineered_data.csv', 'X_train.csv')
