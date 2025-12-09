#!/bin/bash

# Universal File Operator Launch Script
# This script sets up the environment and starts the application

set -e

APP_DIR="/opt/universal-file-operator"
VENV_DIR="$APP_DIR/venv"
LOG_FILE="$HOME/.universal-file-operator.log"

# Function to log messages
log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" >> "$LOG_FILE"
}

# Function to show notification
notify() {
    if command -v notify-send &> /dev/null; then
        notify-send "Universal File Operator" "$1" --icon="$APP_DIR/universal-file-operator.png" --expire-time=3000 2>/dev/null || \
        notify-send "Universal File Operator" "$1" 2>/dev/null || \
        echo "Notification: $1"
    else
        echo "Notification: $1"
    fi
}

# Function to check if port is available
is_port_available() {
    ! nc -z localhost $1 2>/dev/null
}

# Function to find available port
find_available_port() {
    local port=5000
    while ! is_port_available $port && [ $port -lt 5100 ]; do
        port=$((port + 1))
    done
    echo $port
}

# Change to application directory
cd "$APP_DIR"

log "Starting Universal File Operator..."

# Check if virtual environment exists, create if not
if [ ! -d "$VENV_DIR" ]; then
    log "Creating virtual environment..."
    notify "Setting up Universal File Operator for first run..."
    python3 -m venv "$VENV_DIR"
fi

# Activate virtual environment
source "$VENV_DIR/bin/activate"

# Install/update dependencies
log "Installing dependencies..."
pip install --quiet --upgrade pip
pip install --quiet -r requirements.txt

# Find available port
PORT=$(find_available_port)
log "Using port: $PORT"

# Export environment variables
export FLASK_ENV=production
export FLASK_HOST=127.0.0.1
export FLASK_PORT=$PORT

# Start the application
log "Launching web interface on http://127.0.0.1:$PORT"
notify "Universal File Operator is starting..."

# Open browser after a short delay
(sleep 3 && xdg-open "http://127.0.0.1:$PORT" &) &

# Start the Flask application
python3 src/web/app.py >> "$LOG_FILE" 2>&1 &
APP_PID=$!

# Save PID for cleanup
echo $APP_PID > "$HOME/.universal-file-operator.pid"

log "Application started with PID: $APP_PID"
notify "Universal File Operator is ready! Opening in browser..."

# Wait for the application
wait $APP_PID