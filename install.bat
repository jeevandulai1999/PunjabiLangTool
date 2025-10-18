@echo off
echo ========================================
echo Punjabi Language Learning Tool
echo Installation Script (Windows)
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.9 or higher from https://www.python.org/
    pause
    exit /b 1
)

echo Python found:
python --version
echo.

REM Create virtual environment if it doesn't exist
if not exist ".venv" (
    echo [1/4] Creating virtual environment (.venv)...
    python -m venv .venv
    if errorlevel 1 (
        echo Error: Failed to create virtual environment
        pause
        exit /b 1
    )
    echo ✓ Virtual environment created
) else (
    echo [1/4] Virtual environment (.venv) already exists
)

REM Activate virtual environment
echo.
echo [2/4] Activating virtual environment...
call .venv\Scripts\activate.bat

echo.
echo [3/4] Installing dependencies...
echo This may take a few minutes...
echo.

python -m pip install --upgrade pip
pip install -r requirements.txt

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ✓ Dependencies installed successfully
    
    echo.
    echo [4/4] Checking for .env file...
    if not exist ".env" (
        echo .env file not found. Creating from template...
        copy env.example .env
        echo ✓ .env file created
        echo.
        echo ⚠️  IMPORTANT: Edit .env file and add your OpenAI API key!
        echo    Get your API key from: https://platform.openai.com/api-keys
    ) else (
        echo ✓ .env file already exists
    )
    
    echo.
    echo ========================================
    echo ✓ Installation Complete!
    echo ========================================
    echo.
    echo Next steps:
    echo 1. Edit .env and add your OpenAI API key
    echo 2. Run: python run.py
    echo 3. Open: http://localhost:8000
    echo.
    echo ========================================
    echo Future usage:
    echo ========================================
    echo To activate virtual environment:
    echo    .venv\Scripts\activate
    echo.
    echo To run the app:
    echo    python run.py
    echo ========================================
    
) else (
    echo.
    echo ========================================
    echo ✗ Installation failed!
    echo ========================================
    echo Please check your internet connection and try again.
    echo.
)

echo.
pause

