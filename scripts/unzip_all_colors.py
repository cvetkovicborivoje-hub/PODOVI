#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Raspakuj sve ZIP fajlove i organizuj slike
"""

import os
import sys
import zipfile
import shutil
import json
from pathlib import Path

# Fix encoding
sys.stdout.reconfigure(encoding='utf-8')

print("="*80)
print("RASPAKOVAVANJE SVIH ZIP FAJLOVA")
print("="*80)
print()

SOURCE_DIR = r"D:\PODOVI\SAJT\downloads\gerflor_dialog"
OUTPUT_DIR = r"D:\PODOVI\SAJT\public\images\products\lvt\colors"

# Ensure output dir exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Data structure for JSON
all_colors = []

total_zips = 0
total_extracted = 0
errors = []

# Go through each collection folder
for collection_slug in os.listdir(SOURCE_DIR):
    collection_path = os.path.join(SOURCE_DIR, collection_slug)
    
    if not os.path.isdir(collection_path):
        continue
    
    print(f"\n📁 {collection_slug}:")
    
    # Get all ZIPs in this collection
    zips = [f for f in os.listdir(collection_path) if f.endswith('.zip')]
    
    for zip_name in zips:
        total_zips += 1
        zip_path = os.path.join(collection_path, zip_name)
        
        # Extract color info from filename
        # e.g., "ballerina-41870347.zip" or "honey-oak-41870441.zip"
        color_slug = zip_name.replace('.zip', '')
        
        # Create output folder for this color
        color_output_dir = os.path.join(OUTPUT_DIR, collection_slug, color_slug)
        os.makedirs(color_output_dir, exist_ok=True)
        
        try:
            # Extract ZIP
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(color_output_dir)
            
            # Find main image (usually JPG or PNG)
            images = []
            for root, dirs, files in os.walk(color_output_dir):
                for file in files:
                    if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                        images.append(os.path.join(root, file))
            
            # Use first image as main
            main_image = images[0] if images else None
            
            # Copy main image to standardized location
            if main_image:
                ext = os.path.splitext(main_image)[1]
                standard_name = f"{color_slug}{ext}"
                standard_path = os.path.join(OUTPUT_DIR, collection_slug, standard_name)
                shutil.copy2(main_image, standard_path)
                
                # Relative path for website
                relative_path = f"/images/products/lvt/colors/{collection_slug}/{standard_name}"
            else:
                relative_path = None
            
            # Add to data
            all_colors.append({
                "collection": collection_slug,
                "color_slug": color_slug,
                "zip_name": zip_name,
                "image_url": relative_path,
                "image_count": len(images)
            })
            
            total_extracted += 1
            print(f"   ✅ {zip_name} → {len(images)} slika")
            
        except Exception as e:
            print(f"   ❌ {zip_name}: {e}")
            errors.append({
                "collection": collection_slug,
                "zip": zip_name,
                "error": str(e)
            })

print()
print("="*80)
print("ZAVRŠENO!")
print("="*80)
print(f"ZIP fajlova: {total_zips}")
print(f"Raspakovano: {total_extracted}")
print(f"Greške: {len(errors)}")
print()

# Save JSON
json_path = os.path.join(SOURCE_DIR, "extracted_colors.json")
with open(json_path, 'w', encoding='utf-8') as f:
    json.dump({
        "total": total_extracted,
        "colors": all_colors,
        "errors": errors
    }, f, indent=2, ensure_ascii=False)

print(f"JSON: {json_path}")
print()
print("Slike su u: " + OUTPUT_DIR)
