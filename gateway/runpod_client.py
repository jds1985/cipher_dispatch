import os
import requests
from dotenv import load_dotenv

load_dotenv()

RUNPOD_API_KEY = os.getenv("RUNPOD_API_KEY")
RUNPOD_ENDPOINT_ID = os.getenv("RUNPOD_ENDPOINT_ID")

def query_runpod_worker(audio_base64: str, trade_context: str = "hvac") -> dict:
    """
    Sends base64 audio to RunPod Serverless API endpoint.
    Returns transcript, AI response text, and extracted ticket details.
    """
    if not RUNPOD_API_KEY or not RUNPOD_ENDPOINT_ID:
        # Development fallback when keys are not yet configured
        return {
            "status": "mock",
            "reply_text": "Thank you for the details. Is the breaker for the unit switched on?",
            "ticket_data": {
                "symptom": "diagnostic turn in progress",
                "urgency": "standard"
            }
        }

    url = f"https://api.runpod.ai/v2/{RUNPOD_ENDPOINT_ID}/runsync"
    headers = {
        "Authorization": f"Bearer {RUNPOD_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "input": {
            "audio": audio_base64,
            "trade_context": trade_context
        }
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get("output", {})
    except Exception as e:
        print(f"[RunPod Client] Request error: {e}")
        return {"error": str(e)}
