from dataclasses import dataclass
import os
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Config:
    openrouter_key: str = os.getenv("OPENROUTER_API_KEY")
    perplexity_key: str = os.getenv("PERPLEXITY_API_KEY")
    stability_key: str = os.getenv("STABILITY_API_KEY")
    gemini_key: str = os.getenv("GEMINI_API_KEY")
    openai_key: str = os.getenv("OPENAI_API_KEY")
    eleven_key: str = os.getenv("ELEVEN_API_KEY")
    resend_key: str = os.getenv("RESEND_API_KEY")
    notion_key: str = os.getenv("NOTION_API_KEY")
    redis_url: str = os.getenv("REDIS_URL") or os.getenv("UPSTASH_REDIS_URL")
    access_password: str = os.getenv("ACCESS_PASSWORD")
    model: str = os.getenv("DEFAULT_MODEL", "openai/gpt-4o")
    temperature: float = 0.4

# Popular models available in the UI selector (OpenRouter IDs)
RECOMMENDED_MODELS = [
    {"id": "openai/gpt-4o", "name": "GPT-4o (Fast & Smart)"},
    {"id": "anthropic/claude-3.5-sonnet", "name": "Claude 3.5 Sonnet"},
    {"id": "google/gemini-2.0-flash", "name": "Gemini 2.0 Flash"},
    {"id": "x-ai/grok-4", "name": "Grok-4 (xAI)"},
    {"id": "meta-llama/llama-3.3-70b-instruct", "name": "Llama 3.3 70B"},
    {"id": "qwen/qwen-2.5-72b-instruct", "name": "Qwen 2.5 72B"},
]

config = Config()