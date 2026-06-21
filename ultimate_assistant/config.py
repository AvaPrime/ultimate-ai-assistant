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
    model: str = "openai/gpt-4o"          # Change to any model on OpenRouter
    temperature: float = 0.4

config = Config()