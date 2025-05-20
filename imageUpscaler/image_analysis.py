import cv2
import numpy as np
from PIL import Image
import logging
from skimage import feature, measure, color
from scipy import stats
import torch
import torchvision.models as models
from torchvision import transforms

class ImageAnalyzer:
    def __init__(self):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.transform = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
        self.model = models.resnet50(pretrained=True).to(self.device)
        self.model.eval()

    def analyze_image(self, img):
        """Perform comprehensive image analysis."""
        try:
            np_img = np.array(img)
            analysis = {
                'basic_stats': self._get_basic_stats(np_img),
                'color_analysis': self._analyze_colors(np_img),
                'edge_analysis': self._analyze_edges(np_img),
                'texture_analysis': self._analyze_texture(np_img),
                'quality_metrics': self._get_quality_metrics(np_img),
                'object_detection': self._detect_objects(img),
                'scene_classification': self._classify_scene(img)
            }
            return analysis
        except Exception as e:
            logging.error(f"Image analysis failed: {e}")
            return None

    def _get_basic_stats(self, np_img):
        """Get basic image statistics."""
        return {
            'dimensions': np_img.shape,
            'mean': np.mean(np_img),
            'std': np.std(np_img),
            'min': np.min(np_img),
            'max': np.max(np_img),
            'histogram': np.histogram(np_img, bins=256)[0].tolist()
        }

    def _analyze_colors(self, np_img):
        """Analyze color distribution and characteristics."""
        # Convert to HSV for better color analysis
        hsv = cv2.cvtColor(np_img, cv2.COLOR_RGB2HSV)
        h, s, v = cv2.split(hsv)
        
        return {
            'dominant_colors': self._get_dominant_colors(np_img),
            'color_variance': np.var(hsv, axis=(0,1)).tolist(),
            'saturation_stats': {
                'mean': np.mean(s),
                'std': np.std(s)
            },
            'brightness_stats': {
                'mean': np.mean(v),
                'std': np.std(v)
            }
        }

    def _get_dominant_colors(self, np_img, n_colors=5):
        """Extract dominant colors using k-means clustering."""
        pixels = np_img.reshape(-1, 3)
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, 0.1)
        _, labels, centers = cv2.kmeans(np.float32(pixels), n_colors, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
        return centers.astype(int).tolist()

    def _analyze_edges(self, np_img):
        """Analyze edge characteristics."""
        gray = cv2.cvtColor(np_img, cv2.COLOR_RGB2GRAY)
        edges = cv2.Canny(gray, 100, 200)
        
        return {
            'edge_density': np.mean(edges > 0),
            'edge_orientation': self._get_edge_orientation(edges),
            'edge_strength': np.mean(edges[edges > 0])
        }

    def _get_edge_orientation(self, edges):
        """Calculate edge orientation distribution."""
        sobelx = cv2.Sobel(edges, cv2.CV_64F, 1, 0, ksize=3)
        sobely = cv2.Sobel(edges, cv2.CV_64F, 0, 1, ksize=3)
        angles = np.arctan2(sobely, sobelx) * 180 / np.pi
        return np.histogram(angles[edges > 0], bins=36)[0].tolist()

    def _analyze_texture(self, np_img):
        """Analyze texture characteristics."""
        gray = cv2.cvtColor(np_img, cv2.COLOR_RGB2GRAY)
        
        # GLCM features
        glcm = feature.greycomatrix(gray, [1], [0, np.pi/4, np.pi/2, 3*np.pi/4])
        contrast = feature.greycoprops(glcm, 'contrast')
        dissimilarity = feature.greycoprops(glcm, 'dissimilarity')
        homogeneity = feature.greycoprops(glcm, 'homogeneity')
        energy = feature.greycoprops(glcm, 'energy')
        correlation = feature.greycoprops(glcm, 'correlation')
        
        return {
            'contrast': contrast.tolist(),
            'dissimilarity': dissimilarity.tolist(),
            'homogeneity': homogeneity.tolist(),
            'energy': energy.tolist(),
            'correlation': correlation.tolist()
        }

    def _get_quality_metrics(self, np_img):
        """Calculate image quality metrics."""
        gray = cv2.cvtColor(np_img, cv2.COLOR_RGB2GRAY)
        
        # Calculate noise level
        noise = cv2.fastNlMeansDenoising(gray)
        noise_level = np.mean(np.abs(gray - noise))
        
        # Calculate blur metric
        laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
        
        return {
            'noise_level': float(noise_level),
            'blur_metric': float(laplacian_var),
            'sharpness': float(np.mean(cv2.Laplacian(gray, cv2.CV_64F)))
        }

    def _detect_objects(self, img):
        """Detect objects in the image using pre-trained model."""
        try:
            img_tensor = self.transform(img).unsqueeze(0).to(self.device)
            with torch.no_grad():
                output = self.model(img_tensor)
                probabilities = torch.nn.functional.softmax(output[0], dim=0)
                top5_prob, top5_catid = torch.topk(probabilities, 5)
                
            return {
                'top_objects': [
                    {'class': idx.item(), 'probability': prob.item()}
                    for idx, prob in zip(top5_catid, top5_prob)
                ]
            }
        except Exception as e:
            logging.error(f"Object detection failed: {e}")
            return None

    def _classify_scene(self, img):
        """Classify the scene type."""
        try:
            img_tensor = self.transform(img).unsqueeze(0).to(self.device)
            with torch.no_grad():
                output = self.model(img_tensor)
                probabilities = torch.nn.functional.softmax(output[0], dim=0)
                scene_type = torch.argmax(probabilities).item()
                
            return {
                'scene_type': int(scene_type),
                'confidence': float(probabilities[scene_type])
            }
        except Exception as e:
            logging.error(f"Scene classification failed: {e}")
            return None

def get_image_analysis(img):
    """Convenience function to get image analysis."""
    analyzer = ImageAnalyzer()
    return analyzer.analyze_image(img) 