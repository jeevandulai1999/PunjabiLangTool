# Punjabi Language Learning Tool 🗣️

AI-powered conversational Punjabi practice tool using OpenAI's GPT, Whisper, and TTS technologies.

## ✨ Features

### Core Learning Features
- **Scenario-Based Conversations**: Practice real-world scenarios like shopping at the market or school pickup
- **Custom Scenarios**: Create your own conversation scenarios with AI-generated characters
- **Live Speech Interaction**: Speak in Punjabi and see transcriptions in three formats:
  - Gurmukhi script (ਤੁਸੀਂ ਕਿੱਦਾਂ ਹੋ?)
  - **LLM-Powered Romanisation** (tusi kiddan ho?) - Phonetically accurate, context-aware
  - English translation (How are you?)
- **AI Character Responses**: Natural **Doabi Punjabi** responses with optimized text-to-speech audio
- **Help Mode**: Pause conversations to ask for:
  - Grammar explanations
  - Vocabulary breakdowns
  - Cultural context
  - Alternative phrasings
- **Session Analytics**: Track words per minute, vocabulary breadth, confidence scores

### 🆕 New Features
- **📊 Real-Time API Cost Tracking**: 
  - Live cost display during conversations
  - Per-session usage breakdown (Whisper, GPT, TTS)
  - OpenAI account balance checker
  - Typical session cost: **$0.01-0.02** 💰
  
- **🎤 Optimized TTS (Text-to-Speech)**:
  - **Nova voice** - Warm, natural pronunciation for Punjabi
  - Fast `tts-1` model (2-3x faster than HD)
  - Normal 1.0 speed for natural flow
  - Customizable voices and speeds via environment variables
  
- **⚡ Performance Improvements**:
  - Faster translation with `gpt-3.5-turbo`
  - Context-aware romanisation for accurate pronunciation
  - Improved Doabi dialect consistency
  - 3x faster response times

## Tech Stack

- **Backend**: FastAPI (Python 3.9+)
- **Frontend**: Vanilla HTML, CSS, JavaScript (no frameworks)
- **AI Services**: 
  - OpenAI **GPT-4o-mini** (conversation generation)
  - OpenAI **GPT-3.5-turbo** (translation & romanisation)
  - OpenAI **Whisper** (Punjabi speech-to-text with auto-detection)
  - OpenAI **TTS-1** (fast, high-quality text-to-speech)
- **Testing**: pytest with minimal API usage
- **Utilities**: httpx (API calls), pydub (audio processing)

## Prerequisites

- Python 3.9 or higher
- OpenAI API key
- Modern web browser with microphone access

## Installation

### Quick Install (Recommended) 🚀

Use the automated installation scripts that create a `.venv` virtual environment and set everything up:

#### Windows
```bash
install.bat
```

#### Linux/macOS
```bash
chmod +x install.sh
./install.sh
```

The install scripts will:
1. ✅ Check Python installation
2. ✅ Create `.venv` virtual environment
3. ✅ Install all dependencies
4. ✅ Create `.env` file from template

---

### Manual Installation

If you prefer to install manually:

#### 1. Clone the Repository

```bash
git clone <repository-url>
cd PunjabiLangTool
```

#### 2. Create Virtual Environment

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

#### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 4. Set Up Environment Variables

Create a `.env` file in the project root (copy from `env.example`):

```bash
# Windows
copy env.example .env

# macOS/Linux
cp env.example .env
```

Edit `.env` and add your OpenAI API key:

```env
# OpenAI API Key (required)
OPENAI_API_KEY=your_actual_openai_api_key_here

# Application settings
DEBUG=true
HOST=0.0.0.0
PORT=8000

# TTS Settings (optional - defaults are optimized for speed + quality)
TTS_MODEL=tts-1             # Fast & high quality. Use "tts-1-hd" for better quality (slower)
TTS_VOICE=nova              # Best for Punjabi: nova (female), onyx (male)
TTS_SPEED=1.0               # 0.25-4.0, normal speed. Use 0.9 for slower/clearer
```

**Important**: Never commit your `.env` file or expose your API key!

### 🎤 TTS Voice Options

For more details on voice selection, see [`TTS_VOICE_GUIDE.md`](TTS_VOICE_GUIDE.md). Quick options:

- **nova** (Default) - Female, warm, best for Punjabi ⭐
- **onyx** - Male, deep and smooth
- **shimmer** - Female, gentle
- **alloy** - Neutral, balanced

## Running the Application

### Activate Virtual Environment (If Not Already Active)

Before running the application, make sure your virtual environment is activated:

```bash
# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate
```

You'll know it's activated when you see `(.venv)` at the start of your command prompt.

### Start the Backend Server

**Option 1: Using the run script (Recommended)**
```bash
python run.py
```

**Option 2: Using uvicorn directly**
```bash
uvicorn backend.api.main:app --reload --host 0.0.0.0 --port 8000
```

**Option 3: Direct Python execution**
```bash
python -m backend.api.main
```

### Access the Application

Open your web browser and navigate to:

```
http://localhost:8000
```

### Grant Microphone Permissions

When prompted by your browser, allow microphone access for speech recording.

## Usage Guide

### Starting a Conversation

1. **Select a Scenario**: Choose from curated scenarios like "Shopping at the Market" or "School Pickup"
2. **Custom Scenario**: Or enter your own scenario description
3. **Listen to Greeting**: The AI character will greet you in Punjabi
4. **Start Speaking**: Hold the "Hold to Speak" button and speak in Punjabi
5. **View Transcripts**: See your speech transcribed in all three formats
6. **Continue Conversation**: The AI responds naturally in Punjabi with audio

### Using Help Mode

1. Click the **"Help Mode"** button during a conversation
2. Select a topic: Grammar, Vocabulary, Culture, or Alternatives
3. Type your question
4. Click **"Ask"** to get a detailed explanation with examples
5. Close the panel to resume the conversation

### Ending a Session

1. Click **"End Session"**
2. View your session summary with metrics:
   - Words per minute
   - Total words spoken
   - Unique vocabulary used
   - Average confidence score
   - **API cost breakdown** (Whisper + GPT + TTS)
3. Rate your confidence (1-5)
4. Start a new session or return to scenario selection

### 💰 Viewing API Usage

During conversations, you'll see:
- **Live cost** updating in the metrics panel
- **OpenAI account info** (if available with your API key)
- **Session total** spent so far

After ending a session:
- Detailed breakdown by service (ASR, GPT, TTS)
- Total tokens used and characters processed
- Estimated costs (based on current OpenAI pricing)

**API Endpoints for Usage:**
- `GET /api/usage/{session_id}` - Get usage for specific session
- `GET /api/usage/global/summary` - Get cumulative usage
- `GET /api/account/balance` - Check OpenAI balance (if available)

## Project Structure

```
PunjabiLangTool/
├── backend/
│   ├── api/
│   │   └── main.py              # FastAPI application & endpoints
│   ├── models/
│   │   ├── transcript.py        # Tri-script data models
│   │   ├── scenario.py          # Scenario models
│   │   └── session.py           # Session & analytics models
│   ├── services/
│   │   ├── openai_client.py     # OpenAI client wrapper
│   │   ├── asr_service.py       # Whisper ASR service
│   │   ├── tts_service.py       # OpenAI TTS service
│   │   ├── translation_service.py  # Translation service
│   │   ├── transliteration.py   # Gurmukhi → Romanised
│   │   ├── conversation_service.py # AI conversation (Doabi dialect)
│   │   ├── help_service.py      # Help mode assistant
│   │   ├── scenario_service.py  # Scenario management (curated + custom)
│   │   ├── session_manager.py   # Session state & analytics
│   │   ├── usage_tracker.py     # API cost tracking
│   │   └── orchestrator.py      # Service orchestration
│   └── __init__.py
├── frontend/
│   ├── index.html               # Main UI
│   └── static/
│       ├── css/
│       │   └── style.css        # Styles
│       ├── js/
│       │   └── app.js           # Frontend logic
│       └── audio/               # Generated audio files
├── tests/
│   ├── conftest.py              # Pytest configuration
│   ├── test_models.py           # Model tests
│   ├── test_transliteration.py # Transliteration tests
│   ├── test_session_manager.py # Session manager tests
│   └── test_scenario_service.py# Scenario service tests
├── requirements.txt             # Python dependencies
├── pytest.ini                   # Pytest configuration
├── env.example                  # Environment variable template
├── PRD.md                       # Product requirements document
├── MVP_Plan.md                  # MVP delivery plan
├── WHATS_NEW.md                 # Latest features and updates
├── USAGE_TRACKING.md            # API usage tracking guide
├── TTS_VOICE_GUIDE.md           # TTS voice selection guide
└── README.md                    # This file
```

## Running Tests

### Run All Tests

```bash
pytest
```

### Run Specific Test Files

```bash
pytest tests/test_models.py
pytest tests/test_transliteration.py
```

### Run with Coverage

```bash
pytest --cov=backend --cov-report=html
```

### Skip API Tests (to avoid costs)

Most tests don't call external APIs. To skip the few that do:

```bash
pytest -m "not api"
```

## API Endpoints

### Scenarios

- `GET /api/scenarios` - List all curated scenarios
- `GET /api/scenarios/{scenario_id}` - Get specific scenario
- `POST /api/scenarios/custom` - Create custom scenario

### Sessions

- `POST /api/sessions/start` - Start new conversation session
- `POST /api/sessions/{session_id}/turn` - Process conversation turn
- `POST /api/sessions/{session_id}/help` - Get help response
- `POST /api/sessions/{session_id}/complete` - Complete session
- `GET /api/sessions/{session_id}/metrics` - Get current metrics

### Usage & Billing (NEW)

- `GET /api/usage/{session_id}` - Get API usage stats for a session
- `GET /api/usage/global/summary` - Get cumulative usage across all sessions
- `GET /api/account/balance` - Check OpenAI account balance (if available)

### Health

- `GET /health` - Health check endpoint

## Configuration

### Models Used (Optimized for Speed & Quality)

- **ASR**: `whisper-1` (auto-detects Punjabi with prompt guidance)
- **Conversation AI**: `gpt-4o-mini` (Doabi dialect, cost-efficient)
- **Translation**: `gpt-3.5-turbo` (fast, accurate)
- **Romanisation**: `gpt-3.5-turbo` (context-aware, phonetically accurate)
- **TTS**: `tts-1` with **nova voice** (fast, natural Punjabi pronunciation)

### Customizing via Environment Variables

Add to your `.env` file:

```env
# TTS Customization
TTS_MODEL=tts-1-hd          # For highest quality (slower, 2x cost)
TTS_VOICE=onyx              # Try: nova, onyx, shimmer, alloy, echo, fable
TTS_SPEED=0.9               # Slower for beginners (0.8-1.2 range)

# Model Customization
CONVERSATION_MODEL=gpt-4o-mini
TRANSLATION_MODEL=gpt-3.5-turbo
```

See [`TTS_VOICE_GUIDE.md`](TTS_VOICE_GUIDE.md) for detailed voice comparisons.

## Troubleshooting

### Microphone Not Working

- Ensure browser has microphone permissions
- Check system microphone settings
- Try a different browser (Chrome/Edge recommended)

### API Key Errors

- Verify your OpenAI API key is correct in `.env`
- Check that `.env` is in the project root
- Ensure you have API credits available

### Audio Not Playing

- Check browser audio permissions
- Verify audio files are being generated in `frontend/static/audio/`
- Try refreshing the page

### Installation Issues

```bash
# Upgrade pip
python -m pip install --upgrade pip

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

## 💰 Cost Considerations

**Current Pricing (as of 2024):**
- **Whisper ASR**: $0.006 per minute ($0.0001 per second)
- **GPT-3.5-turbo**: $0.50 per 1M input tokens, $1.50 per 1M output tokens
- **GPT-4o-mini**: $0.15 per 1M input tokens, $0.60 per 1M output tokens
- **TTS-1**: $15.00 per 1M characters (~$0.015 per 1K chars)
- **TTS-1-HD**: $30.00 per 1M characters (2x more expensive)

**Typical Session Costs:**
- 10-turn conversation (~5 back-and-forth exchanges): **$0.01-0.02** 🎉
  - Whisper: ~0.5 min = $0.003
  - GPT: ~3000 tokens = $0.002
  - TTS: ~500 chars = $0.008
  
**Real-time tracking** in the app shows exact costs per session!

**Cost-Saving Tips:**
1. Use `tts-1` instead of `tts-1-hd` (50% cheaper, still great quality)
2. Practice in shorter, focused sessions
3. Use the Help Mode sparingly (uses additional GPT tokens)

See [`USAGE_TRACKING.md`](USAGE_TRACKING.md) for detailed usage analytics.

## 🗺️ Future Roadmap

### Planned Features
- 💾 Save and review past conversations
- 📈 Progress tracking across sessions
- 🏆 Achievement system for gamification
- 🎯 Accent-aware feedback using confidence metrics
- 🗣️ Multi-dialect support (Majhi, Malwai, Powadhi)
- 📱 Mobile app (iOS & Android)
- 👨‍🏫 Teacher/admin dashboard
- 🎮 Interactive vocabulary games
- 📊 Advanced analytics dashboard
- 🔊 Voice comparison playback (your voice vs native speaker)

## Contributing

This is an MVP proof of concept. For production use, consider:

- User authentication and persistence
- Database for session storage
- Rate limiting and cost controls
- Content safety filters
- Enhanced error handling
- Internationalization support

## License

See [LICENSE](LICENSE) file for details.

## 📚 Additional Documentation

- **[WHATS_NEW.md](WHATS_NEW.md)** - Latest features and improvements
- **[USAGE_TRACKING.md](USAGE_TRACKING.md)** - API usage tracking guide
- **[TTS_VOICE_GUIDE.md](TTS_VOICE_GUIDE.md)** - Voice selection and optimization
- **[QUICKSTART.md](QUICKSTART.md)** - Quick setup guide
- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Common issues and solutions
- **[PRD.md](PRD.md)** - Product requirements document
- **[MVP_Plan.md](MVP_Plan.md)** - MVP delivery plan

## Support

For issues or questions:
1. Check the troubleshooting guides above
2. Review the PRD.md for detailed specifications
3. Check the terminal logs for error messages
4. Verify your OpenAI API key is valid and has credits

---

Made with 💜 for Punjabi language learners everywhere

**ਧੰਨਵਾਦ** (Dhannvaad) - Thank you for helping preserve and promote the Punjabi language! 🙏
