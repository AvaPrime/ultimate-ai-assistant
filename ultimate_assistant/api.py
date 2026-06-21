import os, base64, json, datetime
from pathlib import Path
from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import httpx
from deep_translator import GoogleTranslator
import redis
from .agent import create_agent
from .config import config

app = FastAPI(title="Ultimate AI Assistant")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

agent = create_agent()

# Redis for persistent chat history (works on Vercel with Upstash)
redis_client = None
if config.redis_url:
    try:
        redis_client = redis.from_url(config.redis_url, decode_responses=True)
    except Exception as e:
        print(f"Redis connection failed: {e}")

HISTORY_DIR = Path("/tmp/chat_history")
HISTORY_DIR.mkdir(exist_ok=True)

VOICES = {
    "rachel": {"id": "21m00Tcm4TlvDq8ikWAM", "name": "Rachel (EN)"},
    "antoni": {"id": "ErXwobaYiN019PkySvjV", "name": "Antoni (EN)"},
    "pablo":  {"id": "pNInz6obpgDQGcFmaJgB", "name": "Pablo (ES)"},
    "isabella": {"id": "AZpi6D2D7e6D6rD8lB3M", "name": "Isabella (ES)"},
    "thomas":  {"id": "GBv7mTt0atIp3Br8iC1J", "name": "Thomas (FR)"},
    "claire":  {"id": "g5Ciwnk5IM4p1n9qM7vL", "name": "Claire (FR)"},
    "hans":    {"id": "VR3W4z3z3z3z3z3z3z3z", "name": "Hans (DE)"},
    "anna":    {"id": "EXAVITQu4vr4xnSDxMaL", "name": "Anna (DE)"},
    "li":      {"id": "IKne3meIYcWjH8u1tKkJ", "name": "Li (ZH)"},
    "yuki":    {"id": "TxGEqnHWrfWFTfGW9XjX", "name": "Yuki (JA)"}
}

# Password protection (optional)
def check_password(pw: str):
    if config.access_password and pw != config.access_password:
        raise HTTPException(status_code=401, detail="Invalid password")

# === Chat History (Redis or File) ===
def save_chat(session_id: str, user_msg: str, ai_msg: str, audio_b64: str = None):
    entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "user": user_msg,
        "ai": ai_msg,
        "audio": audio_b64
    }
    if redis_client:
        key = f"chat:{session_id}"
        existing = redis_client.get(key)
        data = json.loads(existing) if existing else []
        data.append(entry)
        redis_client.set(key, json.dumps(data))
    else:
        file = HISTORY_DIR / f"{session_id}.json"
        data = []
        if file.exists():
            data = json.loads(file.read_text())
        data.append(entry)
        file.write_text(json.dumps(data, indent=2))

def load_chat(session_id: str):
    if redis_client:
        key = f"chat:{session_id}"
        data = redis_client.get(key)
        return json.loads(data) if data else []
    else:
        file = HISTORY_DIR / f"{session_id}.json"
        if file.exists():
            return json.loads(file.read_text())
        return []

# === Translate, TTS, Stream ===
def translate_to_en(text: str) -> str:
    try:
        detected = GoogleTranslator(source='auto', target='en').detect(text)
        if detected != 'en':
            return GoogleTranslator(source='auto', target='en').translate(text)
    except:
        pass
    return text

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

async def stream_response(query: str, speed: float, voice: str, session_id: str, password: str = None):
    check_password(password)
    full_text = ""
    async for chunk in agent.astream({"input": query}):
        text = chunk.get("output", "")
        full_text += text
        yield f"data: {json.dumps({'text': text, 'done': False})}\n\n"
    audio_b64 = await tts(full_text, speed, voice)
    save_chat(session_id, query, full_text, audio_b64)
    yield f"data: {json.dumps({'text': '', 'audio': audio_b64, 'done': True})}\n\n"

@app.get("/", response_class=HTMLResponse)
async def ui(request: Request):
    return templates.get_template("index.html").render({"request": request})

@app.post("/ask")
async def ask(request: Request):
    body = await request.json()
    query = body.get("query", "")
    speed = float(body.get("speed", 1.0))
    voice = body.get("voice", "rachel")
    session_id = body.get("session", "default")
    password = body.get("password")
    translated = translate_to_en(query)
    return StreamingResponse(
        stream_response(translated, speed, voice, session_id, password),
        media_type="text/event-stream"
    )

@app.post("/transcribe")
async def transcribe(audio: str = Form(...)):
    b64_data = audio.split(",", 1)[1]
    with open("/tmp/temp.webm", "wb") as f:
        f.write(base64.b64decode(b64_data))
    with open("/tmp/temp.webm", "rb") as f:
        resp = httpx.post(
            "https://api.openai.com/v1/audio/transcriptions",
            headers={"Authorization": f"Bearer {config.openai_key}"},
            files={"file": ("audio.webm", f, "audio/webm")},
            data={"model": "whisper-1"}
        )
    return {"text": resp.json()["text"]}

@app.get("/export/{session_id}")
async def export_chat(session_id: str, password: str = None):
    check_password(password)
    if redis_client:
        key = f"chat:{session_id}"
        data = redis_client.get(key)
        content = data if data else "[]"
    else:
        file = HISTORY_DIR / f"{session_id}.json"
        content = file.read_text() if file.exists() else "[]"
    return StreamingResponse(
        iter([content]),
        media_type="application/json",
        headers={"Content-Disposition": f"attachment; filename={session_id}.json"}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)