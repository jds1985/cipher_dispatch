import time

class CallSession:
    def __init__(self, stream_sid: str, call_sid: str):
        self.stream_sid = stream_sid
        self.call_sid = call_sid
        self.start_time = time.time()
        self.audio_buffer = bytearray()
        self.transcript = []
        self.ticket = {
            "customer_name": "Pending",
            "phone": "Pending",
            "address": "Pending",
            "equipment": "Pending",
            "symptom": "Pending",
            "urgency": "standard"
        }

    def append_audio(self, chunk: bytes):
        self.audio_buffer.extend(chunk)

    def clear_buffer(self):
        self.audio_buffer.clear()

active_sessions: dict[str, CallSession] = {}

def get_or_create_session(stream_sid: str, call_sid: str = None) -> CallSession:
    if stream_sid not in active_sessions:
        active_sessions[stream_sid] = CallSession(stream_sid, call_sid or stream_sid)
    return active_sessions[stream_sid]

def close_session(stream_sid: str):
    if stream_sid in active_sessions:
        del active_sessions[stream_sid]
