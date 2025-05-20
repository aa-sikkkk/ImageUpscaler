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
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
import time

logging.basicConfig(level=logging.DEBUG)

def get_input(prompt, default=None, cast_type=str):
    """
    Get user input with a prompt, convert it to the specified type, and return it.
    If no input is provided, return the default value.
    """
    while True:
        try:
            user_input = input(prompt).strip()
            if user_input:
                return cast_type(user_input)
            return default
        except ValueError:
            print(f"Invalid input. Please enter a valid {cast_type.__name__} value.")

def get_float_input(prompt, default=1.0):
    """
    Get user input, convert it to float, and return it.
    """
    return get_input(prompt, default, float)

def get_int_input(prompt, default=85):
    """
    Get user input, convert it to int, and return it.
    """
    return get_input(prompt, default, int)

def create_configuration(config_path):
    """
    Create a configuration file by asking the user for input values.
    """
    print("Configuration file not found. Let's create one.")
    config = {}

    config["input_directory"] = get_input("Enter the input directory path: ")
    config["output_directory"] = get_input("Enter the output directory path: ")
    config["upscale_factor"] = get_float_input("Enter the upscale factor (e.g., 2.0, enter 1 for original size): ")
    config["contrast_factor"] = get_float_input("Enter the contrast factor (e.g., 1.0, enter 1 for no change): ")
    config["color_factor"] = get_float_input("Enter the color factor (e.g., 1.0, enter 1 for no change): ")
    config["watermark_text"] = get_input("Enter the watermark text (leave empty for no watermark): ")
    config["watermark_position"] = get_input("Enter the watermark position (e.g., bottom_right): ", "bottom_right").lower()
    config["format_conversion"] = get_input("Enter the output format (e.g., PNG, JPG, enter empty for default): ", "PNG").upper()
    
    crop_settings = get_input("Enter the crop settings as left,top,right,bottom (leave empty for no crop): ")
    if crop_settings:
        config["crop_settings"] = [int(val) for val in crop_settings.split(",")]
    else:
        config["crop_settings"] = None
    
    config["rotation_angle"] = get_float_input("Enter the rotation angle (leave empty for no rotation): ", 0.0)
    config["flip_mode"] = get_input("Enter the flip mode (horizontal/vertical/none): ", None).lower()
    config["noise_reduction"] = get_input("Apply noise reduction? (yes/no): ", "no").lower() == 'yes'
    config["histogram_equalization"] = get_input("Apply histogram equalization? (yes/no): ", "no").lower() == 'yes'
    config["sepia_filter"] = get_input("Apply sepia filter? (yes/no): ", "no").lower() == 'yes'
    config["vignette_filter"] = get_input("Apply vignette filter? (yes/no): ", "no").lower() == 'yes'
    config["face_detection"] = get_input("Apply face detection? (yes/no): ", "no").lower() == 'yes'
    config["background_removal"] = get_input("Remove background? (yes/no): ", "no").lower() == 'yes'
    config["compression_quality"] = get_int_input("Enter compression quality (1-100, leave empty for default 85): ")
    config["preserve_meta"] = get_input("Preserve metadata? (yes/no): ", "no").lower() == 'yes'

    with open(config_path, 'w') as config_file:
        json.dump(config, config_file, indent=4)
    return config

def load_or_create_configuration(config_path):
    """
    Load an existing configuration file or create a new one if it doesn't exist.
    """
    if not os.path.exists(config_path):
        return create_configuration(config_path)
    return load_configuration(config_path)

def process_image(img_path, config, output_directory):
    """
    Process a single image based on the given configuration and save the output.
    """
    try:
        filename = os.path.basename(img_path)
        img = Image.open(img_path)
        original_img = img.copy()

        # Log GPU memory usage before processing
        gpu_info = get_gpu_memory_info()
        if gpu_info:
            logging.debug(f"GPU memory before processing: {gpu_info['allocated'] / 1024**2:.2f}MB allocated")

        # Basic processing
        if config["upscale_factor"] != 1.0:
            img = upscale_image(img, config["upscale_factor"])
            logging.debug(f"Upscaled image by factor: {config['upscale_factor']}")

        if config["contrast_factor"] != 1.0:
            img = adjust_contrast(img, config["contrast_factor"])
            logging.debug(f"Adjusted contrast by factor: {config['contrast_factor']}")

        if config["color_factor"] != 1.0:
            img = adjust_color(img, config["color_factor"])
            logging.debug(f"Adjusted color by factor: {config['color_factor']}")

        # Advanced features with GPU optimization
        if config["advanced_features"]["ai_enhancement"]:
            img = enhance_image_ai(img)
            logging.debug("Applied AI enhancement")

        if config["advanced_features"]["hdr_processing"]:
            img = process_hdr(img)
            logging.debug("Applied HDR processing")

        if config["advanced_features"]["smart_sharpen"]["enabled"]:
            img = smart_sharpen(
                img,
                amount=config["advanced_features"]["smart_sharpen"]["amount"],
                radius=config["advanced_features"]["smart_sharpen"]["radius"],
                threshold=config["advanced_features"]["smart_sharpen"]["threshold"]
            )
            logging.debug("Applied smart sharpening")

        if config["advanced_features"]["auto_color_correction"]:
            img = auto_color_correction(img)
            logging.debug("Applied auto color correction")

        if config["advanced_features"]["detail_enhancement"]["enabled"]:
            img = enhance_details(
                img,
                strength=config["advanced_features"]["detail_enhancement"]["strength"]
            )
            logging.debug("Enhanced details")

        # Clear GPU memory after heavy processing
        clear_gpu_memory()

        # Other processing steps
        if config["watermark_text"]:
            img = add_watermark(img, config["watermark_text"], config["watermark_position"])
            logging.debug(f"Added watermark: {config['watermark_text']}")

        if config["crop_settings"]:
            img = crop_image(img, *config["crop_settings"])
            logging.debug(f"Cropped image with settings: {config['crop_settings']}")

        if config["rotation_angle"]:
            img = rotate_image(img, config["rotation_angle"])
            logging.debug(f"Rotated image by: {config['rotation_angle']} degrees")

        if config["flip_mode"]:
            img = flip_image(img, config["flip_mode"])
            logging.debug(f"Flipped image mode: {config['flip_mode']}")

        if config["histogram_equalization"]:
            img = equalize_histogram(img)
            logging.debug("Applied histogram equalization")

        if config["sepia_filter"]:
            img = apply_sepia_filter(img)
            logging.debug("Applied sepia filter")

        if config["vignette_filter"]:
            img = apply_vignette_filter(img)
            logging.debug("Applied vignette filter")

        if config["face_detection"]:
            faces = detect_faces(img)
            if faces:
                img = draw_rectangles(img, faces)
            logging.debug(f"Detected and drew rectangles on faces: {faces}")

        if config["background_removal"]:
            img = remove_background(img)
            logging.debug("Removed background")

        # Log GPU memory usage after processing
        gpu_info = get_gpu_memory_info()
        if gpu_info:
            logging.debug(f"GPU memory after processing: {gpu_info['allocated'] / 1024**2:.2f}MB allocated")

        # Output handling
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = config["output_settings"]["naming_convention"].format(
            original_name=os.path.splitext(filename)[0],
            timestamp=timestamp
        ) + os.path.splitext(filename)[1]

        output_path = os.path.join(output_directory, output_filename)
        
        # Save processed image
        img.save(output_path, quality=config["compression_quality"])
        logging.info(f"Processed and saved image: {output_path}")

        # Create thumbnail if enabled
        if config["output_settings"]["create_thumbnails"]:
            thumbnail_size = config["output_settings"]["thumbnail_size"]
            thumbnail = img.copy()
            thumbnail.thumbnail(thumbnail_size)
            thumbnail_path = os.path.join(
                output_directory,
                f"thumb_{output_filename}"
            )
            thumbnail.save(thumbnail_path)
            logging.debug(f"Created thumbnail: {thumbnail_path}")

        # Preserve original if enabled
        if config["output_settings"]["preserve_original"]:
            original_path = os.path.join(
                output_directory,
                f"original_{output_filename}"
            )
            original_img.save(original_path)
            logging.debug(f"Preserved original: {original_path}")

        if config["preserve_meta"]:
            img = preserve_metadata(original_img, img)
            logging.debug("Preserved metadata")

        send_notification("Image Processing", f"Processed image saved as: {output_path}")
        return output_path

    except Exception as e:
        logging.error(f"Error processing image {img_path}: {e}")
        return None

def load_images_and_process(input_directory, config, output_directory):
    """
    Load images from the input directory and process them using multiple threads with GPU optimization.
    """
    logging.info("Loading images...")
    images = load_images(input_directory)
    
    if not images:
        logging.error("No images found in the input directory.")
        return

    max_workers = config["batch_processing"]["max_workers"]
    chunk_size = config["batch_processing"]["chunk_size"]

    # Process images in batches for GPU optimization
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for i in range(0, len(images), chunk_size):
            batch = images[i:i + chunk_size]
            future = executor.submit(process_batch, batch, config, output_directory)
            futures.append(future)

        completed = 0
        total = len(images)
        
        for future in tqdm(as_completed(futures), total=len(futures), desc="Processing batches"):
            result = future.result()
            completed += len(result) if result else 0
            if result:
                logging.info(f"Progress: {completed}/{total} images processed")

def process_batch(batch, config, output_directory):
    """
    Process a batch of images with GPU optimization.
    """
    try:
        results = []
        for img_path in batch:
            result = process_image(img_path, config, output_directory)
            results.append(result)
        return results
    except Exception as e:
        logging.error(f"Error processing batch: {e}")
        return []

def main():
    """
    Main function to load the configuration and process images.
    """
    config_path = 'config.json'
    config = load_or_create_configuration(config_path)

    input_directory = config["input_directory"]
    output_directory = config["output_directory"]

    load_images_and_process(input_directory, config, output_directory)

if __name__ == "__main__":
    main()
