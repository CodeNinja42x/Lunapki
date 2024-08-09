#!/bin/bash

echo "Setting up the environment..."
pip uninstall numpy joblib scikit-learn -y
pip install numpy==1.23.5 joblib==1.2.0 scikit-learn==1.2.2

echo "Environment setup complete!"
