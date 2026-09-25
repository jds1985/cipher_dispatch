import os
import json
import base64
from fastapi import FastAPI, WebSocket, Request, Response
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

@app.get("/")
async def root():
    return {"status": "online", "service": "cipher-dispatch-gateway"}

@app.post("/voice")
async def voice_handler(request: Request):
    host = request.headers.get("host")
    twiml_response = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say>Thank you for calling emergency dispatch. Connecting your line now.</Say>
    <Connect>
        <Stream url="wss://{host}/media-stream" />
    </Connect>
</Response>"""
    return Response(content=twiml_response, media_type="application/xml")

@app.websocket("/media-stream")
async def media_stream_handler(websocket: WebSocket):
    await websocket.accept()
    print("[Gateway] Twilio Media Stream connected.")
    try:
        while True:
            message = await websocket.receive_text()
            data = json.loads(message)
            event = data.get("event")

            if event == "start":
                print(f"[Gateway] Call started: {data['start']['streamSid']}")
            elif event == "media":
                pass  # Audio payload arrives here
            elif event == "stop":
                print("[Gateway] Call ended.")
                break
    except Exception as e:
        print(f"[Gateway] Stream error: {e}")
    finally:
        print("[Gateway] Stream closed.")
