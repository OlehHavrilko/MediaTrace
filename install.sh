#!/bin/bash

# Exit on any error
set -e

echo "Setting up MediaTrace..."

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing/Updating dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Setup complete. You can run the application using ./run.sh <url>"
