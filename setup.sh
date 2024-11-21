#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Set up Python virtual environment
python3 -m venv env
source env/bin/activate

# Upgrade pip, setuptools, and wheel to avoid build issues
pip install --upgrade pip setuptools wheel

# Install required Python packages
pip install playsound pyobjc python-dotenv selenium webdriver-manager datetime requests

echo "Environment setup complete!"
