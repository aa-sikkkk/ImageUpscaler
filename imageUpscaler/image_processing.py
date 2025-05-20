import logging
from PIL import Image, ImageEnhance, ImageFilter, ImageDraw, ImageFont, ImageOps
import numpy as np
import cv2
import rembg
from io import BytesIO
from skimage import exposure, restoration
from skimage.filters import unsharp_mask
import torch
from torchvision import transforms
import gc
from functools import lru_cache
import os

# Global device configuration
DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
logging.info(f"Using device: {DEVICE}")

# GPU memory management
def clear_gpu_memory():
    """Clear GPU memory cache."""
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        gc.collect()

def get_gpu_memory_info():
    """Get GPU memory usage information."""
    if torch.cuda.is_available():
        return {
            'total': torch.cuda.get_device_properties(0).total_memory,
            'allocated': torch.cuda.memory_allocated(0),
            'cached': torch.cuda.memory_reserved(0)
        }
    return None

# Model caching with GPU optimization
@lru_cache(maxsize=2)
def get_face_cascade():
    return cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

@lru_cache(maxsize=2)
def get_clahe():
    return cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))

class ModelCache:
    def __init__(self):
        self.models = {}
        self.transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
        self.batch_size = 4  # Default batch size for GPU processing

    def get_model(self, model_name):
        if model_name not in self.models:
            # Load model here (placeholder for actual model loading)
            self.models[model_name] = torch.nn.Sequential(
                torch.nn.Conv2d(3, 64, 3, padding=1),
                torch.nn.ReLU(),
                torch.nn.Conv2d(64, 3, 3, padding=1)
            ).to(DEVICE)
            # Enable CUDA optimizations
            if torch.cuda.is_available():
                self.models[model_name] = torch.nn.DataParallel(self.models[model_name])
                torch.backends.cudnn.benchmark = True
        return self.models[model_name]

    def process_batch(self, images, model_name='default'):
        """Process a batch of images using GPU acceleration."""
        try:
            if not images:
                return []
            
            # Convert images to tensors
            tensors = [self.transform(img).unsqueeze(0) for img in images]
            batch = torch.cat(tensors, dim=0).to(DEVICE)
            
            # Get model and process batch
            model = self.get_model(model_name)
            with torch.no_grad():
                enhanced = model(batch)
            
            # Convert back to PIL Images
            results = []
            for i in range(len(images)):
                img_tensor = enhanced[i].cpu()
                img_np = img_tensor.numpy()
                img_np = np.transpose(img_np, (1, 2, 0))
                img_np = np.clip(img_np * 255, 0, 255).astype(np.uint8)
                results.append(Image.fromarray(img_np))
            
            return results
        except Exception as e:
            logging.error(f"Batch processing failed: {e}")
            return images

    def clear_cache(self):
        """Clear model cache and GPU memory."""
        self.models.clear()
        clear_gpu_memory()

model_cache = ModelCache()

def upscale_image(img, factor):
    return img.resize((int(img.width * factor), int(img.height * factor)), Image.LANCZOS)

def adjust_contrast(img, factor):
    enhancer = ImageEnhance.Contrast(img)
    return enhancer.enhance(factor)

def adjust_color(img, factor):
    enhancer = ImageEnhance.Color(img)
    return enhancer.enhance(factor)

def sharpen_image(img):
    return img.filter(ImageFilter.SHARPEN)

def convert_image_format(img, output_format):
    img = img.convert('RGB')
    output_io = BytesIO()
    img.save(output_io, format=output_format)
    output_io.seek(0)
    return Image.open(output_io)

def add_watermark(img, watermark_text, position, font_size=36, opacity=128):
    img = img.convert('RGBA')
    watermark = Image.new('RGBA', img.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(watermark)
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except IOError:
        font = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), watermark_text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    if position == "center":
        text_position = ((img.width - text_width) // 2, (img.height - text_height) // 2)
    elif position == "bottom_right":
        text_position = (img.width - text_width - 10, img.height - text_height - 10)
    else:
        text_position = (10, 10)

    draw.text(text_position, watermark_text, font=font, fill=(255, 255, 255, opacity))
    watermarked_img = Image.alpha_composite(img, watermark)
    return watermarked_img.convert('RGB')

def crop_image(img, left, top, right, bottom):
    return img.crop((left, top, right, bottom))

def resize_image(img, width, height):
    return img.resize((width, height), Image.LANCZOS)

def rotate_image(img, angle):
    return img.rotate(angle)

def flip_image(img, mode):
    if mode == 'horizontal':
        return img.transpose(Image.FLIP_LEFT_RIGHT)
    elif mode == 'vertical':
        return img.transpose(Image.FLIP_TOP_BOTTOM)

def reduce_noise(img):
    np_img = np.array(img)
    if np_img.size == 0:
        raise ValueError("Image is empty or not loaded correctly.")
    logging.debug(f"reduce_noise: np_img.shape={np_img.shape}, np_img.dtype={np_img.dtype}")
    img_cv2 = cv2.cvtColor(np_img, cv2.COLOR_RGB2BGR)
    dst = cv2.fastNlMeansDenoisingColored(img_cv2, None, 10, 10, 7, 21)
    return Image.fromarray(cv2.cvtColor(dst, cv2.COLOR_BGR2RGB))

def remove_background(img):
    return rembg.remove(img)

def compress_image(img, quality=85):
    output_io = BytesIO()
    img.save(output_io, format='JPEG', quality=quality)
    output_io.seek(0)
    return Image.open(output_io)

def detect_faces(img):
    face_cascade = get_face_cascade()
    
    np_img = np.array(img)
    if np_img.size == 0:
        raise ValueError("Image is empty or not loaded correctly.")
    logging.debug(f"detect_faces: np_img.shape={np_img.shape}, np_img.dtype={np_img.dtype}")

    gray = cv2.cvtColor(np_img, cv2.COLOR_RGB2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    return faces

def draw_rectangles(img, rectangles):
    draw = ImageDraw.Draw(img)
    for (x, y, w, h) in rectangles:
        draw.rectangle(((x, y), (x+w, y+h)), outline="red", width=3)
    return img

def enhance_image_ai(img, model_name='default'):
    """Apply AI-based image enhancement using deep learning with GPU support."""
    try:
        # Convert to tensor and move to GPU if available
        img_tensor = model_cache.transform(img).unsqueeze(0).to(DEVICE)
        
        # Get model and apply enhancement
        model = model_cache.get_model(model_name)
        with torch.no_grad():
            enhanced = model(img_tensor)
        
        # Convert back to PIL Image
        enhanced = enhanced.squeeze(0).cpu().numpy()
        enhanced = np.transpose(enhanced, (1, 2, 0))
        enhanced = np.clip(enhanced * 255, 0, 255).astype(np.uint8)
        return Image.fromarray(enhanced)
    except Exception as e:
        logging.error(f"AI enhancement failed: {e}")
        return img

def process_hdr(img, exposure_values=[-2, 0, 2], merge_method='average'):
    """Process HDR-like effect from a single image with multiple merge methods."""
    try:
        images = []
        for ev in exposure_values:
            adjusted = exposure.adjust_gamma(img, 2 ** ev)
            images.append(np.array(adjusted))
        
        if merge_method == 'average':
            merged = np.mean(images, axis=0)
        elif merge_method == 'maximum':
            merged = np.maximum.reduce(images)
        else:
            merged = exposure.merge_hdr(images)
        
        return Image.fromarray((merged * 255).astype(np.uint8))
    except Exception as e:
        logging.error(f"HDR processing failed: {e}")
        return img

def advanced_noise_reduction(img, method='nlm', strength=1.0):
    """Apply advanced noise reduction techniques with strength control."""
    try:
        np_img = np.array(img)
        if method == 'nlm':
            # Non-local means denoising with strength control
            result = cv2.fastNlMeansDenoisingColored(np_img, None, 10, 10, 7, 21)
        elif method == 'wavelet':
            # Wavelet denoising with strength control
            result = restoration.denoise_wavelet(np_img, multichannel=True, convert2ycbcr=True)
            result = (result * 255).astype(np.uint8)
        elif method == 'bilateral':
            # Bilateral filtering with strength control
            result = cv2.bilateralFilter(np_img, 9, 75, 75)
        
        # Blend with original based on strength
        if strength < 1.0:
            result = cv2.addWeighted(np_img, 1-strength, result, strength, 0)
        
        return Image.fromarray(result)
    except Exception as e:
        logging.error(f"Advanced noise reduction failed: {e}")
        return img

def smart_sharpen(img, amount=1.0, radius=1.0, threshold=0, method='unsharp'):
    """Apply smart sharpening with multiple methods and adaptive parameters."""
    try:
        np_img = np.array(img)
        if method == 'unsharp':
            sharpened = unsharp_mask(np_img, radius=radius, amount=amount, threshold=threshold)
        elif method == 'laplacian':
            kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]]) * amount
            sharpened = cv2.filter2D(np_img, -1, kernel)
        elif method == 'gaussian':
            gaussian = cv2.GaussianBlur(np_img, (0, 0), radius)
            sharpened = cv2.addWeighted(np_img, 1 + amount, gaussian, -amount, 0)
        
        return Image.fromarray(np.clip(sharpened, 0, 255).astype(np.uint8))
    except Exception as e:
        logging.error(f"Smart sharpening failed: {e}")
        return img

def auto_color_correction(img, method='clahe'):
    """Apply automatic color correction with multiple methods."""
    try:
        np_img = np.array(img)
        if method == 'clahe':
            # Convert to LAB color space
            lab = cv2.cvtColor(np_img, cv2.COLOR_RGB2LAB)
            l, a, b = cv2.split(lab)
            
            # Apply CLAHE to L channel
            clahe = get_clahe()
            l = clahe.apply(l)
            
            # Merge channels and convert back to RGB
            lab = cv2.merge((l, a, b))
            corrected = cv2.cvtColor(lab, cv2.COLOR_LAB2RGB)
        elif method == 'histogram':
            # Histogram equalization
            corrected = exposure.equalize_hist(np_img)
            corrected = (corrected * 255).astype(np.uint8)
        elif method == 'adaptive':
            # Adaptive histogram equalization
            corrected = exposure.equalize_adapthist(np_img)
            corrected = (corrected * 255).astype(np.uint8)
        
        return Image.fromarray(corrected)
    except Exception as e:
        logging.error(f"Color correction failed: {e}")
        return img

def enhance_details(img, strength=1.0, method='detail'):
    """Enhance fine details in the image with multiple methods."""
    try:
        np_img = np.array(img)
        if method == 'detail':
            # Detail enhancement
            enhanced = cv2.detailEnhance(np_img, sigma_s=10, sigma_r=0.15)
        elif method == 'edge':
            # Edge enhancement
            kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
            enhanced = cv2.filter2D(np_img, -1, kernel)
        elif method == 'frequency':
            # Frequency domain enhancement
            dft = cv2.dft(np.float32(np_img), flags=cv2.DFT_COMPLEX_OUTPUT)
            dft_shift = np.fft.fftshift(dft)
            magnitude_spectrum = 20 * np.log(cv2.magnitude(dft_shift[:,:,0], dft_shift[:,:,1]))
            enhanced = np.fft.ifftshift(dft_shift)
            enhanced = cv2.idft(enhanced)
            enhanced = cv2.magnitude(enhanced[:,:,0], enhanced[:,:,1])
            enhanced = np.uint8(enhanced * 255 / enhanced.max())
        
        # Blend with original based on strength
        result = cv2.addWeighted(np_img, 1-strength, enhanced, strength, 0)
        return Image.fromarray(result)
    except Exception as e:
        logging.error(f"Detail enhancement failed: {e}")
        return img
