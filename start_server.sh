#!/bin/bash

# Check for existing process on port 5001
PID=$(lsof -t -i:5001)
if [ -n "$PID" ]; then
  echo "Killing existing process on port 5001 with PID $PID"
  kill -9 $PID
fi

# Check for existing virtual environment, create if none
if [ ! -d "venv" ]; then
  echo "Creating virtual environment..."
  python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo "Installing requirements..."
pip install -r requirements.txt

# Start the Flask server
flask --app api/index.py run --port 5001