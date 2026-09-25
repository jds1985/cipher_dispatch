import os
import json
import base64
from fastapi import FastAPI, WebSocket, Request, Response
from dotenv import load_dotenv
from gateway.session_manager import get_or_create_session, close_session
from gateway.runpod_client import query_runpod_worker
from integrations.twilio_sms import send_tech_dispatch_sms

load_dotenv()

app = FastAPI()
TECH_PHONE = os.getenv("TEST_TECH_PHONE")

@app.get("/")
async def root():
    return {"status": "online", "service": "cipher-dispatch-gateway"}

@app.post("/voice")
async def voice_handler(request: Request):
    host = request.headers.get("host")
    twiml_response = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="Polly.Matthew">Thanks for calling emergency dispatch. Please describe your issue.</Say>
    <Connect>
        <Stream url="wss://{host}/media-stream" />
    </Connect>
</Response>"""
    return Response(content=twiml_response, media_type="application/xml")

@app.websocket("/media-stream")
async def media_stream_handler(websocket: WebSocket):
    await websocket.accept()
    print("[Gateway] Live call stream connected.")
    session = None

    try:
        while True:
            message = await websocket.receive_text()
            data = json.loads(message)
            event = data.get("event")

            if event == "start":
                stream_sid = data["start"]["streamSid"]
                call_sid = data["start"]["callSid"]
                session = get_or_create_session(stream_sid, call_sid)
                print(f"[Gateway] Call started: {stream_sid}")

            elif event == "media":
                if session:
                    # Accumulate incoming audio bytes
                    chunk = base64.b64decode(data["media"]["payload"])
                    session.append_audio(chunk)

            elif event == "stop":
                if session:
                    print(f"[Gateway] Call ended. Dispatched ticket summary.")
                    if TECH_PHONE:
                        send_tech_dispatch_sms(TECH_PHONE, session.ticket)
                    close_session(session.stream_sid)
                break

    except Exception as e:
        print(f"[Gateway] Streaming exception: {e}")
    finally:
        print("[Gateway] Stream connection closed.")
