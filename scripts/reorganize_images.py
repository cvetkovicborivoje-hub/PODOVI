#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Reorganizuj slike - tekstura za grid, lifestyle za detail
"""

import os
import sys
import json
import shutil
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

print("="*80)
print("REORGANIZACIJA SLIKA - Tekstura + Lifestyle")
print("="*80)
print()

SOURCE_DIR = r"D:\PODOVI\SAJT\public\images\products\lvt\colors"
OUTPUT_DIR = r"D:\PODOVI\SAJT\public\images\products\lvt\colors-organized"

# Ensure output dir
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load existing colors data
json_path = r"D:\PODOVI\SAJT\downloads\gerflor_dialog\extracted_colors.json"
with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Procesovanje {len(data['colors'])} boja...")
print()

updated_colors = []
stats = {"texture_found": 0, "lifestyle_found": 0, "only_one": 0}

for color in data['colors']:
    collection = color['collection']
    color_slug = color['color_slug']
    
    # Find all images in source folder
    source_folder = os.path.join(SOURCE_DIR, collection, color_slug)
    
    if not os.path.exists(source_folder):
        print(f"⚠️  {collection}/{color_slug} - folder ne postoji")
        continue
    
    # Get all JPG/PNG images
    images = []
    for root, dirs, files in os.walk(source_folder):
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                full_path = os.path.join(root, file)
                size = os.path.getsize(full_path)
                images.append({
                    'path': full_path,
                    'name': file,
                    'size': size
                })
    
    if len(images) == 0:
        print(f"⚠️  {collection}/{color_slug} - nema slika")
        continue
    
    # Sort by size (smaller = texture, larger = lifestyle)
    images.sort(key=lambda x: x['size'])
    
    # Determine which is which based on filename keywords
    texture_img = None
    lifestyle_img = None
    
    # Keywords for identifying image types
    lifestyle_keywords = ['room scene', 'bedroom', 'office', 'chambre', 'dining', 'kitchen', 
                          'living', 'salle', 'interior', 'interieur']
    texture_keywords = ['sky view', 'vdc', 'texture', 'close', 'swatch', 'sample', 'emboss']
    
    if len(images) == 1:
        # Only one image - use it for both
        texture_img = images[0]
        lifestyle_img = images[0]
        stats['only_one'] += 1
    else:
        # Multiple images - use filename analysis
        for img in images:
            name_lower = img['name'].lower()
            
            # Check if it's a lifestyle image (room scene)
            is_lifestyle = any(keyword in name_lower for keyword in lifestyle_keywords)
            # Check if it's a texture (close-up)
            is_texture = any(keyword in name_lower for keyword in texture_keywords)
            
            if is_texture and not texture_img:
                texture_img = img
            elif is_lifestyle and not lifestyle_img:
                lifestyle_img = img
        
        # Fallback: if not found by keywords, use size
        if not texture_img:
            texture_img = images[0]  # Smallest
        if not lifestyle_img:
            lifestyle_img = images[-1]  # Largest
        
        # Make sure they're different
        if texture_img == lifestyle_img and len(images) > 1:
            # Use smallest for texture, largest for lifestyle
            texture_img = images[0]
            lifestyle_img = images[-1]
        
        stats['texture_found'] += 1
        stats['lifestyle_found'] += 1
    
    # Create organized folders
    collection_dir = os.path.join(OUTPUT_DIR, collection)
    os.makedirs(collection_dir, exist_ok=True)
    
    # Copy images with standardized names
    texture_ext = os.path.splitext(texture_img['path'])[1]
    lifestyle_ext = os.path.splitext(lifestyle_img['path'])[1]
    
    texture_new = f"{color_slug}-texture{texture_ext}"
    lifestyle_new = f"{color_slug}-lifestyle{lifestyle_ext}"
    
    texture_path = os.path.join(collection_dir, texture_new)
    lifestyle_path = os.path.join(collection_dir, lifestyle_new)
    
    shutil.copy2(texture_img['path'], texture_path)
    shutil.copy2(lifestyle_img['path'], lifestyle_path)
    
    # URLs for website
    texture_url = f"/images/products/lvt/colors-organized/{collection}/{texture_new}"
    lifestyle_url = f"/images/products/lvt/colors-organized/{collection}/{lifestyle_new}"
    
    updated_colors.append({
        **color,
        'texture_url': texture_url,
        'lifestyle_url': lifestyle_url,
        'texture_size': texture_img['size'],
        'lifestyle_size': lifestyle_img['size']
    })
    
    if (len(updated_colors) % 50) == 0:
        print(f"   Procesovano: {len(updated_colors)}...")

print()
print("="*80)
print("ZAVRŠENO!")
print("="*80)
print(f"Ukupno boja: {len(updated_colors)}")
print(f"Tekstura pronađena: {stats['texture_found']}")
print(f"Lifestyle pronađena: {stats['lifestyle_found']}")
print(f"Samo jedna slika: {stats['only_one']}")
print()

# Save updated JSON
output_json = r"D:\PODOVI\SAJT\public\data\lvt_colors_complete.json"

# Re-load to get code/name
with open(output_json, 'r', encoding='utf-8') as f:
    existing = json.load(f)

# Merge with existing (to keep code/name)
merged = []
for existing_color in existing['colors']:
    # Find matching in updated
    matching = next((u for u in updated_colors if u.get('slug') == existing_color.get('slug') or u.get('color_slug') == existing_color.get('slug')), None)
    if matching:
        merged.append({
            **existing_color,
            'texture_url': matching['texture_url'],
            'lifestyle_url': matching['lifestyle_url']
        })
    else:
        merged.append(existing_color)

# Save
with open(output_json, 'w', encoding='utf-8') as f:
    json.dump({
        "total": len(merged),
        "collections": existing['collections'],
        "colors": merged
    }, f, indent=2, ensure_ascii=False)

print(f"💾 JSON update-ovan: {output_json}")
print(f"📁 Slike organizovane u: {OUTPUT_DIR}")
print()
print("GOTOVO! ✅")
