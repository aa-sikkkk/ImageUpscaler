"""
ImageUpscaler - Advanced Image Processing Package
Version: 3.2
"""

from .main import main, process_image
from .image_processing import *
from .filters import *
from .transformations import *
from .config import load_configuration, default_config

__version__ = '3.2'
__author__ = 'Aas1kk'
__email__ = 'workingaas1kk@outlook.com'

def get_version():
    """Return the version of the package."""
    return __version__

__all__ = [
    'main',
    'process_image',
    'load_configuration',
    'default_config',
    'get_version',
    '__version__',
    '__author__',
    '__email__'
]
