#!/bin/bash

echo "Starting build process..."

# Activate virtual environment
echo "Activating virtual environment..."
source /Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/venv/bin/activate

# Navigate to script directory
echo "Navigating to script directory..."
cd /Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/scripts2

# Install dependencies
echo "Installing dependencies..."
pip install -r ../requirements.txt

# Run tests
echo "Running tests..."
pytest ../tests

# Package the application
echo "Packaging the application..."
cd ..
tar -czvf lunapki_build.tar.gz scripts2

echo "Build completed successfully."

