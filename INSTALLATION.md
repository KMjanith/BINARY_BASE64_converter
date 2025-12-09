# Universal File Operator - Ubuntu 24 Installation Package

## 📦 Installation

### For Team Distribution

1. **Download the package**: `universal-file-operator_1.0.0_all.deb`

2. **Install the package**:
   ```bash
   sudo dpkg -i universal-file-operator_1.0.0_all.deb
   ```

3. **If there are dependency issues, fix them**:
   ```bash
   sudo apt-get install -f
   ```

## 🚀 Usage

### Method 1: Desktop Application
- Open **Applications** menu
- Go to **Office** category  
- Click **Universal File Operator**
- The application will open in your default browser

### Method 2: Command Line
```bash
/opt/universal-file-operator/launch.sh
```

### Method 3: Create Desktop Shortcut
The application automatically creates a desktop entry, but you can also:
1. Right-click on desktop
2. Create new launcher
3. Use command: `/opt/universal-file-operator/launch.sh`

## ✨ Features

- **🔄 Format Conversions**: 70+ combinations including text, binary, base64, hex
- **🖼️ Image Conversions**: PNG, JPEG, GIF, BMP, TIFF, WebP, ICO
- **📄 PDF Merger**: Merge PDFs with preview and drag-drop reordering
- **🔐 Hash Functions**: MD5, SHA1, SHA256, SHA512
- **📊 Data Formats**: JSON, CSV, YAML, XML conversions
- **🔢 Number Bases**: Decimal, Binary, Hex, Octal conversions

## 🌐 Access

The application runs as a web interface accessible at `http://localhost:5000` (or next available port).

## 🛠️ Troubleshooting

### Application Won't Start
1. Check logs: `tail -f ~/.universal-file-operator.log`
2. Manually install dependencies: `sudo apt install python3 python3-pip python3-venv`
3. Restart: `/opt/universal-file-operator/launch.sh`

### Port Already in Use
The launcher automatically finds an available port (5000-5099). Check the log file for the actual port being used.

### Browser Doesn't Open
Manually navigate to: `http://localhost:5000` (or check log for actual port)

## 🗑️ Uninstallation

```bash
sudo dpkg -r universal-file-operator
```

## 📁 File Locations

- **Application**: `/opt/universal-file-operator/`
- **Desktop Entry**: `/usr/share/applications/universal-file-operator.desktop`
- **Icon**: `/usr/share/pixmaps/universal-file-operator.png`
- **Logs**: `~/.universal-file-operator.log`

## 🔧 System Requirements

- **OS**: Ubuntu 24.04 LTS (compatible with most Debian-based systems)
- **Python**: 3.8+
- **Memory**: 512MB RAM minimum
- **Disk**: 100MB available space
- **Browser**: Any modern web browser

## 💡 Tips

- The application creates its own virtual environment for isolation
- First run may take longer as it installs dependencies
- The application automatically opens in your default browser
- Multiple instances can run on different ports
- All conversions are processed locally (no internet required)

---

**Universal File Operator** - Your complete file conversion and PDF merging solution for Ubuntu!