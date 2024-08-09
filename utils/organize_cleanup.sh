#!/bin/bash

echo "Moving model files to the models directory..."
mv *.pkl models/ 2>/dev/null

echo "Moving log files to the logs directory..."
mv *.log logs/ 2>/dev/null

echo "Moving data files to the data directory..."
mv *.csv data/ 2>/dev/null

echo "Cleaning up temporary files..."
rm -f data/temp*.csv

echo "Moving scripts to the scripts directory..."
mv *.py scripts/ 2>/dev/null

echo "Cleanup and organization complete!"
