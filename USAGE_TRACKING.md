# OpenAI API Usage Tracking

This application now includes comprehensive OpenAI API usage tracking to help you monitor your costs.

## Features

### 1. **Live Cost Display**
During conversations, you'll see a live-updating cost display in the metrics panel:
- **API Cost: $X.XX** - Updates after each conversation turn

### 2. **Session Summary**
When you end a session, you'll see:
- Total estimated cost for the session
- Detailed breakdown by service:
  - **Whisper (ASR)**: Minutes of audio transcribed
  - **GPT**: Tokens used for conversation, translation, and romanisation
  - **TTS**: Characters converted to speech

### 3. **API Endpoints**

#### Get Session Usage
```bash
GET /api/usage/{session_id}
```

Returns usage stats for a specific session:
```json
{
  "session_id": "...",
  "usage": {
    "whisper": {
      "seconds": 45.2,
      "minutes": 0.75,
      "cost": "$0.0075"
    },
    "gpt": {
      "input_tokens": 1250,
      "output_tokens": 890,
      "total_tokens": 2140,
      "model": "gpt-3.5-turbo",
      "cost": "$0.0021"
    },
    "tts": {
      "characters": 450,
      "cost": "$0.0068"
    },
    "total_cost": "$0.0164"
  }
}
```

#### Get Global Usage
```bash
GET /api/usage/global/summary
```

Returns cumulative usage across all sessions since server start.

#### Check Account Balance
```bash
GET /api/account/balance
```

Attempts to check your OpenAI account balance. Note: This may not work with all API key types. For accurate balance info, visit: https://platform.openai.com/account/billing

## Cost Estimates

All costs are **estimates** based on current OpenAI pricing (as of 2024):

| Service | Pricing |
|---------|---------|
| Whisper | $0.006 per minute |
| GPT-3.5 Turbo | $0.50 per 1M input tokens, $1.50 per 1M output tokens |
| GPT-4o-mini | $0.15 per 1M input tokens, $0.60 per 1M output tokens |
| TTS | $15 per 1M characters |

**Note**: These are estimates only. Actual costs may vary. Always check your OpenAI dashboard for precise billing information.

## Model Usage

The application uses:
- **Whisper** (`whisper-1`): For speech-to-text transcription
- **GPT-3.5 Turbo**: For translations, romanisation, and conversation generation (faster & cheaper)
- **TTS** (`tts-1`): For text-to-speech generation

## Testing

Run the test script to verify usage tracking:

```bash
python test_usage.py
```

This will:
1. Check global usage statistics
2. Attempt to check account balance
3. Show you how to monitor per-session usage

## Privacy Note

Usage data is stored in memory only and is **not persisted** to any database. When you restart the server, usage tracking starts fresh.

## Optimization Tips

To minimize costs:

1. **Use shorter sessions** - Each turn uses multiple API calls
2. **Speak clearly** - Better transcription = fewer retries
3. **Practice regularly** - Consistent short sessions are more cost-effective than long ones
4. **Monitor your usage** - Keep an eye on the live cost display

## Typical Session Costs

Based on a 10-turn conversation (5 back-and-forth exchanges):

- **Whisper**: ~0.5 minutes = $0.003
- **GPT**: ~3000 tokens = $0.002
- **TTS**: ~500 characters = $0.008
- **Total**: ~$0.013 per session

So about **1-2 cents per practice session**! 🎉

## Questions?

For detailed billing and usage information, always refer to your OpenAI dashboard:
👉 https://platform.openai.com/account/usage

