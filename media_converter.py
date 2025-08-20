import ffmpeg
import sys
from pathlib import Path
from glob import glob
from datetime import datetime
from typing import Optional, List


# Map common format aliases to FFmpeg format names
format_mapping = {
    # --- Images ---
    "jpg": "mjpeg",
    "jpeg": "mjpeg",
    "png": "png",
    "webp": "webp",
    "gif": "gif",
    "bmp": "bmp",
    "tif": "tiff",
    "tiff": "tiff",
    "ico": "ico",
    "svg": "svg",
    "dds": "dds",
    "pam": "pam",
    "pbm": "pbm",
    "pgm": "pgm",
    "ppm": "ppm",
    "dpx": "dpx",
    "exr": "exr",
    "tga": "targa",
    "jp2": "jpeg2000",
    "j2k": "jpeg2000",
    "jxl": "jpegxl",
    "heif": "heif",
    "heic": "hevc",
    # --- Video containers ---
    "mp4": "mp4",
    "mkv": "matroska",
    "avi": "avi",
    "mov": "mov",
    "flv": "flv",
    "webm": "webm",
    "mpeg": "mpeg",
    "mpg": "mpeg",
    "ts": "mpegts",
    "m2ts": "mpegts",
    "ogv": "ogg",
    "3gp": "3gp",
    "3g2": "3g2",
    "vob": "vob",
    "f4v": "f4v",
    "wmv": "asf",
    "rm": "rm",
    "rmvb": "rm",
    # --- Audio formats ---
    "mp3": "mp3",
    "wav": "wav",
    "flac": "flac",
    "aac": "aac",
    "m4a": "ipod",  # FFmpeg muxer for .m4a
    "ogg": "ogg",
    "oga": "ogg",
    "opus": "ogg",
    "wma": "asf",
    "alac": "ipod",
    "amr": "amr",
    "ac3": "ac3",
    "dts": "dts",
    "eac3": "eac3",
    # --- Subtitles ---
    "srt": "srt",
    "ass": "ass",
    "ssa": "ass",
    "vtt": "webvtt",
    "sub": "microdvd",
    "idx": "microdvd",
    "mks": "matroska",
    # --- Other / Data ---
    "swf": "swf",
    "ps": "psp",
    "mxf": "mxf",
    "gxf": "gxf",
    "nut": "nut",
    "yuv": "rawvideo",
    "rgb": "rawvideo",
}


class MediaConverter:
    def __get_files(self, input_file: str) -> List[Path]:
        """Resolve input file(s), supporting glob patterns."""
        if "*" in input_file:
            files = [Path(p) for p in glob(input_file)]
            if not files:
                files = [Path(p) for p in glob(f"**/{input_file}", recursive=True)]
        else:
            files = [Path(input_file)] if Path(input_file).exists() else []

        if not files:
            raise FileNotFoundError(f"No file(s) found matching: {input_file}")

        return files

    def __resolve_output_dir(self, output_dir: Optional[str]) -> Path:
        """Ensure output directory exists and return as Path."""
        path = (
            Path(output_dir).resolve()
            if output_dir
            else Path(__file__).resolve().parent / "converter"
        )
        path.mkdir(parents=True, exist_ok=True)
        return path

    def __build_output_path(
        self, input_file: Path, output_format: str, output_dir: Path
    ) -> Path:
        """Generate output file path with timestamp."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        output_file = f"{input_file.stem}_{timestamp}.{output_format}"
        return output_dir / output_file

    def __convert_file(
        self, input_file: Path, output_format: str, output_dir: Path
    ) -> bool:
        """Convert a single file. Returns True if successful, False otherwise."""
        try:
            ffmpeg_format = format_mapping.get(output_format.lower(), output_format)
            output_path = self.__build_output_path(
                input_file, output_format, output_dir
            )
            (
                ffmpeg.input(str(input_file))
                .output(str(output_path), format=ffmpeg_format)
                .run(quiet=True, overwrite_output=True)
            )
            return True
        except:
            print(f"Error converting {input_file}")
            return False

    def __convert_files(
        self,
        input_files: List[Path],
        output_format: str,
        output_dir: Optional[str] = None,
    ):
        """Convert a batch of files and log summary."""
        resolve_output_dir = self.__resolve_output_dir(output_dir)
        results = [
            self.__convert_file(f, output_format, resolve_output_dir)
            for f in input_files
        ]
        success_count = sum(results)

        if success_count == 1:
            print(f"Success converting {input_files[0]} into {output_format} format")
        else:
            print(f"Success to convert {success_count} files")

        print(f"Saved to {resolve_output_dir} directory")

    def convert(self, args):
        """CLI entry point."""
        try:
            files = self.__get_files(args.path)
            self.__convert_files(files, args.to, args.output_dir)
        except:
            print(f"Error converting file")
            sys.exit(1)


media_converter = MediaConverter()
