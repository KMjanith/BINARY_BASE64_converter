#!/bin/bash

# Universal File Operator Stop Script
# Gracefully stops the application using multiple methods

set -e

PID_FILE="$HOME/.universal-file-operator.pid"
LOG_FILE="$HOME/.universal-file-operator.log"

# Function to log messages
log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" >> "$LOG_FILE"
}

# Function to show notification
notify() {
    if command -v notify-send &> /dev/null; then
        notify-send "Universal File Operator" "$1" --expire-time=3000 2>/dev/null || \
        echo "Notification: $1"
    else
        echo "Notification: $1"
    fi
}

# Function to kill processes by port
kill_by_port() {
    local port=$1
    echo "Checking for processes on port $port..."
    PIDS=$(lsof -ti:$port 2>/dev/null || true)
    if [ -n "$PIDS" ]; then
        echo "Found processes on port $port: $PIDS"
        for pid in $PIDS; do
            if ps -p $pid > /dev/null 2>&1; then
                echo "Stopping process $pid on port $port"
                kill -TERM $pid 2>/dev/null || true
                sleep 1
                # Force kill if still running
                if ps -p $pid > /dev/null 2>&1; then
                    kill -KILL $pid 2>/dev/null || true
                fi
            fi
        done
        return 0
    fi
    return 1
}

# Function to kill processes by name
kill_by_name() {
    echo "Searching for Universal File Operator processes..."
    PIDS=$(pgrep -f "src/web/app.py" 2>/dev/null || true)
    if [ -n "$PIDS" ]; then
        echo "Found Universal File Operator processes: $PIDS"
        for pid in $PIDS; do
            if ps -p $pid > /dev/null 2>&1; then
                echo "Stopping process $pid"
                kill -TERM $pid 2>/dev/null || true
                sleep 1
                # Force kill if still running
                if ps -p $pid > /dev/null 2>&1; then
                    kill -KILL $pid 2>/dev/null || true
                fi
            fi
        done
        return 0
    fi
    return 1
}

echo "Stopping Universal File Operator..."
log "Stop command initiated"

STOPPED=false

# Method 1: Try using saved PID file
if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    echo "Found PID file with PID: $PID"
    
    # Check if process is running
    if ps -p $PID > /dev/null 2>&1; then
        log "Stopping application with PID: $PID"
        notify "Stopping Universal File Operator..."
        
        # Try graceful shutdown first
        kill -TERM $PID 2>/dev/null || true
        
        # Wait for process to stop
        for i in {1..5}; do
            if ! ps -p $PID > /dev/null 2>&1; then
                STOPPED=true
                break
            fi
            sleep 1
        done
        
        # Force kill if still running
        if ! $STOPPED && ps -p $PID > /dev/null 2>&1; then
            log "Process still running, forcing shutdown..."
            kill -KILL $PID 2>/dev/null || true
            STOPPED=true
        fi
        
        # Remove PID file
        rm -f "$PID_FILE"
        
        if $STOPPED; then
            log "Application stopped successfully using PID"
            notify "Universal File Operator stopped"
            echo "✅ Application stopped successfully (PID method)"
            exit 0
        fi
    else
        echo "⚠️  Process with PID $PID not found, removing stale PID file"
        rm -f "$PID_FILE"
    fi
fi

# Method 2: Try killing by port 5000
if kill_by_port 5000; then
    STOPPED=true
    log "Application stopped using port method"
    notify "Universal File Operator stopped"
    echo "✅ Application stopped successfully (Port method)"
    exit 0
fi

# Method 3: Try killing by process name
if kill_by_name; then
    STOPPED=true
    log "Application stopped using process name method"
    notify "Universal File Operator stopped"
    echo "✅ Application stopped successfully (Process name method)"
    exit 0
fi

# Method 4: Check other common ports
for port in 5001 5002 5003 5004 5005; do
    if kill_by_port $port; then
        STOPPED=true
        log "Application stopped from port $port"
        notify "Universal File Operator stopped"
        echo "✅ Application stopped successfully (Port $port method)"
        exit 0
    fi
done

if ! $STOPPED; then
    echo "❌ No Universal File Operator processes found"
    log "Stop command completed - no processes found"
    exit 1
fi