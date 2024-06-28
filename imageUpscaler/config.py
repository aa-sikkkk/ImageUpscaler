import json
import logging
import os

default_config = {
        "input_directory": ".",
        "output_directory": ".",
        "upscale_factor": 2.0,
        "contrast_factor": 1.0,
        "color_factor": 1.0,
        "watermark_text": "Sample Watermark",
        "watermark_position": "bottom_right",
        "format_conversion": "PNG",
        "crop_settings": (0, 0, 100, 100),
        "resize_settings": (800, 600),
        "rotation_angle": 0,
        "flip_mode": "horizontal",
        "noise_reduction": False,
        "histogram_equalization": False,
        "sepia_filter": False,
        "vignette_filter": False,
        "face_detection": False,
        "background_removal": False,
        "compression_quality": 85,
        "preserve_metadata": True
    }
def load_configuration(config_path):
    try:
        if os.path.exists(config_path):
            with open(config_path, 'r') as config_file:
                config = json.load(config_file)
        else:
            logging.warning(f"Configuration file {config_path} not found. Using default configuration.")
            config = default_config
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logging.error(f"Error loading configuration: {e}")
        config = default_config
    return config
