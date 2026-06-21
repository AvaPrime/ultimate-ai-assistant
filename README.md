# Ultimate AI Assistant

Full-featured voice-enabled AI assistant with multilingual support, deployed on Vercel.

## Features
- Grok-4 / Claude / Gemini orchestration via **OpenRouter** (unified gateway)
- Real-time research (Perplexity)
- Image generation (Stable Diffusion)
- Image analysis (Gemini via direct API)
- Voice input (OpenAI Whisper)
- Voice output with speed control + 10+ multilingual voices (ElevenLabs)
- Auto-translate input to English
- Persistent chat history + JSON export
- Clean modular architecture
- One-click Vercel deployment

## Quick Start (Local)

```bash
git clone https://github.com/AvaPrime/ultimate-ai-assistant.git
cd ultimate-ai-assistant
pip install -r requirements.txt
cp .env.example .env   # Add your keys
python -m ultimate_assistant
```

## Deploy to Vercel

1. Go to [vercel.com/new](https://vercel.com/new) and import this repo
2. Add these Environment Variables:
   - `OPENROUTER_API_KEY` (main LLM gateway)
   - `PERPLEXITY_API_KEY`
   - `STABILITY_API_KEY`
   - `GEMINI_API_KEY`
   - `OPENAI_API_KEY` (Whisper)
   - `ELEVEN_API_KEY`

## Architecture

- `api.py` – FastAPI + beautiful streaming UI with voice controls
- `agent.py` – LangChain ReAct agent powered by OpenRouter
- `tools/` – Modular specialized tools
- Fully supports speed control, multilingual voices, auto-translate, and export

## License
MIT