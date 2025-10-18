# Quick Start Guide 🚀

Get up and running with the Punjabi Language Learning Tool in 5 minutes!

## Prerequisites

- Python 3.9+
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

## Setup (5 steps)

### 1. Activate Virtual Environment (if using one)

```bash
# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate
```

You should see `(.venv)` or similar in your prompt.

### 2. Install Dependencies ⚠️ IMPORTANT!

```bash
pip install -r requirements.txt
```

**This step is required!** The application won't run without these packages.

To verify installation:
```bash
pip list | grep fastapi   # macOS/Linux
pip list | findstr fastapi  # Windows
```

### 3. Configure API Key

Create a `.env` file:

```bash
# Windows
copy env.example .env

# macOS/Linux
cp env.example .env
```

Edit `.env` and add your API key:

```env
OPENAI_API_KEY=sk-your-actual-key-here
```

### 4. Run the Application

```bash
python run.py
```

Or:

```bash
uvicorn backend.api.main:app --reload --host 0.0.0.0 --port 8000
```

### 5. Open in Browser

Navigate to: http://localhost:8000

### 6. Allow Microphone Access

When prompted, click "Allow" to enable microphone for speech recording.

## First Conversation

1. Click on **"Shopping at the Market"** scenario
2. Listen to the AI greeting in Punjabi
3. **Hold down** the "Hold to Speak" button
4. Speak in Punjabi (even simple phrases!)
5. Release the button
6. See your speech transcribed in 3 formats
7. Listen to the AI's response

## Need Help?

- Click **"Help Mode"** during conversation
- Ask questions about grammar, vocabulary, or culture
- Get instant explanations with examples

## Running Tests

```bash
# Run all tests (fast, no API calls)
pytest

# Run specific test
pytest tests/test_transliteration.py

# See detailed output
pytest -v
```

## Troubleshooting

### "Module not found" Error
```bash
pip install -r requirements.txt --upgrade
```

### Microphone Not Working
- Check browser permissions
- Use Chrome or Edge (best compatibility)
- Ensure system microphone is enabled

### API Key Error
- Verify your key starts with `sk-`
- Check `.env` file is in the project root
- Ensure you have API credits

## Cost Estimate

- ~$0.10-0.20 per 10-minute session
- Whisper ASR: $0.006/minute
- GPT-4-mini: Very cost-effective
- TTS: $15/1M characters

## Next Steps

- Try the **"School Pickup"** scenario
- Create a **custom scenario** with your own prompt
- End session to see your **progress metrics**
- Rate your confidence to track improvement

## Tips for Best Experience

✅ **Do:**
- Speak clearly and at normal pace
- Use short, conversational phrases
- Hold the button while speaking
- Try the Help Mode to learn

❌ **Don't:**
- Speak too fast or too quietly
- Use very long sentences
- Expect perfect transcription (ASR has limits)
- Worry about mistakes - keep practicing!

---

**Need more details?** Check out the full [README.md](README.md)

**Having issues?** See the troubleshooting section in README.md

Happy learning! 🎉 ਸ਼ੁਭ ਕਾਮਨਾਵਾਂ!

