import os
import sys
from typing import Optional, Dict, Any, Callable, List 
from ..utils.media_format import video_formats, get_format, audio_formats
from pytubefix import YouTube, Playlist
from pytubefix.cli import on_progress
from . import media_converter

def get_output_dir() -> str:
    """Get output directory."""
    return os.path.join(os.getcwd(), "downloads")

def select_stream_by_resolution(yt: YouTube, resolution: Optional[str]):
    """Select stream based on resolution."""
    if resolution is not None:
        return yt.streams.get_by_resolution(resolution)
    return yt.streams.get_highest_resolution()

def get_video_format_or_default(format_arg: Optional[str]) -> str:
    """Get video format with default."""
    if format_arg is None:
        return "mp4"
    
    formats = get_format(format_arg, video_formats)
    if not formats:
        raise ValueError(f"Unsupported format: {format_arg}")
    return formats[0]["format"]

def get_audio_format_or_default(format_arg: Optional[str]) -> str:
    """Get audio format with default."""
    if format_arg is None:
        return "mp3"
    
    formats = get_format(format_arg, audio_formats)
    if not formats:
        raise ValueError(f"Unsupported format: {format_arg}")
    return formats[0]["format"]

def create_output_path(base_dir: str, media_type) -> str:
    """Create output path."""
    return os.path.join(base_dir, media_type)

def extract_file_extension(filepath: str) -> str:
    """Extract file extension from filepath."""
    return os.path.splitext(filepath)[1][1:].lower()

def should_convert_format(current_ext: str, target_format: str) -> bool:
    """Determine if conversion is needed."""
    return current_ext.lower() != target_format.lower()

def create_youtube_instance(url: str, progress_callback: Callable = on_progress) -> YouTube:
    """Factory function for YouTube instance."""
    return YouTube(url, on_progress_callback=progress_callback)


def ensure_directory_exists(path: str) -> str:
    """Ensure directory exists and return path."""
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)
    return path

def download_stream(stream, output_path: str) -> Optional[str]:
    """Download stream to output path."""
    return stream.download(output_path=output_path)

def convert_media_if_needed(downloaded_file: str, target_format: str, args) -> bool:
    """Handle media conversion logic."""
    current_ext = extract_file_extension(downloaded_file)
    
    if should_convert_format(current_ext, target_format):
        print(f"Converting to {target_format} format...")
        media_converter.convert(args)
        os.remove(downloaded_file)
        return True
    return False

def download_playlist_video_pipeline(args) -> List[Dict[str, Any]]:
    """Functional pipeline for playlist video download."""
    try:
        # Data transformations
        output_dir = get_output_dir()
        output_format = get_video_format_or_default(args.format)
        output_path = create_output_path(output_dir, "playlist")
        
        # Create YouTube playlist instance
        pl = Playlist(args.url)
        output_path = os.path.join(output_path, "videos", pl.title)

        download_status = [] 
        for index, yt in enumerate(pl.videos):
            print(f"[{index+1}/{len(list(pl.videos))}] Downloading: {yt.title}")
        
            # Select appropriate stream
            stream = select_stream_by_resolution(yt, args.resolution)
        
            # Ensure output directory exists
            ensure_directory_exists(output_path)
            
            # Download the file
            downloaded_file = download_stream(stream, output_path)
            
            if downloaded_file is None:
                print(f"Error downloading video {yt.title}")
            else:
                print(f"✓ Successfully downloaded {yt.title}")
        
            download_status.append({
                "success": downloaded_file is not None,
                "title": yt.title,
                "path": output_path,
                "format": output_format,
            })
        
        return download_status
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

def download_youtube_video_pipeline(args) -> Dict[str, Any]:
    """Functional pipeline for video download."""
    try:
        # Data transformations
        output_dir = get_output_dir()
        output_format = get_video_format_or_default(args.format)
        output_path = create_output_path(output_dir, "videos")
        
        # Create YouTube instance
        yt = create_youtube_instance(args.url)
        print(f"Download {yt.title}")
        
        # Select appropriate stream
        stream = select_stream_by_resolution(yt, args.resolution)
        
        # Ensure output directory exists
        ensure_directory_exists(output_path)
        
        # Download the file
        downloaded_file = download_stream(stream, output_path)
        
        if downloaded_file is None:
            raise RuntimeError(f"Error downloading video {yt.title}")
        
        # Handle conversion
        was_converted = convert_media_if_needed(downloaded_file, output_format, args)
        
        status_msg = "Video converted and saved to" if was_converted else "Video saved to"
        print(f"{status_msg} {output_path}")
        
        return {
            "success": True,
            "title": yt.title,
            "path": output_path,
            "format": output_format,
            "converted": was_converted
        }
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


def download_video_pipeline(args):
    """Functional pipeline for video download."""

    if "youtube.com" in args.url or "youtu.be" in args.url:
        if "list=" in args.url:
            return download_playlist_video_pipeline(args)
        else:
            return download_youtube_video_pipeline(args)

    raise ValueError(f"Unsupported URL: {args.url}, currently only YouTube URLs are supported.")

def download_audio_pipeline(args) -> Dict[str, Any]:
    """Functional pipeline for audio download."""
    try:
        # Data transformations
        output_dir = get_output_dir()
        output_format = get_audio_format_or_default(args.format)
        output_path = create_output_path(output_dir, "audios")
        
        # Create YouTube instance
        yt = create_youtube_instance(args.url)
        print(f"Download {yt.title}")
        
        # Get audio stream
        stream = yt.streams.get_audio_only()
        
        # Ensure output directory exists
        ensure_directory_exists(output_path)
        
        # Download the file
        downloaded_file = download_stream(stream, output_path)
        
        if downloaded_file is None:
            raise RuntimeError(f"Error downloading audio {yt.title}")
        
        # Handle conversion
        was_converted = convert_media_if_needed(downloaded_file, output_format, args)
        
        print(f"Audio saved to {output_path}")
        
        return {
            "success": True,
            "title": yt.title,
            "path": output_path,
            "format": output_format,
            "converted": was_converted
        }
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


def download(args):
    """Main download dispatcher function."""
    download_functions = {
        "video": download_video_pipeline,
        "audio": download_audio_pipeline
    }
    
    download_func = download_functions.get(args.type)
    if not download_func:
        raise ValueError(f"Unsupported download type: {args.type}")
    
    
    result = download_func(args)

    if isinstance(result, list):
        total_item = len(result)
        success_count = len(list(filter(lambda x: x["success"], result)))
        failed_count = total_item - success_count
        saved_locations = list(map(lambda x: x["path"], result))[0]
        print("Download Summary: ")
        print("- Total items:", total_item)
        print("- Successfully downloaded:", success_count)
        print("- Failed to download:", failed_count)
        print("- Saved to:", saved_locations)
    else:
        print("Downloaded 1 item")
