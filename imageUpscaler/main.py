import logging
import json
from tqdm import tqdm
import os
from imageUpscaler.config import load_configuration
from imageUpscaler.file_utils import load_images
from imageUpscaler.notifications import send_notification
from imageUpscaler.image_processing import *
from imageUpscaler.filters import *
from imageUpscaler.transformations import *
from imageUpscaler.metadata import preserve_metadata


def create_configuration(config_path):
    print("Configuration file not found. Let's create one.")
    config = {}
    
    config["input_directory"] = input("Enter the input directory path: ").strip()
    config["output_directory"] = input("Enter the output directory path: ").strip()
    
    upscale_factor = input("Enter the upscale factor (e.g., 2.0, enter 1 for original size): ").strip()
    config["upscale_factor"] = float(upscale_factor) if upscale_factor else 1.0
    
    contrast_factor = input("Enter the contrast factor (e.g., 1.0, enter 1 for no change): ").strip()
    config["contrast_factor"] = float(contrast_factor) if contrast_factor else 1.0
    
    color_factor = input("Enter the color factor (e.g., 1.0, enter 1 for no change): ").strip()
    config["color_factor"] = float(color_factor) if color_factor else 1.0
    
    watermark_text = input("Enter the watermark text (leave empty for no watermark): ").strip()
    config["watermark_text"] = watermark_text if watermark_text else ""
    
    watermark_position = input("Enter the watermark position (e.g., bottom_right): ").strip().lower()
    config["watermark_position"] = watermark_position if watermark_position in ["center", "bottom_right"] else "bottom_right"
    
    format_conversion = input("Enter the output format (e.g., PNG, JPG, enter empty for default): ").strip().upper()
    config["format_conversion"] = format_conversion if format_conversion else "PNG"
    
    crop_settings = input("Enter the crop settings as left,top,right,bottom (leave empty for no crop): ").strip()
    if crop_settings:
        try:
            left, top, right, bottom = map(int, crop_settings.split(','))
            config["crop_settings"] = (left, top, right, bottom)
        except ValueError:
            print("Invalid crop settings format. Ignoring crop.")
            config["crop_settings"] = (0, 0, 0, 0)
    else:
        config["crop_settings"] = (0, 0, 0, 0)
    
    resize_settings = input("Enter the resize settings as width,height (leave empty for no resize): ").strip()
    if resize_settings:
        try:
            width, height = map(int, resize_settings.split(','))
            config["resize_settings"] = (width, height)
        except ValueError:
            print("Invalid resize settings format. Ignoring resize.")
            config["resize_settings"] = (0, 0)
    else:
        config["resize_settings"] = (0, 0)
    
    rotation_angle = input("Enter the rotation angle (e.g., 0, enter empty for no rotation): ").strip()
    config["rotation_angle"] = int(rotation_angle) if rotation_angle else 0
    
    config["flip_mode"] = input("Enter the flip mode (horizontal or vertical, enter empty for no flip): ").strip().lower()
    
    noise_reduction = input("Enable noise reduction (True/False, enter empty for False): ").strip().lower()
    config["noise_reduction"] = noise_reduction == 'true' if noise_reduction else False
    
    histogram_equalization = input("Enable histogram equalization (True/False, enter empty for False): ").strip().lower()
    config["histogram_equalization"] = histogram_equalization == 'true' if histogram_equalization else False
    
    sepia_filter = input("Enable sepia filter (True/False, enter empty for False): ").strip().lower()
    config["sepia_filter"] = sepia_filter == 'true' if sepia_filter else False
    
    vignette_filter = input("Enable vignette filter (True/False, enter empty for False): ").strip().lower()
    config["vignette_filter"] = vignette_filter == 'true' if vignette_filter else False
    
    face_detection = input("Enable face detection (True/False, enter empty for False): ").strip().lower()
    config["face_detection"] = face_detection == 'true' if face_detection else False
    
    background_removal = input("Enable background removal (True/False, enter empty for False): ").strip().lower()
    config["background_removal"] = background_removal == 'true' if background_removal else False
    
    compression_quality = input("Enter the compression quality (1-100, enter empty for default 85): ").strip()
    config["compression_quality"] = int(compression_quality) if compression_quality else 85
    
    preserve_metadata = input("Preserve metadata (True/False, enter empty for True): ").strip().lower()
    config["preserve_metadata"] = preserve_metadata != 'false' if preserve_metadata else True

    with open(config_path, 'w') as config_file:
        json.dump(config, config_file, indent=4)
    print(f"Configuration file created at {config_path}")


def main():
    config_path = "config.json"
    if not os.path.exists(config_path):
        create_configuration(config_path)

    # Load configuration file
    config = load_configuration(config_path)
    if not config:
        logging.error("Failed to load configuration file. Exiting.")
        return

    # Directory and settings from configuration file
    input_directory = config.get("input_directory", ".")
    output_directory = config.get("output_directory", ".")
    upscale_factor = config.get("upscale_factor", 2.0)
    contrast_factor = config.get("contrast_factor", 1.0)
    color_factor = config.get("color_factor", 1.0)
    watermark_text = config.get("watermark_text", "Sample Watermark")
    watermark_position = config.get("watermark_position", "bottom_right")
    format_conversion = config.get("format_conversion", "PNG")
    crop_settings = config.get("crop_settings", (0, 0, 100, 100))
    resize_settings = config.get("resize_settings", (800, 600))
    rotation_angle = config.get("rotation_angle", 0)
    flip_mode = config.get("flip_mode", "horizontal")
    noise_reduction = config.get("noise_reduction", False)
    histogram_equalization = config.get("histogram_equalization", False)
    sepia_filter = config.get("sepia_filter", False)
    vignette_filter = config.get("vignette_filter", False)
    face_detection = config.get("face_detection", False)
    background_removal = config.get("background_removal", False)
    compression_quality = config.get("compression_quality", 85)
    preserve_meta = config.get("preserve_metadata", True)

    images = load_images(input_directory)

    if not images:
        logging.error("No images found in the input directory.")
        return

    # Process each image
    for filename, img in tqdm(images, desc="Processing images"):
        try:
            logging.debug(f"Processing image: {filename}")
            logging.debug(f"Initial image size: {img.size}, mode: {img.mode}")

            if upscale_factor and upscale_factor != 1.0:
                img = upscale_image(img, upscale_factor)
                logging.debug(f"Upscaled image size: {img.size}")

            if contrast_factor and contrast_factor != 1.0:
                img = adjust_contrast(img, contrast_factor)
                logging.debug(f"Adjusted contrast: {contrast_factor}")

            if color_factor and color_factor != 1.0:
                img = adjust_color(img, color_factor)
                logging.debug(f"Adjusted color: {color_factor}")

            if watermark_text:
                img = add_watermark(img, watermark_text, watermark_position)
                logging.debug(f"Added watermark: {watermark_text} at {watermark_position}")

            if format_conversion and format_conversion != "PNG":
                img = convert_image_format(img, format_conversion)
                logging.debug(f"Converted format to: {format_conversion}")

            if crop_settings and any(crop_settings):
                img = crop_image(img, *crop_settings)
                logging.debug(f"Cropped image to settings: {crop_settings}")

            if resize_settings and any(resize_settings):
                img = resize_image(img, *resize_settings)
                logging.debug(f"Resized image to: {resize_settings}")

            if rotation_angle:
                img = rotate_image(img, rotation_angle)
                logging.debug(f"Rotated image by: {rotation_angle} degrees")

            if flip_mode:
                img = flip_image(img, flip_mode)
                logging.debug(f"Flipped image mode: {flip_mode}")

            if noise_reduction:
                img = reduce_noise(img)
                logging.debug("Applied noise reduction")

            if histogram_equalization:
                img = equalize_histogram(img)
                logging.debug("Applied histogram equalization")

            if sepia_filter:
                img = apply_sepia_filter(img)
                logging.debug("Applied sepia filter")

            if vignette_filter:
                img = apply_vignette_filter(img)
                logging.debug("Applied vignette filter")

            if face_detection:
                faces = detect_faces(img)
                if len(faces) > 0:
                    img = draw_rectangles(img, faces)
                logging.debug(f"Detected and drew rectangles on faces: {faces}")

            if background_removal:
                img = remove_background(img)
                logging.debug("Removed background")

            if compression_quality and compression_quality != 85:
                img = compress_image(img, compression_quality)
                logging.debug(f"Compressed image with quality: {compression_quality}")

            if preserve_meta:
                img = preserve_metadata(img, img)
                logging.debug("Preserved metadata")

            output_path = os.path.join(output_directory, filename)
            img.save(output_path)
            logging.info(f"Processed and saved image: {output_path}")

            # Send a desktop notification
            send_notification("Image Processing", f"Processed image saved as: {output_path}")

        except Exception as e:
            logging.error(f"Error processing {filename}: {e}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    main()