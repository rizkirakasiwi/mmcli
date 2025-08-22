# MMCLI - Multimedia CLI Tools

MMCLI is a simple command-line tool for **Multimedia Helper** like **download youtube or social media video/audio**  and **converting multimedia files** (images, audio, video) into different formats.

⚠️ **Project Status:** This project has just begun and is currently under **heavy development and maintenance**.  
Expect frequent changes, breaking updates, and incomplete features.

---

## ✨ Features

- 🎥 Download YouTube **videos** in the best available quality
- 🎵 Download YouTube **audio only** (e.g., MP3)
- 🖼️ Convert **images** between formats (`jpg`, `png`, `webp`, etc.)
- 🎬 Convert **video** formats (`mp4`, `avi`, `mkv`, etc.)
- 🎧 Convert **audio** formats (`mp3`, `wav`, `flac`, etc.)
- 📂 Support for **batch conversion** with wildcard paths (e.g., `samples/*.jpg`)

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

```bash
# Download a video from YouTube
mmcli download video --url "https://youtube.com/watch?v=example"

# Download video with specific resolution
mmcli download video --url "https://youtube.com/watch?v=example" --resolution 720p

# Download audio only (MP3)
mmcli download audio --url "https://youtube.com/watch?v=example" --format mp3
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

## ⚠️ Notes

* Requires **Python 3.6+**
* Make sure you have [ffmpeg](https://ffmpeg.org/download.html) installed and available in your `PATH` for conversions (the installation script can help with this)
* Downloads use the `pytubefix` library for YouTube support
* Package available on PyPI as `mmcli`

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

### Project Structure

```
mmcli/
├── app/
│   ├── tools/          # Core functionality
│   │   ├── media_converter.py
│   │   └── media_downloader.py
│   └── utils/          # Utilities
│       ├── command_manager.py
│       └── media_format.py
├── bin/
│   ├── mmcli           # Main CLI entry point
│   └── install.*       # Installation scripts
├── tests/              # Test suite
├── samples/            # Sample files for testing
└── main.py             # Application entry point
```

---

## 🛠️ Roadmap / Ideas

* [ ] Allow YouTube playlist downloader 
* [ ] Allow multiple YouTube URLs in one command
* [ ] Download from other social media platforms
* [ ] Add `--verbose` flag for detailed logs
* [ ] Config file (`~/.mmcli/config.json`) for default output paths
* [ ] Progress bars for downloads and conversions
* [ ] Resume interrupted downloads
* [ ] Metadata preservation during conversion
* [ ] MMCLI as MCP (Model Context Protocol) 

---

## 📜 License

MIT License. See [LICENSE](LICENSE) for details.

