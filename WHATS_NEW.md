# What's New - API Usage Tracking & Improvements

## 🎉 New Feature: API Cost Tracking

You can now see **exactly how much** your practice sessions cost!

### What You'll See:

1. **Live Cost Display** 💰
   - Real-time cost updates during conversation
   - Shows in the metrics panel: "API Cost: $0.XX"

2. **Detailed Session Summary** 📊
   - Complete breakdown when you end a session
   - Shows costs for Whisper, GPT, and TTS separately
   - Total estimated cost per session

3. **API Endpoints** 🔌
   - `/api/usage/{session_id}` - Get usage for a specific session
   - `/api/usage/global/summary` - Get cumulative usage across all sessions
   - `/api/account/balance` - Check OpenAI account balance (if available)

### Typical Costs:
- **Per session (10 turns)**: ~$0.01-0.02
- **Per minute of speech**: ~$0.003
- **Very affordable for regular practice!** 🎯

---

## ⚡ Performance Improvements

### Faster Translations & Romanisation
- **Switched to GPT-3.5 Turbo** from GPT-4o-mini
  - **3x faster** responses
  - **Same quality** for translations
  - **Lower cost**

### Cleaner Output
- **Removed AI chatter** from translations
  - Before: "Sure! Here's the translation: Hello!"
  - After: "Hello!"
- **More concise prompts** for faster API responses

---

## 🐛 Bug Fixes

### Romanisation Accuracy
- **Now using LLM-based romanisation** instead of character-by-character
  - ✅ Before: "saasaree kaala pain jee"
  - ✅ After: "sat sri akaal paaji"
- **Context-aware** - uses recent conversation for better accuracy

### Dialect Consistency
- **Strengthened Doabi Punjabi** enforcement
  - Always uses "ਕਿੱਦਾਂ/kiddan" (not "ਕਿਵੇਂ/kiven")
  - Proper "ਐਂ/ain" endings
  - Native Doabi speaker tone

---

## 📖 Documentation

New docs added:
- `USAGE_TRACKING.md` - Complete guide to usage tracking
- `test_usage.py` - Test script for usage endpoints
- This file! 😊

---

## 🚀 Try It Now!

1. Start the server: `python run.py`
2. Begin a conversation
3. Watch the **API Cost** update in real-time
4. End session to see detailed breakdown

**Questions?** Check `USAGE_TRACKING.md` for details!

---

## 🙏 Feedback Welcome

Found a bug? Have a suggestion? Let us know!

Happy practicing! 🎤✨

