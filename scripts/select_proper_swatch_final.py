#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Finalno biranje PRAVIH SWATCH slika
Pravilo: PRVA slika = SWATCH, DRUGA slika = LIFESTYLE
"""

import os
import sys
from pathlib import Path
import shutil

sys.stdout.reconfigure(encoding='utf-8')

print("="*80)
print("FINALNO BIRANJE PRAVIH SWATCH SLIKA")
print("="*80)
print()

def is_lifestyle_image(filename):
    """Proverava da li je lifestyle slika (sa nameštajem)"""
    lower = filename.lower()
    lifestyle_keywords = [
        'sky-view', 'skyview', 'sky view',
        'room-scene', 'roomscene', 'room scene',
        'bedroom', 'kitchen', 'bathroom', 'office',
        'restaurant', 'chambre', 'scandinavian'
    ]
    return any(keyword in lower for keyword in lifestyle_keywords)

def is_swatch_image(filename):
    """Proverava da li je swatch slika"""
    # Swatch slike obično:
    # 1. Imaju samo kod u nazivu (npr. "49041 - 0347 Ballerina.jpg")
    # 2. NEMAJU lifestyle keywords
    # 3. NISU "JPG 72 dpi" sa "Creation" ili "Sky View"
    
    if is_lifestyle_image(filename):
        return False
    
    lower = filename.lower()
    
    # If has "72 dpi" but also has lifestyle keywords, it's lifestyle
    if '72 dpi' in lower or '72dpi' in lower:
        return False
    
    # If starts with 5 digits, it's likely a swatch
    import re
    if re.match(r'^\d{5}', filename):
        return True
    
    return True  # Default to swatch

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
    
    # Find all images (exclude main image)
    all_images = sorted([img for img in product_path.glob("*.jpg") if img.stem != product_name])
    all_images += sorted([img for img in product_path.glob("*.png") if img.stem != product_name])
    
    if len(all_images) == 0:
        errors += 1
        continue
    
    if len(all_images) == 1:
        # Only one image available
        swatch = all_images[0]
    else:
        # Multiple images - select swatch
        swatch_candidates = [img for img in all_images if is_swatch_image(img.name)]
        
        if swatch_candidates:
            # Use FIRST swatch candidate (usually the swatch is first in ZIP)
            swatch = swatch_candidates[0]
        else:
            # No swatch found, use first image
            swatch = all_images[0]
    
    # Target main image
    main_image = product_path / f"{product_name}.jpg"
    
    # Check if already correct
    if main_image.exists():
        try:
            if main_image.samefile(swatch):
                skipped += 1
                continue
        except:
            pass
    
    # Copy swatch to main image
    try:
        shutil.copy2(swatch, main_image)
        print(f"[{idx}/{len(all_products)}] ✓ {product_name}: {swatch.name}")
        replaced += 1
    except Exception as e:
        print(f"[{idx}/{len(all_products)}] ✗ {product_name}: {e}")
        errors += 1
    
    if idx % 100 == 0:
        print(f"\n--- {idx}/{len(all_products)} ---\n")

print("\n" + "="*80)
print("GOTOVO!")
print("="*80)
print(f"✅ Zamenjeno: {replaced}")
print(f"⏭️  Preskočeno: {skipped}")
print(f"❌ Greške: {errors}")
print(f"📊 Ukupno: {len(all_products)}")
