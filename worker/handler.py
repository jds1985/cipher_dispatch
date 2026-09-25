import os
import json
import base64
import tempfile
import runpod
from faster_whisper import WhisperModel
from core.triage_rules import evaluate_emergency
from core.profile_loader import load_trade_profile

# 1. Load Whisper Model onto GPU (falls back to CPU if testing without CUDA)
device = "cuda" if os.getenv("CUDA_VISIBLE_DEVICES") else "cpu"
compute_type = "float16" if device == "cuda" else "int8"

print(f"[Worker] Loading Faster-Whisper on {device} ({compute_type})...")
model = WhisperModel("base.en", device=device, compute_type=compute_type)
print("[Worker] Audio engine ready.")

def transcribe_audio_payload(audio_b64: str) -> str:
    """Decodes base64 μ-law/wav and extracts transcript using Whisper."""
    try:
        audio_bytes = base64.b64decode(audio_b64)
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=True) as temp_audio:
            temp_audio.write(audio_bytes)
            temp_audio.flush()
            
            segments, _ = model.transcribe(temp_audio.name, beam_size=1)
            text = " ".join([segment.text for segment in segments]).strip()
            return text
    except Exception as e:
        print(f"[Worker STT Error] {e}")
        return ""

def process_call_turn(transcript: str, trade_context: str) -> dict:
    """
    Evaluates transcript using trade configuration and triage rules.
    """
    profile = load_trade_profile(trade_context)
    
    # Assess emergency criteria using the triage rules engine
    triage = evaluate_emergency(
        symptoms=[transcript],
        equipment_type="general",
        indoor_temp=None
    )
    
    # Basic conversational response heuristic
    if triage["urgency"] == "emergency":
        reply = "I understand this is an urgent situation. I'm tagging an emergency technician right now. Are you in a safe area?"
    else:
        reply = "Got it. I've noted those details. Could you please confirm your service address?"
        
    return {
        "transcript": transcript,
        "reply_text": reply,
        "triage": triage,
        "trade": trade_context
    }

def handler(job):
    """RunPod Serverless execution entrypoint"""
    job_input = job.get("input", {})
    audio_payload = job_input.get("audio")
    trade_context = job_input.get("trade_context", "hvac")

    if not audio_payload:
        return {"error": "Missing 'audio' in request payload"}

    transcript = transcribe_audio_payload(audio_payload)
    if not transcript:
        return {
            "transcript": "",
            "reply_text": "I didn't catch that. Could you repeat the issue?",
            "triage": {"urgency": "standard"}
        }

    return process_call_turn(transcript, trade_context)

if __name__ == "__main__":
    runpod.serverless.start({"handler": handler})
