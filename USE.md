<p align="center">
 <img src="https://github.com/aa-sikkkk/ImageUpscaler/assets/152005759/52e8d6a2-8e5b-4f1f-a4df-a3a3900a5454">
</p>

## ⚙️ Configuration

The application uses a configuration file (`config.json`) to store user settings. Users can specify the following options:
To streamline your setup process, you can duplicate the default configuration provided and customize it within your project directory.

- **Directories**:
  - `input_directory`: Path to the directory containing input images.
  - `output_directory`: Path to the directory where processed images will be saved.
- **Processing Settings**:
  - `upscale_factor`: Factor by which to upscale images.
  - `contrast_factor`: Factor to adjust contrast.
  - `color_factor`: Factor to adjust color.
  - `watermark_text`: Text for watermarking images.
  - `watermark_position`: Position of the watermark (e.g., `bottom_right`).
  - `format_conversion`: Desired output format (e.g., `PNG`, `JPEG`).
  - `crop_settings`: Coordinates for cropping images (left, top, right, bottom).
  - `resize_settings`: Dimensions for resizing images (width, height).
  - `rotation_angle`: Angle for rotating images.
  - `flip_mode`: Mode for flipping images (`horizontal` or `vertical`).
  - `noise_reduction`: Enable/disable noise reduction.
  - `histogram_equalization`: Enable/disable histogram equalization.
  - `sepia_filter`: Enable/disable sepia filter.
  - `vignette_filter`: Enable/disable vignette filter.
  - `face_detection`: Enable/disable face detection.
  - `background_removal`: Enable/disable background removal.
  - `compression_quality`: Quality setting for image compression (1-100).
  - `preserve_metadata`: Enable/disable metadata preservation.

## ☑️ Implementation

The project is organized into several modules, each responsible for different aspects of image processing:

- **config.py**: Loads the configuration file and provides default settings if the configuration file is not found or invalid.
- **file_utils.py**: Handles loading images from the specified input directory.
- **filters.py**: Contains functions to apply various filters to images (e.g., sepia, vignette, histogram equalization).
- **main.py**: The main script that orchestrates the entire image processing workflow, including loading configuration, processing images, and saving the results.
- **metadata.py**: Handles the preservation of image metadata during processing.
- **notifications.py**: Sends desktop notifications to inform the user about the completion of tasks.
- **transformations.py**: Implements functions for face detection and drawing rectangles around detected faces.

## Usage

To use the ImageUpscaler application, follow these steps:

1. **Setup Configuration**:
   - Run the application. If the configuration file (`config.json`) does not exist, the application will prompt you to create one by entering various settings.

2. **Load Images**:
   - The application will load images from the specified input directory.

3. **Process Images**:
   - Images will be processed according to the settings in the configuration file, applying all specified transformations and enhancements.

4. **Save Images**:
   - Processed images will be saved to the specified output directory.

5. **Receive Notifications**:
   - Upon completion, a desktop notification will be sent.

### Example Configuration

Here is an example of a `config.json` file:

```json
{
    "input_directory": "imageUpscaler/input_folder/",
    "output_directory": "imageUpscaler/output/",
    "upscale_factor": 1.0,
    "contrast_factor": 1.0,
    "color_factor": 1.0,
    "watermark_text": "",
    "watermark_position": "bottom_right",
    "format_conversion": "JPEG",
    "crop_settings": [
        0,
        0,
        0,
        0
    ],
    "resize_settings": [
        0,
        0
    ],
    "rotation_angle": 0,
    "flip_mode": "",
    "noise_reduction": true,
    "histogram_equalization": true,
    "sepia_filter": true,
    "vignette_filter": true,
    "face_detection": true,
    "background_removal": false,
    "compression_quality": 85,
    "preserve_metadata": true
}
```

```
Happy Coding!!
```


