import re
import json
import os
try:
    from PIL import Image
except ImportError:
    os.system("pip3 install Pillow")
    from PIL import Image
import colorsys

def get_vibrance(image_path):
    try:
        # Some unicode files might exist, ensure path is valid
        if not os.path.exists(image_path): 
            # Try to find it ignoring unicode stuff if possible, but let's just assume it exists
            pass
        if not os.path.exists(image_path):
            print(f"File not found: {image_path}")
            return -1
            
        img = Image.open(image_path).convert('RGB')
        img.thumbnail((50, 50))
        pixels = list(img.getdata())
        score = 0
        for r, g, b in pixels:
            h, s, v = colorsys.rgb_to_hsv(r/255.0, g/255.0, b/255.0)
            score += (s * v)
        return score / len(pixels)
    except Exception as e:
        print(f"Error: {e}")
        return -1

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

start_idx = content.find('const ROOMS = [')
end_idx = content.find('];', start_idx)
rooms_str = content[start_idx:end_idx+2]

def sort_images(match):
    images_str = match.group(1)
    try:
        images = json.loads(images_str)
        # Sort by vibrance
        images.sort(key=lambda x: get_vibrance(x), reverse=True)
        # Dump back to JSON, avoiding ascii escaping so unicode is preserved as raw chars if possible
        # Actually javascript had unicode escapes like \u4ef0, json.dumps will produce them if ensure_ascii=True
        # Let's keep ensure_ascii=False to write actual unicode chars, modern HTML is fine with it
        res = json.dumps(images, ensure_ascii=False)
        return 'images:' + res
    except Exception as e:
        print(f"Failed parsing: {images_str}, {e}")
        return match.group(0)

new_rooms_str = re.sub(r'images:\s*(\[.*?\])', sort_images, rooms_str)

new_content = content[:start_idx] + new_rooms_str + content[end_idx+2:]

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_content)
    
print("Images sorted by vibrance successfully!")
