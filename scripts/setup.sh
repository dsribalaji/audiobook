#!/bin/bash
set -e
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_DIR"

if [ -d ".venv" ]; then
    echo "venv already exists. Installing deps..."
    source .venv/bin/activate
    pip install -r requirements.txt
    echo "Done."
    exit 0
fi

echo "Creating venv with uv..."
if command -v uv &> /dev/null; then
    uv venv .venv
    source .venv/bin/activate
    echo "Installing dependencies..."
    uv pip install -r requirements.txt
else
    python3 -m venv .venv
    source .venv/bin/activate
    echo "Installing dependencies..."
    pip install --upgrade pip
    pip install -r requirements.txt
fi

echo ""
echo "Setup complete."
echo "Activate with: source $PROJECT_DIR/.venv/bin/activate"
