import sys
import os 
cur_file_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.dirname(cur_file_path))
import cv2
import os
import json
from pathlib import Path
from paths import image_proc_dir, tagged_image_dir

# Directory containing images
image_dir = Path(image_proc_dir)
json_dir = Path(tagged_image_dir)

# Make sure the directory for json exists
json_dir.mkdir(exist_ok=True)

# Define the categories mapped to keyboard keys
categories = {
    '1': 'close to tree',
    '2': 'tree but not closer',
    '3': 'no tree'
}

def tag_image(image_path):
    # Load the image
    image = cv2.imread(str(image_path))
    cv2.imshow('Image', image)
    print(f"Tagging image: {image_path.name}")
    print("Press '1' for 'close to tree', '2' for 'tree but not closer', '3' for 'no tree', 'q' to quit")
    
    while True:
        key = cv2.waitKey(0) & 0xFF  # Wait for a key press
        if chr(key) in categories:
            return categories[chr(key)]
        elif chr(key) == 'q':
            print("Exiting...")
            return None

def save_tag(image_path, category):
    tag_path = json_dir / (image_path.stem + '.json')
    with open(tag_path, 'w') as f:
        json.dump({'image_name': image_path.name, 'category': category}, f)

# Main loop for tagging images
for image_file in image_dir.glob('*.jpg'):
    json_file = json_dir / (image_file.stem + '.json')
    
    if not json_file.exists():  # Only tag images that haven't been tagged
        category = tag_image(image_file)
        if category is None:
            break  # Exit if 'q' is pressed
        save_tag(image_file, category)

cv2.destroyAllWindows()