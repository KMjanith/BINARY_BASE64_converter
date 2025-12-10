#!/bin/bash

# Universal File Operator Service Manager
# Usage: ./service.sh {start|stop|restart|status}

APP_DIR="/opt/universal-file-operator"
PID_FILE="$HOME/.universal-file-operator.pid"
LOG_FILE="$HOME/.universal-file-operator.log"

# Function to show notification
notify() {
    if command -v notify-send &> /dev/null; then
        notify-send "Universal File Operator" "$1" --expire-time=3000 2>/dev/null || echo "Notification: $1"
    else
        echo "Notification: $1"
    fi
}

# Function to check if app is running
is_running() {
    # Check PID file first
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if ps -p $PID > /dev/null 2>&1; then
            return 0
        else
            # Remove stale PID file
            rm -f "$PID_FILE"
        fi
    fi
    
    # Check by process name as fallback
    PIDS=$(pgrep -f "src/web/app.py" 2>/dev/null || true)
    if [ -n "$PIDS" ]; then
        # Save the first PID we find
        echo "$(echo $PIDS | cut -d' ' -f1)" > "$PID_FILE"
        return 0
    fi
    
    return 1
}

# Function to get status
status() {
    if is_running; then
        PID=$(cat "$PID_FILE")
        echo "✅ Universal File Operator is running (PID: $PID)"
        
        # Try to get the port
        PORT=$(lsof -p $PID -i TCP 2>/dev/null | grep LISTEN | awk '{print $9}' | cut -d: -f2 | head -1)
        if [ -n "$PORT" ]; then
            echo "🌐 Web interface: http://127.0.0.1:$PORT"
        else
            echo "🌐 Web interface: http://127.0.0.1:5000 (default)"
        fi
        return 0
    else
        echo "❌ Universal File Operator is not running"
        return 1
    fi
}

# Function to start the application
start() {
    if is_running; then
        echo "⚠️  Universal File Operator is already running"
        status
        return 1
    fi
    
    echo "🚀 Starting Universal File Operator..."
    notify "Starting Universal File Operator..."
    
    if [ -f "$APP_DIR/launch.sh" ]; then
        "$APP_DIR/launch.sh" &
    else
        echo "❌ Launch script not found at $APP_DIR/launch.sh"
        return 1
    fi
    
    # Wait a moment and check if it started
    sleep 3
    if is_running; then
        echo "✅ Universal File Operator started successfully"
        status
    else
        echo "❌ Failed to start Universal File Operator"
        return 1
    fi
}

# Function to stop the application
stop() {
    echo "🛑 Stopping Universal File Operator..."
    
    # Use the dedicated stop script for robust stopping
    if [ -f "$APP_DIR/stop.sh" ]; then
        "$APP_DIR/stop.sh"
    else
        # Fallback method if stop script not found
        if ! is_running; then
            echo "⚠️  Universal File Operator is not running"
            return 1
        fi
        
        PID=$(cat "$PID_FILE")
        notify "Stopping Universal File Operator..."
        
        # Graceful shutdown
        kill -TERM $PID 2>/dev/null || true
        
        # Wait for process to stop
        for i in {1..10}; do
            if ! ps -p $PID > /dev/null 2>&1; then
                break
            fi
            sleep 1
        done
        
        # Force kill if still running
        if ps -p $PID > /dev/null 2>&1; then
            echo "Force stopping..."
            kill -KILL $PID 2>/dev/null || true
        fi
        
        # Clean up
        rm -f "$PID_FILE"
        
        echo "✅ Universal File Operator stopped"
        notify "Universal File Operator stopped"
    fi
    rm -f "$PID_FILE"
    
    echo "✅ Universal File Operator stopped"
    notify "Universal File Operator stopped"
}

# Function to restart
restart() {
    echo "🔄 Restarting Universal File Operator..."
    stop
    sleep 2
    start
}

# Main script logic
case "$1" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    restart)
        restart
        ;;
    status)
        status
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|status}"
        echo
        echo "Commands:"
        echo "  start   - Start the Universal File Operator"
        echo "  stop    - Stop the Universal File Operator"
        echo "  restart - Restart the Universal File Operator"
        echo "  status  - Show current status"
        exit 1
        ;;
esac

exit $?