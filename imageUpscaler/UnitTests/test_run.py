import unittest
from unittest.mock import patch, mock_open, MagicMock

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) 

import json
from sympy import false, true
from imageUpscaler.metadata import preserve_metadata
from imageUpscaler.config import load_configuration
from imageUpscaler.config import default_config
from imageUpscaler.file_utils import load_images
from imageUpscaler.notifications import send_notification
from imageUpscaler.main import create_configuration, main
from imageUpscaler.image_processing import *
from imageUpscaler.filters import *
from imageUpscaler.transformations import *
from imageUpscaler.banner import about
from PIL import Image
from imageUpscaler.banner import about
class TestConfigFunctions(unittest.TestCase):


    
    def test_load_configuration_existing_file(self):
        config_data = {
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
        with patch('builtins.open', mock_open(read_data=json.dumps(config_data))):
            loaded_config = load_configuration("imageUpscaler/config.json")
            self.assertEqual(loaded_config["input_directory"], "imageUpscaler/input_folder")
 
    def test_load_configuration_invalid_file(self):
        with patch('builtins.open', side_effect=FileNotFoundError):
            loaded_config = load_configuration("imageUpscaler/invalid/config.json")
            self.assertEqual(loaded_config, default_config)

class TestFileUtilsFunctions(unittest.TestCase):

    @patch('os.path.exists', return_value=True)
    def test_load_images_valid_images(self, mock_exists):
        mock_image = MagicMock(spec=Image)
        type(mock_image).verify = MagicMock(return_value=None)

        with patch('os.listdir', return_value=['image1.jpg', 'image2.png']):
            images = load_images("imageUpscaler/input_folder/")
            self.assertEqual(len(images), 2)


    @patch('os.path.exists', return_value=False)
    def test_load_images_invalid_images(self, mock_exists):
        with self.assertRaises(ValueError):
            load_images("imageUpscaler/input_folder/")

class TestFiltersFunctions(unittest.TestCase):

    def test_apply_vignette_filter(self):
        # Mocking an image for testing
        mock_img = MagicMock(spec=Image)
        mock_np_img = MagicMock(spec=np.ndarray)
        type(mock_img).np_img = mock_np_img
        mock_np_img.shape = (100, 100, 3) 

        result = apply_vignette_filter(mock_img)
 
class TestImageProcessingFunctions(unittest.TestCase):

    @patch.object(Image.Image, 'resize')
    def test_upscale_image(self, mock_resize):
        mock_img = MagicMock(spec=Image)
        mock_img.size = (100, 100)

        upscale_image(mock_img, 2.0)
        mock_resize.assert_called_once_with((200, 200))

 
class TestMainScript(unittest.TestCase):

    @patch('os.path.exists', return_value=True)
    @patch('imageUpscaler.notifications.send_notification')
    def test_main_script(self, mock_send_notification, mock_exists):
        # Mocking load_images output
        mock_images = [('image1.jpg', MagicMock(spec=Image))]
        with patch('imageUpscaler.file_utils.load_images', return_value=mock_images):
            main()

        mock_send_notification.assert_called_once()



class TestMetadataFunctions(unittest.TestCase):

    @patch('PIL.Image.Image.info')
    def test_preserve_metadata(self, mock_info):
        mock_original_img = MagicMock(spec=Image)
        mock_processed_img = MagicMock(spec=Image)

        result = preserve_metadata(mock_original_img, mock_processed_img)
        self.assertEqual(result, mock_processed_img)
        mock_info.update.assert_called_once_with(mock_original_img.info)



class TestBannerFunctions(unittest.TestCase):

    @patch('builtins.print')
    def test_about_function(self, mock_print):
        about()
        expected_output = 'Your expected output for about_function'
        mock_print.assert_called_once_with(expected_output)

 
class TestTransformationsFunctions(unittest.TestCase):

    def test_detect_faces(self):
        # Mocking a numpy array for cv2 functions
        mock_np_img = MagicMock(spec=np.ndarray)
        type(mock_np_img).shape = (100, 100, 3)  

        with patch('cv2.CascadeClassifier.detectMultiScale', return_value=[(10, 10, 20, 20)]):
            faces = detect_faces(mock_np_img)
            self.assertEqual(len(faces), 1)
       

if __name__ == '__main__':
    unittest.main()
