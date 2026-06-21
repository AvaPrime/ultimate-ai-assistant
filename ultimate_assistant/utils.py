import httpx
from typing import Any

def post_json(url: str, payload: dict, headers: dict, timeout: int = 60) -> Any:
    resp = httpx.post(url, json=payload, headers=headers, timeout=timeout)
    resp.raise_for_status()
    return resp.json()