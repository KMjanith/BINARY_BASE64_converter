#!/bin/bash

# Simple Universal File Operator Launcher
# Provides clear feedback and reliable startup

INSTALL_DIR="/opt/universal-file-operator"
VENV_DIR="$INSTALL_DIR/venv"

# Function to show user notification
show_notification() {
    echo "Universal File Operator: $1"
    # Try different notification methods
    if command -v notify-send >/dev/null 2>&1; then
        notify-send --expire-time=3000 "Universal File Operator" "$1" 2>/dev/null || true
    elif command -v zenity >/dev/null 2>&1; then
        zenity --info --text="Universal File Operator: $1" --timeout=3 2>/dev/null || true
    fi
}

# Change to install directory
cd "$INSTALL_DIR" || {
    show_notification "Failed to access installation directory"
    exit 1
}

show_notification "Starting application..."

# Activate virtual environment and start server
if [ -d "$VENV_DIR" ]; then
    source "$VENV_DIR/bin/activate"
    echo "Virtual environment activated"
else
    echo "Warning: Virtual environment not found, using system Python"
fi

# Start the Flask application
echo "Starting Universal File Operator on http://127.0.0.1:5000"
python3 -m src.web.app &

# Wait a moment for server to start
sleep 2

# Open browser
if command -v xdg-open >/dev/null 2>&1; then
    xdg-open "http://127.0.0.1:5000" >/dev/null 2>&1 &
elif command -v firefox >/dev/null 2>&1; then
    firefox "http://127.0.0.1:5000" >/dev/null 2>&1 &
elif command -v google-chrome >/dev/null 2>&1; then
    google-chrome "http://127.0.0.1:5000" >/dev/null 2>&1 &
fi

show_notification "Application started! Check your browser."

# Keep the script running
wait