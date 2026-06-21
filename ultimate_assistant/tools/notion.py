from langchain.tools import tool
from ..config import config
import httpx

@tool
def add_to_notion_database(title: str, content: str, database_id: str = None) -> str:
    """Add a new page to a Notion database. Requires NOTION_API_KEY and database_id."""
    if not config.notion_key:
        return "Error: NOTION_API_KEY not configured."
    db_id = database_id or "your_database_id_here"  # User should pass it or set default
    url = "https://api.notion.com/v1/pages"
    headers = {
        "Authorization": f"Bearer {config.notion_key}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }
    payload = {
        "parent": {"database_id": db_id},
        "properties": {
            "Name": {"title": [{"text": {"content": title}}]},
            "Content": {"rich_text": [{"text": {"content": content}}]}
        }
    }
    resp = httpx.post(url, json=payload, headers=headers)
    if resp.status_code in (200, 201):
        return f"Successfully added to Notion database. Page ID: {resp.json().get('id')}"
    return f"Failed to add to Notion: {resp.text}"