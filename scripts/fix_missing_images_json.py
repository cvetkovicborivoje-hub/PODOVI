# -*- coding: utf-8 -*-
"""
Fix JSON URLs to match actual folder structure
Focus on products that actually have folders but wrong URLs
"""
import json
import sys
from pathlib import Path
from urllib.parse import unquote

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

base_images_path = Path('public/images/products/lvt/colors')
json_path = Path('public/data/lvt_colors_complete.json')

# Load JSON
with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Total colors: {len(data['colors'])}\n")

fixed_count = 0
still_missing = []

for color in data['colors']:
    collection = color['collection']
    code = color['code']
    name = color['name']
    
    collection_path = base_images_path / collection
    if not collection_path.exists():
        continue
    
    # Find actual folder for this product
    # Try different folder name patterns
    possible_folders = []
    
    if code and code != 'Unknown':
        # Try code-name format
        name_slug = name.lower().replace(' ', '-').replace('/', '-')
        possible_folders.append(f"{code}-{name_slug}")
        # Try just code
        possible_folders.append(code)
    
    # Try name-based
    name_slug = name.lower().replace(' ', '-').replace('/', '-')
    possible_folders.append(name_slug)
    
    # Find actual folder
    actual_folder = None
    for folder_name in possible_folders:
        folder_path = collection_path / folder_name
        if folder_path.exists() and folder_path.is_dir():
            actual_folder = folder_name
            break
    
    if not actual_folder:
        # Check if it's in URL
        texture_url = color.get('texture_url', '')
        if texture_url:
            clean_url = texture_url.split('?')[0]
            if clean_url.startswith('/images/products/lvt/colors/'):
                rel_path = clean_url[len('/images/products/lvt/colors/'):]
                parts = rel_path.split('/')
                if len(parts) >= 2:
                    url_folder = parts[1]
                    folder_path = collection_path / url_folder
                    if folder_path.exists():
                        actual_folder = url_folder
    
    if not actual_folder:
        still_missing.append({
            'collection': collection,
            'code': code,
            'name': name
        })
        continue
    
    # Found folder - check what images exist
    folder_path = collection_path / actual_folder
    
    pod_images = list((folder_path / 'pod').glob('*.jpg')) if (folder_path / 'pod').exists() else []
    ilustracija_images = list((folder_path / 'ilustracija').glob('*.jpg')) if (folder_path / 'ilustracija').exists() else []
    
    # Update URLs if images exist
    if pod_images:
        pod_image = pod_images[0].name
        # URL encode the filename
        from urllib.parse import quote
        pod_url = f"/images/products/lvt/colors/{collection}/{actual_folder}/pod/{quote(pod_image)}?v=9"
        
        if color.get('texture_url') != pod_url:
            color['texture_url'] = pod_url
            color['image_url'] = pod_url
            fixed_count += 1
    
    if ilustracija_images:
        ilustracija_image = ilustracija_images[0].name
        from urllib.parse import quote
        ilustracija_url = f"/images/products/lvt/colors/{collection}/{actual_folder}/ilustracija/{quote(ilustracija_image)}?v=9"
        
        if color.get('lifestyle_url') != ilustracija_url:
            color['lifestyle_url'] = ilustracija_url
            fixed_count += 1

print(f"Fixed {fixed_count} URLs")
print(f"Still missing: {len(still_missing)}")

# Save updated JSON
if fixed_count > 0:
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"\n✅ Updated JSON saved")
