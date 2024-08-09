import os
import shutil

# Define the current and new project paths
current_base_path = "/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki"
new_base_path = "/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot"

# Define the directory structure to be created
project_structure = {
    "Bot": ["model.py", "bot.py", "data_preprocessing.py"],
    "Bot_Logs/logs": ["data_preprocessing.log", "model.log", "trading_bot.log"],
    "Bot_Logs/fetches": ["preprocessed_data.csv", "fetched_data.csv"],
    "models": [
        "AdaBoost_model.pkl", "CatBoost_model.pkl", "ensemble_model.pkl",
        "GradientBoosting_model.pkl", "LightGBM_model.pkl", "LogisticRegression_model.pkl",
        "model.pkl", "RandomForest_model.pkl", "scaler.pkl", "XGBoost_model.pkl"
    ],
    "scripts": [
        "config.py", "data_preprocessing.py", "generate_sample_data.py",
        "test_binance_api.py", "train_model.py", "visualize_metrics.py"
    ],
    "venv": [],
    "": [".gitattributes", ".gitignore", "LICENSE", "reorganize_project.sh", "requirements.txt"]
}

# Function to create the new directory structure
def create_directory_structure(base_path, structure):
    for folder, files in structure.items():
        folder_path = os.path.join(base_path, folder)
        os.makedirs(folder_path, exist_ok=True)
        for file in files:
            if file:  # Ensure it's not an empty string (for directories without specific files listed)
                src_file = os.path.join(current_base_path, file)
                dest_file = os.path.join(folder_path, file)
                if os.path.exists(src_file):
                    shutil.move(src_file, dest_file)
                    print(f"Moved {src_file} to {dest_file}")

if __name__ == "__main__":
    # Create the new project structure and move files
    create_directory_structure(new_base_path, project_structure)
    print("Project reorganization completed successfully.")
