import os
try:
    from PIL import Image
    print("Pillow is installed!")
except ImportError:
    print("Pillow is not installed. Installing it via pip...")
    import subprocess
    subprocess.run(["pip", "install", "Pillow"], check=True)
    from PIL import Image

def crop_emblem():
    logo_path = "logo.png"
    if not os.path.exists(logo_path):
        print(f"Error: {logo_path} not found!")
        return
        
    im = Image.open(logo_path)
    w, h = im.size
    print(f"Logo dimensions: {w}x{h}")
    
    # The circular icon is in the upper part.
    # Typically, the emblem center is around y = h * 0.32
    # Let's crop the top part. The circular emblem fits in a box from:
    # x = w * 0.22 to x = w * 0.78
    # y = h * 0.08 to y = h * 0.62
    # Let's define the bounding box for the emblem circle.
    # In the provided 800x800 image, let's make it a square crop:
    # left = 0, top = 0, right = w, bottom = int(h * 0.62)
    # Or let's crop a tight square around the circle:
    left = int(w * 0.22)
    top = int(h * 0.08)
    right = int(w * 0.78)
    bottom = int(h * 0.63)
    
    # Let's check dimensions of the crop
    crop_w = right - left
    crop_h = bottom - top
    print(f"Emblem crop box: {left}, {top}, {right}, {bottom} (size {crop_w}x{crop_h})")
    
    # Perform crop
    emblem = im.crop((left, top, right, bottom))
    emblem.save("logo_icon.png", "PNG")
    print("Saved logo_icon.png successfully!")

if __name__ == "__main__":
    crop_emblem()
