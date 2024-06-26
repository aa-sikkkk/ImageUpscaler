from PIL import ImageDraw
import cv2
import numpy as np

def detect_faces(img):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    return faces

def draw_rectangles(img, rectangles):
    draw = ImageDraw.Draw(img)
    for (x, y, w, h) in rectangles:
        draw.rectangle(((x, y), (x + w, y + h)), outline="red", width=3)
    return img
