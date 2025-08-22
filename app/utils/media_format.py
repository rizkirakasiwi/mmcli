video_formats = [
    {"alias": "mp4", "format": "mp4", "desc": "MPEG-4 Part 14"},
    {"alias": "mkv", "format": "matroska", "desc": "Matroska Multimedia Container"},
    {"alias": "avi", "format": "avi", "desc": "Audio Video Interleaved"},
    {"alias": "mov", "format": "mov", "desc": "QuickTime Movie"},
    {"alias": "flv", "format": "flv", "desc": "Flash Video"},
    {"alias": "webm", "format": "webm", "desc": "WebM Video"},
    {"alias": "mpeg", "format": "mpeg", "desc": "MPEG Program Stream"},
    {"alias": "mpg", "format": "mpeg", "desc": "MPEG Program Stream"},
    {"alias": "ts", "format": "mpegts", "desc": "MPEG Transport Stream"},
    {"alias": "m2ts", "format": "mpegts", "desc": "MPEG-2 Transport Stream"},
    {"alias": "ogv", "format": "ogg", "desc": "Ogg Video"},
    {"alias": "3gp", "format": "3gp", "desc": "3GPP Multimedia Container"},
    {"alias": "3g2", "format": "3g2", "desc": "3GPP2 Multimedia Container"},
    {"alias": "vob", "format": "vob", "desc": "DVD Video Object"},
    {"alias": "f4v", "format": "f4v", "desc": "Flash Video F4V"},
    {"alias": "wmv", "format": "asf", "desc": "Windows Media Video"},
    {"alias": "rm", "format": "rm", "desc": "RealMedia"},
    {"alias": "rmvb", "format": "rm", "desc": "RealMedia Variable Bitrate"},
]

audio_formats = [
    {"alias": "mp3", "format": "mp3", "desc": "MPEG Audio Layer III"},
    {"alias": "wav", "format": "wav", "desc": "Waveform Audio File Format"},
    {"alias": "flac", "format": "flac", "desc": "Free Lossless Audio Codec"},
    {"alias": "aac", "format": "aac", "desc": "Advanced Audio Coding"},
    {"alias": "m4a", "format": "ipod", "desc": "MPEG-4 Audio"},
    {"alias": "ogg", "format": "ogg", "desc": "Ogg Vorbis/Opus"},
    {"alias": "oga", "format": "ogg", "desc": "Ogg Audio"},
    {"alias": "opus", "format": "ogg", "desc": "Opus in Ogg"},
    {"alias": "wma", "format": "asf", "desc": "Windows Media Audio"},
    {"alias": "alac", "format": "ipod", "desc": "Apple Lossless Audio Codec"},
    {"alias": "amr", "format": "amr", "desc": "Adaptive Multi-Rate Audio"},
    {"alias": "ac3", "format": "ac3", "desc": "Dolby Digital AC-3"},
    {"alias": "dts", "format": "dts", "desc": "Digital Theater Systems"},
    {"alias": "eac3", "format": "eac3", "desc": "Enhanced AC-3"},
]

image_formats = [
    {"alias": "jpg", "format": "mjpeg", "desc": "JPEG Image"},
    {"alias": "jpeg", "format": "mjpeg", "desc": "JPEG Image"},
    {"alias": "png", "format": "png", "desc": "Portable Network Graphics"},
    {"alias": "webp", "format": "webp", "desc": "WebP Image"},
    {"alias": "gif", "format": "gif", "desc": "Graphics Interchange Format"},
    {"alias": "bmp", "format": "bmp", "desc": "Bitmap Image"},
    {"alias": "tif", "format": "tiff", "desc": "Tagged Image File Format"},
    {"alias": "tiff", "format": "tiff", "desc": "Tagged Image File Format"},
    {"alias": "ico", "format": "ico", "desc": "Windows Icon"},
    {"alias": "svg", "format": "svg", "desc": "Scalable Vector Graphics"},
    {"alias": "heif", "format": "heif", "desc": "High Efficiency Image Format"},
    {"alias": "heic", "format": "hevc", "desc": "High Efficiency Image Coding"},
    {"alias": "jp2", "format": "jpeg2000", "desc": "JPEG 2000"},
    {"alias": "j2k", "format": "jpeg2000", "desc": "JPEG 2000"},
    {"alias": "jxl", "format": "jpegxl", "desc": "JPEG XL"},
]

subtitle_formats = [
    {"alias": "srt", "format": "srt", "desc": "SubRip Subtitle"},
    {"alias": "ass", "format": "ass", "desc": "Advanced SubStation Alpha"},
    {"alias": "ssa", "format": "ass", "desc": "SubStation Alpha"},
    {"alias": "vtt", "format": "webvtt", "desc": "WebVTT Subtitle"},
    {"alias": "sub", "format": "microdvd", "desc": "MicroDVD Subtitle"},
    {"alias": "idx", "format": "microdvd", "desc": "MicroDVD Index"},
    {"alias": "mks", "format": "matroska", "desc": "Matroska Subtitles"},
]

all_formats = video_formats + audio_formats + image_formats + subtitle_formats


def get_format(format: str, formats: list = all_formats) -> list:
    return list(
        filter(lambda f: f["alias"] == format or f["format"] == format, formats)
    )
