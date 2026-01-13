#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pametno bira swatch slike (bez nameštaja) baziran na NAZIVU fajla
"""

import os
import shutil
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

print("="*80)
print("PAMETNO BIRANJE SWATCH SLIKA (BEZ NAMEŠTAJA)")
print("="*80)
print()

# Ključne reči za slike SA nameštajem (ne koristiti)
FURNITURE_KEYWORDS = [
    'sky-view', 'sky view', 'skyview',
    'room scene', 'room-scene', 'roomscene',
    'chambre', 'bedroom', 'office', 'restaurant',
    'bathroom', 'kitchen', 'hall',
    'scandinavian', 'emboss'
]

def has_furniture(filename):
    """Proverava da li naziv fajla sadrži ključne reči za nameštaj"""
    filename_lower = filename.lower()
    for keyword in FURNITURE_KEYWORDS:
        if keyword in filename_lower:
            return True
    return False

def is_swatch(filename):
    """Proverava da li je swatch (samo kod i ime, bez furniture keywords)"""
    # Swatch ima format: "XXXXX - 0XXX-ime.jpg" ili "XXXXX - 0XXX Ime .jpg"
    import re
    # Prioritet: Fajlovi koji počinju sa 5-cifrenim brojem
    if re.match(r'^\d{5}\s*-', filename):
        return True
    # Ili ne sadrži furniture keywords
    return not has_furniture(filename)

# Base path
base_path = Path("public/images/products/lvt/colors")

# Collect all product directories
all_collections = []
for collection_dir in base_path.iterdir():
    if collection_dir.is_dir():
        for product_dir in collection_dir.iterdir():
            if product_dir.is_dir():
                all_collections.append({
                    'collection': collection_dir.name,
                    'product': product_dir.name,
                    'path': product_dir
                })

print(f"Ukupno proizvoda: {len(all_collections)}\n")

# Process each product
replaced = 0
skipped = 0
errors = 0

for idx, item in enumerate(all_collections, 1):
    product_path = item['path']
    product_name = item['product']
    
    # Find all images in the extracted folder
    extracted_folder = product_path
    
    if not extracted_folder.exists():
        errors += 1
        continue
    
    # List all JPG/PNG files
    images = list(extracted_folder.glob("*.jpg")) + list(extracted_folder.glob("*.png"))
    
    if len(images) == 0:
        errors += 1
        continue
    
    # Find swatch (without furniture)
    swatch_candidates = [img for img in images if is_swatch(img.name)]
    
    if len(swatch_candidates) == 0:
        # No swatch found - use the first image (fallback)
        print(f"[{idx}/{len(all_collections)}] ⚠️  {product_name}: Nema swatch, koristim prvu sliku")
        swatch_image = images[0]
        skipped += 1
    elif len(swatch_candidates) == 1:
        swatch_image = swatch_candidates[0]
    else:
        # Multiple swatches - use the one with the simplest name (shortest)
        swatch_image = min(swatch_candidates, key=lambda x: len(x.name))
    
    # Target main image
    main_image = product_path / f"{product_name}.jpg"
    
    # Check if already correct
    if main_image.exists() and main_image.resolve() == swatch_image.resolve():
        # Already using the correct swatch
        skipped += 1
        continue
    
    # Copy swatch to main image
    try:
        shutil.copy2(swatch_image, main_image)
        print(f"[{idx}/{len(all_collections)}] ✓ {product_name}: {swatch_image.name}")
        replaced += 1
    except Exception as e:
        print(f"[{idx}/{len(all_collections)}] ✗ {product_name}: Greška - {e}")
        errors += 1
    
    # Progress
    if idx % 100 == 0:
        print(f"\n--- {idx}/{len(all_collections)} ---\n")

print("\n" + "="*80)
print("GOTOVO!")
print("="*80)
print(f"✅ Zamenjeno: {replaced}")
print(f"⏭️  Preskočeno: {skipped}")
print(f"❌ Greške: {errors}")
print(f"📊 Ukupno: {len(all_collections)}")
