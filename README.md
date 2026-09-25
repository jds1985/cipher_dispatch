# Cipher Dispatch (MEP Emergency Voice Agent)

An intelligent, low-latency after-hours dispatch voice agent built for MEP contractors (HVAC, Plumbing, Electrical).

## Architecture
- **Gateway (`gateway/`):** FastAPI WebSocket server handling bi-directional audio streaming with Twilio Media Streams.
- **Worker (`worker/`):** Dockerized RunPod Serverless container executing STT, trade reasoning, and TTS.
- **Core (`core/`):** Dynamic trade configurations, triage decision engine, and JSON profile loaders.
- **Integrations (`integrations/`):** Instant on-call technician SMS alerts and CRM webhook dispatchers.

## Quickstart

1. Configure `.env`:
   ```bash
   cp .env.example .env
pip install -r gateway/requirements.txt

