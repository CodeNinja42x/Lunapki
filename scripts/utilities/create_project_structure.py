import os

# Define the project structure
directories = [
    "data",
    "notebooks",
    "scripts",
    "models",
    "output",
    "logs"
]

# Create the directories
for directory in directories:
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Created directory: {directory}")
    else:
        print(f"Directory already exists: {directory}")

# Create placeholder files
placeholder_files = {
    "data": "data/.keep",
    "notebooks": "notebooks/.keep",
    "scripts": "scripts/.keep",
    "models": "models/.keep",
    "output": "output/.keep",
    "logs": "logs/.keep"
}

for directory, filepath in placeholder_files.items():
    with open(filepath, 'w') as f:
        f.write('')
        print(f"Created placeholder file in: {directory}")

