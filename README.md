# Ultimate AI Assistant

A production-ready, voice-enabled, multilingual AI assistant with persistent memory, built with **FastAPI + LangChain + OpenRouter** and deployable to Vercel in one click.

## ✨ Features

- **Unified LLM Gateway**: Powered by OpenRouter (switch between Grok-4, Claude 3.5/4, Gemini 2.0, Llama 4, etc. with one key)
- **Voice I/O**: Mic input (Whisper) + natural TTS output with **speed control** and **10+ multilingual voices** (ElevenLabs)
- **Auto-translate**: Any language input is automatically translated to English for the AI
- **Persistent Chat History**: Redis-backed (works across Vercel deploys)
- **Export Chats**: Download full conversation + audio as JSON
- **Extensible Tools**: Research, Image Gen/Analysis, Send Email (Resend), Add to Notion
- **Optional Password Protection**: Simple shared password gate
- **Beautiful Streaming UI**: Mobile-friendly, real-time responses

## 🚀 One-Click Deploy to Vercel

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2FAvaPrime%2Fultimate-ai-assistant)

Or manually:
1. Import repo at [vercel.com/new](https://vercel.com/new)
2. Add the Environment Variables listed below
3. Deploy

## Required Environment Variables (Vercel / .env)

| Variable | Purpose | Required |
|----------|---------|----------|
| `OPENROUTER_API_KEY` | Main LLM (Grok/Claude/Gemini/etc.) | Yes |
| `PERPLEXITY_API_KEY` | Real-time research | Yes |
| `STABILITY_API_KEY` | Image generation | Yes |
| `GEMINI_API_KEY` | Image analysis | Yes |
| `OPENAI_API_KEY` | Whisper speech-to-text | Yes |
| `ELEVEN_API_KEY` | High-quality TTS (multilingual) | Yes |
| `REDIS_URL` or `UPSTASH_REDIS_URL` | Persistent chat history | Recommended |
| `RESEND_API_KEY` | Send emails via tool | Optional |
| `NOTION_API_KEY` | Add pages to Notion DB | Optional |
| `ACCESS_PASSWORD` | Simple shared password protection | Optional |

## Setup Persistent Chat History with Upstash Redis (Free)

1. Go to [upstash.com](https://upstash.com) → Create Redis database (free tier)
2. Copy the `UPSTASH_REDIS_URL` (starts with `rediss://`)
3. Add it to Vercel Environment Variables as `REDIS_URL`
4. Chat history will now persist across deploys and restarts.

## Optional: User Authentication

Set `ACCESS_PASSWORD` environment variable. The UI will prompt for the password on first load. All API calls include it. This is a simple shared-password protection suitable for personal/team use.

For production-grade auth, integrate **Clerk** or **Supabase Auth** (both have excellent Vercel templates).

## Custom Domain Setup Guide

1. In Vercel Dashboard → Your Project → **Domains**
2. Add your domain (e.g. `assistant.yourdomain.com`)
3. Follow Vercel's DNS instructions (usually add a CNAME record)
4. Wait for SSL certificate to provision (automatic)
5. Update any hardcoded URLs if needed (the app is relative-path friendly)

## Adding More Tools (Calendar, Email, Notion, etc.)

New tools are easy to add:

1. Create `ultimate_assistant/tools/your_tool.py` with a `@tool` decorated function
2. Export it in `tools/__init__.py`
3. Import and add it to the `tools` list in `agent.py`

**Already included**:
- `send_email(to, subject, body)` — via Resend
- `add_to_notion_database(title, content, database_id)` — via Notion API

**For Google Calendar / Gmail**:
- Use the official Google APIs with service account credentials (store JSON in env or Vercel)
- Or use MCP servers for desktop integration

## Local Development

```bash
git clone https://github.com/AvaPrime/ultimate-ai-assistant.git
cd ultimate-ai-assistant
pip install -r requirements.txt
cp .env.example .env
# Add your keys to .env
python -m ultimate_assistant
```

Then open http://localhost:8000

## Architecture

- `api.py` – FastAPI backend + beautiful voice UI + streaming + Redis chat
- `agent.py` – LangChain ReAct agent with OpenRouter
- `tools/` – Modular, plug-and-play tools
- `config.py` – All secrets and settings

## License
MIT — Feel free to fork and customize.