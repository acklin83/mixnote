FROM mwader/static-ffmpeg:8.1.2 AS ffmpeg

FROM python:3.12-slim

WORKDIR /app

# Static ffmpeg + ffprobe binaries — avoids apt's huge ffmpeg dependency tree
# (hundreds of packages, very slow to "Setting up" on a NAS). Multi-arch image.
COPY --from=ffmpeg /ffmpeg /ffprobe /usr/local/bin/

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--timeout-keep-alive", "75"]
