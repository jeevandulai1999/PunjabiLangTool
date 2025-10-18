# Troubleshooting Guide

## Common Issues and Solutions

### Issue: "Failed to process your speech"

**Symptoms**: 
- You can start a scenario and hear the AI greeting
- When you hold to speak and release, you get an error
- Terminal shows `500 Internal Server Error`

**Possible Causes**:

#### 1. OpenAI API Key Issues

**Check if your API key is valid:**
```powershell
# Verify .env file exists and has your key
type .env
```

Your `.env` should look like:
```
OPENAI_API_KEY=sk-proj-xxxxx... (starts with sk-)
```

**Test the API key:**
```powershell
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('API Key loaded:', os.getenv('OPENAI_API_KEY')[:20] + '...')"
```

**Common API key errors:**
- Key is invalid or expired
- No credits available on your OpenAI account
- Rate limit exceeded

**Solution**: 
- Check your OpenAI dashboard: https://platform.openai.com/account/api-keys
- Verify you have credits: https://platform.openai.com/account/billing
- Try a new API key if needed

#### 2. Audio Format Issues

**Check browser console** (F12 → Console tab):
Look for messages like:
```
Sending audio: 45.23 KB, type: audio/webm, extension: webm
```

**Supported formats**: Whisper API accepts webm, mp3, mp4, mpeg, mpga, m4a, wav, ogg

**Solution**: The code has been updated to use the browser's native audio format.

#### 3. Microphone Recording Issues

**Check if audio is actually being recorded:**
- Browser console should show audio size > 0 KB
- Recording should last more than 0.5 seconds

**Solution**:
- Speak for at least 1-2 seconds
- Ensure microphone is not muted
- Try a different browser (Chrome/Edge recommended)

#### 4. Network/Connection Issues

**Check terminal output for**:
```
ERROR in ASR: [specific error message]
```

**Common errors:**
- Connection timeout
- Network unreachable
- SSL errors

**Solution**:
- Check internet connection
- Try disabling VPN if using one
- Check firewall settings

---

### Issue: Dependencies not installed

**Symptoms**:
- `python run.py` exits immediately
- No error message or silent failure

**Solution**:
```powershell
pip install -r requirements.txt
```

---

### Issue: Port 8000 already in use

**Symptoms**:
```
ERROR: [Errno 48] Address already in use
```

**Solution**:
```powershell
# Use a different port
uvicorn backend.api.main:app --host 0.0.0.0 --port 8080

# Or find and kill the process using port 8000
netstat -ano | findstr :8000
taskkill /PID <process_id> /F
```

---

### Issue: Module not found errors

**Symptoms**:
```
ModuleNotFoundError: No module named 'fastapi'
```

**Solution**:
```powershell
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Verify installation
pip list | findstr fastapi
```

---

### Issue: Server starts but browser shows connection refused

**Symptoms**:
- Terminal shows "Uvicorn running on http://0.0.0.0:8000"
- Browser can't connect to localhost:8000

**Solution**:
```powershell
# Try explicit localhost
# Run server with:
uvicorn backend.api.main:app --host 127.0.0.1 --port 8000

# Then open: http://127.0.0.1:8000
```

---

### Issue: Audio playback not working

**Symptoms**:
- AI greeting doesn't play
- Audio files are generated but silent

**Solution**:
1. Check browser audio is not muted
2. Check system volume
3. Check browser console for audio errors
4. Try a different browser

---

## Debugging Steps

### Step 1: Check Server Logs

When an error occurs, check the terminal for detailed error messages:
```
ERROR in process_turn: [error details]
```

### Step 2: Check Browser Console

Press F12, go to Console tab, look for:
- Red error messages
- Network errors
- JavaScript errors

### Step 3: Check Browser Network Tab

Press F12, go to Network tab, click on failed request, check:
- Request payload (audio file size)
- Response (error message)
- Status code

### Step 4: Test Components Individually

**Test OpenAI connection:**
```powershell
python -c "from backend.services.openai_client import get_openai_client; client = get_openai_client(); print('✓ OpenAI client initialized')"
```

**Test imports:**
```powershell
python -c "from backend.api.main import app; print('✓ App imports successfully')"
```

---

## Getting More Debug Information

### Enable Verbose Logging

Edit `run.py` and change log level:
```python
uvicorn.run(
    "backend.api.main:app",
    host=os.getenv("HOST", "0.0.0.0"),
    port=int(os.getenv("PORT", 8000)),
    reload=os.getenv("DEBUG", "true").lower() == "true",
    log_level="debug"  # Add this line
)
```

### Check Audio File

If audio files are being created, check them:
```powershell
dir frontend\static\audio\*.mp3
```

Listen to the generated audio files to verify TTS is working.

---

## Still Not Working?

### Collect Information

1. **Python version**: `python --version`
2. **Package versions**: `pip list`
3. **OpenAI library**: `pip show openai`
4. **Terminal error output** (full traceback)
5. **Browser console errors** (screenshot)
6. **Network tab details** (failed request)

### Check These Files

- `.env` - Has valid API key
- `requirements.txt` - All packages listed
- `frontend/static/audio/` - Directory exists and is writable

### Try Fresh Install

```powershell
# Deactivate and remove venv
deactivate
rmdir /s .venv

# Create new venv
python -m venv .venv
.venv\Scripts\activate

# Reinstall
pip install -r requirements.txt

# Run
python run.py
```

---

## OpenAI API Errors

### Error: "Invalid API key"
- Double-check your API key in `.env`
- Ensure no extra spaces or quotes
- Try generating a new key

### Error: "You exceeded your current quota"
- Add credits to your OpenAI account
- Check usage at: https://platform.openai.com/usage

### Error: "Rate limit exceeded"
- Wait a few minutes and try again
- Upgrade your OpenAI plan for higher limits

### Error: "Model not found"
- Ensure you have access to GPT-4 models
- Try using `gpt-3.5-turbo` instead (edit service files)

---

## Browser-Specific Issues

### Chrome/Edge
- Usually works best
- Check microphone permissions in Settings

### Firefox
- May use different audio codec
- Check: `about:config` → `media.recorder.audio.enabled`

### Safari
- Limited MediaRecorder support
- Use Chrome/Edge instead for best results

---

## Need More Help?

1. Check the full error in terminal (scroll up)
2. Check browser console (F12)
3. Enable debug logging (see above)
4. Verify all prerequisites are met
5. Try the troubleshooting steps in order

The debug output added to the code will show:
- Exact audio format being sent
- Where in the pipeline it's failing
- Full error tracebacks

