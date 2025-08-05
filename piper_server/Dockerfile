ARG BASE_IMAGE=dustynv/piper-tts:r36.4.0-cu128-24.04
FROM ${BASE_IMAGE}

LABEL maintainer="Frédéric Collonval <frederic.collonval@webscit.com>"

# Download voice models
RUN mkdir -p /data/piper/models && \
    wget https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/lessac/high/en_US-lessac-high.onnx.json -O /data/piper/models/en_US-lessac-high.onnx.json && \
    wget https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/lessac/high/en_US-lessac-high.onnx -O /data/piper/models/en_US-lessac-high.onnx && \
    wget https://huggingface.co/rhasspy/piper-voices/resolve/main/fr/fr_FR/upmc/medium/fr_FR-upmc-medium.onnx.json -O /data/piper/models/fr_FR-upmc-medium.onnx.json && \
    wget https://huggingface.co/rhasspy/piper-voices/resolve/main/fr/fr_FR/upmc/medium/fr_FR-upmc-medium.onnx -O /data/piper/models/fr_FR-upmc-medium.onnx

# Install custom Python script
COPY http_server.py /data/piper/models/http_server.py

WORKDIR /data/piper/models

EXPOSE 5000
CMD ["python3", "http_server.py", "--host", "0.0.0.0", "--port", "5000", "--model", "/data/piper/models/en_US-lessac-high.onnx", "--data-dir", "/data/piper/models"]
