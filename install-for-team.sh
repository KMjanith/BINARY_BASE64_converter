#!/bin/bash

# Universal File Operator - Team Distribution Script
# Run this on Ubuntu 24.04 systems to install the application

set -e

PACKAGE_NAME="universal-file-operator_1.0.0_all.deb"
APP_NAME="Universal File Operator"

echo "🚀 $APP_NAME Installation Script"
echo "================================"

# Check if running on Ubuntu
if ! lsb_release -d | grep -q "Ubuntu"; then
    echo "⚠️  Warning: This package is designed for Ubuntu. Continuing anyway..."
fi

# Check if package file exists
if [ ! -f "$PACKAGE_NAME" ]; then
    echo "❌ Package file '$PACKAGE_NAME' not found!"
    echo "Please ensure the .deb file is in the current directory."
    exit 1
fi

echo "📦 Found package: $PACKAGE_NAME"

# Check if already installed
if dpkg -l | grep -q universal-file-operator; then
    echo "🔄 $APP_NAME is already installed. Upgrading..."
    sudo dpkg -i "$PACKAGE_NAME"
else
    echo "🆕 Installing $APP_NAME..."
    sudo dpkg -i "$PACKAGE_NAME"
fi

# Fix any dependency issues
echo "🔧 Fixing dependencies..."
sudo apt-get install -f -y

echo ""
echo "✅ $APP_NAME installed successfully!"
echo ""
echo "🎯 How to use:"
echo "  1. Open Applications → Office → Universal File Operator"
echo "  2. Or run: /opt/universal-file-operator/launch.sh"
echo "  3. The app will open in your web browser automatically"
echo ""
echo "📋 Features:"
echo "  • File format conversions (70+ combinations)"
echo "  • PDF merging with drag-and-drop reordering"
echo "  • Image format conversions"
echo "  • Hash generation and verification"
echo "  • Data format conversions (JSON, CSV, XML, YAML)"
echo ""
echo "🔧 Troubleshooting:"
echo "  • Logs: tail -f ~/.universal-file-operator.log"
echo "  • Manual start: /opt/universal-file-operator/launch.sh"
echo "  • Uninstall: sudo dpkg -r universal-file-operator"
echo ""
echo "🎉 Ready to use! Enjoy $APP_NAME!"