# ImageUpscaler - Advanced image processing and analysis package
# Copyright (C) 2024 Aas1kk
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# See the LICENSE file or <https://www.gnu.org/licenses/> for details.

# Package File For ImageUpscaler
from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as file:
    long_description = file.read()

install_requires = [
    'opencv-python==4.10.0.84',
    'pillow==10.3.0',
    'pyfiglet==1.0.2',
    'scipy==1.12.0',
    'realesrgan==0.3.0',
    'numpy==1.26.4',
    'torch==2.2.0',
    'torchvision==0.17.0',
    'scikit-image==0.22.0',
    'scikit-learn==1.4.0',
    'matplotlib==3.8.2',
    'seaborn==0.13.1',
    'pandas==2.2.0',
    'rembg==2.0.66',
    'plyer==2.1.0',
    'tqdm==4.66.1'
]

setup(
    name='ImageUpscaler',
    version='3.2',
    packages=find_packages(),
    include_package_data=True,
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
            'imageUpscaler=imageUpscaler.run:main_cli',
            'imageUpscaler-analyze=imageUpscaler.run:analyze_image',
        ],
    },
    author='Aas1kk',
    author_email='workwithaa.sik@gmail.com',
    description='Advanced image processing and analysis package with AI-powered enhancement.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/aa-sikkkk/ImageUpscaler',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: OS Independent',
        'Topic :: Multimedia :: Graphics',
        'Topic :: Scientific/Engineering :: Image Processing',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
    ],
    python_requires='>=3.8',
    keywords='image-processing, upscaling, ai, computer-vision, deep-learning',
    project_urls={
        'Documentation': 'https://github.com/aa-sikkkk/ImageUpscaler#readme',
        'Source': 'https://github.com/aa-sikkkk/ImageUpscaler',
        'Tracker': 'https://github.com/aa-sikkkk/ImageUpscaler/issues',
    },
)