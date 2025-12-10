#!/bin/bash

# Simple Universal File Operator Launcher
# Provides clear feedback and reliable startup

INSTALL_DIR="/opt/universal-file-operator"
VENV_DIR="$INSTALL_DIR/venv"
PID_FILE="$HOME/.universal-file-operator.pid"
LOG_FILE="$HOME/.universal-file-operator.log"

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

# Function to log messages
log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" >> "$LOG_FILE"
}

# Check if already running
if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    if ps -p $PID > /dev/null 2>&1; then
        show_notification "Application is already running (PID: $PID)"
        # Try to open browser to existing instance
        if command -v xdg-open >/dev/null 2>&1; then
            xdg-open "http://127.0.0.1:5000" >/dev/null 2>&1 &
        fi
        exit 0
    else
        # Remove stale PID file
        rm -f "$PID_FILE"
    fi
fi

# Change to install directory
cd "$INSTALL_DIR" || {
    show_notification "Failed to access installation directory"
    exit 1
}

show_notification "Starting application..."
log "Starting Universal File Operator via simple-start.sh"

# Activate virtual environment and start server
if [ -d "$VENV_DIR" ]; then
    source "$VENV_DIR/bin/activate"
    echo "Virtual environment activated"
else
    echo "Warning: Virtual environment not found, using system Python"
fi

# Start the Flask application
echo "Starting Universal File Operator on http://127.0.0.1:5000"
python3 -m src.web.app >> "$LOG_FILE" 2>&1 &
APP_PID=$!

# Save PID for stop script
echo $APP_PID > "$PID_FILE"
log "Application started with PID: $APP_PID"

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

# Keep the script running and wait for the application
wait $APP_PID