# MMCLI - Multimedia CLI Tools

MMCLI is a powerful command-line tool for **Multimedia Helper** like **downloading YouTube videos/playlists** and **converting multimedia files** (images, audio, video) into different formats.

✨ **Project Status:** Recently in active development. Expect frequent updates and changes.

---

## ✨ Features

### YouTube Downloads
- 🎥 Download YouTube **videos** in the best available quality
- 🎵 Download YouTube **audio only** in original format (optional conversion with --format flag)
- 📋 Download entire **YouTube playlists** (both video and audio)
- ⚡ **Parallel playlist downloads** for faster performance (configurable workers)
- 🎯 Choose specific video resolution (720p, 1080p, etc.)
- 🔄 Optional format conversion with --format flag
- 📂 Auto-organized output with playlist subfolders

### Media Conversion  
- 🖼️ Convert **images** between formats (`jpg`, `png`, `webp`, `avif`, etc.)
- 🎬 Convert **video** formats (`mp4`, `avi`, `mkv`, `webm`, etc.)
- 🎧 Convert **audio** formats (`mp3`, `wav`, `flac`, `aac`, etc.)
- 📂 Support for **batch conversion** with wildcard paths (e.g., `samples/*.jpg`)
- ⚡ **Parallel batch conversions** with configurable workers
- 🎛️ **Centralized configuration** via `config.toml` for all defaults
- ⚡ High-performance functional programming architecture

---

## 📦 Installation

For the easiest installation, see the [Installation Guide](doc/INSTALL_README.md) which includes automated installation scripts.

Or install manually:

```bash
git clone https://github.com/rizkirakasiwi/mmcli.git
cd mmcli
pip install -e .
```

### Quick Install with pip
```bash
pip install mmcli
```

---

## 🚀 Usage

After installation, use the `mmcli` command:

```bash
mmcli --help
mmcli --version
```

### Commands

MMCLI uses subcommands for different operations:

* `mmcli download` → Download from YouTube
* `mmcli convert` → Convert media files

### Download Examples

#### Single Video/Audio Downloads
```bash
# Download a video from YouTube
mmcli download video --url "https://youtube.com/watch?v=example"

# Download video with specific resolution
mmcli download video --url "https://youtube.com/watch?v=example" --resolution 720p

# Download audio only (original format)
mmcli download audio --url "https://youtube.com/watch?v=example"

# Download audio and convert to MP3
mmcli download audio --url "https://youtube.com/watch?v=example" --format mp3

# Download video and convert to specific format
mmcli download video --url "https://youtube.com/watch?v=example" --format mkv
```

#### Playlist Downloads
```bash
# Download entire video playlist
mmcli download video --url "https://youtube.com/playlist?list=PLrAXtmRdnEQy..."

# Download playlist as audio files (original format)
mmcli download audio --url "https://youtube.com/playlist?list=PLrAXtmRdnEQy..."

# Download playlist as audio files and convert to MP3
mmcli download audio --url "https://youtube.com/playlist?list=PLrAXtmRdnEQy..." --format mp3

# Download playlist videos with specific resolution
mmcli download video --url "https://youtube.com/playlist?list=PLrAXtmRdnEQy..." --resolution 720p
```

### Convert Examples

```bash
# Convert a single file
mmcli convert --path input.png --to jpg

# Convert multiple files with wildcard pattern
mmcli convert --path "samples/*.avif" --to jpg

# Convert and save to custom output directory
mmcli convert --path video.mp4 --to mp3 --output_dir converted/

# Parallel batch conversion with 4 workers
mmcli convert --path "videos/*.mp4" --to mp3 --max-workers 4

# Sequential conversion (safe mode)
mmcli convert --path "large_files/*.mov" --to mp4 --max-workers 1
```

### Advanced Examples

#### Parallel Processing with Configuration

Create `config.toml` for optimized performance:

```toml
[downloads.playlist]
max_workers = 5              # Fast playlist downloads

[downloads.video]
format = "mkv"               # Default format
resolution = "720p"          # Default resolution
```

Now downloads are automatically optimized:

```bash
# Uses config defaults (5 parallel workers, 720p, MKV format)  
mmcli download video --url "https://youtube.com/playlist?list=..."

# Override specific settings
mmcli download video --url "..." --resolution 1080p --format mp4
```

#### Batch Operations

```bash
# Parallel batch conversion with 4 workers
mmcli convert --path "photos/*.avif" --to jpg --max-workers 4

# Sequential processing for large files (safe mode)
mmcli convert --path "videos/*.mov" --to mp4 --max-workers 1
```

### Development Usage

If running from source without installation:

```bash
python main.py download video --url "https://youtube.com/watch?v=example"
python main.py convert --path input.png --to jpg
```

---

## 🎯 Supported Formats

* **Images:** `jpg`, `jpeg`, `png`, `webp`, `gif`, `bmp`, `tiff`, `avif`
* **Videos:** `mp4`, `avi`, `mkv`, `mov`, `webm`, `flv`, `3gp`
* **Audio:** `mp3`, `wav`, `flac`, `aac`, `ogg`, `wma`, `m4a`
* **Subtitles:** `srt`, `ass`, `vtt`

---

## ⚙️ Configuration

MMCLI now supports **centralized configuration** via `config.toml` in your project directory. This allows you to set default formats, parallel workers, and other preferences.

### Default Configuration

Create a `config.toml` file in your project directory:

```toml
[downloads.video]
format = "mp4"                    # Default video format
resolution = "highest"           # Default resolution

[downloads.audio]
format = "m4a"                   # Default audio format

[downloads.playlist]
max_workers = 3                  # Parallel downloads (3 workers)
create_subfolders = true         # Organize by playlist title
batch_convert = true             # Efficient format conversion

[conversion]
output_dir = "converter"         # Default output directory

[general]
progress_bar = true              # Show progress bars
auto_cleanup = true              # Clean up temporary files
```

### Benefits
- 🎯 **No repetitive CLI arguments** - set your preferences once
- ⚡ **Optimized playlist downloads** - parallel processing by default
- 📁 **Auto-organized output** - playlist videos in dedicated folders
- 🔧 **Customizable performance** - adjust workers based on your system

See [doc/configuration.md](doc/configuration.md) for complete configuration options.

---

## ⚠️ Technical Notes

### Requirements
* Requires **Python 3.6+**
* [FFmpeg](https://ffmpeg.org/download.html) installed and available in `PATH` for conversions
* Internet connection for YouTube downloads
* Optional: `tomli` for Python <3.11 (TOML config support)
* Optional: `PyYAML` for YAML config support

### Dependencies
* **pytubefix** - YouTube downloading with playlist support
* **ffmpeg-python** - Media conversion backend  
* **pytest** - Testing framework (development)

### Architecture
* **Functional Programming**: Uses `map`, `reduce`, `partial`, and pure functions
* **Configuration Objects**: Structured data flow instead of parameter passing
* **Error Handling**: Graceful failure with detailed error reporting
* **Test Coverage**: 103+ tests ensuring reliability

### Performance
* **Parallel playlist downloads** with configurable workers (default: 3)
* **Parallel batch conversions** for multiple files
* Memory-efficient streaming for large files
* Automatic cleanup of temporary files
* Smart sequential fallback for single operations

---

## 🤝 Contributing

We welcome contributions! Since this project is at an **early stage**, any feedback, bug reports, or feature ideas are highly appreciated.

**⚠️ Important**: All contributors must read our [Contributor Guidance](doc/CONTRIBUTOR_GUIDANCE.md) before submitting Pull Requests.

### Quick Start for Contributors

1. Fork the repository
2. Read [doc/CONTRIBUTOR_GUIDANCE.md](doc/CONTRIBUTOR_GUIDANCE.md) 
3. Set up development environment: `pip install -e .[test]`
4. **Run tests before submitting**: `pytest`
5. Create Pull Request

**All tests must pass before PR submission** - see contributor guidance for details.

### Testing

The project has comprehensive test coverage (103+ tests):

```bash
# Run all tests
pytest

# Run with coverage report  
pytest --cov=app --cov-report=html --cov-report=term-missing

# Run specific test suites
pytest tests/test_playlist_downloader.py    # Playlist functionality tests
pytest tests/test_media_converter.py        # Conversion functionality tests
pytest tests/test_media_downloader.py       # Download functionality tests
pytest tests/test_integration.py            # End-to-end integration tests
```

**Test Coverage Includes:**
- ✅ Single video/audio downloads
- ✅ Playlist downloads (video and audio)
- ✅ Media format conversions
- ✅ Error handling and edge cases
- ✅ CLI argument parsing
- ✅ Integration testing
- ✅ URL validation and routing

### Project Architecture

MMCLI uses a **functional programming architecture** for better maintainability and testability:

```
mmcli/
├── app/
│   ├── tools/          # Core functionality modules
│   │   ├── media_converter.py      # Media format conversion (parallel support)
│   │   ├── media_downloader.py     # Download orchestration (config-driven)
│   │   └── youtube_downloader.py   # YouTube-specific operations (parallel)
│   └── utils/          # Utility modules  
│       ├── command_manager.py      # CLI argument parsing
│       ├── media_format.py         # Format definitions
│       └── config.py               # Configuration management
├── doc/                # Documentation
│   ├── commands.md     # Complete CLI reference
│   ├── configuration.md # Configuration guide
│   ├── INSTALL_README.md # Installation guide
│   └── CONTRIBUTOR_GUIDANCE.md # Contributor guidelines
├── tests/              # Comprehensive test suite (103+ tests)
│   ├── test_media_converter.py
│   ├── test_media_downloader.py
│   ├── test_playlist_downloader.py # Playlist-specific tests
│   ├── test_integration.py
│   └── ...
├── samples/            # Sample files for testing
├── config.toml         # Default configuration
└── main.py             # Application entry point
```

**Key Architecture Features:**
- **Functional Programming**: Pure functions, immutable data flow
- **Parallel Processing**: ThreadPoolExecutor for playlist downloads and batch conversions
- **Centralized Configuration**: TOML/YAML config system with smart defaults
- **Separation of Concerns**: YouTube logic separated from general download logic  
- **Configuration-Based**: Functions use configuration objects for parameters
- **Comprehensive Testing**: 103+ tests covering all functionality including playlists

---

## 🛠️ Roadmap / Ideas

### ✅ Recently Completed
* [x] **YouTube playlist downloader** (both video and audio)
* [x] **Parallel playlist downloads** for faster performance
* [x] **Centralized configuration system** via `config.toml`
* [x] **Parallel batch conversions** with configurable workers
* [x] **Functional programming refactor** for better maintainability  
* [x] **Comprehensive test coverage** (103+ tests including playlist tests)
* [x] **Separated YouTube logic** into dedicated module

### 🔄 In Progress / Planned
* [ ] Allow multiple YouTube URLs in one command
* [ ] Download from other social media platforms (TikTok, Instagram, etc.)
* [ ] Add `--verbose` flag for detailed logs
* [ ] Enhanced progress bars for downloads and conversions
* [ ] Resume interrupted downloads
* [ ] Metadata preservation during conversion
* [ ] MMCLI as MCP (Model Context Protocol)
* [ ] Download quality selection (best/worst/specific bitrate)
* [ ] YAML configuration support
* [ ] Config validation and migration tools 

---

## 📜 License

MIT License. See [LICENSE](LICENSE) for details.

