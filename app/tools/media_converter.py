import ffmpeg
import os
import textwrap
import sys
from pathlib import Path
from glob import glob
from datetime import datetime
from typing import Optional, List, Dict, Any
from functools import partial, reduce
from concurrent.futures import ThreadPoolExecutor, as_completed
from ..utils.media_format import all_formats
from ..utils.config import get_max_workers_default


def resolve_file_paths(input_pattern: str) -> List[Path]:
    """Resolve input file pattern to actual file paths, supporting glob patterns."""
    if "*" in input_pattern:
        files = [Path(p) for p in glob(input_pattern)]
        if not files:
            files = [Path(p) for p in glob(f"**/{input_pattern}", recursive=True)]
    else:
        files = [Path(input_pattern)] if Path(input_pattern).exists() else []

    if not files:
        raise FileNotFoundError(f"No file(s) found matching: {input_pattern}")

    return files


def ensure_output_directory(output_dir: Optional[str]) -> Path:
    """Create output directory if needed and return Path object."""
    path = Path(output_dir) if output_dir else Path(os.getcwd()) / "convert"
    path.mkdir(parents=True, exist_ok=True)
    return path


def generate_output_filename(input_file: Path, output_format: str) -> str:
    """Generate unique output filename with timestamp."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    return f"{input_file.stem}_{timestamp}.{output_format}"


def create_output_path(input_file: Path, output_format: str, output_dir: Path) -> Path:
    """Create full output file path."""
    output_filename = generate_output_filename(input_file, output_format)
    return output_dir / output_filename


def find_ffmpeg_format(output_format: str) -> Optional[str]:
    """Find matching ffmpeg format from format alias."""
    format_matches = list(filter(lambda fmt: fmt["alias"] == output_format, all_formats))
    return format_matches[0]["format"] if format_matches else None


def create_conversion_config(input_file: Path, output_format: str, output_dir: Path) -> Dict[str, Any]:
    """Create conversion configuration object."""
    ffmpeg_format = find_ffmpeg_format(output_format)
    output_path = create_output_path(input_file, output_format, output_dir)
    
    return {
        "input_file": input_file,
        "output_path": output_path,
        "ffmpeg_format": ffmpeg_format,
        "output_format": output_format
    }


def execute_ffmpeg_conversion(config: Dict[str, Any]) -> bool:
    """Execute ffmpeg conversion with given configuration."""
    if not config["ffmpeg_format"]:
        print(f"Unsupported format: {config['output_format']}")
        return False

    try:
        ffmpeg.input(str(config["input_file"])).output(
            str(config["output_path"]), 
            format=config["ffmpeg_format"]
        ).run(quiet=True, overwrite_output=True)
        return True
    except Exception as e:
        print(f"Error converting {config['input_file']}: {e}")
        return False


def convert_single_file_functional(
    input_file: Path, 
    output_format: str, 
    output_dir: Path
) -> Dict[str, Any]:
    """Convert single file using functional approach with detailed result."""
    config = create_conversion_config(input_file, output_format, output_dir)
    success = execute_ffmpeg_conversion(config)
    
    return {
        "input_file": str(input_file),
        "output_file": str(config["output_path"]) if success else None,
        "success": success,
        "format": output_format
    }


def process_conversion_batch(
    input_files: List[Path], 
    output_format: str, 
    output_dir: Path,
    max_workers: int = 1
) -> List[Dict[str, Any]]:
    """Process batch conversion using parallel or sequential approach."""
    convert_func = partial(
        convert_single_file_functional,
        output_format=output_format,
        output_dir=output_dir
    )
    
    if len(input_files) == 1 or max_workers <= 1:
        # Sequential conversion for single files or when max_workers is 1
        print(f"Converting {len(input_files)} file(s) to {output_format}...")
        return list(map(convert_func, input_files))
    else:
        # Parallel conversion for multiple files
        print(f"Converting {len(input_files)} file(s) to {output_format} using {max_workers} workers...")
        results = []
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all conversion tasks
            future_to_file = {
                executor.submit(convert_func, input_file): input_file 
                for input_file in input_files
            }
            
            # Collect results as they complete
            for future in as_completed(future_to_file):
                input_file = future_to_file[future]
                try:
                    result = future.result()
                    results.append(result)
                    if result["success"]:
                        print(f"✓ Converted {input_file.name}")
                    else:
                        print(f"✗ Failed to convert {input_file.name}")
                except Exception as e:
                    print(f"✗ Error converting {input_file.name}: {e}")
                    results.append({
                        "input_file": str(input_file),
                        "output_file": None,
                        "success": False,
                        "format": output_format,
                        "error": str(e)
                    })
        
        # Sort results to match input file order
        file_order = {str(f): i for i, f in enumerate(input_files)}
        results.sort(key=lambda r: file_order.get(r["input_file"], 999))
        
        return results


def calculate_conversion_stats(results: List[Dict[str, Any]]) -> Dict[str, int]:
    """Calculate conversion statistics from results."""
    return reduce(
        lambda acc, result: {
            "total": acc["total"] + 1,
            "success": acc["success"] + (1 if result["success"] else 0),
            "failed": acc["failed"] + (0 if result["success"] else 1)
        },
        results,
        {"total": 0, "success": 0, "failed": 0}
    )


def format_conversion_summary(stats: Dict[str, int], output_format: str, output_dir: str) -> str:
    """Format conversion summary message."""
    return textwrap.dedent(f"""
        Summary:
        Successfully converted: {stats['success']}
        Failed to convert: {stats['failed']}
        Format: {output_format}
        Output directory: {output_dir}
    """).strip()


def print_conversion_results(results: List[Dict[str, Any]], output_format: str, output_dir: str) -> None:
    """Print detailed conversion results and summary."""
    stats = calculate_conversion_stats(results)
    
    print("Conversion complete.")
    print(format_conversion_summary(stats, output_format, output_dir))
    
    if stats["failed"] > 0:
        print("\nFailed conversions:")
        failed_files = [r["input_file"] for r in results if not r["success"]]
        for file_path in failed_files:
            print(f"  - {file_path}")


def convert_files_functional(
    input_files: List[Path], 
    output_format: str, 
    output_dir: Optional[str] = None,
    max_workers: int = 1
) -> List[Dict[str, Any]]:
    """Convert batch of files using parallel or sequential approach."""
    resolved_output_dir = ensure_output_directory(output_dir)
    
    results = process_conversion_batch(input_files, output_format, resolved_output_dir, max_workers)
    print_conversion_results(results, output_format, str(resolved_output_dir))
    
    return results


def validate_conversion_args(args) -> Dict[str, Any]:
    """Validate and extract conversion arguments."""
    if not hasattr(args, 'path') or not args.path:
        raise ValueError("Input path is required")
    if not hasattr(args, 'to') or not args.to:
        raise ValueError("Output format is required")
    
    # Get max_workers from CLI args or config default
    max_workers = getattr(args, 'max_workers', None)
    if max_workers is None:
        max_workers = get_max_workers_default()
    
    return {
        "input_pattern": args.path,
        "output_format": args.to,
        "output_dir": getattr(args, 'output_dir', None),
        "max_workers": max_workers
    }


def convert(args) -> List[Dict[str, Any]]:
    """Main convert function with functional programming approach."""
    try:
        validated_args = validate_conversion_args(args)
        input_files = resolve_file_paths(validated_args["input_pattern"])
        
        return convert_files_functional(
            input_files,
            validated_args["output_format"],
            validated_args["output_dir"],
            validated_args["max_workers"]
        )
        
    except Exception as e:
        print(f"Error converting file: {e}")
        sys.exit(1)
