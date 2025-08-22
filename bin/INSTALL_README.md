# mmcli Installation Guide

This guide explains how to install mmcli (multimedia CLI tool) on your system so you can use it from anywhere in your terminal.

## Quick Installation

### Windows
1. Double-click `install.bat` in the `bin/` folder
2. Wait for the installation to complete
3. The script will handle everything automatically

### Linux/macOS
1. Make the script executable: `chmod +x bin/install.sh`
2. Run: `./bin/install.sh`
3. Wait for the installation to complete

## What the Installation Does

The installation script will:
1. ✅ Check system prerequisites (Python, pip)
2. ✅ **Automatically detect and install ffmpeg** (when possible)
3. ✅ Create a virtual environment
4. ✅ Install all required Python dependencies
5. ✅ Install mmcli globally as a command-line tool
6. ✅ Verify the installation works

## Prerequisites

### Required
- **Python 3.6+** - [Download from python.org](https://python.org/downloads/)
- **pip** - Usually comes with Python

### Automatically Handled
- **ffmpeg** - The installer will attempt to install this automatically:
  - **Windows**: Via Chocolatey or winget (if available)
  - **Ubuntu/Debian**: `sudo apt install ffmpeg`
  - **CentOS/RHEL**: `sudo yum install ffmpeg`
  - **Fedora**: `sudo dnf install ffmpeg`
  - **Arch Linux**: `sudo pacman -S ffmpeg`
  - **macOS**: `brew install ffmpeg` (if Homebrew is installed)

## After Installation

Once installed, you can use mmcli from anywhere in your terminal:

```bash
# Download YouTube video
mmcli download video --url "https://youtube.com/watch?v=..." --resolution 720p

# Download YouTube audio
mmcli download audio --url "https://youtube.com/watch?v=..." --format mp3

# Convert media files
mmcli convert --path "videos/*.mp4" --to mp3 --output_dir converted/
mmcli convert --path "image.jpg" --to png

# Get help and version
mmcli --help
mmcli --version
```

## Troubleshooting

### "mmcli command not found"
- On Windows: Restart your command prompt
- On Linux/macOS: Add `~/.local/bin` to your PATH or restart terminal

### "ffmpeg not found" 
- The installer should have offered to install ffmpeg automatically
- If automatic installation failed:
  - **Windows**: Install via `choco install ffmpeg` or `winget install ffmpeg`
  - **Ubuntu/Debian**: `sudo apt install ffmpeg`
  - **CentOS/RHEL**: `sudo yum install ffmpeg`
  - **macOS**: `brew install ffmpeg`
- Make sure ffmpeg is in your system PATH
- Restart your terminal after installing ffmpeg

### Permission errors on Linux/macOS
- Try: `pip install --user -e .`
- Or run with sudo: `sudo ./install.sh`

### Python version issues
- Ensure you have Python 3.6 or newer
- On some systems, use `python3` instead of `python`

## Manual Installation

If the automatic scripts don't work, you can install manually:

```bash
# Navigate to project root
cd /path/to/multimedia

# Install dependencies
pip install ffmpeg-python pytubefix

# Install the package
pip install -e .

# Test installation
mmcli --help
```

## Uninstallation

To remove mmcli:
```bash
pip uninstall mmcli
```
