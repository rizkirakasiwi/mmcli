from typing import Optional, Dict, Any, Callable, List
from functools import partial
from pytubefix import YouTube, Playlist
from pytubefix.cli import on_progress


def create_youtube_instance(url: str, progress_callback: Callable = on_progress) -> YouTube:
    """Create YouTube instance with progress callback."""
    return YouTube(url, on_progress_callback=progress_callback)


def create_playlist_instance(url: str) -> Playlist:
    """Create YouTube playlist instance."""
    return Playlist(url)


def select_video_stream(yt: YouTube, resolution: Optional[str]):
    """Select video stream based on resolution preference."""
    if resolution is not None:
        return yt.streams.get_by_resolution(resolution)
    return yt.streams.get_highest_resolution()


def select_audio_stream(yt: YouTube):
    """Select best available audio stream."""
    return yt.streams.get_audio_only()


def download_stream(stream, output_path: str) -> Optional[str]:
    """Download stream to specified output path."""
    return stream.download(output_path=output_path)


def get_video_metadata(yt: YouTube) -> Dict[str, Any]:
    """Extract video metadata."""
    return {
        "title": yt.title,
        "length": yt.length,
        "views": yt.views,
        "author": yt.author
    }


def get_playlist_metadata(playlist: Playlist) -> Dict[str, Any]:
    """Extract playlist metadata."""
    return {
        "title": playlist.title,
        "video_count": len(list(playlist.videos)),
        "owner": playlist.owner
    }


def download_single_video(
    url: str, 
    output_path: str, 
    resolution: Optional[str] = None,
    progress_callback: Callable = on_progress
) -> Dict[str, Any]:
    """Download single YouTube video."""
    yt = create_youtube_instance(url, progress_callback)
    stream = select_video_stream(yt, resolution)
    
    downloaded_file = download_stream(stream, output_path)
    metadata = get_video_metadata(yt)
    
    return {
        "success": downloaded_file is not None,
        "file_path": downloaded_file,
        "metadata": metadata
    }


def download_single_audio(
    url: str, 
    output_path: str,
    progress_callback: Callable = on_progress
) -> Dict[str, Any]:
    """Download single YouTube audio."""
    yt = create_youtube_instance(url, progress_callback)
    stream = select_audio_stream(yt)
    
    downloaded_file = download_stream(stream, output_path)
    metadata = get_video_metadata(yt)
    
    return {
        "success": downloaded_file is not None,
        "file_path": downloaded_file,
        "metadata": metadata
    }


def download_playlist_videos(
    url: str,
    output_path: str,
    resolution: Optional[str] = None,
    progress_callback: Callable = on_progress
) -> List[Dict[str, Any]]:
    """Download all videos from YouTube playlist."""
    playlist = create_playlist_instance(url)
    playlist_meta = get_playlist_metadata(playlist)
    
    download_video_func = partial(
        download_single_video,
        output_path=output_path,
        resolution=resolution,
        progress_callback=progress_callback
    )
    
    results = []
    for index, yt in enumerate(playlist.videos):
        print(f"[{index+1}/{playlist_meta['video_count']}] Downloading: {yt.title}")
        
        try:
            result = download_video_func(yt.watch_url)
            if result["success"]:
                print(f"✓ Successfully downloaded {yt.title}")
            else:
                print(f"✗ Failed to download {yt.title}")
            results.append(result)
        except Exception as e:
            print(f"✗ Error downloading {yt.title}: {e}")
            results.append({
                "success": False,
                "file_path": None,
                "metadata": {"title": yt.title, "error": str(e)}
            })
    
    return results


def download_playlist_audios(
    url: str,
    output_path: str,
    progress_callback: Callable = on_progress
) -> List[Dict[str, Any]]:
    """Download all audios from YouTube playlist."""
    playlist = create_playlist_instance(url)
    playlist_meta = get_playlist_metadata(playlist)
    
    download_audio_func = partial(
        download_single_audio,
        output_path=output_path,
        progress_callback=progress_callback
    )
    
    results = []
    for index, yt in enumerate(playlist.videos):
        print(f"[{index+1}/{playlist_meta['video_count']}] Downloading: {yt.title}")
        
        try:
            result = download_audio_func(yt.watch_url)
            if result["success"]:
                print(f"✓ Successfully downloaded {yt.title}")
            else:
                print(f"✗ Failed to download {yt.title}")
            results.append(result)
        except Exception as e:
            print(f"✗ Error downloading {yt.title}: {e}")
            results.append({
                "success": False,
                "file_path": None,
                "metadata": {"title": yt.title, "error": str(e)}
            })
    
    return results


def is_youtube_url(url: str) -> bool:
    """Check if URL is a YouTube URL."""
    return "youtube.com" in url or "youtu.be" in url


def is_playlist_url(url: str) -> bool:
    """Check if URL is a playlist URL."""
    return "list=" in url


def validate_youtube_url(url: str) -> Dict[str, bool]:
    """Validate YouTube URL and determine type."""
    return {
        "is_valid": is_youtube_url(url),
        "is_playlist": is_playlist_url(url)
    }
