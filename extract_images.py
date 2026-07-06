import re
import base64
import os

html_path = "/Users/celeste/Downloads/yangwang_moodboard_espaces_V3.html"
images_dir = "/Users/celeste/Downloads/images"
os.makedirs(images_dir, exist_ok=True)

with open(html_path, "r", encoding="utf-8") as f:
    content = f.read()

def replacer(match):
    global counter
    b64_data = match.group(1)
    img_data = base64.b64decode(b64_data)
    filename = f"scene_{counter}.webp"
    filepath = os.path.join(images_dir, filename)
    with open(filepath, "wb") as img_file:
        img_file.write(img_data)
    
    counter += 1
    return f"url('images/{filename}')"

counter = 1
# match url('data:image/webp;base64,...')
new_content, num_subs = re.subn(r"url\('data:image/webp;base64,([^']+)'\)", replacer, content)

print(f"Extracted {num_subs} images.")

with open(html_path, "w", encoding="utf-8") as f:
    f.write(new_content)

print("HTML updated.")
