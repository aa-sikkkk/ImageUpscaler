# ImageUpscaler - The Easiest Way to Enhance Your Photos! 🚀

<p align="center">
 <img height="400" width="400" src="https://github.com/aa-sikkkk/ImageUpscaler/assets/152005759/0af66753-5e4a-4322-ac35-fade40b1656b">
</p>
<p align="center">
  <img src="https://img.shields.io/github/license/aa-sikkkk/ImageUpscaler" alt="License">
  <img src="https://img.shields.io/github/issues/aa-sikkkk/ImageUpscaler" alt="Issues">
  <img src="https://img.shields.io/github/stars/aa-sikkkk/ImageUpscaler" alt="Stars">
</p>

## 📸 What Can ImageUpscaler Do For You?

Imagine having a magic wand for your photos! ImageUpscaler can:

✨ **Make Small Photos Bigger**
- Turn tiny photos into large, clear images
- Perfect for printing or social media

🎨 **Add Beautiful Effects**
- Make photos look vintage
- Add soft edges
- Remove unwanted noise

👤 **Smart Features**
- Find faces in your photos
- Remove backgrounds
- Keep your photos looking natural

## 🎯 Let's Get Started - Step by Step!

### Step 1: Download ImageUpscaler
1. Click the green "Code" button on our [GitHub page](https://github.com/aa-sikkkk/ImageUpscaler)
2. Click "Download ZIP"
3. Unzip the file to a folder on your computer

### Step 2: Install ImageUpscaler
1. Open Command Prompt (Windows) or Terminal (Mac)
   - Windows: Press `Windows + R`, type `cmd`, press Enter
   - Mac: Press `Command + Space`, type `terminal`, press Enter

2. Copy and paste these commands (one at a time):
```bash
# Go to your ImageUpscaler folder
cd path/to/ImageUpscaler

# Install the tool
pip install -e .
```

### Step 3: Your First Photo Enhancement
1. Create two folders on your computer:
   - `my_photos` (for your original photos)
   - `enhanced_photos` (for the improved photos)

2. Put some photos in the `my_photos` folder

3. Run this command:
```bash
imageUpscaler process --input my_photos --output enhanced_photos
```

4. Check your `enhanced_photos` folder - your improved photos are there! 🎉

## 🎨 Try These Cool Features!

### 1. Make Photos Bigger
```bash
# Make photos 2 times bigger
imageUpscaler process --input my_photos --output enhanced_photos --upscale 2.0
```

Before and After:
```
[Small Photo] → [Big, Clear Photo]
```

### 2. Add Vintage Look
```bash
# Make photos look old and artistic
imageUpscaler process --input my_photos --output enhanced_photos --sepia
```

Before and After:
```
[Color Photo] → [Vintage Style Photo]
```

### 3. Remove Noise
```bash
# Make photos clearer
imageUpscaler process --input my_photos --output enhanced_photos --noise-reduction
```

Before and After:
```
[Grainy Photo] → [Clear Photo]
```

## ⚙️ Easy Settings

Create a file named `config.json` in your ImageUpscaler folder. Copy this example:

```json
{
    "input_directory": "my_photos",
    "output_directory": "enhanced_photos",
    "upscale_factor": 2.0,
    "noise_reduction": true,
    "compression_quality": 85
}
```

## 🎯 Common Tasks Made Easy

### Task 1: Enhance One Photo
```bash
# Replace 'family.jpg' with your photo name
imageUpscaler process --input family.jpg --output family_enhanced.jpg
```

### Task 2: Add Your Name to Photos
```bash
imageUpscaler process --input my_photos --output enhanced_photos \
    --watermark "© Your Name" \
    --watermark-position bottom-right
```

### Task 3: Save as Different Format
```bash
# Save as PNG (better quality)
imageUpscaler process --input my_photos --output enhanced_photos --format PNG
```

## 💡 Tips for Perfect Photos

1. **Start with One Photo**
   - Try one photo first
   - Make sure you like the result
   - Then try more photos

2. **Keep Your Originals**
   - Always keep a copy of your original photos
   - You can always try different settings

3. **Check Your Results**
   - Look at the enhanced photos
   - Make sure they look good
   - Try different settings if needed

## 🆘 Help! Something's Not Working

### Problem: "Command not found"
Solution: 
1. Make sure you're in the right folder
2. Try installing again: `pip install -e .`

### Problem: Photos look blurry
Solution: 
1. Try a smaller upscale (like 1.5 instead of 2.0)
2. Check if your original photo is clear

### Problem: It's taking too long
Solution: 
1. Try fewer photos at once
2. Close other programs
3. Make sure your computer has enough space

## 📚 Need More Help?

- Visit our [GitHub page](https://github.com/aa-sikkkk/ImageUpscaler)
- Check our [examples](https://github.com/aa-sikkkk/ImageUpscaler/examples)
- Join our [Discord community](https://discord.gg/imageupscaler)

## 🎯 Ready for More?

Once you're comfortable, try these:
- [Advanced Features](https://github.com/aa-sikkkk/ImageUpscaler/wiki/Advanced-Features)
- [GPU Speed Boost](https://github.com/aa-sikkkk/ImageUpscaler/wiki/GPU-Support)
- [Process Many Photos](https://github.com/aa-sikkkk/ImageUpscaler/wiki/Batch-Processing)

---

<p align="center">
  <img width="250" height="350" src="https://github.com/aa-sikkkk/ImageUpscaler/assets/152005759/6fd814dc-02ef-4147-a30e-bded623efae1">
</p>

`Happy Photo Enhancing! 🎨`
