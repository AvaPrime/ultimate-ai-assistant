from langchain.tools import tool
from ..config import config
import google.generativeai as genai

genai.configure(api_key=config.gemini_key)
model = genai.GenerativeModel("gemini-1.5-flash")

@tool
def analyze_image(image_b64_url: str, question: str) -> str:
    """Analyze image with Gemini vision."""
    data = image_b64_url.split(",", 1)[1]
    img = {"inline_data": {"mime_type": "image/png", "data": data}}
    resp = model.generate_content([question, img])
    return resp.text
