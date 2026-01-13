#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ISPRAVKA SLIKA - koristi MANJE slike (bez nameštaja)
"""

import os
import sys
from PIL import Image
import shutil

sys.stdout.reconfigure(encoding='utf-8')

print("="*80)
print("ISPRAVKA SLIKA - KORISTI MANJE (BEZ NAMEŠTAJA)")
print("="*80)
print()

BASE_DIR = "public/images/products/lvt/colors"

collections = [d for d in os.listdir(BASE_DIR) if os.path.isdir(os.path.join(BASE_DIR, d))]

total_fixed = 0

for collection in collections:
    collection_dir = os.path.join(BASE_DIR, collection)
    
    print(f"\n📁 {collection}:")
    
    items = os.listdir(collection_dir)
    color_folders = [item for item in items if os.path.isdir(os.path.join(collection_dir, item))]
    
    for color_folder in color_folders:
        folder_path = os.path.join(collection_dir, color_folder)
        main_image = os.path.join(collection_dir, f"{color_folder}.jpg")
        
        if not os.path.exists(main_image):
            continue
        
        # Get all images in folder
        folder_images = []
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                    img_path = os.path.join(root, file)
                    folder_images.append(img_path)
        
        if len(folder_images) < 2:
            continue
        
        try:
            # Get dimensions of all images
            image_data = []
            for img_path in folder_images:
                try:
                    with Image.open(img_path) as img:
                        width, height = img.size
                        area = width * height
                        image_data.append({
                            'path': img_path,
                            'width': width,
                            'height': height,
                            'area': area,
                            'name': os.path.basename(img_path)
                        })
                except:
                    pass
            
            if len(image_data) < 2:
                continue
            
            # Sort by area - SMALLEST first (that's WITHOUT furniture)
            image_data.sort(key=lambda x: x['area'])
            
            smallest = image_data[0]  # This is the one WITHOUT furniture
            largest = image_data[-1]  # This is the one WITH furniture
            
            # Get current main image size
            with Image.open(main_image) as main_img:
                main_area = main_img.width * main_img.height
            
            # Check if main image is the LARGE one (WITH furniture)
            # If so, replace with SMALL one (WITHOUT furniture)
            diff_to_small = abs(main_area - smallest['area'])
            diff_to_large = abs(main_area - largest['area'])
            
            # If closer to large, it's using the wrong image
            if diff_to_large < diff_to_small or main_area > smallest['area'] * 1.5:
                print(f"   🔄 {color_folder}: Zamenjujem sa malom slikom (bez nameštaja)")
                print(f"      Stara: {main_area//1000}k pixels")
                print(f"      Nova: {smallest['area']//1000}k pixels ({smallest['name']})")
                
                # Copy the SMALLEST (without furniture) to main
                shutil.copy2(smallest['path'], main_image)
                total_fixed += 1
            
        except Exception as e:
            print(f"   ✗ {color_folder}: {e}")
    
    print(f"   ✓ Završeno")

print("\n" + "="*80)
print("GOTOVO!")
print("="*80)
print(f"Ispravljeno slika: {total_fixed}")
