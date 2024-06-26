import logging
from PIL import Image, ImageEnhance, ImageFilter, ImageDraw, ImageFont
import numpy as np
import cv2
import rembg
from io import BytesIO


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
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
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
