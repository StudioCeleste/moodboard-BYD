import os
import json
import re

base_dir = "NEW MOOD"
html_file = "moodboard-yang-wang.html"

def get_images(folder_name):
    path = os.path.join(base_dir, folder_name)
    if not os.path.exists(path):
        return []
    valid_exts = {".jpg", ".jpeg", ".png", ".webp"}
    images = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if os.path.splitext(file)[1].lower() in valid_exts:
                rel_path = os.path.relpath(os.path.join(root, file), start=".")
                images.append(rel_path.replace("\\", "/"))
    return sorted(images)

rooms_map = [
  {"name": "Overview", "folder": "00_OVERVIEW"},
  {"name": "Scène 01", "folder": "01_SCENE"},
  {"name": "Scène 02", "folder": "02_SCENE"},
  {"name": "Scène 03", "folder": "03_SCENE"},
  {"name": "Scène 04", "folder": "04_SCENE"},
  {"name": "Scène 05", "folder": "05_SCENE"},
  {"name": "Scène 06", "folder": "06_SCENE"},
  {"name": "Scène 07", "folder": "07_SCENE"},
  {"name": "Scène 08", "folder": "08_SCENE"},
]

with open(html_file, "r", encoding="utf-8") as f:
    content = f.read()

lines = content.split('\n')
in_rooms = False
new_lines = []
for line in lines:
    if "const ROOMS =" in line:
        in_rooms = True
        new_lines.append(line)
        continue
    
    if in_rooms:
        if line.strip() == "];":
            in_rooms = False
            new_lines.append(line)
            continue
            
        match = re.search(r'name:"([^"]+)"', line)
        if match:
            name = match.group(1)
            folder = next((r["folder"] for r in rooms_map if r["name"] == name), None)
            if folder:
                images = get_images(folder)
                images_json = json.dumps(images)
                # using lambda to avoid escape sequence issues
                line = re.sub(r'images:\[.*?\]', lambda m: f'images:{images_json}', line)
    
    new_lines.append(line)

with open(html_file, "w", encoding="utf-8") as f:
    f.write('\n'.join(new_lines))

print("Updated HTML with new images.")
