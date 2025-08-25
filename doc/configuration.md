# MMCLI Configuration Guide

This guide explains how to configure MMCLI using the centralized configuration system introduced in v0.1.0a1+.

## Table of Contents

- [Overview](#overview)
- [Configuration File Formats](#configuration-file-formats)
- [Configuration Sections](#configuration-sections)
- [Default Configuration](#default-configuration)
- [Advanced Configuration](#advanced-configuration)
- [Environment-Specific Configs](#environment-specific-configs)
- [Migration Guide](#migration-guide)

---

## Overview

MMCLI supports **centralized configuration** to eliminate repetitive CLI arguments and customize default behavior. Instead of specifying the same options every time, set your preferences once in a configuration file.

### Benefits

- 🎯 **No repetitive CLI arguments** - Set preferences once
- ⚡ **Optimized defaults** - Parallel processing, smart organization
- 🔧 **Customizable performance** - Adjust workers for your system
- 📁 **Auto-organized output** - Structured directory layouts
- 🎛️ **Quality control** - Video/audio encoding preferences

### Quick Start

1. Create `config.toml` in your project directory
2. Customize settings for your needs
3. Run MMCLI commands - configuration is automatically applied

---

## Configuration File Formats

### TOML (Recommended)

TOML is the primary and recommended format:

```toml
# config.toml
[downloads.video]
format = "mp4"
resolution = "720p"

[downloads.playlist]
max_workers = 4
```

### YAML (Optional)

YAML is also supported (requires `PyYAML`):

```yaml
# config.yaml
downloads:
  video:
    format: mp4
    resolution: 720p
  playlist:
    max_workers: 4
```

**Installation for YAML support:**
```bash
pip install PyYAML
```

### File Discovery

MMCLI automatically searches for configuration files in this order:

1. `config.toml` (current directory)
2. `mmcli.toml` (current directory)
3. `config.yaml` (current directory)  
4. `mmcli.yaml` (current directory)
5. Falls back to built-in defaults if no config found

---

## Configuration Sections

### Downloads Configuration

#### Video Downloads

```toml
[downloads.video]
format = "mp4"              # Default video format
resolution = "highest"      # Default resolution
```

**Supported Values:**

- **format**: `mp4`, `mkv`, `avi`, `mov`, `webm`, `flv`, `3gp`, `wmv`
- **resolution**: `144p`, `240p`, `360p`, `480p`, `720p`, `1080p`, `1440p`, `2160p`, `highest`, `lowest`

#### Audio Downloads

```toml
[downloads.audio]
format = "m4a"              # Default audio format  
```

**Supported Values:**

- **format**: `m4a`, `mp3`, `wav`, `flac`, `aac`, `ogg`, `opus`, `wma`

#### Playlist Downloads

```toml
[downloads.playlist]
max_workers = 3             # Number of parallel downloads
create_subfolders = true    # Create playlist title subfolders
batch_convert = true        # Use efficient batch conversion
```

**Configuration Details:**

- **max_workers**: 
  - `1` = Sequential downloads (safest)
  - `2-4` = Balanced performance (recommended)
  - `5+` = High performance (powerful systems only)

- **create_subfolders**:
  - `true` = Organize by playlist title (recommended)
  - `false` = All files in same directory

- **batch_convert**:
  - `true` = Efficient parallel conversion (recommended)
  - `false` = Convert files individually

#### General Download Settings

```toml
[downloads]
output_dir = "downloads"    # Base output directory
```

### Conversion Configuration

#### Output Settings

```toml
[conversion]
output_dir = "converter"    # Default conversion output directory
```

#### Video Conversion

```toml
[conversion.video]
preserve_quality = true     # Maintain original quality
default_codec = "libx264"   # Default video codec
```

#### Audio Conversion

```toml
[conversion.audio]
preserve_quality = true     # Maintain original quality
default_codec = "aac"       # Default audio codec
bitrate = "128k"           # Default audio bitrate
```

### General Application Settings

```toml
[general]
verbose = false             # Enable detailed logging
progress_bar = true         # Show progress bars
auto_cleanup = true         # Clean temporary files
max_retries = 3            # Retry attempts on failure
```

#### File Naming

```toml
[general.naming]
add_timestamp = true        # Add timestamp to filenames
sanitize_filenames = true   # Remove special characters
max_filename_length = 255   # Maximum filename length
```

---

## Default Configuration

Here's the complete default configuration that MMCLI uses if no config file is found:

```toml
# Default MMCLI Configuration

[downloads]
output_dir = "downloads"

[downloads.video]
format = "mp4"
resolution = "highest"

[downloads.audio]
format = "m4a"

[downloads.playlist]
max_workers = 3
create_subfolders = true
batch_convert = true

[conversion]
output_dir = "converter"

[conversion.video]
preserve_quality = true
default_codec = "libx264"

[conversion.audio]
preserve_quality = true
default_codec = "aac"
bitrate = "128k"

[general]
verbose = false
progress_bar = true
auto_cleanup = true
max_retries = 3

[general.naming]
add_timestamp = true
sanitize_filenames = true
max_filename_length = 255
```

---

## Advanced Configuration

### Performance Optimization

#### High-Performance System

```toml
# For powerful workstations with fast storage
[downloads.playlist]
max_workers = 6             # More parallel downloads

[conversion.video]
preserve_quality = true
default_codec = "libx265"   # Better compression (slower)

[conversion.audio]
preserve_quality = true
bitrate = "320k"           # Higher quality audio
```

#### Resource-Constrained System

```toml
# For laptops or systems with limited resources
[downloads.playlist]
max_workers = 1             # Sequential processing

[conversion.video]
preserve_quality = false    # Faster processing
default_codec = "libx264"   # Faster encoding

[conversion.audio]
preserve_quality = false
bitrate = "128k"           # Standard quality
```

### Storage Optimization

#### Custom Directory Structure

```toml
[downloads]
output_dir = "/media/external/downloads"

[conversion]
output_dir = "/tmp/conversions"

[downloads.playlist]
create_subfolders = false   # Flat structure for easier management
```

#### Quality vs Size Balance

```toml
# Optimized for storage efficiency
[downloads.video]
format = "webm"            # Better compression
resolution = "720p"        # Reasonable quality/size

[downloads.audio]
format = "opus"            # Efficient audio codec

[conversion.audio]
bitrate = "96k"           # Smaller file sizes
```

### Development/Testing Configuration

```toml
# For testing and development
[downloads.playlist]
max_workers = 1             # Easier debugging

[general]
verbose = true              # Detailed logging
auto_cleanup = false        # Keep temp files for inspection

[general.naming]
add_timestamp = false       # Consistent filenames for testing
```

---

## Environment-Specific Configs

### Production Environment

```toml
# production-config.toml
[downloads.playlist]
max_workers = 4
batch_convert = true

[conversion]
output_dir = "/opt/mmcli/output"

[general]
verbose = false
auto_cleanup = true
max_retries = 5             # More resilient
```

### Development Environment

```toml
# dev-config.toml
[downloads]
output_dir = "test-downloads"

[conversion]
output_dir = "test-conversions"

[downloads.playlist]
max_workers = 1             # Easier debugging

[general]
verbose = true              # Detailed logging
auto_cleanup = false        # Keep files for inspection
```

### CI/CD Environment

```toml
# ci-config.toml
[downloads.playlist]
max_workers = 2             # Limited CI resources

[general]
verbose = true              # Detailed logs for debugging
progress_bar = false        # No interactive elements
auto_cleanup = true         # Clean environment
max_retries = 1             # Fail fast for CI
```

---

## Migration Guide

### From CLI-Only Usage

**Before (repetitive CLI args):**
```bash
mmcli download video --url "..." --resolution 720p --format mkv
mmcli download audio --url "..." --format mp3
mmcli convert --path "*.jpg" --to png --max-workers 4
```

**After (with config):**
```toml
# config.toml
[downloads.video]
format = "mkv"
resolution = "720p"

[downloads.audio]  
format = "mp3"
```

```bash
# Simplified commands
mmcli download video --url "..."
mmcli download audio --url "..."
mmcli convert --path "*.jpg" --to png --max-workers 4
```

### Configuration Validation

Test your configuration:

```bash
# Test configuration loading
python -c "from app.utils.config import config; print('Video format:', config.get('downloads.video.format'))"

# Verify all settings
python -c "from app.utils.config import config; import json; print(json.dumps(config._config_data, indent=2))"
```

### Common Migration Issues

**Issue**: Configuration not loading
```bash
# Solution: Verify file location and format
ls -la config.toml  # Check if file exists
python -c "import tomllib; tomllib.load(open('config.toml', 'rb'))"  # Test TOML syntax
```

**Issue**: Performance degradation
```bash
# Solution: Adjust worker counts
[downloads.playlist]
max_workers = 2  # Reduce if system struggles
```

---

## Configuration Examples by Use Case

### Content Creator

```toml
# Optimized for content creation workflow
[downloads.video]
format = "mp4"
resolution = "1080p"        # High quality for editing

[downloads.audio]
format = "wav"              # Lossless for audio editing

[downloads.playlist]
max_workers = 4             # Fast playlist downloads
create_subfolders = true    # Organized by series/playlist

[conversion.video]
preserve_quality = true     # Maintain quality for editing
```

### Music Enthusiast

```toml
# Optimized for music collection
[downloads.audio]
format = "flac"             # Lossless audio

[downloads.playlist]
max_workers = 3             # Good balance
create_subfolders = true    # Organized by album/artist

[conversion.audio]
preserve_quality = true
bitrate = "320k"           # High quality conversions
```

### System Administrator

```toml
# Optimized for server/batch operations
[downloads]
output_dir = "/opt/mmcli/downloads"

[conversion]
output_dir = "/opt/mmcli/conversions"

[downloads.playlist]
max_workers = 2             # Conservative for servers
batch_convert = true        # Efficient processing

[general]
verbose = true              # Detailed logging
auto_cleanup = true         # Clean environment
max_retries = 5             # Resilient operations
```

---

## Troubleshooting Configuration

### Configuration Issues

**Problem**: Settings not applied
```bash
# Check if config file is found
python -c "from app.utils.config import config; print('Config loaded from:', config._find_config_file())"
```

**Problem**: Invalid configuration values
```bash
# Validate specific settings
python -c "from app.utils.config import config; print('Max workers:', config.get('downloads.playlist.max_workers'))"
```

### Performance Issues

**Problem**: System overloaded
```toml
# Reduce worker counts
[downloads.playlist]
max_workers = 1

# Or create performance profile
[downloads.playlist]
max_workers = 2             # Conservative setting
```

**Problem**: Slow processing
```toml
# Optimize for speed
[conversion.video]
preserve_quality = false    # Faster processing
```

For complete command examples and usage, see [commands.md](commands.md).