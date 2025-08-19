import argparse
import media_converter
import media_downloader


def main():
    parser = argparse.ArgumentParser(
        description="Centralized multimedia tool for downloading and converting media files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
            Examples:
              Download video: %(prog)s --download --video https://youtube.com/watch?v=example
              Download audio: %(prog)s --download --audio https://youtube.com/watch?v=example
              Convert files:  %(prog)s --convert --path samples/*.avif --to jpg
        """,
    )

    parser.add_argument("--download", action="store_true", help="Download mode")
    parser.add_argument("--convert", action="store_true", help="Convert mode")

    # Download options
    parser.add_argument("--video", help="YouTube URL to download as video")
    parser.add_argument("--audio", help="YouTube URL to download as audio only")

    # Convert options
    parser.add_argument(
        "--path", "-p", help="Path to file(s), supports pattern format like files/*.jpg"
    )
    parser.add_argument(
        "--to",
        "-t",
        choices=[
            "jpg",
            "jpeg",
            "png",
            "webp",
            "gif",
            "bmp",
            "tiff",
            "mp4",
            "avi",
            "mkv",
            "mov",
            "webm",
            "mp3",
            "wav",
            "flac",
            "aac",
            "ogg",
            "wma",
            "m4a",
        ],
        help="Target format to convert to",
    )
    parser.add_argument("--output_dir", "-o", help="Output directory")

    args = parser.parse_args()

    if args.download:
        if args.video:
            media_downloader.youtube_downloader(args.video)
        elif args.audio:
            media_downloader.youtube_audio_downloader(args.audio)
        else:
            print("Error: --download requires either --video or --audio")
            parser.print_help()

    elif args.convert:
        if not args.path or not args.to:
            print("Error: --convert requires --path and --to")
            parser.print_help()
            return
        files = media_converter.get_files(args.path)
        media_converter.convert(files, args.to, args.output_dir)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()

