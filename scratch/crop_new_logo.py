import os
from PIL import Image

def crop_logo_files():
    # Paths
    emblem_src = "C:/Users/mehru/.gemini/antigravity-ide/brain/866b7be1-d812-4254-b01a-ee2e24e7fcfd/media__1781893889890.png"
    wordmark_src = "C:/Users/mehru/.gemini/antigravity-ide/brain/866b7be1-d812-4254-b01a-ee2e24e7fcfd/media__1781893864553.png"
    
    # Crop Emblem
    if os.path.exists(emblem_src):
        im_emblem = Image.open(emblem_src)
        # Bounding box for the candlestick A emblem
        # left=210, top=40, right=700, bottom=450
        emblem_crop = im_emblem.crop((210, 40, 700, 450))
        emblem_crop.save("logo_icon.png", "PNG")
        print("Cropped and saved logo_icon.png")
    else:
        print(f"Emblem source not found: {emblem_src}")
        
    # Crop Wordmark
    if os.path.exists(wordmark_src):
        im_wordmark = Image.open(wordmark_src)
        # Bounding box for AUREON + line + subtitle
        # left=15, top=0, right=750, bottom=180
        wordmark_crop = im_wordmark.crop((15, 0, 750, 180))
        wordmark_crop.save("logo_title.png", "PNG")
        print("Cropped and saved logo_title.png")
        
        # Crop just the word AUREON
        word_crop = im_wordmark.crop((11, 0, 750, 95))
        word_crop.save("logo_word.png", "PNG")
        print("Cropped and saved logo_word.png")
    else:
        print(f"Wordmark source not found: {wordmark_src}")

if __name__ == "__main__":
    crop_logo_files()
