import pytest
from app.utils.media_format import (
    video_formats,
    audio_formats,
    image_formats,
    subtitle_formats,
    all_formats,
    get_format,
)


class TestMediaFormat:
    def test_video_formats_structure(self):
        """Test video formats structure"""
        assert isinstance(video_formats, list)
        assert len(video_formats) > 0
        
        for format_info in video_formats:
            assert isinstance(format_info, dict)
            assert "alias" in format_info
            assert "format" in format_info
            assert "desc" in format_info
            assert isinstance(format_info["alias"], str)
            assert isinstance(format_info["format"], str)
            assert isinstance(format_info["desc"], str)

    def test_audio_formats_structure(self):
        """Test audio formats structure"""
        assert isinstance(audio_formats, list)
        assert len(audio_formats) > 0
        
        for format_info in audio_formats:
            assert isinstance(format_info, dict)
            assert "alias" in format_info
            assert "format" in format_info
            assert "desc" in format_info

    def test_image_formats_structure(self):
        """Test image formats structure"""
        assert isinstance(image_formats, list)
        assert len(image_formats) > 0
        
        for format_info in image_formats:
            assert isinstance(format_info, dict)
            assert "alias" in format_info
            assert "format" in format_info
            assert "desc" in format_info

    def test_subtitle_formats_structure(self):
        """Test subtitle formats structure"""
        assert isinstance(subtitle_formats, list)
        assert len(subtitle_formats) > 0
        
        for format_info in subtitle_formats:
            assert isinstance(format_info, dict)
            assert "alias" in format_info
            assert "format" in format_info
            assert "desc" in format_info

    def test_all_formats_combination(self):
        """Test all_formats is combination of all format lists"""
        expected_length = (
            len(video_formats) +
            len(audio_formats) +
            len(image_formats) +
            len(subtitle_formats)
        )
        assert len(all_formats) == expected_length

    def test_common_video_formats_exist(self):
        """Test common video formats exist"""
        video_aliases = [f["alias"] for f in video_formats]
        
        assert "mp4" in video_aliases
        assert "mkv" in video_aliases
        assert "avi" in video_aliases
        assert "mov" in video_aliases
        assert "webm" in video_aliases

    def test_common_audio_formats_exist(self):
        """Test common audio formats exist"""
        audio_aliases = [f["alias"] for f in audio_formats]
        
        assert "mp3" in audio_aliases
        assert "wav" in audio_aliases
        assert "flac" in audio_aliases
        assert "aac" in audio_aliases
        assert "ogg" in audio_aliases

    def test_common_image_formats_exist(self):
        """Test common image formats exist"""
        image_aliases = [f["alias"] for f in image_formats]
        
        assert "jpg" in image_aliases
        assert "jpeg" in image_aliases
        assert "png" in image_aliases
        assert "gif" in image_aliases
        assert "webp" in image_aliases
        assert "bmp" in image_aliases

    def test_common_subtitle_formats_exist(self):
        """Test common subtitle formats exist"""
        subtitle_aliases = [f["alias"] for f in subtitle_formats]
        
        assert "srt" in subtitle_aliases
        assert "ass" in subtitle_aliases
        assert "vtt" in subtitle_aliases

    def test_get_format_by_alias(self):
        """Test getting format by alias"""
        result = get_format("mp4")
        assert len(result) == 1
        assert result[0]["alias"] == "mp4"
        assert result[0]["format"] == "mp4"

    def test_get_format_by_format_name(self):
        """Test getting format by format name"""
        result = get_format("matroska")
        assert len(result) >= 1
        # Should find mkv format
        mkv_formats = [f for f in result if f["alias"] == "mkv"]
        assert len(mkv_formats) == 1

    def test_get_format_nonexistent(self):
        """Test getting nonexistent format"""
        result = get_format("nonexistent")
        assert result == []

    def test_get_format_case_sensitive(self):
        """Test format search is case sensitive"""
        result_lower = get_format("mp4")
        result_upper = get_format("MP4")
        
        assert len(result_lower) == 1
        assert len(result_upper) == 0

    def test_get_format_with_specific_format_list(self):
        """Test getting format from specific format list"""
        result = get_format("mp3", audio_formats)
        assert len(result) == 1
        assert result[0]["alias"] == "mp3"
        
        # mp3 should not be found in video formats
        result_video = get_format("mp3", video_formats)
        assert len(result_video) == 0

    def test_get_format_multiple_matches(self):
        """Test formats that might have multiple matches"""
        # Test jpeg vs jpg (both should exist for images)
        jpeg_result = get_format("jpeg")
        jpg_result = get_format("jpg")
        
        assert len(jpeg_result) == 1
        assert len(jpg_result) == 1
        assert jpeg_result[0]["alias"] == "jpeg"
        assert jpg_result[0]["alias"] == "jpg"

    def test_format_aliases_unique_per_category(self):
        """Test that aliases are unique within each category"""
        video_aliases = [f["alias"] for f in video_formats]
        audio_aliases = [f["alias"] for f in audio_formats]
        image_aliases = [f["alias"] for f in image_formats]
        subtitle_aliases = [f["alias"] for f in subtitle_formats]
        
        # Check for duplicates within each category
        assert len(video_aliases) == len(set(video_aliases))
        assert len(audio_aliases) == len(set(audio_aliases))
        assert len(image_aliases) == len(set(image_aliases))
        assert len(subtitle_aliases) == len(set(subtitle_aliases))

    def test_format_descriptions_not_empty(self):
        """Test that all format descriptions are not empty"""
        for format_info in all_formats:
            assert format_info["desc"].strip() != ""
            assert len(format_info["desc"]) > 3  # Reasonable description length

    def test_mp4_video_format_details(self):
        """Test specific MP4 format details"""
        mp4_formats = get_format("mp4")
        assert len(mp4_formats) == 1
        
        mp4 = mp4_formats[0]
        assert mp4["alias"] == "mp4"
        assert mp4["format"] == "mp4"
        assert "MPEG" in mp4["desc"]

    def test_mp3_audio_format_details(self):
        """Test specific MP3 format details"""
        mp3_formats = get_format("mp3")
        assert len(mp3_formats) == 1
        
        mp3 = mp3_formats[0]
        assert mp3["alias"] == "mp3"
        assert mp3["format"] == "mp3"
        assert "MPEG" in mp3["desc"]

    def test_png_image_format_details(self):
        """Test specific PNG format details"""
        png_formats = get_format("png")
        assert len(png_formats) == 1
        
        png = png_formats[0]
        assert png["alias"] == "png"
        assert png["format"] == "png"
        assert "PNG" in png["desc"] or "Network Graphics" in png["desc"]