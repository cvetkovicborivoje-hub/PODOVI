#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Spaja prava imena sa svim proizvodima
"""

import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

print("="*80)
print("SPAJANJE PRAVIH IMENA SA SVIM PROIZVODIMA")
print("="*80)
print()

# Load real names (50 products)
with open("scripts/products_real_scraped_final.json", 'r', encoding='utf-8') as f:
    real_names_data = json.load(f)

real_names = {}
for product in real_names_data['products']:
    code = product['code']
    real_names[code] = product['real_name']

print(f"Učitao {len(real_names)} pravih imena")
print(f"Kodovi: {', '.join(sorted(real_names.keys())[:10])}...\n")

# Load all products (583 from extracted_colors.json)
with open("downloads/gerflor_dialog/extracted_colors.json", 'r', encoding='utf-8') as f:
    all_colors_data = json.load(f)

all_colors = all_colors_data['colors']
print(f"Ukupno proizvoda: {len(all_colors)}\n")

# Merge
updated = 0
not_found = []

for color in all_colors:
    # Extract code from zip_name or image_url
    # Example: "CREATION-30-0347-BALLERINA.zip" -> 0347
    # Example: "/images/products/lvt/colors/creation-30/ballerina-41890347/49041 - 0347 Ballerina .jpg" -> 0347
    
    import re
    
    # Extract code from color_slug
    # Format: "ballerina-41870347" -> last 4 digits = 0347
    # Format: "beige-41741712" -> last 4 digits = 1712
    if 'color_slug' in color and color['color_slug']:
        # Get last 4 digits
        match = re.search(r'(\d{4})$', color['color_slug'])
        if match:
            code = match.group(1)
        else:
            code = None
    else:
        code = None
    
    if code and code in real_names:
        color['real_name'] = real_names[code]
        updated += 1
    else:
        # Keep original name from zip or extract from image_url
        if code:
            not_found.append(code)
        # Extract name from image_url filename
        if 'image_url' in color and color['image_url']:
            filename = color['image_url'].split('/')[-1]
            # "49041 - 0347 Ballerina .jpg" -> "BALLERINA"
            parts = filename.split('-')
            if len(parts) >= 3:
                name_part = parts[2].split('.')[0].strip()
                color['real_name'] = name_part.upper()
            else:
                color['real_name'] = filename.split('.')[0].strip().upper()
        else:
            color['real_name'] = "UNKNOWN"

print(f"✓ Ažurirano: {updated} proizvoda")
print(f"✗ Nije pronađeno: {len(not_found)} proizvoda")
if not_found:
    print(f"  Kodovi koji nedostaju: {', '.join(sorted(set(not_found))[:20])}...\n")

# Save
output_path = "scripts/all_products_with_real_names.json"
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(all_colors, f, indent=2, ensure_ascii=False)

print(f"\n✅ Sačuvano u: {output_path}")
print(f"Ukupno proizvoda: {len(all_colors)}")
