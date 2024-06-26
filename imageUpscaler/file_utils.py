import os
from PIL import Image
import logging

logging.basicConfig(level=logging.DEBUG)

def load_images(directory):
    images = []
    supported_extensions = (".png", ".jpg", ".jpeg")
    
    if not os.path.exists(directory):
        logging.error(f"Directory {directory} does not exist.")
        return images
    
    if not os.listdir(directory):
        logging.warning(f"Directory {directory} is empty.")
        return images
    
    for filename in os.listdir(directory):
        if filename.lower().endswith(supported_extensions):
            try:
                img_path = os.path.join(directory, filename)
                logging.debug(f"Loading image {img_path}")
                img = Image.open(img_path)
                img.verify()  # Verify that this is an image
                img = Image.open(img_path)  # Reopen the image after verify
                if img:
                    images.append((filename, img))
                    logging.debug(f"Successfully loaded {filename}")
                else:
                    logging.warning(f"Failed to load {filename}. Image is empty.")
            except (IOError, OSError) as e:
                logging.error(f"Error loading {filename}: {e}")
            except Exception as e:
                logging.error(f"Unexpected error loading {filename}: {e}")
    return images
