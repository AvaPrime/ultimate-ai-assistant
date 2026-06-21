from langchain.tools import tool
from ..config import config
from ..utils import post_json

@tool
def research(query: str) -> str:
    """Real-time web research via Perplexity."""
    url = "https://api.perplexity.ai/chat/completions"
    payload = {
        "model": "sonar-medium-online",
        "messages": [{"role": "user", "content": query}]
    }
    headers = {"Authorization": f"Bearer {config.perplexity_key}", "Content-Type": "application/json"}
    data = post_json(url, payload, headers)
    return data["choices"][0]["message"]["content"]
