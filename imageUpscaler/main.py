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
from concurrent.futures import ThreadPoolExecutor

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

        if config["upscale_factor"] != 1.0:
            img = upscale_image(img, config["upscale_factor"])
            logging.debug(f"Upscaled image by factor: {config['upscale_factor']}")

        if config["contrast_factor"] != 1.0:
            img = adjust_contrast(img, config["contrast_factor"])
            logging.debug(f"Adjusted contrast by factor: {config['contrast_factor']}")

        if config["color_factor"] != 1.0:
            img = adjust_color(img, config["color_factor"])
            logging.debug(f"Adjusted color by factor: {config['color_factor']}")

        if config["watermark_text"]:
            img = add_watermark(img, config["watermark_text"], config["watermark_position"])
            logging.debug(f"Added watermark: {config['watermark_text']} at {config['watermark_position']}")

        if config["crop_settings"]:
            img = crop_image(img, *config["crop_settings"])
            logging.debug(f"Cropped image with settings: {config['crop_settings']}")

        if config["rotation_angle"]:
            img = rotate_image(img, config["rotation_angle"])
            logging.debug(f"Rotated image by: {config['rotation_angle']} degrees")

        if config["flip_mode"]:
            img = flip_image(img, config["flip_mode"])
            logging.debug(f"Flipped image mode: {config['flip_mode']}")

        if config["noise_reduction"]:
            img = reduce_noise(img)
            logging.debug("Applied noise reduction")

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

        if config["compression_quality"] != 85:
            img = compress_image(img, config["compression_quality"])
            logging.debug(f"Compressed image with quality: {config['compression_quality']}")

        if config["preserve_meta"]:
            img = preserve_metadata(img, img)
            logging.debug("Preserved metadata")

        output_path = os.path.join(output_directory, filename)
        img.save(output_path)
        logging.info(f"Processed and saved image: {output_path}")

        send_notification("Image Processing", f"Processed image saved as: {output_path}")

    except Exception as e:
        logging.error(f"Error processing {filename}: {e}")

def load_images_and_process(input_directory, config, output_directory):
    """
    Load images from the input directory and process them using multiple threads.
    """
    logging.info("Loading images...")
    images = load_images(input_directory)
    
    if not images:
        logging.error("No images found in the input directory.")
        return

    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(process_image, img_path, config, output_directory) for img_path in images]
        for future in tqdm(futures, desc="Processing images"):
            future.result()

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
