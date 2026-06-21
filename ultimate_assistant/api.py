import os, base64, json, datetime, logging
from pathlib import Path
from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import httpx
from deep_translator import GoogleTranslator
import redis
from .agent import create_agent
from .config import config, RECOMMENDED_MODELS

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Ultimate AI Assistant")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Redis client (Vercel KV / Upstash compatible)
redis_client = None
if config.redis_url:
    try:
        redis_client = redis.from_url(config.redis_url, decode_responses=True)
        logger.info("Redis connected for persistent chat history")
    except Exception as e:
        logger.error(f"Redis connection failed: {e}")

HISTORY_DIR = Path("/tmp/chat_history")
HISTORY_DIR.mkdir(exist_ok=True)

VOICES = { ... same as before ... }  # (keeping the voice dict for brevity in this response, assume full in actual)

# ... (full previous functions for check_password, save_chat, load_chat, translate_to_en, tts remain the same)

def check_password(pw: str):
    if config.access_password and pw != config.access_password:
        raise HTTPException(status_code=401, detail="Invalid password")

def save_chat(session_id: str, user_msg: str, ai_msg: str, audio_b64: str = None):
    entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "user": user_msg,
        "ai": ai_msg,
        "audio": audio_b64
    }
    if redis_client:
        try:
            key = f"chat:{session_id}"
            existing = redis_client.get(key)
            data = json.loads(existing) if existing else []
            data.append(entry)
            redis_client.set(key, json.dumps(data))
        except Exception as e:
            logger.error(f"Redis save failed: {e}")
    else:
        file = HISTORY_DIR / f"{session_id}.json"
        data = []
        if file.exists():
            data = json.loads(file.read_text())
        data.append(entry)
        file.write_text(json.dumps(data, indent=2))

def load_chat(session_id: str):
    if redis_client:
        try:
            key = f"chat:{session_id}"
            data = redis_client.get(key)
            return json.loads(data) if data else []
        except Exception as e:
            logger.error(f"Redis load failed: {e}")
            return []
    else:
        file = HISTORY_DIR / f"{session_id}.json"
        if file.exists():
            return json.loads(file.read_text())
        return []

async def tts(text: str, speed: float = 1.0, voice_key: str = "rachel") -> str:
    voice = VOICES.get(voice_key, VOICES["rachel"])
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice['id']}/stream"
    headers = {"xi-api-key": config.eleven_key, "Content-Type": "application/json"}
    payload = {
        "text": text,
        "voice_settings": {"stability": 0.75, "similarity_boost": 0.8, "speed": speed}
    }
    resp = httpx.post(url, json=payload, headers=headers, timeout=60)
    return base64.b64encode(resp.content).decode()

async def stream_response(query: str, speed: float, voice: str, session_id: str, password: str = None, model: str = None):
    try:
        check_password(password)
        agent = create_agent(model)  # Dynamic model per request
        full_text = ""
        async for chunk in agent.astream({"input": query}):
            text = chunk.get("output", "")
            full_text += text
            yield f"data: {json.dumps({'text': text, 'done': False})}\n\n"
        audio_b64 = await tts(full_text, speed, voice)
        save_chat(session_id, query, full_text, audio_b64)
        yield f"data: {json.dumps({'text': '', 'audio': audio_b64, 'done': True})}\n\n"
    except Exception as e:
        logger.error(f"Stream error for session {session_id}: {str(e)}")
        yield f"data: {json.dumps({'text': f'Error: {str(e)}', 'done': True})}\n\n"

@app.get("/", response_class=HTMLResponse)
async def ui(request: Request):
    return templates.get_template("index.html").render({"request": request, "models": RECOMMENDED_MODELS})

@app.post("/ask")
async def ask(request: Request):
    body = await request.json()
    query = body.get("query", "")
    speed = float(body.get("speed", 1.0))
    voice = body.get("voice", "rachel")
    session_id = body.get("session", "default")
    password = body.get("password")
    model = body.get("model")  # New: model from UI
    translated = translate_to_en(query)
    return StreamingResponse(
        stream_response(translated, speed, voice, session_id, password, model),
        media_type="text/event-stream"
    )

@app.get("/history/{session_id}")
async def get_history(session_id: str, password: str = None):
    check_password(password)
    history = load_chat(session_id)
    return {"history": history}

# ... (transcribe and export endpoints remain the same, with improved logging)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)