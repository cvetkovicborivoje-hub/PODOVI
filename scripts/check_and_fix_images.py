#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Proverava slike i zamenjuje ako ima nameštaj
Logika: koristi manju sliku (swatch) umesto velike (sa nameštajem)
"""

import os
import sys
from PIL import Image
import shutil

sys.stdout.reconfigure(encoding='utf-8')

print("="*80)
print("PROVERA I ZAMENA SLIKA")
print("="*80)
print()

BASE_DIR = "public/images/products/lvt/colors"

# Get all collections
collections = [d for d in os.listdir(BASE_DIR) if os.path.isdir(os.path.join(BASE_DIR, d))]

total_checked = 0
total_replaced = 0
errors = []

for collection in collections:
    collection_dir = os.path.join(BASE_DIR, collection)
    
    print(f"\n📁 {collection}:")
    
    # Get all color folders
    items = os.listdir(collection_dir)
    color_folders = [item for item in items if os.path.isdir(os.path.join(collection_dir, item))]
    
    for color_folder in color_folders:
        folder_path = os.path.join(collection_dir, color_folder)
        main_image = os.path.join(collection_dir, f"{color_folder}.jpg")
        
        # Check if main image exists
        if not os.path.exists(main_image):
            print(f"   ⚠️  {color_folder}: Nema glavnu sliku")
            continue
        
        total_checked += 1
        
        # Get all images in folder
        folder_images = []
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                    img_path = os.path.join(root, file)
                    folder_images.append(img_path)
        
        if len(folder_images) == 0:
            continue
        elif len(folder_images) == 1:
            # Only one image, use it
            continue
        else:
            # Multiple images - find the swatch (smaller one)
            try:
                # Get sizes of all images
                image_sizes = []
                for img_path in folder_images:
                    try:
                        with Image.open(img_path) as img:
                            width, height = img.size
                            file_size = os.path.getsize(img_path)
                            image_sizes.append({
                                'path': img_path,
                                'width': width,
                                'height': height,
                                'file_size': file_size,
                                'area': width * height
                            })
                    except Exception as e:
                        print(f"   ⚠️  {color_folder}: Ne mogu da pročitam {os.path.basename(img_path)}")
                
                if len(image_sizes) < 2:
                    continue
                
                # Sort by area (smallest first - that's the swatch without furniture)
                image_sizes.sort(key=lambda x: x['area'])
                
                smallest = image_sizes[0]
                largest = image_sizes[-1]
                
                # Check if current main image is the largest (with furniture)
                with Image.open(main_image) as main_img:
                    main_width, main_height = main_img.size
                    main_area = main_width * main_height
                
                # If main image is closer to largest than smallest, replace it
                diff_to_smallest = abs(main_area - smallest['area'])
                diff_to_largest = abs(main_area - largest['area'])
                
                if diff_to_largest < diff_to_smallest:
                    # Main image is the large one (with furniture), replace with small one
                    print(f"   🔄 {color_folder}: Zamenjujem sliku sa nameštajem")
                    shutil.copy2(smallest['path'], main_image)
                    total_replaced += 1
                else:
                    # Already using small image
                    pass
                
            except Exception as e:
                print(f"   ✗ {color_folder}: Greška - {e}")
                errors.append({'folder': color_folder, 'error': str(e)})
    
    print(f"   ✓ Provereno")

print("\n" + "="*80)
print("GOTOVO!")
print("="*80)
print(f"Ukupno provereno: {total_checked}")
print(f"Zamenjeno: {total_replaced}")
print(f"Greške: {len(errors)}")
