# Punjabi Language Learning Tool 🗣️

AI-powered conversational Punjabi practice tool using OpenAI's GPT, Whisper, and TTS technologies.

## Features

- **Scenario-Based Conversations**: Practice real-world scenarios like shopping at the market or school pickup
- **Custom Scenarios**: Create your own conversation scenarios
- **Live Speech Interaction**: Speak in Punjabi and see transcriptions in three formats:
  - Gurmukhi script (ਤੁਸੀਂ ਕਿਵੇਂ ਹੋ?)
  - Romanised Punjabi (tusi kiven ho?)
  - English translation (How are you?)
- **AI Character Responses**: Natural Doabi Punjabi responses with text-to-speech audio
- **Help Mode**: Pause conversations to ask for:
  - Grammar explanations
  - Vocabulary breakdowns
  - Cultural context
  - Alternative phrasings
- **Session Analytics**: Track words per minute, vocabulary breadth, confidence scores

## Tech Stack

- **Backend**: FastAPI (Python)
- **Frontend**: HTML, CSS, JavaScript
- **AI Services**: 
  - OpenAI GPT-4 (conversation & translation)
  - OpenAI Whisper (speech-to-text)
  - OpenAI TTS (text-to-speech)
- **Testing**: pytest

## Prerequisites

- Python 3.9 or higher
- OpenAI API key
- Modern web browser with microphone access

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd PunjabiLangTool
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the project root (copy from `env.example`):

```bash
# Windows
copy env.example .env

# macOS/Linux
cp env.example .env
```

Edit `.env` and add your OpenAI API key:

```env
OPENAI_API_KEY=your_actual_openai_api_key_here
DEBUG=true
HOST=0.0.0.0
PORT=8000
```

**Important**: Never commit your `.env` file or expose your API key!

## Running the Application

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
3. Rate your confidence (1-5)
4. Start a new session or return to scenario selection

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
│   │   ├── conversation_service.py # AI conversation
│   │   ├── help_service.py      # Help mode assistant
│   │   ├── scenario_service.py  # Scenario management
│   │   ├── session_manager.py   # Session state & analytics
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
├── PRD.md                       # Product requirements
├── MVP_Plan.md                  # MVP delivery plan
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

### Health

- `GET /health` - Health check endpoint

## Configuration

### Models Used

- **ASR**: `whisper-1` (Punjabi language)
- **Conversation AI**: `gpt-4o-mini` (cost-efficient)
- **Translation**: `gpt-4o-mini`
- **TTS**: `tts-1` (faster, standard quality)

### Customizing Models

Edit service initializations in `backend/services/` files to use different models:

```python
# For higher quality TTS
tts_service = TTSService(model="tts-1-hd")

# For better conversation quality (higher cost)
conversation_service = ConversationService(model="gpt-4")
```

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

## Cost Considerations

- ASR (Whisper): $0.006 per minute of audio
- GPT-4-mini: ~$0.15 per 1M input tokens, ~$0.60 per 1M output tokens
- TTS: $15.00 per 1M characters

Typical 10-minute session costs approximately $0.10-0.20.

## Future Roadmap

- Save and review past conversations
- Progress tracking across sessions
- Achievement system for gamification
- Accent-aware feedback using confidence metrics
- Multi-dialect support
- Mobile app
- Teacher/admin dashboard

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

## Support

For issues or questions, please refer to the PRD.md and MVP_Plan.md for detailed specifications.

---

Made with 💜 for Punjabi language learners
