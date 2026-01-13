#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Finalno spajanje SVIH imena - pravi prioritet:
1. Prava imena iz scraping-a (50)
2. Očiščena imena iz ZIP fajlova (583)
"""

import json
import sys
import re
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

print("="*80)
print("FINALNO SPAJANJE SVIH IMENA")
print("="*80)
print()

# 1. Load real scraped names (50)
with open("scripts/products_real_scraped_final.json", 'r', encoding='utf-8') as f:
    real_names_data = json.load(f)

real_names = {}
for product in real_names_data['products']:
    code = product['code']
    real_names[code] = product['real_name']

print(f"✓ Učitano {len(real_names)} pravih imena sa sajta")

# 2. Load all colors from extracted_colors.json
with open("downloads/gerflor_dialog/extracted_colors.json", 'r', encoding='utf-8') as f:
    colors_data = json.load(f)

all_colors = colors_data['colors']
print(f"✓ Učitano {len(all_colors)} boja\n")

# 3. Extract names from ZIP filenames
def extract_name_from_zip(color_slug, image_url):
    """Ekstraktuje ime iz ZIP foldera ili image URL-a"""
    # Try from image_url first
    if image_url:
        # Get the folder path
        # Example: /images/products/lvt/colors/creation-30/ballerina-41870347.jpg
        path_parts = image_url.split('/')
        
        if len(path_parts) > 2:
            folder_name = path_parts[-1].replace('.jpg', '').replace('.png', '')
            
            # Look for actual files in that folder
            base_path = Path(f"public{image_url}").parent
            
            if base_path.exists():
                # Find all images
                images = list(base_path.glob("*.jpg")) + list(base_path.glob("*.png"))
                
                if images:
                    # Use first image filename to extract name
                    filename = images[0].name
                    
                    # Extract from filename
                    # "49041 - 0347 Ballerina .jpg" -> "BALLERINA"
                    # "62346 - JPG 72 dpi-Backyard-Light-Beige-sky-view.jpg" -> "BACKYARD LIGHT BEIGE"
                    
                    # Remove file extension
                    name = filename.rsplit('.', 1)[0]
                    
                    # Remove leading numbers and dashes
                    name = re.sub(r'^\d+\s*-\s*', '', name)
                    
                    # Remove code if present (4 digits)
                    name = re.sub(r'^\d{4}\s*-?\s*', '', name)
                    
                    # Remove "JPG 72 dpi-" prefix
                    name = re.sub(r'^JPG\s+72\s+dpi-', '', name, flags=re.IGNORECASE)
                    
                    # Remove "RS" prefix with numbers
                    name = re.sub(r'^RS\d+_?', '', name, flags=re.IGNORECASE)
                    
                    # Remove "Creation XX -" prefix
                    name = re.sub(r'Creation\s+\d+\s+-?\s*', '', name, flags=re.IGNORECASE)
                    
                    # Remove Sky View suffix
                    name = re.sub(r'-?Sky\s+View$', '', name, flags=re.IGNORECASE)
                    name = re.sub(r'-?sky-view$', '', name, flags=re.IGNORECASE)
                    
                    # Remove Room scene suffix
                    name = re.sub(r'-?Room\s+scene$', '', name, flags=re.IGNORECASE)
                    name = re.sub(r'-?room-scene$', '', name, flags=re.IGNORECASE)
                    
                    # Remove _Creation suffix
                    name = re.sub(r'_Creation$', '', name, flags=re.IGNORECASE)
                    
                    # Replace dashes/underscores with spaces
                    name = name.replace('-', ' ').replace('_', ' ')
                    
                    # Clean up multiple spaces
                    name = ' '.join(name.split())
                    
                    return name.upper()
    
    # Fallback: use color_slug
    # "ballerina-41870347" -> "BALLERINA"
    name = re.sub(r'-\d+$', '', color_slug)
    return name.upper().replace('-', ' ')

# 4. Build final products
final_products = []

for color in all_colors:
    # Extract code from color_slug
    match = re.search(r'(\d{4})$', color['color_slug'])
    if match:
        code = match.group(1)
    else:
        code = None
    
    # Try to get real name first
    if code and code in real_names:
        name = real_names[code]
        source = "scraped"
    else:
        # Extract from ZIP filename
        name = extract_name_from_zip(color['color_slug'], color['image_url'])
        source = "extracted"
    
    final_products.append({
        "collection": color['collection'],
        "color_slug": color['color_slug'],
        "code": code or "Unknown",
        "name": name,
        "image_url": color['image_url'],
        "source": source
    })

# Statistics
scraped_count = len([p for p in final_products if p['source'] == 'scraped'])
extracted_count = len([p for p in final_products if p['source'] == 'extracted'])

print(f"✅ Ime sa sajta (scraped): {scraped_count}")
print(f"📦 Ime iz ZIP-a (extracted): {extracted_count}")
print(f"📊 Ukupno: {len(final_products)}\n")

# Save
output_path = "scripts/all_products_final_names.json"
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump({
        "total": len(final_products),
        "products": final_products
    }, f, indent=2, ensure_ascii=False)

print(f"✅ Sačuvano u: {output_path}")

# Show some examples
print("\nPrimeri imena:\n")
for i in range(min(20, len(final_products))):
    p = final_products[i]
    print(f"  {p['code']} {p['name']} ({p['source']})")
