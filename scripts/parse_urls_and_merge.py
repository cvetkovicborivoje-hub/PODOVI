#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Parsira URL-ove i spaja sa slikama iz extracted_colors.json
"""

import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

print("="*80)
print("PARSIRANJE URL-OVA I SPAJANJE SA SLIKAMA")
print("="*80)
print()

# Load download results (contains URLs)
with open("downloads/gerflor_dialog/download_results.json", 'r', encoding='utf-8') as f:
    download_data = json.load(f)

# Load extracted colors (contains image paths)
with open("downloads/gerflor_dialog/extracted_colors.json", 'r', encoding='utf-8') as f:
    extracted_data = json.load(f)

# Create lookup dict for images by color_slug
image_lookup = {}
for color in extracted_data['colors']:
    collection = color['collection']
    color_slug = color['color_slug']
    image_url = color['image_url']
    
    key = f"{collection}/{color_slug}"
    image_lookup[key] = {
        "image_url": image_url,
        "image_count": color.get('image_count', 0)
    }

print(f"Učitano {len(image_lookup)} slika iz extracted_colors.json\n")

# Process all colors from download_results
all_products = []

for collection in download_data['collections']:
    collection_name = collection['name']
    collection_slug = collection['slug']
    
    print(f"📁 {collection_name}:")
    
    for color in collection['colors']:
        url = color.get('url', '')
        if not url:
            continue
        
        # Parse URL to extract: code and name
        # Example: /products/creation-40-new-collection-0347-ballerina-41840347
        url_parts = url.split('/')[-1]  # "creation-40-new-collection-0347-ballerina-41840347"
        
        # Remove collection slug from URL
        url_without_collection = url_parts.replace(collection_slug, '').replace('-new-collection', '')
        url_without_collection = url_without_collection.strip('-')
        
        # Now we have: "0347-ballerina-41840347"
        # Split by '-'
        parts = url_without_collection.split('-')
        
        # Find 4-digit code (e.g., "0347")
        code = None
        code_idx = None
        for i, part in enumerate(parts):
            if re.match(r'^\d{4}$', part):
                code = part
                code_idx = i
                break
        
        # Find 8-digit SKU (e.g., "41840347")
        sku = None
        for part in parts:
            if re.match(r'^\d{8}$', part):
                sku = part
                break
        
        # Everything between code and SKU is the name
        if code_idx is not None:
            name_parts = []
            for i in range(code_idx + 1, len(parts)):
                part = parts[i]
                # Stop if we hit SKU
                if re.match(r'^\d{8}$', part):
                    break
                name_parts.append(part)
            
            name = ' '.join(name_parts).upper() if name_parts else color['name'].upper()
        else:
            name = color['name'].upper()
        
        # Get image from lookup
        image_key = f"{collection_slug}/{color['name']}"
        image_data = image_lookup.get(image_key, {})
        image_url = image_data.get('image_url', None)
        
        # If no image found, try without collection prefix in key
        if not image_url:
            # Try just the color slug
            for key, img_data in image_lookup.items():
                if key.endswith(color['name']):
                    image_url = img_data['image_url']
                    break
        
        product = {
            "collection": collection_name,
            "collection_slug": collection_slug,
            "code": code or "Unknown",
            "name": name,
            "sku": sku,
            "url": url,
            "image_url": image_url,
            "color_slug": color['name']
        }
        
        all_products.append(product)
    
    print(f"   ✓ {len(collection['colors'])} boja\n")

# Save results
output_path = "scripts/all_products_final.json"
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump({
        "total": len(all_products),
        "products": all_products
    }, f, indent=2, ensure_ascii=False)

print("="*80)
print("GOTOVO!")
print("="*80)
print(f"Ukupno proizvoda: {len(all_products)}")
print(f"Sačuvano u: {output_path}")
print()

# Statistics
with_images = sum(1 for p in all_products if p.get('image_url'))
with_code = sum(1 for p in all_products if p['code'] != 'Unknown')
with_sku = sum(1 for p in all_products if p.get('sku'))

print(f"Sa slikama: {with_images}/{len(all_products)}")
print(f"Sa kodom: {with_code}/{len(all_products)}")
print(f"Sa SKU: {with_sku}/{len(all_products)}")
