import argparse
from .media_format import all_formats

def command_manager():
    epilog_text = """
    Other:
        download --help     Show available command for download
        convert --help      Show available command for convert

    Examples:
        Downloads:
            mmcli download video --url "https://youtube.com/watch?v=..." --resolution 720p
            mmcli download audio --url "https://youtube.com/watch?v=..." --format mp3
            mmcli download --help

        Convert:
            mmcli convert --path "videos/*.mp4" --to mp3 --output_dir converted/
            mmcli convert --path "image.jpg" --to png
            mmcli convert --help
    """
    parser = argparse.ArgumentParser(
        description="Multimedia Helper CLI Command",
        epilog=epilog_text,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    
    # Add version argument
    parser.add_argument(
        "--version", "-v",
        action="version",
        version="mmcli 0.1.0a1"
    )

    # Top-level commands
    subparsers = parser.add_subparsers(
        dest="command", required=True, help="Available commands"
    )
    __download_command(subparsers)
    __convert_command(subparsers)

    return parser.parse_args()


def __download_command(subparsers):
    # Download command
    download_parser = subparsers.add_parser(
        "download",
        help="Download video/audio from YouTube or other platforms",
    )
    # Subcommands for download
    download_subparser = download_parser.add_subparsers(
        dest="type", required=True, help="Download type"
    )

    # Video downloader
    video_parser = download_subparser.add_parser("video", help="Download video")
    video_parser.add_argument("--url", "-u", required=True, help="Video URL")
    video_parser.add_argument(
        "--resolution",
        "-r",
        help="(Optional) Video resolution (e.g. '720p', '480p') default: higher resolution",
    )
    video_parser.add_argument(
        "--format",
        "-f",
        help="(Optional) Output format (e.g. 'mp4', 'mkv') default: mp4",
    )

    # Audio downloader
    audio_parser = download_subparser.add_parser("audio", help="Download audio")
    audio_parser.add_argument("--url", "-u", required=True, help="Audio URL")
    audio_parser.add_argument(
        "--format", "-f", help="(Optional) Output format (default: m4a)"
    )


def __convert_command(subparsers):
    # Convert command
    convert_parser = subparsers.add_parser(
        "convert",
        help="Convert video/audio into another format",
    )
    # Arguments for convert
    convert_parser.add_argument(
        "--path",
        "-p",
        required=True,
        help="Path to file(s), supports patterns like file/to/*.jpg",
    )
    convert_parser.add_argument(
        "--to",
        "-t",
        required=True,
        choices=list(map(lambda f: f["alias"], all_formats)),
        help="Target format to convert to",
    )
    convert_parser.add_argument(
        "--output_dir",
        "-o",
        help="(Optional) Output directory for converted files. default: converter/",
    )
    convert_parser.add_argument(
        "--max-workers", "-w",
        type=int,
        help="(Optional) Number of parallel conversions for batch operations (default: from config)"
    )
