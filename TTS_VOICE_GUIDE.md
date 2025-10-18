# TTS Voice Selection Guide for Punjabi

The app now uses **improved TTS settings** optimized for Punjabi pronunciation!

## 🎯 Current Defaults (Optimized for Speed + Quality)

- **Model**: `tts-1` (Fast and high quality)
- **Voice**: `nova` (Female, warm and natural)
- **Speed**: `1.0` (Normal speed, natural flow)

## 🎤 Available Voices (Ranked for Punjabi)

### 1. **Nova** ⭐ (Current Default - Female)
- **Best overall for Punjabi**
- Warm, natural, and clear
- Handles Gurmukhi pronunciation well
- Recommended for most users

### 2. **Onyx** (Male Alternative)
- Deep, smooth male voice
- Good pronunciation
- Excellent if you prefer male voice

### 3. **Shimmer** (Female)
- Gentle and clear
- Slightly higher pitch than Nova
- Good alternative

### 4. **Alloy** (Neutral)
- Balanced, neither masculine nor feminine
- Consistent pronunciation
- Good for variety

### 5. **Echo** (Male)
- Strong, confident voice
- May sound less natural for Punjabi

### 6. **Fable** (Expressive)
- More dramatic and varied
- May be too expressive for learning

## 🔧 How to Change Voice

### Option 1: Environment Variable (Recommended)

Edit your `.env` file:

```bash
TTS_VOICE=onyx    # Try: nova, onyx, shimmer, alloy, echo, fable
TTS_SPEED=0.95    # Adjust: 0.8 (slower) to 1.1 (faster)
TTS_MODEL=tts-1-hd # Or "tts-1" for faster/cheaper
```

Then restart the server:
```bash
python run.py
```

### Option 2: Quick Test Different Voices

Try each voice to find your favorite:

```bash
# In your .env file, try one at a time:
TTS_VOICE=nova     # Restart and test
TTS_VOICE=onyx     # Restart and test
TTS_VOICE=shimmer  # Restart and test
```

## ⚡ Speed Settings

- **0.85**: Slower, very clear (good for beginners)
- **0.95**: Default, natural and clear
- **1.0**: Normal speed
- **1.1**: Slightly faster (for advanced learners)

## 💰 Cost Difference

- **tts-1**: $15 per 1M characters (fast, high quality) ⭐
- **tts-1-hd**: $30 per 1M characters (highest quality, slower)

**Recommendation**: The default `tts-1` is **perfect for most users** - it's fast, sounds great, and costs less (~$0.004 per typical session). Use `tts-1-hd` only if you want the absolute best quality and don't mind slower responses.

## 🎯 Recommended Settings by Preference

### Fast & High Quality (Current Default) ⚡
```bash
TTS_MODEL=tts-1
TTS_VOICE=nova
TTS_SPEED=1.0
```

### Male Voice Alternative
```bash
TTS_MODEL=tts-1
TTS_VOICE=onyx
TTS_SPEED=1.0
```

### Highest Quality (Slower, costs 2x)
```bash
TTS_MODEL=tts-1-hd
TTS_VOICE=nova
TTS_SPEED=1.0
```

### Slower for Beginners
```bash
TTS_MODEL=tts-1
TTS_VOICE=nova
TTS_SPEED=0.85
```

## 🔍 Why These Changes Matter

### Before:
- Voice: "alloy" (generic)
- Speed: 1.0 (default, not optimized)
- Model: "tts-1" (standard)
- ❌ Sounded like "English person speaking Punjabi"

### After:
- Voice: "nova" (optimized for Punjabi)
- Speed: 1.0 (natural flow)
- Model: "tts-1" (fast & high quality)
- ✅ More natural Punjabi pronunciation + faster response

## 📝 Tips

1. **Try different voices** - Everyone has preferences!
2. **Adjust speed** - Start slower (0.85-0.90) if you're a beginner
3. **Use HD model** - The quality difference is worth the small extra cost
4. **Listen actively** - Compare AI pronunciation with native speakers

## 🔄 Changes Take Effect

After modifying your `.env` file, **restart the server**:
```bash
# Stop server (Ctrl+C)
# Then restart:
python run.py
```

The new settings will apply immediately to all new conversations!

---

**Try it now**: Restart your server and start a new conversation. The voice should sound much more natural! 🎉

