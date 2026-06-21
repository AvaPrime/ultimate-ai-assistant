# Ultimate AI Assistant

Full-featured, voice-enabled, multi-model AI assistant with persistent memory, multilingual TTS, and tool use.

## Features
- **Model Selector**: Switch between GPT-4o, Claude 3.5, Gemini 2.0, Grok-4, Llama 3.3, Qwen 2.5 on the fly.
- **Voice Input** (OpenAI Whisper)
- **Voice Output** with speed control + 10 multilingual voices (ElevenLabs)
- **Auto-translate** non-English input to English for better reasoning
- **Tools**: Web research (Perplexity), Image generation (Stable Diffusion), Image analysis (Gemini), Email (Resend), Notion database
- **Persistent Chat History**: Uses Redis (Vercel KV or Upstash) — survives deploys
- **Password Protection** (optional shared password)
- **Export** full chat as JSON

## Quick Deploy to Vercel
1. Fork or use the repo
2. Click **Deploy to Vercel**
3. Add these Environment Variables in Vercel:
   - `OPENROUTER_API_KEY` (required)
   - `PERPLEXITY_API_KEY`, `STABILITY_API_KEY`, `GEMINI_API_KEY`, `OPENAI_API_KEY`, `ELEVEN_API_KEY`
   - `REDIS_URL` or `UPSTASH_REDIS_URL` (for persistent history — recommended, free tier available)
   - `RESEND_API_KEY`, `NOTION_API_KEY` (optional tools)
   - `ACCESS_PASSWORD` (optional)
   - `DEFAULT_MODEL` (optional, e.g. `anthropic/claude-3.5-sonnet`)

## Model Selector
The UI now has a **Model** dropdown at the top. Changing it instantly uses that model for the next message via OpenRouter (no restart needed).

## Persistent Storage (Vercel KV / Redis)
- Set `REDIS_URL` in Vercel (create a KV store in Vercel Dashboard → Storage → KV)
- History is saved per session ID (stored in browser localStorage)
- Click **Load History** to restore previous conversation

## Error Handling & Logging
- All agent errors are caught and shown in chat
- Server logs visible in Vercel Function Logs
- Redis failures gracefully fall back to /tmp file storage

## Local Run
```bash
pip install -r requirements.txt
uvicorn ultimate_assistant.api:app --reload
```

Open http://localhost:8000

## Tech Stack
FastAPI + LangChain + OpenRouter + Redis + ElevenLabs + Whisper

Built with ❤️ for maximum capability in one clean interface.