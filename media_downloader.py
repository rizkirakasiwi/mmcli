import os
import argparse
from pytubefix import YouTube
from pytubefix.cli import on_progress
import media_converter

output_dir = os.path.join(os.getcwd(), "downloads")


def youtube_downloader(url: str):
    yt = YouTube(url, on_progress_callback=on_progress)
    print(yt.title)
    ys = yt.streams.get_highest_resolution()
    output_path = os.path.join(output_dir, "videos")
    if not os.path.exists(output_path):
        os.makedirs(output_path, exist_ok=True)
    ys.download(output_path=output_path)  # type: ignore
    print(f"Video saved to {output_path}")


def youtube_audio_downloader(url: str):
    yt = YouTube(url, on_progress_callback=on_progress)
    print(yt.title)
    ys = yt.streams.get_audio_only()
    output_path = os.path.join(output_dir, "audios")
    if not os.path.exists(output_path):
        os.makedirs(output_path, exist_ok=True)

    ys.download(output_path=output_path)  # type: ignore
    downloaded_file = os.path.join(output_path, f"{yt.title}.m4a")
    media_converter.convert(
        input_files=[downloaded_file], output_dir=output_path, output_format="mp3"
    )
    os.remove(downloaded_file)
    print(f"Audio saved to {output_dir}")


def main():
    parser = argparse.ArgumentParser(
        description="Download videos and audio from YouTube"
    )
    parser.add_argument("--video", type=str, help="URL to download as video")
    parser.add_argument("--audio", type=str, help="URL to download as audio only")

    args = parser.parse_args()

    if args.video:
        youtube_downloader(args.video)
    elif args.audio:
        youtube_audio_downloader(args.audio)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
