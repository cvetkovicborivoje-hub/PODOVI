#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI detekcija nameštaja na slikama
Koristi edge detection i complexity analysis
"""

import sys
from pathlib import Path
from PIL import Image, ImageFilter
import shutil

sys.stdout.reconfigure(encoding='utf-8')

print("="*80)
print("AI DETEKCIJA NAMEŠTAJA")
print("="*80)
print()

def has_furniture(img_path):
    """
    Detektuje da li slika ima nameštaj
    Slike sa nameštajem imaju:
    - Više edges (konture objekata)
    - Više različitih regiona
    - Manje uniformna distribucija boja
    """
    try:
        img = Image.open(img_path).convert('RGB')
        
        # Resize za brže procesiranje
        img = img.resize((300, 300))
        
        # 1. Edge detection
        edges = img.filter(ImageFilter.FIND_EDGES)
        edge_pixels = list(edges.getdata())
        edge_count = sum(1 for pixel in edge_pixels if sum(pixel) > 100)
        edge_ratio = edge_count / len(edge_pixels)
        
        # 2. Color uniformity
        pixels = list(img.getdata())
        unique_colors = len(set(pixels))
        color_ratio = unique_colors / len(pixels)
        
        # 3. Brightness variation
        brightness_values = [sum(p) / 3 for p in pixels]
        avg_brightness = sum(brightness_values) / len(brightness_values)
        brightness_variance = sum((b - avg_brightness) ** 2 for b in brightness_values) / len(brightness_values)
        
        # Decision logic:
        # Slike SA nameštajem:
        # - Više edges (edge_ratio > 0.3)
        # - Više različitih boja (color_ratio > 0.4)
        # - Veća varijansa (brightness_variance > 2000)
        
        furniture_score = 0
        
        if edge_ratio > 0.25:
            furniture_score += 1
        if color_ratio > 0.35:
            furniture_score += 1
        if brightness_variance > 1500:
            furniture_score += 1
        
        # Ako ima 2 ili više indikatora, verovatno ima nameštaj
        has_furn = furniture_score >= 2
        
        return {
            'has_furniture': has_furn,
            'edge_ratio': edge_ratio,
            'color_ratio': color_ratio,
            'brightness_variance': brightness_variance,
            'score': furniture_score
        }
    
    except Exception as e:
        return None

# Base path
base_path = Path("public/images/products/lvt/colors")

# Collect all products
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
    
    # Find all images (exclude main)
    all_images = sorted([img for img in product_path.glob("*.jpg") if img.stem != product_name])
    all_images += sorted([img for img in product_path.glob("*.png") if img.stem != product_name])
    
    if len(all_images) == 0:
        errors += 1
        continue
    
    if len(all_images) == 1:
        # Only one image
        swatch = all_images[0]
    else:
        # Analyze each image
        image_analysis = []
        for img_path in all_images:
            analysis = has_furniture(img_path)
            if analysis:
                image_analysis.append({
                    'path': img_path,
                    'name': img_path.name,
                    **analysis
                })
        
        if not image_analysis:
            swatch = all_images[0]
        else:
            # Select image WITHOUT furniture
            no_furniture = [img for img in image_analysis if not img['has_furniture']]
            
            if no_furniture:
                # Use first image without furniture
                swatch = no_furniture[0]['path']
            else:
                # All have furniture, use the one with lowest score
                swatch = min(image_analysis, key=lambda x: x['score'])['path']
    
    # Target main image
    main_image = product_path / f"{product_name}.jpg"
    
    # Copy swatch
    try:
        shutil.copy2(swatch, main_image)
        
        # Show detection result if available
        if len(all_images) > 1 and image_analysis:
            analysis_for_selected = next((a for a in image_analysis if a['path'] == swatch), None)
            if analysis_for_selected:
                print(f"[{idx}/{len(all_products)}] ✓ {product_name}: {swatch.name} (furn={analysis_for_selected['has_furniture']}, score={analysis_for_selected['score']})")
            else:
                print(f"[{idx}/{len(all_products)}] ✓ {product_name}: {swatch.name}")
        else:
            print(f"[{idx}/{len(all_products)}] ✓ {product_name}: {swatch.name}")
        
        replaced += 1
    except Exception as e:
        print(f"[{idx}/{len(all_products)}] ✗ {product_name}: {e}")
        errors += 1
    
    if idx % 50 == 0:
        print(f"\n--- {idx}/{len(all_products)} ---\n")

print("\n" + "="*80)
print("GOTOVO!")
print("="*80)
print(f"✅ Zamenjeno: {replaced}")
print(f"❌ Greške: {errors}")
print(f"📊 Ukupno: {len(all_products)}")
