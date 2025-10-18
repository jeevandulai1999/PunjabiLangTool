#!/bin/bash

echo "========================================"
echo "Punjabi Language Learning Tool"
echo "Installation Script"
echo "========================================"
echo ""

# Check if virtual environment exists
if [ -f ".venv/bin/activate" ]; then
    echo "[1/3] Virtual environment found"
    source .venv/bin/activate
else
    echo "[1/3] No virtual environment found, using global Python"
fi

echo ""
echo "[2/3] Installing dependencies..."
echo "This may take a few minutes..."
echo ""

pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo ""
    echo "========================================"
    echo "✓ Installation successful!"
    echo "========================================"
    echo ""
    echo "[3/3] Verifying installation..."
    python -c "import fastapi" 2>/dev/null && echo "✓ FastAPI verified" || echo "✗ FastAPI not found"
    python -c "import openai" 2>/dev/null && echo "✓ OpenAI verified" || echo "✗ OpenAI not found"
    python -c "import uvicorn" 2>/dev/null && echo "✓ Uvicorn verified" || echo "✗ Uvicorn not found"
    
    echo ""
    echo "========================================"
    echo "Next steps:"
    echo "========================================"
    echo "1. Create .env file: cp env.example .env"
    echo "2. Edit .env and add your OpenAI API key"
    echo "3. Run: python run.py"
    echo "4. Open: http://localhost:8000"
    echo "========================================"
    
else
    echo ""
    echo "========================================"
    echo "✗ Installation failed!"
    echo "========================================"
    echo "Please check your internet connection and try again."
fi

echo ""

