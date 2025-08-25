import pytest
import tempfile
import shutil
import os
from pathlib import Path
from unittest.mock import patch, MagicMock, call
from app.tools.media_downloader import (
    create_playlist_config,
    download_playlist_videos,
    download_playlist_audios,
    route_video_download,
    route_audio_download,
)
from app.tools.youtube_downloader import (
    create_playlist_instance,
    get_playlist_metadata,
    download_playlist_videos as yt_download_playlist_videos,
    download_playlist_audios as yt_download_playlist_audios,
    validate_youtube_url,
    is_playlist_url,
)


class TestPlaylistDownloader:
    def setup_method(self):
        """Set up test fixtures"""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.playlist_url = "https://youtube.com/playlist?list=PLrAXtmRdnEQy4TyTh9zg8qFm9K2vOzIEm"
        self.video_url_in_playlist = "https://youtube.com/watch?v=test123&list=PLrAXtmRdnEQy4TyTh9zg8qFm9K2vOzIEm"

    def teardown_method(self):
        """Clean up test fixtures"""
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)

    def test_is_playlist_url_detection(self):
        """Test playlist URL detection"""
        # Test various playlist URL formats
        assert is_playlist_url(self.playlist_url) is True
        assert is_playlist_url(self.video_url_in_playlist) is True
        assert is_playlist_url("https://youtube.com/watch?v=test123") is False
        assert is_playlist_url("https://youtu.be/test123") is False

    def test_validate_youtube_playlist_url(self):
        """Test YouTube playlist URL validation"""
        result = validate_youtube_url(self.playlist_url)
        assert result["is_valid"] is True
        assert result["is_playlist"] is True

        result = validate_youtube_url(self.video_url_in_playlist)
        assert result["is_valid"] is True
        assert result["is_playlist"] is True

        result = validate_youtube_url("https://youtube.com/watch?v=test123")
        assert result["is_valid"] is True
        assert result["is_playlist"] is False

    @patch('app.tools.youtube_downloader.Playlist')
    def test_create_playlist_instance(self, mock_playlist_class):
        """Test creating YouTube playlist instance"""
        mock_playlist = MagicMock()
        mock_playlist_class.return_value = mock_playlist
        
        result = create_playlist_instance(self.playlist_url)
        
        assert result == mock_playlist
        mock_playlist_class.assert_called_once_with(self.playlist_url)

    @patch('app.tools.youtube_downloader.Playlist')
    def test_get_playlist_metadata(self, mock_playlist_class):
        """Test extracting playlist metadata"""
        mock_playlist = MagicMock()
        mock_playlist.title = "Test Playlist"
        mock_playlist.owner = "Test Owner"
        mock_playlist.videos = [MagicMock(), MagicMock(), MagicMock()]  # 3 videos
        mock_playlist_class.return_value = mock_playlist
        
        playlist = create_playlist_instance(self.playlist_url)
        result = get_playlist_metadata(playlist)
        
        assert result["title"] == "Test Playlist"
        assert result["owner"] == "Test Owner"
        assert result["video_count"] == 3

    @patch('app.tools.media_downloader.ensure_directory_exists')
    @patch('app.tools.media_downloader.create_playlist_config')
    @patch('app.tools.youtube_downloader.download_playlist_videos')
    def test_download_playlist_videos_success(self, mock_yt_download, mock_config, mock_ensure_dir):
        """Test successful playlist video download"""
        mock_args = MagicMock()
        mock_args.url = self.playlist_url
        mock_args.format = "mp4"
        mock_args.resolution = "720p"

        # Setup config
        config = {
            "url": self.playlist_url,
            "output_path": "/downloads/playlist/videos/Test Playlist",
            "output_format": "mp4",
            "resolution": "720p",
            "args": mock_args
        }
        mock_config.return_value = config

        # Setup YouTube downloader response
        mock_yt_download.return_value = [
            {
                "success": True,
                "file_path": "/downloads/playlist/videos/Test Playlist/video1.mp4",
                "metadata": {"title": "Video 1", "length": 120}
            },
            {
                "success": True,
                "file_path": "/downloads/playlist/videos/Test Playlist/video2.mp4",
                "metadata": {"title": "Video 2", "length": 180}
            }
        ]

        result = download_playlist_videos(config)

        assert len(result) == 2
        assert all(item["success"] for item in result)
        assert result[0]["title"] == "Video 1"
        assert result[1]["title"] == "Video 2"
        mock_yt_download.assert_called_once_with(
            self.playlist_url,
            "/downloads/playlist/videos/Test Playlist",
            "720p"
        )

    @patch('app.tools.media_downloader.ensure_directory_exists')
    @patch('app.tools.media_downloader.create_playlist_config')
    @patch('app.tools.youtube_downloader.download_playlist_audios')
    @patch('app.tools.media_downloader.convert_if_needed')
    def test_download_playlist_audios_success(self, mock_convert, mock_yt_download, mock_config, mock_ensure_dir):
        """Test successful playlist audio download"""
        mock_args = MagicMock()
        mock_args.url = self.playlist_url
        mock_args.format = "mp3"

        # Setup config
        config = {
            "url": self.playlist_url,
            "output_path": "/downloads/playlist/audios/Test Playlist",
            "output_format": "mp3",
            "args": mock_args
        }
        mock_config.return_value = config

        # Setup YouTube downloader response
        mock_yt_download.return_value = [
            {
                "success": True,
                "file_path": "/downloads/playlist/audios/Test Playlist/audio1.webm",
                "metadata": {"title": "Audio 1", "length": 120}
            },
            {
                "success": False,
                "file_path": None,
                "metadata": {"title": "Audio 2", "error": "Download failed"}
            }
        ]
        
        # Mock conversion
        mock_convert.return_value = True

        result = download_playlist_audios(config)

        assert len(result) == 2
        assert result[0]["success"] is True
        assert result[0]["title"] == "Audio 1"
        assert result[1]["success"] is False
        assert result[1]["title"] == "Audio 2"
        mock_yt_download.assert_called_once_with(
            self.playlist_url,
            "/downloads/playlist/audios/Test Playlist"
        )

    @patch('app.tools.youtube_downloader.Playlist')
    @patch('app.tools.youtube_downloader.download_single_video')
    def test_youtube_download_playlist_videos_integration(self, mock_download_single, mock_playlist_class):
        """Test YouTube playlist video download integration"""
        # Setup playlist mock
        mock_playlist = MagicMock()
        mock_playlist.title = "Test Playlist"
        
        # Setup video mocks
        mock_video1 = MagicMock()
        mock_video1.title = "Video 1"
        mock_video1.watch_url = "https://youtube.com/watch?v=video1"
        
        mock_video2 = MagicMock()
        mock_video2.title = "Video 2"
        mock_video2.watch_url = "https://youtube.com/watch?v=video2"
        
        mock_playlist.videos = [mock_video1, mock_video2]
        mock_playlist_class.return_value = mock_playlist

        # Setup download responses
        mock_download_single.side_effect = [
            {
                "success": True,
                "file_path": "/downloads/video1.mp4",
                "metadata": {"title": "Video 1"}
            },
            {
                "success": True,
                "file_path": "/downloads/video2.mp4",
                "metadata": {"title": "Video 2"}
            }
        ]

        result = yt_download_playlist_videos(
            self.playlist_url,
            "/downloads",
            "720p"
        )

        assert len(result) == 2
        assert all(item["success"] for item in result)
        assert mock_download_single.call_count == 2
        
        # Verify calls were made with correct URLs and parameters
        call_args_list = mock_download_single.call_args_list
        assert call_args_list[0][0][0] == "https://youtube.com/watch?v=video1"
        assert call_args_list[0][1]["output_path"] == "/downloads"
        assert call_args_list[0][1]["resolution"] == "720p"
        
        assert call_args_list[1][0][0] == "https://youtube.com/watch?v=video2"
        assert call_args_list[1][1]["output_path"] == "/downloads"
        assert call_args_list[1][1]["resolution"] == "720p"

    @patch('app.tools.youtube_downloader.Playlist')
    @patch('app.tools.youtube_downloader.download_single_audio')
    def test_youtube_download_playlist_audios_integration(self, mock_download_single, mock_playlist_class):
        """Test YouTube playlist audio download integration"""
        # Setup playlist mock
        mock_playlist = MagicMock()
        mock_playlist.title = "Test Playlist"
        
        # Setup video mocks (for audio extraction)
        mock_video1 = MagicMock()
        mock_video1.title = "Audio 1"
        mock_video1.watch_url = "https://youtube.com/watch?v=video1"
        
        mock_playlist.videos = [mock_video1]
        mock_playlist_class.return_value = mock_playlist

        # Setup download response
        mock_download_single.return_value = {
            "success": True,
            "file_path": "/downloads/audio1.webm",
            "metadata": {"title": "Audio 1"}
        }

        result = yt_download_playlist_audios(
            self.playlist_url,
            "/downloads"
        )

        assert len(result) == 1
        assert result[0]["success"] is True
        # Verify the call was made with expected arguments
        mock_download_single.assert_called_once()
        call_args = mock_download_single.call_args
        assert call_args[0][0] == "https://youtube.com/watch?v=video1"  # URL
        assert call_args[1]["output_path"] == "/downloads"  # output_path
        assert "progress_callback" in call_args[1]  # progress_callback

    def test_playlist_config_creation(self):
        """Test playlist configuration creation"""
        mock_args = MagicMock()
        mock_args.url = self.playlist_url
        mock_args.format = "mp4"
        mock_args.resolution = "720p"

        with patch('app.tools.media_downloader.youtube_downloader.validate_youtube_url') as mock_validate, \
             patch('app.tools.media_downloader.youtube_downloader.create_playlist_instance') as mock_create_playlist, \
             patch('app.tools.media_downloader.ensure_directory_exists') as mock_ensure_dir:
            
            mock_validate.return_value = {"is_valid": True, "is_playlist": True}
            mock_playlist = MagicMock()
            mock_playlist.title = "My Test Playlist"
            mock_create_playlist.return_value = mock_playlist
            mock_ensure_dir.return_value = "/downloads/playlist/videos/My Test Playlist"

            from app.tools.media_downloader import create_playlist_config
            config = create_playlist_config(mock_args, "video")

            assert config["url"] == self.playlist_url
            assert config["output_format"] == "mp4"
            assert config["resolution"] == "720p"
            assert "My Test Playlist" in config["output_path"]

    @patch('app.tools.media_downloader.youtube_downloader.validate_youtube_url')
    @patch('app.tools.media_downloader.create_playlist_config')
    @patch('app.tools.media_downloader.download_playlist_videos')
    def test_route_video_download_playlist(self, mock_download_playlist, mock_create_config, mock_validate):
        """Test routing video download for playlist URLs"""
        mock_args = MagicMock()
        mock_args.url = self.playlist_url
        mock_args.format = "mp4"

        mock_validate.return_value = {"is_valid": True, "is_playlist": True}
        mock_config = {"url": self.playlist_url, "output_format": "mp4"}
        mock_create_config.return_value = mock_config
        
        mock_download_playlist.return_value = [
            {"success": True, "title": "Video 1"},
            {"success": True, "title": "Video 2"}
        ]

        result = route_video_download(mock_args)

        assert len(result) == 2
        mock_validate.assert_called_once_with(self.playlist_url)
        mock_create_config.assert_called_once_with(mock_args, "video")
        mock_download_playlist.assert_called_once_with(mock_config)

    @patch('app.tools.media_downloader.youtube_downloader.validate_youtube_url')
    @patch('app.tools.media_downloader.create_playlist_config')
    @patch('app.tools.media_downloader.download_playlist_audios')
    def test_route_audio_download_playlist(self, mock_download_playlist, mock_create_config, mock_validate):
        """Test routing audio download for playlist URLs"""
        mock_args = MagicMock()
        mock_args.url = self.playlist_url
        mock_args.format = "mp3"

        mock_validate.return_value = {"is_valid": True, "is_playlist": True}
        mock_config = {"url": self.playlist_url, "output_format": "mp3"}
        mock_create_config.return_value = mock_config
        
        mock_download_playlist.return_value = [
            {"success": True, "title": "Audio 1"},
            {"success": False, "title": "Audio 2"}
        ]

        result = route_audio_download(mock_args)

        assert len(result) == 2
        mock_validate.assert_called_once_with(self.playlist_url)
        mock_create_config.assert_called_once_with(mock_args, "audio")
        mock_download_playlist.assert_called_once_with(mock_config)

    @patch('app.tools.youtube_downloader.Playlist')
    def test_playlist_error_handling(self, mock_playlist_class):
        """Test playlist error handling for individual video failures"""
        # Setup playlist mock
        mock_playlist = MagicMock()
        mock_playlist.title = "Test Playlist"
        
        # Setup video mock that will cause an error
        mock_video = MagicMock()
        mock_video.title = "Problematic Video"
        mock_video.watch_url = "https://youtube.com/watch?v=problem"
        mock_playlist.videos = [mock_video]
        mock_playlist_class.return_value = mock_playlist

        with patch('app.tools.youtube_downloader.download_single_video') as mock_download:
            mock_download.side_effect = Exception("Network error")
            
            result = yt_download_playlist_videos(
                self.playlist_url,
                "/downloads",
                "720p"
            )

            assert len(result) == 1
            assert result[0]["success"] is False
            assert "Network error" in result[0]["metadata"]["error"]

    def test_empty_playlist_handling(self):
        """Test handling of empty playlists"""
        with patch('app.tools.youtube_downloader.Playlist') as mock_playlist_class:
            mock_playlist = MagicMock()
            mock_playlist.title = "Empty Playlist"
            mock_playlist.videos = []  # Empty playlist
            mock_playlist_class.return_value = mock_playlist

            result = yt_download_playlist_videos(
                self.playlist_url,
                "/downloads",
                "720p"
            )

            assert result == []

    @patch('builtins.print')
    def test_playlist_download_progress_output(self, mock_print):
        """Test that playlist downloads show progress information"""
        with patch('app.tools.youtube_downloader.Playlist') as mock_playlist_class, \
             patch('app.tools.youtube_downloader.download_single_video') as mock_download:
            
            mock_playlist = MagicMock()
            mock_playlist.title = "Test Playlist"
            
            mock_video1 = MagicMock()
            mock_video1.title = "Video 1"
            mock_video1.watch_url = "https://youtube.com/watch?v=video1"
            mock_playlist.videos = [mock_video1]
            mock_playlist_class.return_value = mock_playlist

            mock_download.return_value = {
                "success": True,
                "file_path": "/downloads/video1.mp4",
                "metadata": {"title": "Video 1"}
            }

            yt_download_playlist_videos(self.playlist_url, "/downloads", "720p")

            # Check that progress was printed
            print_calls = [call[0][0] for call in mock_print.call_args_list]
            assert any("[1/1] Downloading: Video 1" in call for call in print_calls)
            assert any("✓ Successfully downloaded Video 1" in call for call in print_calls)