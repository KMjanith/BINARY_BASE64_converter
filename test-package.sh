#!/bin/bash

# Test script for Universal File Operator .deb package

echo "🧪 Testing Universal File Operator .deb Package"
echo "=============================================="

# Check if package file exists
if [ ! -f "universal-file-operator_1.0.0_all.deb" ]; then
    echo "❌ Package file not found!"
    exit 1
fi

echo "✅ Package file exists"

# Check package contents
echo "📦 Package contents:"
dpkg-deb -c universal-file-operator_1.0.0_all.deb

echo ""
echo "📋 Package information:"
dpkg-deb -I universal-file-operator_1.0.0_all.deb

echo ""
echo "🔍 Package validation:"
# Check if package is valid
if dpkg-deb --fsys-tarfile universal-file-operator_1.0.0_all.deb > /dev/null 2>&1; then
    echo "✅ Package structure is valid"
else
    echo "❌ Package structure is invalid"
    exit 1
fi

echo ""
echo "🚀 Ready for installation!"
echo "To install: sudo dpkg -i universal-file-operator_1.0.0_all.deb"
echo "To test: sudo dpkg -i universal-file-operator_1.0.0_all.deb && /opt/universal-file-operator/launch.sh"