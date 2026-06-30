#!/bin/bash
set -e

REPO="https://github.com/dsribalaji/audiobook.git"
INSTALL_DIR="$HOME/.audiobook-skill"

echo "=== Book to Audiobook Installer ==="
echo ""

# Clone or update
if [ -d "$INSTALL_DIR" ]; then
    echo "Updating existing install at $INSTALL_DIR..."
    cd "$INSTALL_DIR"
    git pull --quiet
else
    echo "Cloning to $INSTALL_DIR..."
    git clone --quiet "$REPO" "$INSTALL_DIR"
    cd "$INSTALL_DIR"
fi

# Setup venv
echo "Setting up Python environment..."
bash scripts/setup.sh

# Install opencode command if opencode config exists
if [ -d "$HOME/.config/opencode" ]; then
    echo "Detected opencode. Installing /audiobook command..."
    mkdir -p "$HOME/.config/opencode/command"
    cp "$INSTALL_DIR/command/audiobook.md" "$HOME/.config/opencode/command/audiobook.md"
    echo "  -> /audiobook command installed"
fi

echo ""
echo "=== Done ==="
echo ""
echo "Usage:"
echo "  opencode:  type /audiobook"
echo "  manual:    cd $INSTALL_DIR && source .venv/bin/activate"
echo "  agent:     point your agent at $INSTALL_DIR/SKILL.md"
echo ""
echo "Output will be in: $INSTALL_DIR/output/<book-name>/"
