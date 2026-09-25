FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app
ENV HF_HOME=/app/cache
ENV CTRANSLATE2_CACHE_DIR=/app/cache

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    libsndfile1 \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /app/cache && chmod -R 777 /app/cache

COPY worker/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY core/ /app/core/
COPY worker/handler.py /app/handler.py

CMD ["python3", "-u", "/app/handler.py"]
