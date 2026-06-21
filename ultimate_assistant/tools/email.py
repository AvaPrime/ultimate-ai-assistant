from langchain.tools import tool
from ..config import config
import httpx

@tool
def send_email(to: str, subject: str, body: str) -> str:
    """Send an email using Resend (add RESEND_API_KEY to env)."""
    if not config.resend_key:
        return "Error: RESEND_API_KEY not configured."
    url = "https://api.resend.com/emails"
    headers = {"Authorization": f"Bearer {config.resend_key}", "Content-Type": "application/json"}
    payload = {
        "from": "assistant@yourdomain.com",  # Change to your verified domain
        "to": to,
        "subject": subject,
        "html": body.replace("\n", "<br>")
    }
    resp = httpx.post(url, json=payload, headers=headers)
    if resp.status_code == 200:
        return f"Email sent successfully to {to}. ID: {resp.json().get('id')}"
    return f"Failed to send email: {resp.text}"