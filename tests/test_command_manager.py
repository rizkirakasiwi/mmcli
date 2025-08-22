import pytest
import argparse
import sys
from unittest.mock import patch
from app.utils.command_manager import command_manager


class TestCommandManager:
    def test_download_video_command(self):
        """Test download video command parsing"""
        test_args = ['download', 'video', '--url', 'https://youtube.com/watch?v=test']
        with patch.object(sys, 'argv', ['mmcli'] + test_args):
            args = command_manager()
            assert args.command == 'download'
            assert args.type == 'video'
            assert args.url == 'https://youtube.com/watch?v=test'
            assert args.resolution is None
            assert args.format is None

    def test_download_video_with_resolution(self):
        """Test download video with resolution"""
        test_args = ['download', 'video', '--url', 'https://youtube.com/watch?v=test', '--resolution', '720p']
        with patch.object(sys, 'argv', ['mmcli'] + test_args):
            args = command_manager()
            assert args.command == 'download'
            assert args.type == 'video'
            assert args.url == 'https://youtube.com/watch?v=test'
            assert args.resolution == '720p'

    def test_download_video_with_format(self):
        """Test download video with format"""
        test_args = ['download', 'video', '--url', 'https://youtube.com/watch?v=test', '--format', 'mkv']
        with patch.object(sys, 'argv', ['mmcli'] + test_args):
            args = command_manager()
            assert args.command == 'download'
            assert args.type == 'video'
            assert args.url == 'https://youtube.com/watch?v=test'
            assert args.format == 'mkv'

    def test_download_audio_command(self):
        """Test download audio command parsing"""
        test_args = ['download', 'audio', '--url', 'https://youtube.com/watch?v=test']
        with patch.object(sys, 'argv', ['mmcli'] + test_args):
            args = command_manager()
            assert args.command == 'download'
            assert args.type == 'audio'
            assert args.url == 'https://youtube.com/watch?v=test'
            assert args.format is None

    def test_download_audio_with_format(self):
        """Test download audio with format"""
        test_args = ['download', 'audio', '--url', 'https://youtube.com/watch?v=test', '--format', 'wav']
        with patch.object(sys, 'argv', ['mmcli'] + test_args):
            args = command_manager()
            assert args.command == 'download'
            assert args.type == 'audio'
            assert args.url == 'https://youtube.com/watch?v=test'
            assert args.format == 'wav'

    def test_convert_command(self):
        """Test convert command parsing"""
        test_args = ['convert', '--path', 'test.mp4', '--to', 'mp3']
        with patch.object(sys, 'argv', ['mmcli'] + test_args):
            args = command_manager()
            assert args.command == 'convert'
            assert args.path == 'test.mp4'
            assert args.to == 'mp3'
            assert args.output_dir is None

    def test_convert_with_output_dir(self):
        """Test convert command with output directory"""
        test_args = ['convert', '--path', 'test.mp4', '--to', 'mp3', '--output_dir', 'converted/']
        with patch.object(sys, 'argv', ['mmcli'] + test_args):
            args = command_manager()
            assert args.command == 'convert'
            assert args.path == 'test.mp4'
            assert args.to == 'mp3'
            assert args.output_dir == 'converted/'

    def test_convert_with_glob_pattern(self):
        """Test convert command with glob pattern"""
        test_args = ['convert', '--path', 'videos/*.mp4', '--to', 'mp3']
        with patch.object(sys, 'argv', ['mmcli'] + test_args):
            args = command_manager()
            assert args.command == 'convert'
            assert args.path == 'videos/*.mp4'
            assert args.to == 'mp3'

    def test_missing_required_args(self):
        """Test error handling for missing required arguments"""
        with patch.object(sys, 'argv', ['mmcli']):
            with pytest.raises(SystemExit):
                command_manager()

    def test_download_missing_url(self):
        """Test error handling for download without URL"""
        test_args = ['download', 'video']
        with patch.object(sys, 'argv', ['mmcli'] + test_args):
            with pytest.raises(SystemExit):
                command_manager()

    def test_convert_missing_path(self):
        """Test error handling for convert without path"""
        test_args = ['convert', '--to', 'mp3']
        with patch.object(sys, 'argv', ['mmcli'] + test_args):
            with pytest.raises(SystemExit):
                command_manager()

    def test_convert_missing_to_format(self):
        """Test error handling for convert without target format"""
        test_args = ['convert', '--path', 'test.mp4']
        with patch.object(sys, 'argv', ['mmcli'] + test_args):
            with pytest.raises(SystemExit):
                command_manager()

    def test_short_options(self):
        """Test short option flags"""
        test_args = ['download', 'video', '-u', 'https://youtube.com/watch?v=test', '-r', '1080p', '-f', 'mp4']
        with patch.object(sys, 'argv', ['mmcli'] + test_args):
            args = command_manager()
            assert args.url == 'https://youtube.com/watch?v=test'
            assert args.resolution == '1080p'
            assert args.format == 'mp4'

        test_args = ['convert', '-p', 'test.mp4', '-t', 'mp3', '-o', 'output/']
        with patch.object(sys, 'argv', ['mmcli'] + test_args):
            args = command_manager()
            assert args.path == 'test.mp4'
            assert args.to == 'mp3'
            assert args.output_dir == 'output/'

    def test_version_command(self):
        """Test --version command"""
        test_args = ['--version']
        with patch.object(sys, 'argv', ['mmcli'] + test_args):
            with pytest.raises(SystemExit) as excinfo:
                command_manager()
            assert excinfo.value.code == 0

    def test_version_command_short_flag(self):
        """Test -v command"""
        test_args = ['-v']
        with patch.object(sys, 'argv', ['mmcli'] + test_args):
            with pytest.raises(SystemExit) as excinfo:
                command_manager()
            assert excinfo.value.code == 0