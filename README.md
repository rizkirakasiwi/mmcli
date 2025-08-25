# MMCLI - Multimedia CLI Tools

MMCLI is a powerful command-line tool for **Multimedia Helper** like **downloading YouTube videos/playlists** and **converting multimedia files** (images, audio, video) into different formats.

✨ **Project Status:** Recently refactored with functional programming architecture and comprehensive test coverage. The project is stable and production-ready for basic operations while continuing active development.

---

## ✨ Features

### YouTube Downloads
- 🎥 Download YouTube **videos** in the best available quality
- 🎵 Download YouTube **audio only** in original format (optional conversion with --format flag)
- 📋 Download entire **YouTube playlists** (both video and audio)
- 🎯 Choose specific video resolution (720p, 1080p, etc.)
- 🔄 Optional format conversion with --format flag

### Media Conversion  
- 🖼️ Convert **images** between formats (`jpg`, `png`, `webp`, `avif`, etc.)
- 🎬 Convert **video** formats (`mp4`, `avi`, `mkv`, `webm`, etc.)
- 🎧 Convert **audio** formats (`mp3`, `wav`, `flac`, `aac`, etc.)
- 📂 Support for **batch conversion** with wildcard paths (e.g., `samples/*.jpg`)
- ⚡ High-performance functional programming architecture

---

## 📦 Installation

For the easiest installation, see the [Installation Guide](bin/INSTALL_README.md) which includes automated installation scripts.

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
```

### Development Usage

If running from source without installation:

```bash
python bin/mmcli download video --url "https://youtube.com/watch?v=example"
python bin/mmcli convert --path input.png --to jpg
```

---

## 🎯 Supported Formats

* **Images:** `jpg`, `jpeg`, `png`, `webp`, `gif`, `bmp`, `tiff`, `avif`
* **Videos:** `mp4`, `avi`, `mkv`, `mov`, `webm`, `flv`, `3gp`
* **Audio:** `mp3`, `wav`, `flac`, `aac`, `ogg`, `wma`, `m4a`
* **Subtitles:** `srt`, `ass`, `vtt`

---

## ⚠️ Technical Notes

### Requirements
* Requires **Python 3.6+**
* [FFmpeg](https://ffmpeg.org/download.html) installed and available in `PATH` for conversions
* Internet connection for YouTube downloads

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
* Efficient batch processing for playlist downloads
* Parallel-ready architecture for future enhancements
* Memory-efficient streaming for large files
* Automatic cleanup of temporary files

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
│   │   ├── media_converter.py      # Media format conversion (functional)
│   │   ├── media_downloader.py     # Download orchestration (functional)
│   │   └── youtube_downloader.py   # YouTube-specific operations
│   └── utils/          # Utility modules  
│       ├── command_manager.py      # CLI argument parsing
│       └── media_format.py         # Format definitions
├── bin/
│   ├── mmcli           # Main CLI entry point
│   └── install.*       # Installation scripts
├── tests/              # Comprehensive test suite (103 tests)
│   ├── test_media_converter.py
│   ├── test_media_downloader.py
│   ├── test_playlist_downloader.py # Playlist-specific tests
│   ├── test_integration.py
│   └── ...
├── samples/            # Sample files for testing
└── main.py             # Application entry point
```

**Key Architecture Features:**
- **Functional Programming**: Pure functions, immutable data flow
- **Separation of Concerns**: YouTube logic separated from general download logic  
- **Configuration-Based**: Functions use configuration objects for parameters
- **Comprehensive Testing**: 103+ tests covering all functionality including playlists

---

## 🛠️ Roadmap / Ideas

### ✅ Recently Completed
* [x] **YouTube playlist downloader** (both video and audio)
* [x] **Functional programming refactor** for better maintainability  
* [x] **Comprehensive test coverage** (103+ tests including playlist tests)
* [x] **Separated YouTube logic** into dedicated module

### 🔄 In Progress / Planned
* [ ] Allow multiple YouTube URLs in one command
* [ ] Download from other social media platforms (TikTok, Instagram, etc.)
* [ ] Add `--verbose` flag for detailed logs
* [ ] Config file (`~/.mmcli/config.json`) for default output paths
* [ ] Progress bars for downloads and conversions
* [ ] Resume interrupted downloads
* [ ] Metadata preservation during conversion
* [ ] MMCLI as MCP (Model Context Protocol)
* [ ] Parallel playlist downloads for faster performance
* [ ] Download quality selection (best/worst/specific bitrate) 

---

## 📜 License

MIT License. See [LICENSE](LICENSE) for details.

