import pytest
import tempfile
import shutil
import os
from pathlib import Path
from unittest.mock import patch, MagicMock, call
from app.tools.media_downloader import (
    get_output_dir,
    get_video_format_or_default,
    get_audio_format_or_default,
    create_output_path,
    extract_file_extension,
    should_convert_format,
    ensure_directory_exists,
    convert_if_needed,
    route_video_download,
    route_audio_download,
    download,
)
from app.tools.youtube_downloader import (
    create_youtube_instance,
    select_video_stream,
    select_audio_stream,
    download_stream,
)


class TestMediaDownloader:
    def setup_method(self):
        """Set up test fixtures"""
        self.temp_dir = Path(tempfile.mkdtemp())

    def teardown_method(self):
        """Clean up test fixtures"""
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)

    @patch('os.getcwd')
    def test_get_output_dir(self, mock_getcwd):
        """Test getting output directory"""
        mock_getcwd.return_value = "/test/path"
        result = get_output_dir()
        expected = os.path.join("/test/path", "downloads")
        assert result == expected

    def test_select_stream_by_resolution_with_resolution(self):
        """Test stream selection with specific resolution"""
        mock_yt = MagicMock()
        mock_stream = MagicMock()
        mock_yt.streams.get_by_resolution.return_value = mock_stream
        
        result = select_video_stream(mock_yt, "720p")
        
        assert result == mock_stream
        mock_yt.streams.get_by_resolution.assert_called_once_with("720p")
        mock_yt.streams.get_highest_resolution.assert_not_called()

    def test_select_stream_by_resolution_highest(self):
        """Test stream selection with highest resolution"""
        mock_yt = MagicMock()
        mock_stream = MagicMock()
        mock_yt.streams.get_highest_resolution.return_value = mock_stream
        
        result = select_video_stream(mock_yt, None)
        
        assert result == mock_stream
        mock_yt.streams.get_highest_resolution.assert_called_once()
        mock_yt.streams.get_by_resolution.assert_not_called()

    def test_get_video_format_or_default_none(self):
        """Test video format with None input"""
        result = get_video_format_or_default(None)
        assert result == "mp4"

    @patch('app.tools.media_downloader.get_format')
    def test_get_video_format_or_default_valid(self, mock_get_format):
        """Test video format with valid input"""
        mock_get_format.return_value = [{"format": "mkv"}]
        result = get_video_format_or_default("mkv")
        assert result == "mkv"

    @patch('app.tools.media_downloader.get_format')
    def test_get_video_format_or_default_invalid(self, mock_get_format):
        """Test video format with invalid input"""
        mock_get_format.return_value = []
        with pytest.raises(ValueError, match="Unsupported format: invalid"):
            get_video_format_or_default("invalid")

    def test_get_audio_format_or_default_none(self):
        """Test audio format with None input"""
        result = get_audio_format_or_default(None)
        assert result is None  # None indicates no conversion needed

    @patch('app.tools.media_downloader.get_format')
    def test_get_audio_format_or_default_valid(self, mock_get_format):
        """Test audio format with valid input"""
        mock_get_format.return_value = [{"format": "wav"}]
        result = get_audio_format_or_default("wav")
        assert result == "wav"

    def test_create_output_path(self):
        """Test creating output path"""
        result = create_output_path("/base", "videos")
        expected = os.path.join("/base", "videos")
        assert result == expected

    def test_extract_file_extension(self):
        """Test extracting file extension"""
        assert extract_file_extension("test.mp4") == "mp4"
        assert extract_file_extension("test.MP4") == "mp4"
        assert extract_file_extension("path/to/file.avi") == "avi"
        assert extract_file_extension("no_extension") == ""

    def test_should_convert_format(self):
        """Test format conversion decision"""
        assert should_convert_format("mp4", "mp3") is True
        assert should_convert_format("mp4", "MP4") is False
        assert should_convert_format("MP4", "mp4") is False
        assert should_convert_format("webm", "mp4") is True

    @patch('app.tools.youtube_downloader.YouTube')
    def test_create_youtube_instance(self, mock_youtube):
        """Test YouTube instance creation"""
        mock_instance = MagicMock()
        mock_youtube.return_value = mock_instance
        
        result = create_youtube_instance("https://youtube.com/watch?v=test")
        
        assert result == mock_instance
        mock_youtube.assert_called_once()

    @patch('os.path.exists')
    @patch('os.makedirs')
    def test_ensure_directory_exists_new(self, mock_makedirs, mock_exists):
        """Test ensuring new directory exists"""
        mock_exists.return_value = False
        
        result = ensure_directory_exists("/test/path")
        
        assert result == "/test/path"
        mock_makedirs.assert_called_once_with("/test/path", exist_ok=True)

    @patch('os.path.exists')
    @patch('os.makedirs')
    def test_ensure_directory_exists_existing(self, mock_makedirs, mock_exists):
        """Test ensuring existing directory exists"""
        mock_exists.return_value = True
        
        result = ensure_directory_exists("/test/path")
        
        assert result == "/test/path"
        mock_makedirs.assert_not_called()

    def test_download_stream(self):
        """Test downloading stream"""
        mock_stream = MagicMock()
        mock_stream.download.return_value = "/path/to/downloaded/file.mp4"
        
        result = download_stream(mock_stream, "/output/path")
        
        assert result == "/path/to/downloaded/file.mp4"
        mock_stream.download.assert_called_once_with(output_path="/output/path")

    @patch('app.tools.media_downloader.media_converter')
    @patch('os.remove')
    @pytest.mark.asyncio
    async def test_convert_media_if_needed_conversion_required(self, mock_remove, mock_converter):
        """Test media conversion when needed"""
        mock_args = MagicMock()
        from unittest.mock import AsyncMock
        mock_converter.convert.side_effect = AsyncMock(return_value=[{"success": True, "output_file": "test.mp4"}])
        
        result = await convert_if_needed("test.webm", "mp4", mock_args)
        
        assert result == "test.mp4"
        mock_remove.assert_called_once_with("test.webm")

    @patch('app.tools.media_downloader.media_converter')
    @patch('os.remove')
    @pytest.mark.asyncio
    async def test_convert_media_if_needed_no_conversion(self, mock_remove, mock_converter):
        """Test media conversion when not needed"""
        mock_args = MagicMock()
        
        result = await convert_if_needed("test.mp4", "mp4", mock_args)
        
        assert result == "test.mp4"
        mock_converter.convert.assert_not_called()
        mock_remove.assert_not_called()

    @patch('app.tools.media_downloader.get_output_dir')
    @patch('app.tools.media_downloader.get_video_format_or_default')
    @patch('app.tools.youtube_downloader.create_youtube_instance')
    @patch('app.tools.youtube_downloader.select_video_stream')
    @patch('app.tools.media_downloader.ensure_directory_exists')
    @patch('app.tools.youtube_downloader.download_stream')
    @patch('app.tools.media_downloader.convert_if_needed')
    @pytest.mark.asyncio
    async def test_download_youtube_video_pipeline_success(self, mock_convert, mock_download, 
                                           mock_ensure_dir, mock_select_stream,
                                           mock_create_yt, mock_get_format,
                                           mock_get_dir):
        """Test successful video download pipeline"""
        # Setup mocks
        mock_args = MagicMock()
        mock_args.url = "https://youtube.com/watch?v=test"
        mock_args.format = "mp4"
        mock_args.resolution = "720p"
        
        mock_get_dir.return_value = "/downloads"
        mock_get_format.return_value = "mp4"
        mock_yt = MagicMock()
        mock_yt.title = "Test Video"
        mock_create_yt.return_value = mock_yt
        mock_stream = MagicMock()
        mock_select_stream.return_value = mock_stream
        mock_ensure_dir.return_value = "/downloads/videos"
        mock_download.return_value = "/downloads/videos/test.mp4"
        from unittest.mock import AsyncMock
        mock_convert.side_effect = AsyncMock(return_value="/downloads/videos/test.mp4")
        
        result = await route_video_download(mock_args)
        
        # Verify result
        assert result["success"] is True
        assert result["title"] == "Test Video"
        assert result["format"] == "mp4"
        assert result["converted"] is False
        
        # Verify function calls (create_youtube_instance is called with url and progress callback)
        mock_create_yt.assert_called_once()
        mock_select_stream.assert_called_once_with(mock_yt, "720p")
        # Path will be normalized by the function, so check actual call
        mock_download.assert_called_once_with(mock_stream, "/downloads/videos")

    @patch('app.tools.media_downloader.get_output_dir')
    @patch('app.tools.media_downloader.get_audio_format_or_default')
    @patch('app.tools.youtube_downloader.create_youtube_instance')
    @patch('app.tools.media_downloader.ensure_directory_exists')
    @patch('app.tools.youtube_downloader.download_stream')
    @patch('app.tools.media_downloader.convert_if_needed')
    @pytest.mark.asyncio
    async def test_download_audio_pipeline_success(self, mock_convert, mock_download,
                                           mock_ensure_dir, mock_create_yt,
                                           mock_get_format, mock_get_dir):
        """Test successful audio download pipeline"""
        # Setup mocks
        mock_args = MagicMock()
        mock_args.url = "https://youtube.com/watch?v=test"
        mock_args.format = "mp3"
        
        mock_get_dir.return_value = "/downloads"
        mock_get_format.return_value = "mp3"
        mock_yt = MagicMock()
        mock_yt.title = "Test Audio"
        mock_create_yt.return_value = mock_yt
        mock_stream = MagicMock()
        mock_yt.streams.get_audio_only.return_value = mock_stream
        mock_ensure_dir.return_value = "/downloads/audios"
        mock_download.return_value = "/downloads/audios/test.webm"
        from unittest.mock import AsyncMock
        mock_convert.side_effect = AsyncMock(return_value=True)
        
        result = await route_audio_download(mock_args)
        
        # Verify result
        assert result["success"] is True
        assert result["title"] == "Test Audio"
        assert result["format"] == "mp3"
        assert result["converted"] is True

    @patch('app.tools.media_downloader.route_video_download')
    @pytest.mark.asyncio
    async def test_download_dispatcher_video(self, mock_video_pipeline):
        """Test download dispatcher for video"""
        mock_args = MagicMock()
        mock_args.type = "video"
        mock_result = {"success": True}
        from unittest.mock import AsyncMock
        mock_video_pipeline.side_effect = AsyncMock(return_value=mock_result)
        
        result = await download(mock_args)
        
        assert result == mock_result
        mock_video_pipeline.assert_called_once_with(mock_args)

    @patch('app.tools.media_downloader.route_audio_download')
    @pytest.mark.asyncio
    async def test_download_dispatcher_audio(self, mock_audio_pipeline):
        """Test download dispatcher for audio"""
        mock_args = MagicMock()
        mock_args.type = "audio"
        mock_result = {"success": True}
        from unittest.mock import AsyncMock
        mock_audio_pipeline.side_effect = AsyncMock(return_value=mock_result)
        
        result = await download(mock_args)
        
        assert result == mock_result
        mock_audio_pipeline.assert_called_once_with(mock_args)

    @pytest.mark.asyncio
    async def test_download_dispatcher_invalid_type(self):
        """Test download dispatcher with invalid type"""
        mock_args = MagicMock()
        mock_args.type = "invalid"
        
        with pytest.raises(ValueError, match="Unsupported download type: invalid"):
            await download(mock_args)

    @pytest.mark.asyncio
    async def test_download_youtube_video_pipeline_error(self):
        """Test video download pipeline error handling"""
        mock_args = MagicMock()
        mock_args.url = "https://invalid.com/watch?v=test"  # Invalid URL
        mock_args.format = "mp4"
        
        # Should raise ValueError for unsupported URL
        with pytest.raises(ValueError, match="Unsupported URL"):
            await route_video_download(mock_args)
