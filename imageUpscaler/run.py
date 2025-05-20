import argparse
import json
from pathlib import Path
from imageUpscaler.banner import display_banner, about
from imageUpscaler.main import main
from imageUpscaler.image_analysis import get_image_analysis
from imageUpscaler.config import load_configuration
import logging
from datetime import datetime
from imageUpscaler import __version__, __author__, __email__

def setup_logging():
    """Setup logging configuration."""
    log_dir = Path('logs')
    log_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_file = log_dir / f'imageUpscaler_{timestamp}.log'
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )

def analyze_image(args):
    """Analyze an image and save the results."""
    try:
        from PIL import Image
        img = Image.open(args.image)
        analysis = get_image_analysis(img)
        
        if analysis:
            output_file = args.output or f"{Path(args.image).stem}_analysis.json"
            with open(output_file, 'w') as f:
                json.dump(analysis, f, indent=4)
            print(f"Analysis saved to {output_file}")
        else:
            print("Analysis failed")
    except Exception as e:
        logging.error(f"Error during analysis: {e}")
        print(f"Error: {e}")

def show_version():
    """Show version information and GPU status."""
    from imageUpscaler.image_processing import get_gpu_memory_info
    from imageUpscaler.version import __version__, __author__, __email__
    
    print(f"ImageUpscaler version {__version__}")
    print(f"Author: {__author__}")
    print(f"Email: {__email__}")
    
    # Show GPU status
    gpu_info = get_gpu_memory_info()
    if gpu_info:
        print("\nGPU Information:")
        print(f"Total Memory: {gpu_info['total'] / 1024**2:.2f}MB")
        print(f"Allocated Memory: {gpu_info['allocated'] / 1024**2:.2f}MB")
        print(f"Cached Memory: {gpu_info['cached'] / 1024**2:.2f}MB")
    else:
        print("\nNo GPU detected. Running on CPU.")

def main_cli():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description='ImageUpscaler - Advanced Image Processing Tool')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Process command
    process_parser = subparsers.add_parser('process', help='Process images')
    process_parser.add_argument('--config', type=str, help='Path to configuration file')
    process_parser.add_argument('--input', type=str, help='Input directory')
    process_parser.add_argument('--output', type=str, help='Output directory')

    # Analyze command
    analyze_parser = subparsers.add_parser('analyze', help='Analyze an image')
    analyze_parser.add_argument('image', type=str, help='Path to image file')
    analyze_parser.add_argument('--output', type=str, help='Output JSON file for analysis results')

    # Version command
    subparsers.add_parser('version', help='Show version information')

    args = parser.parse_args()

    if args.command == 'process':
        if args.config:
            config = load_configuration(args.config)
        else:
            config = load_configuration('config.json')
        
        if args.input:
            config['input_directory'] = args.input
        if args.output:
            config['output_directory'] = args.output
        
        main()
    elif args.command == 'analyze':
        analyze_image(args)
    elif args.command == 'version':
        show_version()
    else:
        display_banner()
        about()
        main()

if __name__ == "__main__":
    setup_logging()
    main_cli()
