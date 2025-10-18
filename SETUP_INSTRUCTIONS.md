# Setup Instructions - Punjabi Language Learning Tool

## Issue: Dependencies Not Installed

If `python run.py` fails immediately, it's because the dependencies from `requirements.txt` haven't been installed yet.

## Step-by-Step Setup

### 1. Ensure You're in the Virtual Environment

```powershell
# You should see (.venv) in your prompt
# If not, activate it:
.venv\Scripts\activate
```

### 2. Install All Dependencies

```powershell
pip install -r requirements.txt
```

This will install:
- `openai` - OpenAI API client
- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `python-dotenv` - Environment variable management
- `python-multipart` - File upload handling
- `pydub` - Audio processing
- `pydantic` - Data validation
- `aiofiles` - Async file operations
- `pytest` and testing tools

### 3. Verify Installation

```powershell
# Check if FastAPI is installed
python -c "import fastapi; print('FastAPI:', fastapi.__version__)"

# Check if OpenAI is installed
python -c "import openai; print('OpenAI:', openai.__version__)"

# Check if uvicorn is installed
python -c "import uvicorn; print('Uvicorn:', uvicorn.__version__)"
```

### 4. Set Up Environment Variables

Create a `.env` file:

```powershell
copy env.example .env
```

Edit `.env` and add your OpenAI API key:

```
OPENAI_API_KEY=sk-your-actual-api-key-here
DEBUG=true
HOST=0.0.0.0
PORT=8000
```

### 5. Run the Application

**Option A: Using run.py (Recommended)**
```powershell
python run.py
```

**Option B: Using uvicorn directly**
```powershell
uvicorn backend.api.main:app --reload --host 0.0.0.0 --port 8000
```

**Option C: No reload mode (if reload causes issues)**
```powershell
uvicorn backend.api.main:app --host 0.0.0.0 --port 8000
```

### 6. Open in Browser

Navigate to: http://localhost:8000

### 7. Allow Microphone Access

When prompted, click "Allow" to enable microphone for speech recording.

## Troubleshooting

### Problem: "Module not found" errors

**Solution**: Install dependencies
```powershell
pip install -r requirements.txt
```

### Problem: uvicorn dies immediately with reload warning

**Cause**: When passing an app object instead of an import string to uvicorn with reload=True

**Solution**: The `run.py` has been fixed to use import string. If still failing, try without reload:
```powershell
uvicorn backend.api.main:app --host 0.0.0.0 --port 8000
```

### Problem: Can't import backend modules

**Solution**: Make sure you're in the project root directory:
```powershell
cd E:\Code\PunjabiLangTool\PunjabiLangTool
```

### Problem: ".env file not found" warning

**Solution**: Create .env file:
```powershell
copy env.example .env
# Then edit .env with your API key
```

### Problem: "OPENAI_API_KEY not set" error

**Solution**: Edit `.env` file and add your actual API key:
```
OPENAI_API_KEY=sk-your-key-starts-with-sk
```

### Problem: Import errors or silent failures

**Solution**: Reinstall with verbose output:
```powershell
pip install --upgrade --force-reinstall -r requirements.txt
```

### Problem: Port 8000 already in use

**Solution**: Use a different port:
```powershell
uvicorn backend.api.main:app --host 0.0.0.0 --port 8080
# Then open http://localhost:8080
```

### Problem: Terminal output suppressed

If pip/python commands show no output, try:
```powershell
python -u run.py  # -u for unbuffered output
```

## Verification Checklist

Before running the app, verify:

- [ ] Virtual environment is activated (see `.venv` in prompt)
- [ ] All packages installed: `pip list | findstr fastapi`
- [ ] `.env` file exists with valid API key
- [ ] In correct directory: `E:\Code\PunjabiLangTool\PunjabiLangTool`
- [ ] OpenAI API key is valid and has credits

## Quick Test

Run this to test all imports:

```powershell
python test_import.py
```

Expected output:
```
Python version: 3.x.x
Starting imports...
1. Importing FastAPI...
   ✓ FastAPI imported
2. Importing backend modules...
   ✓ Models imported
   ✓ Services imported
3. Importing main app...
   ✓ App imported

✅ All imports successful!
App: <fastapi.applications.FastAPI object at 0x...>
```

## Manual Installation (if requirements.txt fails)

Install packages one by one:

```powershell
pip install openai>=1.12.0
pip install python-dotenv>=1.0.0
pip install "fastapi>=0.109.0"
pip install "uvicorn[standard]>=0.27.0"
pip install python-multipart>=0.0.9
pip install pydub>=0.25.1
pip install "pydantic>=2.6.0"
pip install pytest>=8.0.0
pip install pytest-asyncio>=0.23.0
pip install pytest-mock>=3.12.0
pip install httpx>=0.26.0
pip install aiofiles>=23.2.1
```

## Still Not Working?

1. Check if you're using Python 3.9+:
   ```powershell
   python --version
   ```

2. Try creating a fresh virtual environment:
   ```powershell
   python -m venv venv_new
   venv_new\Scripts\activate
   pip install -r requirements.txt
   python run.py
   ```

3. Check the project structure is correct:
   ```powershell
   dir backend\api\main.py
   # Should show the file exists
   ```

4. Try running FastAPI directly:
   ```powershell
   python -m backend.api.main
   ```

## Success Indicators

When working correctly, you should see:

```
✓ Environment configured
✓ Starting Punjabi Language Learning Tool...

🌐 Open your browser to: http://localhost:8000

Press Ctrl+C to stop the server

INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

Then the browser should load the Punjabi Language Learning Tool interface!

---

**Need more help?** Check README.md or QUICKSTART.md

