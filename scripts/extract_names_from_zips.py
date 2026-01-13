#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ekstrakt PRAVA imena iz slika u ZIP fajlovima
"""

import os
import sys
import zipfile
import re
import json

sys.stdout.reconfigure(encoding='utf-8')

print("="*80)
print("EKSTRAKCIJA PRAVIH IMENA IZ ZIP FAJLOVA")
print("="*80)
print()

BASE_DIR = "downloads/gerflor_dialog"

all_products = []

# Collection mapping
collection_names = {
    "creation-30": "Gerflor Creation 30",
    "creation-40": "Gerflor Creation 40",
    "creation-40-clic": "Gerflor Creation 40 Clic",
    "creation-40-clic-acoustic": "Gerflor Creation 40 Clic Acoustic",
    "creation-40-zen": "Gerflor Creation 40 Zen",
    "creation-55": "Gerflor Creation 55",
    "creation-55-clic": "Gerflor Creation 55 Clic",
    "creation-55-clic-acoustic": "Gerflor Creation 55 Clic Acoustic",
    "creation-55-looselay": "Gerflor Creation 55 Looselay",
    "creation-55-looselay-acoustic": "Gerflor Creation 55 Looselay Acoustic",
    "creation-55-zen": "Gerflor Creation 55 Zen",
    "creation-70": "Gerflor Creation 70",
    "creation-70-clic": "Gerflor Creation 70 Clic",
    "creation-70-connect": "Gerflor Creation 70 Connect",
    "creation-70-looselay": "Gerflor Creation 70 Looselay",
    "creation-70-megaclic": "Gerflor Creation 70 Megaclic",
    "creation-70-zen": "Gerflor Creation 70 Zen",
    "creation-saga2": "Gerflor Creation Saga²",
}

# Go through each collection folder
collections = [d for d in os.listdir(BASE_DIR) if os.path.isdir(os.path.join(BASE_DIR, d))]

for collection_slug in collections:
    collection_dir = os.path.join(BASE_DIR, collection_slug)
    
    print(f"\n📁 {collection_names.get(collection_slug, collection_slug)}:")
    
    # Get all ZIPs
    zips = [f for f in os.listdir(collection_dir) if f.endswith('.zip')]
    
    for zip_name in zips:
        zip_path = os.path.join(collection_dir, zip_name)
        color_slug = zip_name.replace('.zip', '')
        
        try:
            with zipfile.ZipFile(zip_path, 'r') as z:
                # Get all image files
                image_files = [f for f in z.namelist() if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
                
                if not image_files:
                    continue
                
                # Parse name from FIRST image file name
                # Format: "49041 - 0347 Ballerina .jpg"
                first_image = image_files[0]
                basename = os.path.splitext(first_image)[0]  # Remove extension
                
                # Try to extract code and name
                # Pattern: "digits - 4digit name"
                match = re.search(r'(\d{4})\s+(.+?)(?:\s*\.)?$', basename)
                
                if match:
                    code = match.group(1)
                    name = match.group(2).strip()
                else:
                    # Fallback - try to find 4-digit code anywhere
                    code_match = re.search(r'\b(\d{4})\b', basename)
                    code = code_match.group(1) if code_match else "Unknown"
                    
                    # Name is everything after the code
                    if code != "Unknown":
                        name_part = basename.split(code, 1)[-1]
                        name = name_part.strip(' -._')
                    else:
                        name = color_slug.title()
                
                # Extract SKU from color_slug
                sku_match = re.search(r'(\d{8})', color_slug)
                sku = sku_match.group(1) if sku_match else None
                
                all_products.append({
                    'collection': collection_names.get(collection_slug, collection_slug),
                    'collection_slug': collection_slug,
                    'code': code,
                    'name': name.upper(),
                    'sku': sku,
                    'color_slug': color_slug,
                    'image_url': f"/images/products/lvt/colors/{collection_slug}/{color_slug}.jpg"
                })
                
                print(f"   ✓ {code} {name}")
        
        except Exception as e:
            print(f"   ✗ {zip_name}: {e}")

# Save
output_path = "scripts/products_real_names_final.json"
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump({
        "total": len(all_products),
        "products": all_products
    }, f, indent=2, ensure_ascii=False)

print("\n" + "="*80)
print("GOTOVO!")
print("="*80)
print(f"Ekstrahovano: {len(all_products)} proizvoda")
print(f"Sačuvano u: {output_path}")
