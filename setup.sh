#!/bin/bash

echo "Jetson Orin Nano Setup for the Curious Frame"
echo "============================================"

# Check if running on Jetson
if [[ $(uname -m) != "aarch64" ]]; then
    echo "Warning: This script is designed for ARM64 architecture (Jetson)"
    echo "Current architecture: $(uname -m)"
fi

# Install Ollama if not present
if ! command -v ollama &> /dev/null; then
    echo "Installing Ollama..."
    curl -fsSL https://ollama.ai/install.sh | sh
else
    echo "Ollama is already installed"
fi

echo "Building the docker containers... This may take a while."
docker compose build

DIR="$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Installing service..."
cat <<EOF > /tmp/curious_frame.sh
#!/bin/bash
cd ${DIR}
docker compose -f ${DIR}/docker-compose.yaml up
EOF
chmod +x /tmp/curious_frame.sh
sudo mv /tmp/curious_frame.sh /usr/local/bin/curious_frame.sh

echo "Setting up systemd service..."
sudo cp scripts/curious_frame.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable curious_frame.service
sudo systemctl start curious_frame.service
sudo systemctl status curious_frame.service

# Test Ollama connection
echo "Testing Ollama installation..."
if curl -s http://127.0.0.1:11434/api/tags > /dev/null; then
    echo "Ollama server is running"
    ollama pull hf.co/unsloth/gemma-3n-E2B-it-GGUF:Q4_K_M
else
    echo "Ollama server is not running"
    echo "Please execute the following command:"
    echo "1. ollama serve"
    echo "2. ollama pull hf.co/unsloth/gemma-3n-E2B-it-GGUF:Q4_K_M"
fi
