#!/bin/bash

# Ensure virtual environment is activated
if [ ! -d "venv" ]; then
    echo "Error: Virtual environment not found. Please run ./install.sh first."
    exit 1
fi

source venv/bin/activate

# Execute the application
python3 src/main.py "$@"
