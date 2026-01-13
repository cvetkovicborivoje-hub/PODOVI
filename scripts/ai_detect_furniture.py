#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Koristi AI da detektuje da li slika ima nameštaj
Jednostavna metoda: računa broj različitih boja i complexity
"""

import sys
from pathlib import Path
from PIL import Image
import numpy as np
import shutil

sys.stdout.reconfigure(encoding='utf-8')

print("="*80)
print("AI DETEKCIJA NAMEŠTAJA NA SLIKAMA")
print("="*80)
print()

def calculate_image_complexity(img_path):
    """
    Računa kompleksnost slike
    Slike sa nameštajem imaju više detalja i boja
    Swatch slike su uniformnije
    """
    try:
        img = Image.open(img_path)
        
        # Convert to RGB
        img = img.convert('RGB')
        
        # Resize for faster processing
        img = img.resize((100, 100))
        
        # Convert to numpy array
        img_array = np.array(img)
        
        # Calculate metrics
        # 1. Number of unique colors
        pixels = img_array.reshape(-1, 3)
        unique_colors = len(np.unique(pixels, axis=0))
        
        # 2. Standard deviation (complexity)
        std_dev = np.std(img_array)
        
        # 3. Variance
        variance = np.var(img_array)
        
        # Swatch images typically have:
        # - Lower unique colors
        # - Lower std dev
        # - Lower variance
        
        # Score: lower = more likely swatch
        complexity_score = (unique_colors / 1000) + (std_dev / 100) + (variance / 10000)
        
        return {
            'unique_colors': unique_colors,
            'std_dev': std_dev,
            'variance': variance,
            'complexity_score': complexity_score,
            'is_swatch': complexity_score < 1.5  # Threshold
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
    
    if len(all_images) < 2:
        if len(all_images) == 1:
            # Only one image
            main_image = product_path / f"{product_name}.jpg"
            if not main_image.exists():
                shutil.copy2(all_images[0], main_image)
                replaced += 1
            else:
                skipped += 1
        else:
            errors += 1
        continue
    
    # Analyze all images
    image_scores = []
    for img_path in all_images:
        complexity = calculate_image_complexity(img_path)
        if complexity:
            image_scores.append({
                'path': img_path,
                'name': img_path.name,
                **complexity
            })
    
    if not image_scores:
        errors += 1
        continue
    
    # Sort by complexity (lowest first = swatch)
    image_scores.sort(key=lambda x: x['complexity_score'])
    
    # Select the image with LOWEST complexity (most uniform = swatch)
    swatch = image_scores[0]['path']
    
    # Target main image
    main_image = product_path / f"{product_name}.jpg"
    
    # Copy swatch to main
    try:
        shutil.copy2(swatch, main_image)
        score = image_scores[0]
        print(f"[{idx}/{len(all_products)}] ✓ {product_name}: {score['name']} (score={score['complexity_score']:.2f}, colors={score['unique_colors']}, std={score['std_dev']:.1f})")
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
print(f"⏭️  Preskočeno: {skipped}")
print(f"❌ Greške: {errors}")
print(f"📊 Ukupno: {len(all_products)}")
