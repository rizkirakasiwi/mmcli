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

Clone the repository and install dependencies:

```bash
git clone https://github.com/rizkirakasiwi/mmcli.git
cd mmcli
pip install -r requirements.txt
````

---

## 🚀 Usage

Run the CLI with `python`:

```bash
python multimedia_cli.py [OPTIONS]
```

### Modes

You must choose **one mode**:

* `--download` → Download from YouTube
* `--convert` → Convert files

### Download Examples

```bash
# Download a video from YouTube
python multimedia_cli.py --download --video https://youtube.com/watch?v=example

# Download audio only (MP3)
python multimedia_cli.py --download --audio https://youtube.com/watch?v=example
```

### Convert Examples

```bash
# Convert a single file
python multimedia_cli.py --convert --path input.png --to jpg

# Convert multiple files with wildcard pattern
python multimedia_cli.py --convert --path "samples/*.avif" --to jpg

# Convert and save to custom output directory
python multimedia_cli.py --convert --path video.mp4 --to mp3 --output_dir converted/
```

---

## 🎯 Supported Formats

* **Images:** `jpg`, `jpeg`, `png`, `webp`, `gif`, `bmp`, `tiff`
* **Videos:** `mp4`, `avi`, `mkv`, `mov`, `webm`
* **Audio:** `mp3`, `wav`, `flac`, `aac`, `ogg`, `wma`, `m4a`

---

## ⚠️ Notes

* Requires **Python 3.8+**
* Make sure you have [ffmpeg](https://ffmpeg.org/download.html) installed and available in your `PATH` for conversions.
* Downloads depend on the `pytube` (or similar) library, see `requirements.txt`.

---

## 🤝 Contributing

Contributions are welcome! Since this project is still at an **early stage**, any feedback, bug reports, or feature ideas are highly appreciated.

To contribute:

1. Fork the repository
2. Create a new feature branch (`git checkout -b feature/my-feature`)
3. Commit your changes (`git commit -m "Add my feature"`)
4. Push to your fork (`git push origin feature/my-feature`)
5. Open a Pull Request

Please make sure your code follows Python best practices and includes basic documentation or examples.

---

## 🛠️ Roadmap / Ideas

* [ ] Add progress bar for downloads and conversions
* [ ] Allow multiple YouTube URLs in one command
* [ ] Add `--verbose` flag for detailed logs
* [ ] Config file (`~/.mmcli/config.json`) for default output paths

---

## 📜 License

MIT License. See [LICENSE](LICENSE) for details.

