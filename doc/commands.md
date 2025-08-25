# MMCLI Commands Reference

This document provides a comprehensive guide to all available MMCLI commands with detailed examples and explanations.

## Table of Contents

- [Getting Started](#getting-started)
- [Download Commands](#download-commands)
- [Convert Commands](#convert-commands)
- [Configuration](#configuration)
- [Advanced Usage](#advanced-usage)
- [Troubleshooting](#troubleshooting)

---

## Getting Started

### Basic Usage

```bash
# Show help
mmcli --help

# Show version
mmcli --version

# Show help for specific commands
mmcli download --help
mmcli convert --help
```

### Command Structure

MMCLI uses a hierarchical command structure:

```
mmcli <command> <subcommand> [options]
```

**Available Commands:**
- `download` - Download media from YouTube
- `convert` - Convert media files between formats

---

## Download Commands

### Overview

The `download` command supports downloading from YouTube with two main subcommands:

- `mmcli download video` - Download YouTube videos
- `mmcli download audio` - Download YouTube audio

**Features:**
- ✅ Single video/audio downloads
- ✅ Full playlist downloads  
- ✅ Parallel processing for playlists (configurable)
- ✅ Format conversion during download
- ✅ Auto-organized output directories
- ✅ Smart resolution and format selection

### Video Downloads

#### Single Video Downloads

```bash
# Basic video download (uses config defaults)
mmcli download video --url "https://youtube.com/watch?v=dQw4w9WgXcQ"

# Download with specific resolution
mmcli download video --url "https://youtube.com/watch?v=dQw4w9WgXcQ" --resolution 720p

# Download and convert to MKV format
mmcli download video --url "https://youtube.com/watch?v=dQw4w9WgXcQ" --format mkv

# Combine resolution and format
mmcli download video --url "https://youtube.com/watch?v=dQw4w9WgXcQ" --resolution 1080p --format mp4
```

**Available Resolutions:**
- `144p`, `240p`, `360p`, `480p`, `720p`, `1080p`, `1440p`, `2160p`
- `highest` (default) - Best available quality
- `lowest` - Lowest available quality

**Supported Video Formats:**
- `mp4` (default), `mkv`, `avi`, `mov`, `webm`, `flv`, `3gp`, `wmv`

#### Playlist Video Downloads

```bash
# Download entire playlist (uses parallel processing by default)
mmcli download video --url "https://youtube.com/playlist?list=PLrAXtmRdnEQy..."

# Download playlist with specific resolution
mmcli download video --url "https://youtube.com/playlist?list=PLrAXtmRdnEQy..." --resolution 720p

# Download and convert playlist to MKV
mmcli download video --url "https://youtube.com/playlist?list=PLrAXtmRdnEQy..." --format mkv
```

**Playlist Features:**
- **Parallel Downloads**: Uses 3 workers by default (configurable in `config.toml`)
- **Auto-Organization**: Creates subfolders by playlist title
- **Batch Conversion**: Efficient format conversion for entire playlist
- **Progress Tracking**: Shows download progress for each video
- **Error Handling**: Continues downloading even if individual videos fail

### Audio Downloads

#### Single Audio Downloads

```bash
# Basic audio download (original format)
mmcli download audio --url "https://youtube.com/watch?v=dQw4w9WgXcQ"

# Download and convert to MP3
mmcli download audio --url "https://youtube.com/watch?v=dQw4w9WgXcQ" --format mp3

# Download and convert to FLAC (lossless)
mmcli download audio --url "https://youtube.com/watch?v=dQw4w9WgXcQ" --format flac
```

**Supported Audio Formats:**
- `m4a` (default), `mp3`, `wav`, `flac`, `aac`, `ogg`, `opus`, `wma`

#### Playlist Audio Downloads

```bash
# Download playlist as audio files
mmcli download audio --url "https://youtube.com/playlist?list=PLrAXtmRdnEQy..."

# Download playlist and convert to MP3
mmcli download audio --url "https://youtube.com/playlist?list=PLrAXtmRdnEQy..." --format mp3

# Download playlist and convert to FLAC
mmcli download audio --url "https://youtube.com/playlist?list=PLrAXtmRdnEQy..." --format flac
```

### Output Directory Structure

Downloads are automatically organized:

```
downloads/
├── videos/                 # Single video downloads
├── audios/                 # Single audio downloads  
└── playlist/
    ├── videos/
    │   └── [Playlist Name]/    # Playlist videos
    └── audios/
        └── [Playlist Name]/    # Playlist audios
```

---

## Convert Commands

### Overview

The `convert` command transforms media files between different formats with support for:

- ✅ Single file conversion
- ✅ Batch conversion with glob patterns
- ✅ Parallel processing for multiple files
- ✅ Custom output directories
- ✅ Quality preservation options

### Basic Conversion

```bash
# Convert single file
mmcli convert --path input.jpg --to png

# Convert with custom output directory
mmcli convert --path video.mp4 --to mp3 --output_dir converted/

# Convert and specify output directory
mmcli convert --path image.webp --to jpg --output_dir images/
```

### Batch Conversion

#### Using Glob Patterns

```bash
# Convert all JPEG images to PNG
mmcli convert --path "*.jpg" --to png

# Convert all MP4 videos to MP3
mmcli convert --path "videos/*.mp4" --to mp3

# Convert all AVIF images to JPG
mmcli convert --path "photos/*.avif" --to jpg

# Recursive conversion
mmcli convert --path "**/*.webp" --to jpg
```

#### Parallel Processing

```bash
# Default parallel conversion (uses config default workers)
mmcli convert --path "videos/*.mp4" --to mp3

# Specify number of parallel workers
mmcli convert --path "photos/*.avif" --to jpg --max-workers 4

# Force sequential processing (safe mode)
mmcli convert --path "large_files/*.mov" --to mp4 --max-workers 1

# Maximum performance (8 workers)
mmcli convert --path "batch/*.png" --to webp --max-workers 8
```

**Worker Guidelines:**
- **1 worker**: Sequential processing, safest for large files
- **2-4 workers**: Good balance for most systems
- **4-8 workers**: High performance for powerful systems
- **8+ workers**: Only for very powerful systems with fast storage

### Supported Formats

#### Images
- **Input**: `jpg`, `jpeg`, `png`, `webp`, `gif`, `bmp`, `tif`, `tiff`, `avif`, `heic`, `heif`
- **Output**: `jpg`, `png`, `webp`, `gif`, `bmp`, `tiff`, `avif`

#### Videos  
- **Input**: `mp4`, `avi`, `mkv`, `mov`, `webm`, `flv`, `wmv`, `3gp`, `m4v`
- **Output**: `mp4`, `avi`, `mkv`, `mov`, `webm`, `flv`, `3gp`

#### Audio
- **Input**: `mp3`, `wav`, `flac`, `aac`, `m4a`, `ogg`, `wma`, `opus`
- **Output**: `mp3`, `wav`, `flac`, `aac`, `m4a`, `ogg`, `opus`

### Output Directory Structure

```
converter/                  # Default output directory
├── image_20240825_143022.jpg
├── video_20240825_143023.mp4
└── audio_20240825_143024.mp3
```

**File Naming:**
- Format: `{original_name}_{timestamp}.{new_extension}`
- Timestamp prevents filename conflicts
- Preserves original filename for identification

---

## Configuration

MMCLI supports centralized configuration via `config.toml`. See [configuration.md](configuration.md) for complete details.

### Quick Configuration Examples

Create `config.toml` in your project directory:

```toml
# Faster playlist downloads
[downloads.playlist]
max_workers = 5

# Different default formats
[downloads.video]
format = "mkv"
resolution = "720p"

[downloads.audio]
format = "mp3"

# Faster batch conversions
[conversion]
output_dir = "my_conversions"
```

---

## Advanced Usage

### Complex Examples

#### Mixed Playlist Operations

```bash
# Download playlist videos in 720p and convert to MKV
mmcli download video \
  --url "https://youtube.com/playlist?list=PLrAXtmRdnEQy..." \
  --resolution 720p \
  --format mkv

# Download playlist audio and convert to FLAC
mmcli download audio \
  --url "https://youtube.com/playlist?list=PLrAXtmRdnEQy..." \
  --format flac
```

#### Batch Processing Workflows

```bash
# Download playlist, then batch convert to different format
mmcli download video --url "https://youtube.com/playlist?list=PLrAXtmRdnEQy..."
mmcli convert --path "downloads/playlist/videos/*/*.mp4" --to mkv --max-workers 4

# Convert multiple formats in parallel
mmcli convert --path "media/*.{mp4,avi,mov}" --to webm --max-workers 6
```

### Performance Optimization

#### System Resource Management

```bash
# For systems with limited CPU/memory
mmcli convert --path "*.mp4" --to mp3 --max-workers 1

# For powerful workstations  
mmcli convert --path "batch/*.avif" --to jpg --max-workers 8

# Balance between speed and system responsiveness
mmcli convert --path "photos/*.png" --to webp --max-workers 4
```

#### Storage Considerations

```bash
# Convert to smaller output directory for SSDs
mmcli convert --path "large/*.mov" --to mp4 --output_dir /tmp/conversions/

# Keep originals and conversions separate
mmcli convert --path "originals/*.tiff" --to jpg --output_dir compressed/
```

---

## Troubleshooting

### Common Issues

#### Download Issues

**Problem**: Playlist download fails
```bash
# Solution: Try with sequential processing
# Set max_workers = 1 in config.toml
```

**Problem**: Video resolution not available
```bash
# Solution: Use highest or specify available resolution
mmcli download video --url "..." --resolution highest
```

#### Conversion Issues

**Problem**: Batch conversion runs out of memory
```bash
# Solution: Reduce workers or process sequentially
mmcli convert --path "*.mov" --to mp4 --max-workers 1
```

**Problem**: FFmpeg not found
```bash
# Solution: Install FFmpeg and ensure it's in PATH
# Windows: Download from https://ffmpeg.org/
# Linux: sudo apt install ffmpeg
# macOS: brew install ffmpeg
```

### Performance Tips

1. **Use appropriate worker counts**:
   - Start with default (3 workers)
   - Increase for powerful systems
   - Decrease for stability issues

2. **Monitor system resources**:
   - Watch CPU and memory usage
   - Reduce workers if system becomes unresponsive

3. **Consider file sizes**:
   - Large files: Use fewer workers
   - Small files: Can use more workers

4. **Storage optimization**:
   - Use fast storage for output directories
   - Consider temporary directories for processing

### Debug Mode

```bash
# Enable verbose output (if available)
mmcli --verbose download video --url "..."

# Check configuration loading
python -c "from app.utils.config import config; print(config._config_data)"
```

---

## Examples Summary

### Quick Reference

```bash
# Downloads
mmcli download video --url "https://youtube.com/watch?v=..." --resolution 720p
mmcli download audio --url "https://youtube.com/watch?v=..." --format mp3
mmcli download video --url "https://youtube.com/playlist?list=..." --format mkv

# Conversions  
mmcli convert --path "*.jpg" --to png
mmcli convert --path "videos/*.mp4" --to mp3 --max-workers 4
mmcli convert --path "image.avif" --to jpg --output_dir converted/

# Configuration
# Create config.toml with your preferred defaults
# See doc/configuration.md for complete options
```

For more detailed configuration options, see [configuration.md](configuration.md).