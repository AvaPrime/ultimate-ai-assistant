from langchain.tools import tool
from ..config import config
from ..utils import post_json

@tool
def generate_image(prompt: str) -> str:
    """Generate image via Stability AI."""
    url = "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image"
    headers = {
        "Authorization": f"Bearer {config.stability_key}",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    payload = {"text_prompts": [{"text": prompt}], "samples": 1, "width": 1024, "height": 1024}
    data = post_json(url, payload, headers)
    img_b64 = data["artifacts"][0]["base64"]
    return f"data:image/png;base64,{img_b64}"
