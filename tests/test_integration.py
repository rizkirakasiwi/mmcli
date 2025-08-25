import pytest
import subprocess
import tempfile
import shutil
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock
import main


class TestIntegration:
    def setup_method(self):
        """Set up test fixtures"""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.test_file = self.temp_dir / "test.jpg"
        # Create a simple test file
        self.test_file.write_bytes(b'\xff\xd8\xff\xe0' + b'\x00' * 100)  # Minimal JPEG header

    def teardown_method(self):
        """Clean up test fixtures"""
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)

    @patch('main.download')
    @patch('main.command_manager')
    def test_main_download_video_command(self, mock_command_manager, mock_download):
        """Test main function with download video command"""
        mock_args = MagicMock()
        mock_args.command = "download"
        mock_args.type = "video"
        mock_args.url = "https://youtube.com/watch?v=test"
        mock_command_manager.return_value = mock_args
        mock_download.return_value = {"success": True}

        main.main()

        mock_command_manager.assert_called_once()
        mock_download.assert_called_once_with(mock_args)

    @patch('main.download')
    @patch('main.command_manager')
    def test_main_download_audio_command(self, mock_command_manager, mock_download):
        """Test main function with download audio command"""
        mock_args = MagicMock()
        mock_args.command = "download"
        mock_args.type = "audio"
        mock_args.url = "https://youtube.com/watch?v=test"
        mock_command_manager.return_value = mock_args
        mock_download.return_value = {"success": True}

        main.main()

        mock_command_manager.assert_called_once()
        mock_download.assert_called_once_with(mock_args)

    @patch('main.convert')
    @patch('main.command_manager')
    def test_main_convert_command(self, mock_command_manager, mock_convert):
        """Test main function with convert command"""
        mock_args = MagicMock()
        mock_args.command = "convert"
        mock_args.path = "test.jpg"
        mock_args.to = "png"
        mock_command_manager.return_value = mock_args

        main.main()

        mock_command_manager.assert_called_once()
        mock_convert.assert_called_once_with(mock_args)

    @patch('builtins.print')
    @patch('main.command_manager')
    def test_main_invalid_command(self, mock_command_manager, mock_print):
        """Test main function with invalid command"""
        mock_args = MagicMock()
        mock_args.command = "invalid"
        mock_args.print_help = MagicMock()
        mock_command_manager.return_value = mock_args

        main.main()

        mock_command_manager.assert_called_once()
        mock_print.assert_called_with("Command not found")
        mock_args.print_help.assert_called_once()

    def test_cli_help_message(self):
        """Test CLI help message displays correctly"""
        try:
            result = subprocess.run(
                [sys.executable, "main.py", "--help"],
                cwd=str(Path(__file__).parent.parent),
                capture_output=True,
                text=True,
                timeout=10
            )
            
            assert "Multimedia Helper CLI Command" in result.stdout
            assert "download" in result.stdout
            assert "convert" in result.stdout
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pytest.skip("CLI not available for integration testing")

    def test_cli_download_help(self):
        """Test CLI download help message"""
        try:
            result = subprocess.run(
                [sys.executable, "main.py", "download", "--help"],
                cwd=str(Path(__file__).parent.parent),
                capture_output=True,
                text=True,
                timeout=10
            )
            
            assert "video" in result.stdout
            assert "audio" in result.stdout
            # --url is only shown in video/audio subcommand help, not in download help
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pytest.skip("CLI not available for integration testing")

    def test_cli_convert_help(self):
        """Test CLI convert help message"""
        try:
            result = subprocess.run(
                [sys.executable, "main.py", "convert", "--help"],
                cwd=str(Path(__file__).parent.parent),
                capture_output=True,
                text=True,
                timeout=10
            )
            
            assert "--path" in result.stdout
            assert "--to" in result.stdout
            assert "--output_dir" in result.stdout
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pytest.skip("CLI not available for integration testing")

    def test_cli_download_video_help(self):
        """Test CLI download video help message"""
        try:
            result = subprocess.run(
                [sys.executable, "main.py", "download", "video", "--help"],
                cwd=str(Path(__file__).parent.parent),
                capture_output=True,
                text=True,
                timeout=10
            )
            
            assert "--url" in result.stdout
            assert "--resolution" in result.stdout
            assert "--format" in result.stdout
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pytest.skip("CLI not available for integration testing")

    def test_cli_download_audio_help(self):
        """Test CLI download audio help message"""
        try:
            result = subprocess.run(
                [sys.executable, "main.py", "download", "audio", "--help"],
                cwd=str(Path(__file__).parent.parent),
                capture_output=True,
                text=True,
                timeout=10
            )
            
            assert "--url" in result.stdout
            assert "--format" in result.stdout
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pytest.skip("CLI not available for integration testing")

    def test_cli_missing_required_args(self):
        """Test CLI with missing required arguments"""
        try:
            # Test download without URL
            result = subprocess.run(
                [sys.executable, "main.py", "download", "video"],
                cwd=str(Path(__file__).parent.parent),
                capture_output=True,
                text=True,
                timeout=10
            )
            
            assert result.returncode != 0
            assert "required" in result.stderr.lower() or "error" in result.stderr.lower()
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pytest.skip("CLI not available for integration testing")

    def test_cli_convert_missing_args(self):
        """Test CLI convert with missing arguments"""
        try:
            # Test convert without path
            result = subprocess.run(
                [sys.executable, "main.py", "convert", "--to", "mp3"],
                cwd=str(Path(__file__).parent.parent),
                capture_output=True,
                text=True,
                timeout=10
            )
            
            assert result.returncode != 0
            assert "required" in result.stderr.lower() or "error" in result.stderr.lower()
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pytest.skip("CLI not available for integration testing")

    @patch('app.tools.media_converter.resolve_file_paths')
    @patch('app.tools.media_converter.convert_files_functional')
    def test_end_to_end_convert_flow(self, mock_convert_files, mock_get_files):
        """Test end-to-end convert flow"""
        # Mock the file operations
        mock_get_files.return_value = [self.test_file]
        mock_convert_files.return_value = None
        
        # Simulate command line args
        with patch('sys.argv', ['main.py', 'convert', '--path', str(self.test_file), '--to', 'png']):
            main.main()
            
        # Verify the flow
        mock_get_files.assert_called_once()
        mock_convert_files.assert_called_once()

    @patch('app.tools.youtube_downloader.create_youtube_instance')
    @patch('app.tools.media_downloader.ensure_directory_exists')
    def test_end_to_end_download_flow_mock(self, mock_ensure_dir, mock_create_yt):
        """Test end-to-end download flow with mocks"""
        # Setup mocks
        mock_yt = MagicMock()
        mock_yt.title = "Test Video"
        mock_create_yt.return_value = mock_yt
        mock_ensure_dir.return_value = "/downloads/videos"
        
        mock_stream = MagicMock()
        mock_stream.download.return_value = "/downloads/videos/test.mp4"
        mock_yt.streams.get_highest_resolution.return_value = mock_stream
        
        # Simulate command line args
        with patch('sys.argv', ['main.py', 'download', 'video', '--url', 'https://youtube.com/watch?v=test']):
            try:
                main.main()
            except SystemExit:
                # Expected if conversion fails, but download logic should execute
                pass
            
        # Verify YouTube instance was created
        mock_create_yt.assert_called_once()

    def test_format_validation_integration(self):
        """Test format validation in integration"""
        try:
            result = subprocess.run(
                [sys.executable, "main.py", "convert", "--path", "test.jpg", "--to", "invalid_format"],
                cwd=str(Path(__file__).parent.parent),
                capture_output=True,
                text=True,
                timeout=10
            )
            
            # Should fail with invalid format
            assert result.returncode != 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pytest.skip("CLI not available for integration testing")

    @patch('main.convert')
    @patch('main.download')
    def test_command_routing(self, mock_download, mock_convert):
        """Test command routing logic"""
        # Test download routing
        mock_download_args = MagicMock()
        mock_download_args.command = "download"
        mock_download.return_value = {"success": True}
        
        with patch('main.command_manager', return_value=mock_download_args):
            main.main()
        mock_download.assert_called_once_with(mock_download_args)
        
        # Reset mocks for second test
        mock_download.reset_mock()
        mock_convert.reset_mock()
        
        # Test convert routing
        mock_convert_args = MagicMock()
        mock_convert_args.command = "convert"
        
        with patch('main.command_manager', return_value=mock_convert_args):
            main.main()
        mock_convert.assert_called_once_with(mock_convert_args)