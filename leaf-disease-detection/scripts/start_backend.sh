#!/bin/bash

# Start Backend API Server

echo "=========================================="
echo "Starting Leaf Disease Detection Backend"
echo "=========================================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Please run setup.sh first"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "❌ .env file not found!"
    echo "Please create .env and add your GROQ_API_KEY"
    exit 1
fi

# Load environment variables
export $(grep -v '^#' .env | xargs)

# Check if GROQ_API_KEY is set
if [ -z "$GROQ_API_KEY" ]; then
    echo "❌ GROQ_API_KEY not set in .env file!"
    echo "Please add your API key to .env"
    exit 1
fi

echo "✅ Environment loaded"
echo "✅ Starting backend on http://localhost:8000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start the server
python main.py
