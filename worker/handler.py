import os
import sys
import base64
import tempfile
import runpod
from faster_whisper import WhisperModel
from core.triage_rules import evaluate_emergency
from core.profile_loader import load_trade_profile

device = "cuda" if os.getenv("CUDA_VISIBLE_DEVICES") else "cpu"
compute_type = "float16" if device == "cuda" else "int8"
print(f"[Worker] Loading Faster-Whisper on {device} ({compute_type})...")
model = WhisperModel("base.en", device=device, compute_type=compute_type)
print("[Worker] Audio engine ready.")

def transcribe_audio_payload(audio_b64: str) -> str:
    try:
        audio_bytes = base64.b64decode(audio_b64)
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=True) as temp_audio:
            temp_audio.write(audio_bytes)
            temp_audio.flush()
            segments, _ = model.transcribe(temp_audio.name, beam_size=5)
            return " ".join([s.text for s in segments]).strip()
    except Exception as e:
        print(f"[Worker Error] Transcription failed: {e}")
        return ""

def process_call_turn(transcript: str, trade_context: str = "hvac") -> dict:
    profile = load_trade_profile(trade_context)
    triage = evaluate_emergency(transcript, trade_context)
    reply_text = f"Thanks for calling. We noted: '{transcript}'. Let us get an emergency technician dispatched right away." if triage["urgency"] == "critical" else f"Thanks for reaching out about {trade_context}. We have logged your request."
    return {
        "transcript": transcript,
        "reply_text": reply_text,
        "triage": triage
    }

def handler(job):
    job_input = job.get("input", {})
    audio_payload = job_input.get("audio")
    trade_context = job_input.get("trade_context", "hvac")

    if not audio_payload:
        return {"error": "Missing audio in request payload"}

    transcript = transcribe_audio_payload(audio_payload)
    if not transcript:
        return {
            "transcript": "",
            "reply_text": "I didn't catch that. Could you repeat the issue?",
            "triage": {"urgency": "standard"}
        }

    return process_call_turn(transcript, trade_context)

if ___name__ == "__main__":
    runpod.serverless.start({"handler": handler})
