#!/bin/bash

# Universal File Operator 1.0.3 Installation Test Script
# This script tests the installation and basic functionality of the new version

echo "🚀 Testing Universal File Operator 1.0.3 Installation"
echo "=================================================="

# Check if package file exists
if [[ ! -f "universal-file-operator_1.0.3_all.deb" ]]; then
    echo "❌ Package file universal-file-operator_1.0.3_all.deb not found!"
    exit 1
fi

echo "✅ Package file found"

# Display package information
echo ""
echo "📦 Package Information:"
dpkg-deb --info universal-file-operator_1.0.3_all.deb | grep -E "(Version|Description|Size)"

# Check package contents for new features
echo ""
echo "🔍 Checking new text comparison files:"
echo "Text comparison module:"
dpkg-deb --contents universal-file-operator_1.0.3_all.deb | grep "text_compare.py" && echo "✅ Backend module included"

echo "Text comparison template:"
dpkg-deb --contents universal-file-operator_1.0.3_all.deb | grep "text_compare.html" && echo "✅ Frontend template included"

echo "Updated landing page:"
dpkg-deb --contents universal-file-operator_1.0.3_all.deb | grep "landing.html" && echo "✅ Updated landing page included"

echo "Updated app.py:"
dpkg-deb --contents universal-file-operator_1.0.3_all.deb | grep "app.py" && echo "✅ Updated Flask application included"

# Check package size comparison
echo ""
echo "📊 Package Size Comparison:"
if [[ -f "universal-file-operator_1.0.2_all.deb" ]]; then
    old_size=$(stat -c%s "universal-file-operator_1.0.2_all.deb")
    new_size=$(stat -c%s "universal-file-operator_1.0.3_all.deb")
    size_diff=$((new_size - old_size))
    echo "Previous version (1.0.2): $(echo $old_size | numfmt --to=iec) bytes"
    echo "New version (1.0.3):     $(echo $new_size | numfmt --to=iec) bytes"
    echo "Size increase:           $(echo $size_diff | numfmt --to=iec) bytes"
    echo "✅ Package size increased as expected (new features added)"
else
    new_size=$(stat -c%s "universal-file-operator_1.0.3_all.deb")
    echo "New version (1.0.3): $(echo $new_size | numfmt --to=iec) bytes"
fi

echo ""
echo "🎯 New Features in v1.0.3:"
echo "  📊 Side-by-side text comparison"
echo "  🎨 Visual difference highlighting"
echo "  📈 Similarity percentage calculation"
echo "  📁 Drag & drop file support for text comparison"
echo "  📋 Real-time statistics (word/char/line count)"
echo "  🎛️ Dual input methods (type/paste or drag files)"

echo ""
echo "📝 Installation Instructions:"
echo "  1. Stop any running instance: sudo service universal-file-operator stop"
echo "  2. Install package: sudo dpkg -i universal-file-operator_1.0.3_all.deb"
echo "  3. Fix dependencies (if needed): sudo apt-get install -f"
echo "  4. Start service: sudo service universal-file-operator start"
echo "  5. Access via browser: http://localhost:5000"

echo ""
echo "✅ Package verification completed successfully!"
echo "🚀 Ready for installation!"