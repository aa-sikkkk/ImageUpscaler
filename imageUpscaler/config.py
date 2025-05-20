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
    "noise_reduction": {
        "enabled": False,
        "method": "nlm",  # nlm, wavelet, or bilateral
        "strength": 1.0
    },
    "histogram_equalization": False,
    "sepia_filter": False,
    "vignette_filter": False,
    "face_detection": False,
    "background_removal": False,
    "compression_quality": 85,
    "preserve_metadata": True,
    "advanced_features": {
        "ai_enhancement": False,
        "hdr_processing": False,
        "smart_sharpen": {
            "enabled": False,
            "amount": 1.0,
            "radius": 1.0,
            "threshold": 0
        },
        "auto_color_correction": False,
        "detail_enhancement": {
            "enabled": False,
            "strength": 1.0
        }
    },
    "gpu_settings": {
        "enabled": True,
        "batch_size": 4,
        "memory_limit": 0.8,  # Maximum GPU memory usage (0.0 to 1.0)
        "optimization_level": "high",  # low, medium, high
        "mixed_precision": True,  # Use mixed precision for faster processing
        "cudnn_benchmark": True,  # Enable cuDNN benchmarking
        "clear_cache_after_batch": True  # Clear GPU cache after each batch
    },
    "batch_processing": {
        "enabled": True,
        "max_workers": 4,
        "chunk_size": 10
    },
    "output_settings": {
        "preserve_original": True,
        "create_thumbnails": False,
        "thumbnail_size": (200, 200),
        "naming_convention": "{original_name}_enhanced_{timestamp}"
    }
}

def load_configuration(config_path):
    try:
        if os.path.exists(config_path):
            with open(config_path, 'r') as config_file:
                config = json.load(config_file)
                # Merge with default config to ensure all options exist
                merged_config = default_config.copy()
                merged_config.update(config)
                return merged_config
        else:
            logging.warning(f"Configuration file {config_path} not found. Using default configuration.")
            return default_config
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logging.error(f"Error loading configuration: {e}")
        return default_config
