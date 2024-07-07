# Package File For ImageUpscaler
from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as file:
    long_description = file.read()

install_requires = [
    'absl-py==2.1.0',
    'opencv-python==4.10.0.84',
    'piexif==1.1.3',
    'pillow==10.3.0',
    'pyfiglet==1.0.2',
    'scikit-image==0.24.0',
    'scipy==1.13.1',
    'realesrgan==0.3.0'
    'torch==2.3.1',
    'torchvision==0.18.1',
    
]


setup(
    name='ImageUpscaler',
    version='3.1',
    packages=find_packages(where='imageUpscaler'),
    package_dir={'': 'imageUpscaler'},
    include_package_data=True,
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
            'imageUpscaler=run:main',
        ],
    },
    author='Aas1kk',
    author_email='workingaas1kk@outlook.com',
    description='A package for upscaling images using neural networks.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/aa-sikkkk/ImageUpscaler',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)