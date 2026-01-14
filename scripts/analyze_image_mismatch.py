# -*- coding: utf-8 -*-
"""
Analyze mismatch between JSON URLs and actual folder structure
"""
import json
import sys
from pathlib import Path
from urllib.parse import unquote

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

base_images_path = Path('public/images/products/lvt/colors')
json_path = Path('public/data/lvt_colors_complete.json')

with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Focus on creation-40-clic as example
collection = 'creation-40-clic'
colors = [c for c in data['colors'] if c['collection'] == collection]

print(f"Analyzing {collection}: {len(colors)} colors\n")

# Get actual folders
collection_path = base_images_path / collection
if collection_path.exists():
    actual_folders = [f.name for f in collection_path.iterdir() if f.is_dir() and f.name not in ['pod', 'ilustracija']]
    print(f"Actual folders: {len(actual_folders)}")
    print(f"Sample folders: {sorted(actual_folders)[:10]}\n")
else:
    print(f"ERROR: Collection folder {collection} does not exist!")
    sys.exit(1)

# Analyze each color
mismatches = []

for color in colors[:10]:  # First 10 for analysis
    code = color['code']
    name = color['name']
    texture_url = color.get('texture_url', '')
    
    # Extract folder name from URL
    if texture_url:
        clean_url = texture_url.split('?')[0]
        if clean_url.startswith('/images/products/lvt/colors/'):
            rel_path = clean_url[len('/images/products/lvt/colors/'):]
            parts = rel_path.split('/')
            if len(parts) >= 2:
                folder_from_url = parts[1]  # collection/folder/...
                
                # What folder should exist?
                # Code-based: code-name (e.g., "0850-cedar-brown")
                # Name-based: name-slug
                
                print(f"Color: {code} {name}")
                print(f"  URL folder: {folder_from_url}")
                print(f"  URL: {texture_url[:100]}")
                
                # Check if folder exists
                expected_folders = [
                    folder_from_url,
                    f"{code}-{name.lower().replace(' ', '-')}" if code and code != 'Unknown' else None,
                    name.lower().replace(' ', '-'),
                ]
                expected_folders = [f for f in expected_folders if f]
                
                found = False
                for exp_folder in expected_folders:
                    folder_path = collection_path / exp_folder
                    if folder_path.exists():
                        print(f"  ✅ Folder exists: {exp_folder}")
                        found = True
                        break
                
                if not found:
                    print(f"  ❌ Folder NOT found: {folder_from_url}")
                    print(f"  Expected options: {expected_folders}")
                    mismatches.append({
                        'code': code,
                        'name': name,
                        'url_folder': folder_from_url,
                        'expected': expected_folders
                    })
                print()

print(f"\nMismatches found: {len(mismatches)}")
