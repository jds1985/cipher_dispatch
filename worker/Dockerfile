FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    libsndfile1 \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY worker/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy core logic and worker entrypoint
COPY core/ /app/core/
COPY worker/handler.py /app/handler.py

CMD ["python3", "-u", "handler.py"]
