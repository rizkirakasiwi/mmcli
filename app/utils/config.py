import os
import sys
from typing import Dict, Any, Optional
from pathlib import Path

try:
    import tomllib  # Python 3.11+
except ImportError:
    try:
        import tomli as tomllib  # Fallback for older Python versions
    except ImportError:
        tomllib = None

try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False


class ConfigurationError(Exception):
    """Configuration related errors."""
    pass


class Config:
    """Configuration manager for MMCLI."""
    
    _instance = None
    _config_data = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._config_data is None:
            self._config_data = self._load_config()
    
    def _find_config_file(self) -> Optional[Path]:
        """Find configuration file in project directory."""
        # Start from the current working directory and work up
        current_dir = Path.cwd()
        
        # Look for config files in current directory and parent directories
        search_paths = [current_dir]
        
        # Also check the script's directory
        if hasattr(sys, '_MEIPASS'):  # PyInstaller
            search_paths.append(Path(sys._MEIPASS))
        else:
            # Get the directory where the main module is located
            main_module_path = Path(__file__).parent.parent.parent
            search_paths.append(main_module_path)
        
        for search_dir in search_paths:
            # Check for TOML first, then YAML
            for config_name in ['config.toml', 'mmcli.toml', 'config.yaml', 'mmcli.yaml']:
                config_path = search_dir / config_name
                if config_path.exists():
                    return config_path
        
        return None
    
    def _load_toml_config(self, config_path: Path) -> Dict[str, Any]:
        """Load TOML configuration file."""
        if tomllib is None:
            raise ConfigurationError(
                "TOML support not available. Please install 'tomli' package: pip install tomli"
            )
        
        try:
            with open(config_path, 'rb') as f:
                return tomllib.load(f)
        except Exception as e:
            raise ConfigurationError(f"Failed to load TOML config from {config_path}: {e}")
    
    def _load_yaml_config(self, config_path: Path) -> Dict[str, Any]:
        """Load YAML configuration file."""
        if not YAML_AVAILABLE:
            raise ConfigurationError(
                "YAML support not available. Please install 'PyYAML' package: pip install PyYAML"
            )
        
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f) or {}
        except Exception as e:
            raise ConfigurationError(f"Failed to load YAML config from {config_path}: {e}")
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file or return defaults."""
        config_path = self._find_config_file()
        
        if config_path is None:
            return self._get_default_config()
        
        if config_path.suffix.lower() in ['.toml']:
            config_data = self._load_toml_config(config_path)
        elif config_path.suffix.lower() in ['.yaml', '.yml']:
            config_data = self._load_yaml_config(config_path)
        else:
            raise ConfigurationError(f"Unsupported config file format: {config_path.suffix}")
        
        # Merge with defaults to ensure all keys exist
        defaults = self._get_default_config()
        return self._merge_config(defaults, config_data)
    
    def _merge_config(self, defaults: Dict[str, Any], user_config: Dict[str, Any]) -> Dict[str, Any]:
        """Merge user configuration with defaults."""
        result = defaults.copy()
        
        for key, value in user_config.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._merge_config(result[key], value)
            else:
                result[key] = value
        
        return result
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration values."""
        return {
            "downloads": {
                "output_dir": "downloads",
                "video": {
                    "format": "mp4",
                    "resolution": "highest"
                },
                "audio": {
                    "format": "m4a"
                },
                "playlist": {
                    "max_workers": 3,
                    "create_subfolders": True,
                    "batch_convert": True
                }
            },
            "conversion": {
                "output_dir": "converter",
                "video": {
                    "preserve_quality": True,
                    "default_codec": "libx264"
                },
                "audio": {
                    "preserve_quality": True,
                    "default_codec": "aac",
                    "bitrate": "128k"
                }
            },
            "general": {
                "verbose": False,
                "progress_bar": True,
                "auto_cleanup": True,
                "max_retries": 3,
                "naming": {
                    "add_timestamp": True,
                    "sanitize_filenames": True,
                    "max_filename_length": 255
                }
            }
        }
    
    def get(self, key_path: str, default: Any = None) -> Any:
        """
        Get configuration value using dot notation.
        
        Examples:
            config.get('downloads.video.format')  # Returns 'mp4'
            config.get('downloads.playlist.max_workers')  # Returns 3
        """
        keys = key_path.split('.')
        current = self._config_data
        
        try:
            for key in keys:
                current = current[key]
            return current
        except (KeyError, TypeError):
            return default
    
    def get_downloads_config(self) -> Dict[str, Any]:
        """Get downloads configuration section."""
        return self._config_data.get("downloads", {})
    
    def get_conversion_config(self) -> Dict[str, Any]:
        """Get conversion configuration section."""
        return self._config_data.get("conversion", {})
    
    def get_general_config(self) -> Dict[str, Any]:
        """Get general configuration section."""
        return self._config_data.get("general", {})
    
    def get_video_defaults(self) -> Dict[str, Any]:
        """Get default video settings."""
        return self.get_downloads_config().get("video", {})
    
    def get_audio_defaults(self) -> Dict[str, Any]:
        """Get default audio settings."""
        return self.get_downloads_config().get("audio", {})
    
    def get_playlist_defaults(self) -> Dict[str, Any]:
        """Get default playlist settings."""
        return self.get_downloads_config().get("playlist", {})
    
    def reload(self) -> None:
        """Reload configuration from file."""
        self._config_data = self._load_config()


# Global configuration instance
config = Config()


# Convenience functions
def get_config_value(key_path: str, default: Any = None) -> Any:
    """Get configuration value using dot notation."""
    return config.get(key_path, default)


def get_video_format_default() -> str:
    """Get default video format from config."""
    return config.get('downloads.video.format', 'mp4')


def get_audio_format_default() -> str:
    """Get default audio format from config."""
    return config.get('downloads.audio.format', 'm4a')


def get_video_resolution_default() -> str:
    """Get default video resolution from config."""
    return config.get('downloads.video.resolution', 'highest')


def get_output_dir_default() -> str:
    """Get default output directory from config."""
    return config.get('downloads.output_dir', 'downloads')


def get_conversion_output_dir_default() -> str:
    """Get default conversion output directory from config."""
    return config.get('conversion.output_dir', 'converter')


def get_max_workers_default() -> int:
    """Get default max workers for parallel downloads."""
    return config.get('downloads.playlist.max_workers', 3)


def should_create_playlist_subfolders() -> bool:
    """Check if playlist subfolders should be created."""
    return config.get('downloads.playlist.create_subfolders', True)


def should_use_batch_convert() -> bool:
    """Check if batch conversion should be used for playlists."""
    return config.get('downloads.playlist.batch_convert', True)