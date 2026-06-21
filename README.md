# Ultimate AI Assistant

A powerful, modular, voice-enabled AI assistant with real-time research, image generation, multilingual voice output, persistent chat history, model switching, and more.

## Features

- **OpenRouter** as central model gateway (switch models on the fly: Grok-4, Claude 3.5, GPT-4o, Gemini, Llama, etc.)
- **Voice Input** (Whisper) + **Voice Output** with speed control and 10+ multilingual voices (ElevenLabs)
- **Voice Cloning** (ElevenLabs Instant Voice Cloning)
- **Auto-translate** input to English
- **Persistent Chat History** with Redis (works across deploys)
- **Clickable Chat History Sidebar** with preview snippets
- **Usage Dashboard** (`/dashboard`)
- **Rate Limiting** (30 req/min)
- **Dark Mode** + excellent mobile styling
- **Tools**: Perplexity research, Stable Diffusion images, Gemini vision, Email (Resend), Notion pages, Google Calendar, Web search with citations

## Quick Deploy to Vercel

1. Fork or use this repo
2. Click **Deploy to Vercel**
3. Add these Environment Variables in Vercel:
   - `OPENROUTER_API_KEY` (required)
   - `PERPLEXITY_API_KEY`, `STABILITY_API_KEY`, `GEMINI_API_KEY`, `OPENAI_API_KEY`, `ELEVEN_API_KEY`
   - `REDIS_URL` or `UPSTASH_REDIS_URL` (for persistent history + rate limiting)
   - `RESEND_API_KEY`, `NOTION_API_KEY` (optional)
   - `ACCESS_PASSWORD` (optional shared password)

## New Features (Latest Update)

### Clickable Chat History with Preview Snippets
- Left sidebar shows recent chats with the last message preview (first 80 characters).
- Click any session to instantly load the full conversation.
- "Refresh Sessions" and "+ New Chat" buttons.

### Usage Dashboard
- Visit `/dashboard` on your deployed app to see:
  - Total requests
  - Total tokens used
  - Breakdown by model

### Google Calendar Integration
**Simple path (recommended for personal use):**
- Use a Google Service Account (create in Google Cloud Console → IAM & Admin → Service Accounts).
- Download JSON key and add as `GOOGLE_SERVICE_ACCOUNT_JSON` env var (base64 encoded or as secret).
- The agent can then call `add_calendar_event`.

**Full OAuth flow (for multi-user):**
- Implement Google OAuth2 using `google-auth-oauthlib` and store tokens per user in Redis.
- Add a `/auth/google` endpoint that redirects to Google's consent screen.
- Callback at `/auth/google/callback` exchanges code for tokens.
- Store `credentials` in Redis under user session.
- See `tools/calendar.py` for starter code.

### Enhanced Tools
- **Notion Pages**: Create rich pages with the Notion API.
- **Email with Attachments**: Send emails via Resend with file attachments (base64).
- **Web Search with Citations**: Uses Perplexity or Brave Search and returns sources.

## Running Locally

```bash
pip install -r requirements.txt
uvicorn ultimate_assistant.api:app --reload
```

Open http://localhost:8000

## Architecture
- FastAPI backend
- LangChain + OpenRouter for agent orchestration
- Redis for state, history, rate limiting, usage tracking
- Modular tools in `ultimate_assistant/tools/`

## Next Steps / Roadmap
- Full multi-user auth (JWT + login page)
- More tools (Slack, Linear, etc.)
- Voice cloning improvements
- Analytics dashboard

Built with ❤️ using Grok, OpenRouter, and modern AI tooling.