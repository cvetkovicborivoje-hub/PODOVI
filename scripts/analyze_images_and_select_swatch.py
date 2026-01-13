#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Analizira slike i bira PRAVU swatch sliku (bez nameštaja)
Koristi aspect ratio i dimenzije da detektuje swatch vs lifestyle
"""

import os
import sys
from pathlib import Path
from PIL import Image
import shutil

sys.stdout.reconfigure(encoding='utf-8')

print("="*80)
print("ANALIZA SLIKA - BIRANJE PRAVOG SWATCH-A")
print("="*80)
print()

def analyze_image(img_path):
    """Analizira sliku i vraća metrike"""
    try:
        img = Image.open(img_path)
        width, height = img.size
        aspect_ratio = width / height
        
        # Swatch slike su obično:
        # - Kvadratne ili skoro kvadratne (aspect ratio blizu 1.0)
        # - Manje dimenzije
        # - Uniformnija boja (manje detalja)
        
        return {
            'width': width,
            'height': height,
            'aspect_ratio': aspect_ratio,
            'pixels': width * height,
            'is_square': 0.9 <= aspect_ratio <= 1.1,  # Skoro kvadratna
            'path': img_path,
        }
    except Exception as e:
        return None

def select_swatch(images_info):
    """Bira swatch sliku iz liste slika"""
    if not images_info:
        return None
    
    # Filter out images that are too large (likely lifestyle)
    # Lifestyle slike su obično 1920x1080 ili slično
    # Swatch slike su obično 500x500 ili manje
    
    small_images = [img for img in images_info if img['pixels'] < 1000000]  # < 1M pixels
    
    if small_images:
        # Prefer square images
        square_images = [img for img in small_images if img['is_square']]
        if square_images:
            # Return smallest square image
            return min(square_images, key=lambda x: x['pixels'])
        else:
            # Return smallest image
            return min(small_images, key=lambda x: x['pixels'])
    else:
        # No small images, return smallest overall
        return min(images_info, key=lambda x: x['pixels'])

# Base path
base_path = Path("public/images/products/lvt/colors")

# Collect all product directories
all_products = []
for collection_dir in base_path.iterdir():
    if collection_dir.is_dir():
        for product_dir in collection_dir.iterdir():
            if product_dir.is_dir():
                all_products.append({
                    'collection': collection_dir.name,
                    'product': product_dir.name,
                    'path': product_dir
                })

print(f"Ukupno proizvoda: {len(all_products)}\n")

replaced = 0
skipped = 0
errors = 0

for idx, item in enumerate(all_products, 1):
    product_path = item['path']
    product_name = item['product']
    
    # Find all images in the folder (exclude main image)
    all_images = [img for img in product_path.glob("*.jpg") if img.stem != product_name]
    all_images += [img for img in product_path.glob("*.png") if img.stem != product_name]
    
    if len(all_images) < 2:
        # Only one image or no images
        if len(all_images) == 1:
            # Copy the only available image
            main_image = product_path / f"{product_name}.jpg"
            if not main_image.exists() or main_image.stat().st_size != all_images[0].stat().st_size:
                try:
                    shutil.copy2(all_images[0], main_image)
                    print(f"[{idx}/{len(all_products)}] ✓ {product_name}: Kopirano {all_images[0].name}")
                    replaced += 1
                except Exception as e:
                    print(f"[{idx}/{len(all_products)}] ✗ {product_name}: Greška - {e}")
                    errors += 1
            else:
                skipped += 1
        else:
            errors += 1
        continue
    
    # Analyze all images
    images_info = []
    for img_path in all_images:
        info = analyze_image(img_path)
        if info:
            images_info.append(info)
    
    if not images_info:
        print(f"[{idx}/{len(all_products)}] ✗ {product_name}: Ne mogu da analiziram slike")
        errors += 1
        continue
    
    # Select best swatch
    swatch = select_swatch(images_info)
    
    if not swatch:
        print(f"[{idx}/{len(all_products)}] ✗ {product_name}: Ne mogu da odaberem swatch")
        errors += 1
        continue
    
    # Target main image
    main_image = product_path / f"{product_name}.jpg"
    
    # Check if already correct
    if main_image.exists() and main_image.resolve() == Path(swatch['path']).resolve():
        skipped += 1
        continue
    
    # Copy swatch to main image
    try:
        shutil.copy2(swatch['path'], main_image)
        print(f"[{idx}/{len(all_products)}] ✓ {product_name}: {Path(swatch['path']).name} ({swatch['width']}x{swatch['height']}, ratio={swatch['aspect_ratio']:.2f})")
        replaced += 1
    except Exception as e:
        print(f"[{idx}/{len(all_products)}] ✗ {product_name}: Greška - {e}")
        errors += 1
    
    # Progress
    if idx % 100 == 0:
        print(f"\n--- {idx}/{len(all_products)} ---\n")

print("\n" + "="*80)
print("GOTOVO!")
print("="*80)
print(f"✅ Zamenjeno: {replaced}")
print(f"⏭️  Preskočeno: {skipped}")
print(f"❌ Greške: {errors}")
print(f"📊 Ukupno: {len(all_products)}")
