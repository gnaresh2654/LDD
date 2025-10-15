#!/bin/bash

# Leaf Disease Detection System - Setup Script
# This script helps you set up the project quickly

set -e  # Exit on error

echo "=========================================="
echo "Leaf Disease Detection System - Setup"
echo "=========================================="
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python version: $python_version"

# Check if Python 3.11+ is available
required_version="3.11"
if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then 
    echo "⚠️  Warning: Python 3.11+ is recommended. You have $python_version"
else
    echo "✅ Python version is compatible"
fi

echo ""

# Create virtual environment
echo "Creating virtual environment..."
if [ -d "venv" ]; then
    echo "Virtual environment already exists. Skipping..."
else
    python3 -m venv venv
    echo "✅ Virtual environment created"
fi

echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo "✅ Virtual environment activated"

echo ""

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
echo "✅ Dependencies installed"

echo ""

# Create necessary directories
echo "Creating necessary directories..."
mkdir -p .streamlit
echo "✅ Directories created"

echo ""

# Setup environment variables
if [ -f ".env" ]; then
    echo ".env file already exists. Skipping..."
else
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "✅ .env file created"
    echo ""
    echo "⚠️  IMPORTANT: Please edit .env and add your GROQ_API_KEY"
    echo "   You can get a free API key from: https://console.groq.com"
fi

echo ""

# Setup Streamlit secrets
if [ -f ".streamlit/secrets.toml" ]; then
    echo "Streamlit secrets file already exists. Skipping..."
else
    echo "Creating Streamlit secrets file..."
    cat > .streamlit/secrets.toml << EOF
# Streamlit Secrets Configuration
API_BASE_URL = "http://localhost:8000"
EOF
    echo "✅ Streamlit secrets file created"
fi

echo ""

# Setup .gitignore
if [ -f ".gitignore" ]; then
    echo ".gitignore already exists. Skipping..."
else
    echo "Creating .gitignore..."
    cat > .gitignore << EOF
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/

# Environment variables
.env
.env.local

# Streamlit
.streamlit/secrets.toml

# IDEs
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Test outputs
test_analysis_result.json
*.log

# Uploads
uploads/
EOF
    echo "✅ .gitignore created"
fi

echo ""
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Edit .env and add your GROQ_API_KEY"
echo "   Get it from: https://console.groq.com"
echo ""
echo "2. Start the backend API:"
echo "   python main.py"
echo ""
echo "3. In a new terminal, start the frontend:"
echo "   streamlit run app.py"
echo ""
echo "4. Open your browser to:"
echo "   http://localhost:8501"
echo ""
echo "5. Test the API (optional):"
echo "   python test_api.py path/to/leaf/image.jpg"
echo ""
echo "=========================================="
echo ""

# Ask if user wants to open editor for .env
read -p "Do you want to edit .env now? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    ${EDITOR:-nano} .env
fi
