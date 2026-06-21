# Ultimate AI Assistant

**Full-featured, voice-enabled, multi-model AI assistant** with persistent history, tools, and production deployment.

## Features
- **OpenRouter** as model gateway (switch models on the fly: Grok-4, Claude 3.5, GPT-4o, Gemini, etc.)
- **Voice Input** (Whisper) + **Voice Output** (ElevenLabs with speed control + 10+ multilingual voices)
- **Voice Cloning** (upload audio to create custom voice)
- **Chat History Sidebar** with clickable past sessions (powered by Redis / Vercel KV)
- **Auto-translate** input to English
- **Google Calendar tool** (add events directly from chat)
- **Email & Notion tools**
- **Rate limiting** & robust error handling + logging
- **Dark mode** + excellent mobile styling
- **Export** full chat as JSON
- One-click deploy to Vercel

## Quick Deploy (Mobile Friendly)
1. Go to https://github.com/AvaPrime/ultimate-ai-assistant
2. Click **Deploy to Vercel**
3. Add these Environment Variables in Vercel:
   - `OPENROUTER_API_KEY` (required)
   - `ELEVEN_API_KEY`, `OPENAI_API_KEY`, `PERPLEXITY_API_KEY`, etc.
   - `REDIS_URL` or `UPSTASH_REDIS_URL` (for persistent history across deploys)
   - `RESEND_API_KEY`, `NOTION_API_KEY` (optional)
   - `ACCESS_PASSWORD` (optional shared password)
4. Deploy!

Your app will be live at `https://your-project.vercel.app`

## Local Development
```bash
pip install -r requirements.txt
uvicorn ultimate_assistant.api:app --reload
```

## New in This Update
- Chat history sidebar with clickable sessions
- Google Calendar integration
- Voice cloning UI
- Dark mode toggle
- Rate limiting (30 req/min per IP)
- Improved logging and error handling

See the code for full implementation details.

**Repository is fully up to date with complete, working code (no placeholders).**