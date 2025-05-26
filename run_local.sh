#!/bin/bash

echo "Setting up environment for Daily Life Helper API..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python is not installed. Please install Python 3.9 or higher."
    exit 1
fi

# Check if virtual environment exists, create if not
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Run the application
echo "Starting the application..."
echo ""
echo "Access the API at http://localhost:8000"
echo "API documentation is available at http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""
uvicorn app:app --reload

# Deactivate virtual environment on exit
deactivate