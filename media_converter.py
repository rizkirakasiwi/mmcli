import ffmpeg
import argparse
import sys
import os
from glob import glob
from datetime import datetime
from typing import Optional


def get_files(input_file) -> list:
    if "*" in input_file:
        files = glob(input_file)
        if not files:
            files = glob(f"**/{input_file}", recursive=True)
    else:
        files = [input_file] if os.path.exists(input_file) else []

    if not files:
        print(f"No file found matching for {input_file}")
        sys.exit(1)

    return files


def convert(
    input_files: list,
    output_format: str,
    output_dir: Optional[str] = None,
):
    # Map common format aliases to FFmpeg format names
    format_mapping = {
        'jpg': 'mjpeg',
        'jpeg': 'mjpeg',
        'png': 'png',
        'webp': 'webp',
        'gif': 'gif',
        'bmp': 'bmp',
        'tiff': 'tiff',
        'mp4': 'mp4',
        'avi': 'avi',
        'mkv': 'matroska',
        'mov': 'mov',
        'webm': 'webm',
        'mp3': 'mp3',
        'wav': 'wav',
        'flac': 'flac',
        'aac': 'aac',
        'ogg': 'ogg',
        'wma': 'wma',
        'm4a': 'm4a'
    }
    
    ffmpeg_format = format_mapping.get(output_format.lower(), output_format)
    if output_dir is None:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        output_dir = os.path.join(script_dir, "converter")

    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    converted_count = 0
    for input_file in input_files:
        try:
            base_name = os.path.splitext(os.path.basename(input_file))[0]
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"{base_name}_{timestamp}.{output_format}"
            output_path = os.path.join(output_dir, output_file)
            
            print(f"Converting {input_file} -> {output_path}")
            ffmpeg.input(input_file).output(output_path, format=ffmpeg_format).run()
            converted_count += 1
            
        except Exception as e:
            print(f"Error converting {input_file}: {e}")
            continue
    
    print(f"Successfully converted {converted_count}/{len(input_files)} files")


def main():
    """Entry point for the CLI application."""
    parser = argparse.ArgumentParser(description="Multimedia converter CLI Tool")

    parser.add_argument(
        "--path",
        "-p",
        help="[P]ath/to/file, support pattern format like file/to/*.jpg",
        required=True,
    )
    parser.add_argument(
        "--to",
        "-t",
        help="[T]o format do you want convert ex: jpg, png, mp4",
        required=True,
        choices=[
            'jpg',
            'jpeg',
            'png',
            'webp',
            'gif',
            'bmp',
            'tiff',
            'mp4',
            'avi',
            'mkv',
            'mov',
            'webm',
            'mp3',
            'wav',
            'flac',
            'aac',
            'ogg',
            'wma',
            'm4a'
       ]
    )
    parser.add_argument("--output_dir", "-o", help="[O]utput path directory")

    args = parser.parse_args()

    files = get_files(args.path)
    convert(files, args.to, args.output_dir)


if __name__ == "__main__":
    main()
