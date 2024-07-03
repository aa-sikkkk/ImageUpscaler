import pyfiglet
from termcolor import colored

def display_banner():
    fig = pyfiglet.Figlet(font='slant')
    text = fig.renderText('ImageUpscaler')
    colored_text = colored(text, 'cyan', attrs=['bold'])
    print(colored_text)

def about():
    print("Welcome to ImageUpscaler")
    print('''Features:
          1. Image Upscaling: Increase the resolution of your images.
          2. Image Contrast Manipulation: Adjust the contrast to make your images pop.
          3. Image Color Saturation Adjustment: Enhance or reduce the color saturation.
          4. Deblurring & High Resolution Enhancement using REAL-ESRGAN: Improve clarity and detail.
          5. Image Format Conversion: Convert images to different formats.
          6. Watermarking: Add a custom watermark to your images.
          7. Cropping and Resizing: Adjust the dimensions of your images.
          8. Rotating and Flipping: Rotate or flip your images.
          9. Noise Reduction: Reduce noise for cleaner images.
          10. Histogram Equalization: Improve the overall appearance by adjusting the contrast.
          11. Batch Processing with Custom Settings per Image.
          12. Image Metadata Preservation.
          13. Automated Format Detection.
          14. Progress Logging.
          15. Advanced Filters: Sepia, Vignette, Artistic Filters.
          16. Face Detection and Enhancement.
          17. Dynamic Watermark Placement.
          18. Multiple Output Resolutions.
          19. Automatic Background Removal.
          20. Image Compression.
          21. Script Configuration File.
          22. Desktop Notifications.
          23. Image Analysis and Reporting.
          VERSION: 2.1.0''')
