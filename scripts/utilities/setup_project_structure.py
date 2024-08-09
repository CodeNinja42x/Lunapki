import os

# Define the folder structure
folders = {
    'scripts': ['preprocess_data.py', 'train_model.py', 'backtest.py'],
    'data': [],
    'models': [],
    'logs': [],
    'output': [],
    'notebooks': []
}

# Create folders and files
for folder, files in folders.items():
    folder_path = os.path.join(os.getcwd(), folder)
    
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f'Created directory: {folder_path}')
    else:
        print(f'Directory already exists: {folder_path}')
    
    for file in files:
        file_path = os.path.join(folder_path, file)
        if not os.path.exists(file_path):
            with open(file_path, 'w') as f:
                f.write(f'# Placeholder for {file}')
            print(f'Created file: {file_path}')
        else:
            print(f'File already exists: {file_path}')

print("Project structure setup is complete.")
