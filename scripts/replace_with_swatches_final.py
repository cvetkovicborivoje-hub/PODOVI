#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Zamenjuje slike sa nameštajem sa SWATCHEVIMA (male slike)
Sigurno koristi MANJU sliku iz svakog ZIP-a
"""

import os
import sys
import zipfile
import shutil
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8')

print("="*80)
print("ZAMENA SLIKA - KORISTIMO SWATCHEVE (MALE SLIKE)")
print("="*80)
print()

BASE_DIR = "downloads/gerflor_dialog"
OUTPUT_DIR = "public/images/products/lvt/colors"

collections = [d for d in os.listdir(BASE_DIR) if os.path.isdir(os.path.join(BASE_DIR, d))]

total_replaced = 0

for collection_slug in collections:
    collection_dir = os.path.join(BASE_DIR, collection_slug)
    
    print(f"\n📁 {collection_slug}:")
    
    # Get all ZIPs
    zips = [f for f in os.listdir(collection_dir) if f.endswith('.zip')]
    
    for zip_name in zips:
        zip_path = os.path.join(collection_dir, zip_name)
        color_slug = zip_name.replace('.zip', '')
        
        main_image_path = os.path.join(OUTPUT_DIR, collection_slug, f"{color_slug}.jpg")
        
        try:
            with zipfile.ZipFile(zip_path, 'r') as z:
                # Get all image files
                image_files = [f for f in z.namelist() if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
                
                if len(image_files) < 1:
                    continue
                
                # Extract all images to temp and find the SMALLEST one
                temp_dir = f"temp_{color_slug}"
                os.makedirs(temp_dir, exist_ok=True)
                
                image_data = []
                for img_file in image_files:
                    z.extract(img_file, temp_dir)
                    img_path = os.path.join(temp_dir, img_file)
                    
                    try:
                        with Image.open(img_path) as img:
                            width, height = img.size
                            area = width * height
                            image_data.append({
                                'path': img_path,
                                'area': area,
                                'name': img_file
                            })
                    except:
                        pass
                
                if len(image_data) > 0:
                    # Sort by area - SMALLEST first (that's the swatch WITHOUT furniture)
                    image_data.sort(key=lambda x: x['area'])
                    smallest = image_data[0]
                    
                    # Copy the SMALLEST image as the main image
                    print(f"   🔄 {color_slug}: Koristim {smallest['name']} ({smallest['area']//1000}k px)")
                    shutil.copy2(smallest['path'], main_image_path)
                    total_replaced += 1
                
                # Clean up temp
                shutil.rmtree(temp_dir)
        
        except Exception as e:
            print(f"   ✗ {zip_name}: {e}")

print("\n" + "="*80)
print("GOTOVO!")
print("="*80)
print(f"Zamenjeno slika: {total_replaced}")
