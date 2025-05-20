
<p align="center">
 <img height="350" width="400" src="https://github.com/aa-sikkkk/ImageUpscaler/assets/152005759/0af66753-5e4a-4322-ac35-fade40b1656b">
</p>
<p align="center">
  <img src="https://img.shields.io/github/license/aa-sikkkk/ImageUpscaler" alt="License">
  <img src="https://img.shields.io/github/issues/aa-sikkkk/ImageUpscaler" alt="Issues">
  <img src="https://img.shields.io/github/stars/aa-sikkkk/ImageUpscaler" alt="Stars">
</p>

ImageUpscaler is a versatile image processing tool designed to enhance, transform, and manipulate images with a wide range of customizable settings. The application allows users to upscale images, adjust contrast and color, apply various filters, detect faces, and more. It also supports the preservation of metadata and format conversion!

## 📷 Features

### Core Features
- **GPU Acceleration**: Automatically uses GPU if available for faster processing
- **Batch Processing**: Process multiple images in parallel with optimized GPU batches
- **AI Enhancement**: Deep learning-based image enhancement
- **Advanced Filters**: Noise reduction, HDR processing, smart sharpening, and more
- **Metadata Preservation**: Preserve image metadata during processing
- **Configurable**: Highly configurable via `config.json` or command-line arguments

### Image Processing Features
- **Upscaling**: Increase the resolution of images by a specified factor
- **Contrast and Color Adjustment**: Adjust the contrast and color levels of images to enhance visual quality
- **Watermarking**: Add custom text watermarks to images at specified positions
- **Format Conversion**: Convert images to different formats, such as PNG, JPEG, etc.
- **Cropping and Resizing**: Crop images to specific dimensions and resize them to desired widths and heights
- **Rotation and Flipping**: Rotate images by a specified angle and flip them horizontally or vertically
- **Noise Reduction**: Reduce noise in images to improve clarity
- **Histogram Equalization**: Apply histogram equalization to enhance the contrast of images
- **Filters**: Apply sepia and vignette filters for artistic effects
- **Face Detection**: Detect faces in images and draw rectangles around them
- **Background Removal**: Remove the background from images to isolate the subject
- **Compression**: Compress images to reduce file size while maintaining quality
- **Desktop Notifications**: Send desktop notifications upon completion of image processing tasks

<p align="center">
 <img width="250" height="350" src="https://github.com/aa-sikkkk/ImageUpscaler/assets/152005759/6fd814dc-02ef-4147-a30e-bded623efae1">
</p>

## Installation

```bash
pip install -e .
```

## Usage

### Basic Usage

```bash
imageUpscaler process --input <input_dir> --output <output_dir>
```

### Analyze an Image

```bash
imageUpscaler analyze <image_path> --output <analysis_output.json>
```

### Show Version and GPU Status

```bash
imageUpscaler version
```

For detailed usage instructions, see [USAGE.md](USE.md)

## Configuration

Edit `config.json` to customize processing options, including GPU settings:

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

## 🏆 Acknowledgments

- [Real-ESRGAN](https://github.com/xinntao/Real-ESRGAN)
- [Pillow](https://python-pillow.org/)
- [OpenCV](https://opencv.org/)
- [pyfiglet](https://github.com/pwaller/pyfiglet)
- [termcolor](https://pypi.org/project/termcolor/)

## 🎟️ License 

This project is licensed under the [GNU General Public License](https://github.com/aa-sikkkk/ImageUpscaler/blob/master/LICENSE)

## Author

- **Aas1kk**
- Email: workwithaa.sik@gmail.com
- GitHub: [aa-sikkkk](https://github.com/aa-sikkkk)

## 🦮 Contribute 

**We are excited to have you join us in making ImageUpscaler even better! Whether you're fixing bugs, adding new features, improving documentation, or suggesting new ideas, your contributions are welcome and appreciated.**

`Happy Coding!`
