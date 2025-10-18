@echo off
echo ========================================
echo Punjabi Language Learning Tool
echo Installation Script
echo ========================================
echo.

REM Check if virtual environment exists
if exist ".venv\Scripts\activate.bat" (
    echo [1/3] Virtual environment found
    call .venv\Scripts\activate.bat
) else (
    echo [1/3] No virtual environment found, using global Python
)

echo.
echo [2/3] Installing dependencies...
echo This may take a few minutes...
echo.

pip install -r requirements.txt

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo ✓ Installation successful!
    echo ========================================
    echo.
    echo [3/3] Verifying installation...
    python -c "import fastapi; print('✓ FastAPI installed')" 2>nul && echo ✓ FastAPI verified || echo ✗ FastAPI not found
    python -c "import openai; print('✓ OpenAI installed')" 2>nul && echo ✓ OpenAI verified || echo ✗ OpenAI not found  
    python -c "import uvicorn; print('✓ Uvicorn installed')" 2>nul && echo ✓ Uvicorn verified || echo ✗ Uvicorn not found
    
    echo.
    echo ========================================
    echo Next steps:
    echo ========================================
    echo 1. Create .env file: copy env.example .env
    echo 2. Edit .env and add your OpenAI API key
    echo 3. Run: python run.py
    echo 4. Open: http://localhost:8000
    echo ========================================
    
) else (
    echo.
    echo ========================================
    echo ✗ Installation failed!
    echo ========================================
    echo Please check your internet connection and try again.
)

echo.
pause

