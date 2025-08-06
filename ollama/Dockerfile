ARG BASE_IMAGE=dustynv/ollama:r36.4.0
FROM ${BASE_IMAGE}

LABEL maintainer="Frédéric Collonval <frederic.collonval@webscit.com>"

# Install Ollama models
RUN ollama serve & sleep 5s && \
    ollama pull hf.co/unsloth/gemma-3n-E2B-it-GGUF:Q4_K_M

EXPOSE 11434

CMD /start_ollama && sleep infinity
