#!/bin/bash

echo "Verifying setup..."
# Check for necessary files
ls models/ | grep "trained_model.pkl"
ls data/ | grep "actual_values.csv"
ls data/ | grep "predictions.csv"

# Check installed packages
pip list | grep -E "numpy|joblib|scikit-learn"

# Clean up unnecessary files
rm -f data/temp*.csv

# Verify scripts
python /Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/scripts2/feature_engineering.py
python /Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/scripts2/data_preprocessing.py
python /Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/scripts2/model_prediction.py
python /Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/scripts2/model_evaluation.py

echo "Setup verification complete!"
