# ImageUpscaler Usage Guide

<p align="center">
 <img height="400" width="400" src="https://github.com/aa-sikkkk/ImageUpscaler/assets/152005759/0af66753-5e4a-4322-ac35-fade40b1656b">
</p>
<p align="center">
  <img src="https://img.shields.io/github/license/aa-sikkkk/ImageUpscaler" alt="License">
  <img src="https://img.shields.io/github/issues/aa-sikkkk/ImageUpscaler" alt="Issues">
  <img src="https://img.shields.io/github/stars/aa-sikkkk/ImageUpscaler" alt="Stars">
</p>

## 📋 Table of Contents
- [Installation](#installation)
- [Basic Usage](#basic-usage)
- [Configuration](#configuration)
- [Advanced Features](#advanced-features)
- [Command Line Interface](#command-line-interface)
- [Examples](#examples)

## 🚀 Installation

```bash
# Clone the repository
git clone https://github.com/aa-sikkkk/ImageUpscaler.git

# Navigate to the project directory
cd ImageUpscaler

# Install the package
pip install -e .
```

## 🎯 Basic Usage

### Command Line Interface

```bash
# Process images with default settings
imageUpscaler process --input <input_dir> --output <output_dir>

# Analyze an image
imageUpscaler analyze <image_path> --output <analysis_output.json>

# Show version and GPU status
imageUpscaler version
```

### Python API

```python
from imageUpscaler import ImageProcessor

# Initialize the processor
processor = ImageProcessor()

# Process a single image
processor.process_image("input.jpg", "output.jpg")

# Process a directory of images
processor.process_directory("input_dir", "output_dir")
```

## ⚙️ Configuration

The application uses a `config.json` file to store user settings. You can customize the following options:

### Directory Settings
```json
{
    "input_directory": "path/to/input",
    "output_directory": "path/to/output"
}
```

### Processing Settings
```json
{
    "upscale_factor": 2.0,
    "contrast_factor": 1.2,
    "color_factor": 1.1,
    "compression_quality": 85,
    "preserve_metadata": true
}
```

### Enhancement Settings
```json
{
    "noise_reduction": true,
    "histogram_equalization": true,
    "face_detection": true,
    "background_removal": false
}
```

### Filter Settings
```json
{
    "sepia_filter": false,
    "vignette_filter": false,
    "watermark_text": "",
    "watermark_position": "bottom_right"
}
```

### Transformation Settings
```json
{
    "crop_settings": [0, 0, 0, 0],
    "resize_settings": [0, 0],
    "rotation_angle": 0,
    "flip_mode": ""
}
```

## 🔧 Advanced Features

### GPU Acceleration
The application automatically uses GPU if available. Configure GPU settings in `config.json`:

```json
"gpu_settings": {
    "enabled": true,
    "batch_size": 4,
    "memory_limit": 0.8,
    "optimization_level": "high",
    "mixed_precision": true,
    "cudnn_benchmark": true,
    "clear_cache_after_batch": true
}
```

### Batch Processing
Process multiple images in parallel:
```bash
imageUpscaler process --input <input_dir> --output <output_dir> --batch-size 4
```

### Image Analysis
Generate detailed analysis reports:
```bash
imageUpscaler analyze <image_path> --output analysis.json --detailed
```

## 📝 Examples

### Example 1: Basic Image Processing
```bash
imageUpscaler process --input ./images --output ./processed --upscale 2.0
```

### Example 2: Advanced Processing with Filters
```bash
imageUpscaler process --input ./images --output ./processed \
    --upscale 2.0 \
    --noise-reduction \
    --face-detection \
    --watermark "© 2024" \
    --watermark-position bottom-right
```

### Example 3: Batch Processing with GPU
```bash
imageUpscaler process --input ./images --output ./processed \
    --batch-size 4 \
    --gpu \
    --memory-limit 0.8
```

## 🎯 Best Practices

1. **Backup Your Images**: Always keep a backup of your original images before processing.
2. **Test Settings**: Test processing settings on a small batch of images first.
3. **Monitor Resources**: Keep an eye on GPU memory usage when processing large batches.
4. **Use Appropriate Formats**: Choose the right output format based on your needs:
   - Use PNG for lossless quality
   - Use JPEG for smaller file sizes
   - Use WebP for web optimization

## 🆘 Troubleshooting

### Common Issues

1. **GPU Not Detected**
   - Ensure CUDA is properly installed
   - Check GPU compatibility
   - Verify GPU drivers are up to date

2. **Memory Issues**
   - Reduce batch size
   - Lower memory limit
   - Process images in smaller batches

3. **Quality Issues**
   - Adjust compression quality
   - Check input image format
   - Verify processing settings

## 📚 Additional Resources

- [Documentation](https://github.com/aa-sikkkk/ImageUpscaler/wiki)
- [Issue Tracker](https://github.com/aa-sikkkk/ImageUpscaler/issues)
- [Contributing Guidelines](CONTRIBUTING.md)

---

<p align="center">
  <img width="250" height="350" src="https://github.com/aa-sikkkk/ImageUpscaler/assets/152005759/6fd814dc-02ef-4147-a30e-bded623efae1">
</p>

`Happy Coding!`
