#!/bin/bash

echo "========================================"
echo "Punjabi Language Learning Tool"
echo "Installation Script (Linux/macOS)"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    echo "Please install Python 3.9 or higher"
    exit 1
fi

echo "Python found:"
python3 --version
echo ""

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "[1/4] Creating virtual environment (.venv)..."
    python3 -m venv .venv
    if [ $? -ne 0 ]; then
        echo "Error: Failed to create virtual environment"
        exit 1
    fi
    echo "✓ Virtual environment created"
else
    echo "[1/4] Virtual environment (.venv) already exists"
fi

# Activate virtual environment
echo ""
echo "[2/4] Activating virtual environment..."
source .venv/bin/activate

echo ""
echo "[3/4] Installing dependencies..."
echo "This may take a few minutes..."
echo ""

python -m pip install --upgrade pip
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo ""
    echo "✓ Dependencies installed successfully"
    
    echo ""
    echo "[4/4] Checking for .env file..."
    if [ ! -f ".env" ]; then
        echo ".env file not found. Creating from template..."
        cp env.example .env
        echo "✓ .env file created"
        echo ""
        echo "⚠️  IMPORTANT: Edit .env file and add your OpenAI API key!"
        echo "   Get your API key from: https://platform.openai.com/api-keys"
    else
        echo "✓ .env file already exists"
    fi
    
    echo ""
    echo "========================================"
    echo "✓ Installation Complete!"
    echo "========================================"
    echo ""
    echo "Next steps:"
    echo "1. Edit .env and add your OpenAI API key"
    echo "2. Run: python run.py"
    echo "3. Open: http://localhost:8000"
    echo ""
    echo "========================================"
    echo "Future usage:"
    echo "========================================"
    echo "To activate virtual environment:"
    echo "   source .venv/bin/activate"
    echo ""
    echo "To run the app:"
    echo "   python run.py"
    echo "========================================"
    
else
    echo ""
    echo "========================================"
    echo "✗ Installation failed!"
    echo "========================================"
    echo "Please check your internet connection and try again."
    echo ""
fi

echo ""

