import pytest
import tempfile
import shutil
from pathlib import Path
from unittest.mock import patch, MagicMock, call
from app.tools.media_converter import (
    resolve_file_paths,
    ensure_output_directory,
    create_output_path,
    find_ffmpeg_format,
    convert_single_file_functional,
    convert_files_functional,
    convert,
)


class TestMediaConverter:
    def setup_method(self):
        """Set up test fixtures"""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.test_file = self.temp_dir / "test.mp4"
        self.test_file.touch()

    def teardown_method(self):
        """Clean up test fixtures"""
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)

    def test_get_files_single_file(self):
        """Test getting single file"""
        files = resolve_file_paths(str(self.test_file))
        assert len(files) == 1
        assert files[0] == self.test_file

    def test_get_files_nonexistent_file(self):
        """Test error handling for nonexistent file"""
        with pytest.raises(FileNotFoundError):
            resolve_file_paths("nonexistent.mp4")

    @patch('app.tools.media_converter.glob')
    def test_get_files_glob_pattern(self, mock_glob):
        """Test getting files with glob pattern"""
        mock_glob.return_value = [str(self.test_file)]
        files = resolve_file_paths("*.mp4")
        assert len(files) == 1
        assert str(files[0]) == str(self.test_file)

    @patch('glob.glob')
    def test_get_files_glob_pattern_no_matches(self, mock_glob):
        """Test glob pattern with no matches"""
        mock_glob.return_value = []
        with pytest.raises(FileNotFoundError):
            resolve_file_paths("*.nonexistent")

    def test_resolve_output_dir_default(self):
        """Test resolve output directory with default"""
        output_dir = ensure_output_directory(None)
        assert output_dir.exists()
        assert "convert" in str(output_dir)

    def test_resolve_output_dir_custom(self):
        """Test resolve output directory with custom path"""
        custom_dir = self.temp_dir / "custom_output"
        output_dir = ensure_output_directory(str(custom_dir))
        assert output_dir == custom_dir
        assert output_dir.exists()

    def test_build_output_path(self):
        """Test building output path with timestamp"""
        input_file = Path("test.mp4")
        output_format = "mp3"
        output_dir = self.temp_dir
        
        output_path = create_output_path(input_file, output_format, output_dir)
        
        assert output_path.parent == output_dir
        assert output_path.suffix == ".mp3"
        assert "test_" in output_path.name
        assert len(output_path.stem.split('_')) >= 3  # test_YYYYMMDD_HHMMSS...

    def test_get_ffmpeg_format_valid(self):
        """Test getting valid ffmpeg format"""
        result = find_ffmpeg_format("mp3")
        assert result == "mp3"

    def test_get_ffmpeg_format_invalid(self):
        """Test getting invalid ffmpeg format"""
        result = find_ffmpeg_format("invalid_format")
        assert result is None

    @patch('ffmpeg.input')
    @pytest.mark.asyncio
    async def test_convert_single_file_success(self, mock_input):
        """Test successful single file conversion"""
        mock_stream = MagicMock()
        mock_output_stream = MagicMock()
        mock_input.return_value = mock_stream
        mock_stream.output.return_value = mock_output_stream
        mock_output_stream.run = MagicMock()

        result = await convert_single_file_functional(self.test_file, "mp3", self.temp_dir)
        
        assert result["success"] is True
        mock_input.assert_called_once()
        mock_stream.output.assert_called_once()
        mock_output_stream.run.assert_called_once()

    @patch('ffmpeg.input')
    @pytest.mark.asyncio
    async def test_convert_single_file_invalid_format(self, mock_input):
        """Test single file conversion with invalid format"""
        result = await convert_single_file_functional(self.test_file, "invalid_format", self.temp_dir)
        assert result["success"] is False
        mock_input.assert_not_called()

    @patch('ffmpeg.input')
    @pytest.mark.asyncio
    async def test_convert_single_file_ffmpeg_error(self, mock_input):
        """Test single file conversion with ffmpeg error"""
        mock_stream = MagicMock()
        mock_output_stream = MagicMock()
        mock_input.return_value = mock_stream
        mock_stream.output.return_value = mock_output_stream
        mock_output_stream.run.side_effect = Exception("FFmpeg error")

        result = await convert_single_file_functional(self.test_file, "mp3", self.temp_dir)
        assert result["success"] is False

    @patch('app.tools.media_converter.convert_single_file_functional')
    @patch('app.tools.media_converter.ensure_output_directory')
    @pytest.mark.asyncio
    async def test_convert_files(self, mock_resolve_dir, mock_convert_single):
        """Test batch file conversion"""
        mock_resolve_dir.return_value = self.temp_dir
        from unittest.mock import AsyncMock
        mock_convert_single.side_effect = AsyncMock(return_value={"success": True, "input_file": str(self.test_file), "output_file": "output.mp3", "format": "mp3"})
        
        files = [self.test_file]
        result = await convert_files_functional(files, "mp3", str(self.temp_dir))
        
        mock_resolve_dir.assert_called_once()
        mock_convert_single.assert_called_once()
        assert len(result) == 1
        assert result[0]["success"] is True

    @patch('app.tools.media_converter.resolve_file_paths')
    @patch('app.tools.media_converter.convert_files_functional')
    @pytest.mark.asyncio
    async def test_convert_main_function_success(self, mock_convert_files, mock_get_files):
        """Test main convert function success"""
        mock_args = MagicMock()
        mock_args.path = "*.mp4"
        mock_args.to = "mp3"
        mock_args.output_dir = None
        
        mock_get_files.return_value = [self.test_file]
        from unittest.mock import AsyncMock
        mock_convert_files.side_effect = AsyncMock(return_value=[{"success": True}])
        
        await convert(mock_args)
        
        mock_get_files.assert_called_once_with("*.mp4")
        # Check that convert_files was called with the expected arguments (including max_workers)
        assert mock_convert_files.called
        call_args = mock_convert_files.call_args
        assert call_args[0][:3] == ([self.test_file], "mp3", None)  # Check first 3 args, ignore max_workers

    @patch('app.tools.media_converter.resolve_file_paths')
    @pytest.mark.asyncio
    async def test_convert_main_function_error(self, mock_get_files):
        """Test main convert function error handling"""
        mock_args = MagicMock()
        mock_args.path = "nonexistent.mp4"
        
        mock_get_files.side_effect = Exception("File not found")
        
        with pytest.raises(SystemExit):
            await convert(mock_args)

    @patch('builtins.print')
    def test_print_conversion_summary(self, mock_print):
        """Test conversion summary printing"""
        from app.tools.media_converter import print_conversion_results
        
        results = [{"success": True}, {"success": True}, {"success": False, "input_file": "test.mp4"}]
        print_conversion_results(results, "mp3", str(self.temp_dir))
        
        # Check that print was called multiple times
        assert mock_print.call_count >= 3
        
        # Check some expected content in the calls
        call_args = [call[0][0] for call in mock_print.call_args_list]
        assert any("Conversion complete" in arg for arg in call_args)
        assert any("Successfully converted: 2" in arg for arg in call_args)
        assert any("Failed to convert: 1" in arg for arg in call_args)