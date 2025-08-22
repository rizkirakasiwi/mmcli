import ffmpeg
import textwrap
import sys
from pathlib import Path
from glob import glob
from datetime import datetime
from typing import Optional, List
from functools import partial
from ..utils.media_format import all_formats

def get_files(input_file: str) -> List[Path]:
    """Resolve input file(s), supporting glob patterns."""
    if "*" in input_file:
        files = [Path(p) for p in glob(input_file)]
        if not files:
            files = [Path(p) for p in glob(f"**/{input_file}", recursive=True)]
    else:
        files = [Path(input_file)] if Path(input_file).exists() else []

    if not files:
        raise FileNotFoundError(f"No file(s) found matching: {input_file}")

    return files

def resolve_output_dir(output_dir: Optional[str]) -> Path:
    """Ensure output directory exists and return as Path."""
    path = (
        Path(output_dir).resolve()
        if output_dir
        else Path(__file__).resolve().parent / "converter"
    )
    path.mkdir(parents=True, exist_ok=True)
    return path

def build_output_path(input_file: Path, output_format: str, output_dir: Path) -> Path:
    """Generate output file path with timestamp."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    output_file = f"{input_file.stem}_{timestamp}.{output_format}"
    return output_dir / output_file

def get_ffmpeg_format(output_format: str) -> Optional[str]:
    """Get ffmpeg format from alias."""
    ffmpeg_format = list(filter(lambda item: item["alias"] == output_format, all_formats))
    return ffmpeg_format[0]["format"] if ffmpeg_format else None

def convert_single_file(input_file: Path, output_format: str, output_dir: Path) -> bool:
    """Convert a single file. Returns True if successful, False otherwise."""
    try:
        ffmpeg_format = get_ffmpeg_format(output_format)
        if not ffmpeg_format:
            print(f"Unsupported format: {output_format}")
            return False

        output_path = build_output_path(input_file, output_format, output_dir)
        ffmpeg.input(str(input_file)).output(str(output_path), format=ffmpeg_format).run(quiet=True, overwrite_output=True)
        
        return True
    except:
        print(f"Error converting {input_file}")
        return False

def print_conversion_summary(results: List[bool], output_format: str, output_dir: Path) -> None:
    """Print conversion summary."""
    success_count = sum(results)
    failed_count = len(results) - success_count
    
    summary = textwrap.dedent("""
                              Summary:
                              Successfully converted: {success_count}
                              Failed to convert: {failed_count}
                              """)
    
    print(f"Conversion complete.")
    print(summary.format(success_count=success_count, failed_count=failed_count))
    print(f"Output files can be found in: {output_dir}")

def convert_files(input_files: List[Path], output_format: str, output_dir: Optional[str] = None) -> None:
    """Convert a batch of files and log summary."""
    print(f"Converting to {output_format}...")
    resolved_output_dir = resolve_output_dir(output_dir)
    
    # Create a partial function with fixed output_format and output_dir
    convert_file_partial = partial(convert_single_file, output_format=output_format, output_dir=resolved_output_dir)
    
    # Convert all files
    results = list(map(convert_file_partial, input_files))
    
    # Print summary
    print_conversion_summary(results, output_format, resolved_output_dir)

def convert(args) -> None:
    """MAIN convert dispatcher function."""
    try:
        files = get_files(args.path)
        convert_files(files, args.to, args.output_dir)
    except Exception as e:
        print(f"Error converting file: {e}")
        sys.exit(1)
