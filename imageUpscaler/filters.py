import numpy as np
from PIL import Image
import cv2

def apply_sepia_filter(img):
    if img.mode != 'RGB':
        img = img.convert('RGB')
    np_img = np.array(img)
    tr = 0.393 * np_img[:, :, 0] + 0.769 * np_img[:, :, 1] + 0.189 * np_img[:, :, 2]
    tg = 0.349 * np_img[:, :, 0] + 0.686 * np_img[:, :, 1] + 0.168 * np_img[:, :, 2]
    tb = 0.272 * np_img[:, :, 0] + 0.534 * np_img[:, :, 1] + 0.131 * np_img[:, :, 2]
    sepia_img = np.stack((tr, tg, tb), axis=-1)
    sepia_img = np.clip(sepia_img, 0, 255).astype(np.uint8)
    return Image.fromarray(sepia_img)

def apply_vignette_filter(img):
    if img.mode != 'RGB':
        img = img.convert('RGB')
    np_img = np.array(img)
    rows, cols = np_img.shape[:2]
    kernel_x = cv2.getGaussianKernel(cols, 200)
    kernel_y = cv2.getGaussianKernel(rows, 200)
    kernel = kernel_y * kernel_x.T
    mask = 255 * kernel / np.linalg.norm(kernel)
    vignette = np.copy(np_img)
    for i in range(3):
        vignette[:, :, i] = vignette[:, :, i] * mask
    return Image.fromarray(np.clip(vignette, 0, 255).astype(np.uint8))

def equalize_histogram(image):
    # Ensure the image has 3 color channels
    if image.mode != 'RGB':
        image = image.convert('RGB')
    img_yuv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2YUV)
    img_yuv[:,:,0] = cv2.equalizeHist(img_yuv[:,:,0])
    img_output = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2RGB)
    return Image.fromarray(img_output)
