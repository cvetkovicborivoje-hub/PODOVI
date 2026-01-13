#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generiše SVE proizvode iz extracted_colors.json sa rekonstruisanim URL-ovima
"""

import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

print("="*80)
print("GENERISANJE SVIH PROIZVODA")
print("="*80)
print()

# Load extracted colors (contains all 583 colors with images)
with open("downloads/gerflor_dialog/extracted_colors.json", 'r', encoding='utf-8') as f:
    extracted_data = json.load(f)

# Collection name mapping
collection_name_map = {
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

# URL mapping for collections
collection_url_map = {
    "creation-30": "creation-30-new-collection",
    "creation-40": "creation-40-new-collection",
    "creation-40-clic": "creation-40-clic-new-collection",
    "creation-40-clic-acoustic": "creation-40-clic-acoustic-new-collection",
    "creation-40-zen": "creation-40-zen",
    "creation-55": "creation-55-new-collection",
    "creation-55-clic": "creation-55-clic-new-collection",
    "creation-55-clic-acoustic": "creation-55-clic-acoustic-new-collection",
    "creation-55-looselay": "creation-55-looselay",
    "creation-55-looselay-acoustic": "creation-55-looselay-acoustic",
    "creation-55-zen": "creation-55-zen",
    "creation-70": "creation-70-new-collection",
    "creation-70-clic": "creation-70-clic-5mm-new-collection",
    "creation-70-connect": "creation-70-connect",
    "creation-70-looselay": "new-2025-creation-70-looselay",
    "creation-70-megaclic": "creation-70-megaclic",
    "creation-70-zen": "creation-70-zen",
    "creation-saga2": "creation-saga2",
}

all_products = []

for color in extracted_data['colors']:
    collection_slug = color['collection']
    color_slug = color['color_slug']  # e.g., "ballerina-41870347"
    image_url = color['image_url']
    
    # Parse color_slug to extract: name and SKU
    # Example: "ballerina-41870347"
    parts = color_slug.split('-')
    
    # Last part is usually SKU (8 digits)
    sku = None
    sku_idx = None
    for i in range(len(parts) - 1, -1, -1):
        if re.match(r'^\d{8}$', parts[i]):
            sku = parts[i]
            sku_idx = i
            break
    
    # Extract 4-digit code from SKU (e.g., "0347" from "41870347")
    code = None
    if sku and len(sku) == 8:
        code = sku[4:]  # Last 4 digits
    
    # Name is everything before SKU
    if sku_idx is not None:
        name_parts = parts[:sku_idx]
        name = ' '.join(name_parts).upper()
    else:
        name = color_slug.upper()
    
    # Reconstruct URL
    # Format: https://www.gerflor-cee.com/products/{collection-url}-{code}-{name-slug}-{sku}
    collection_url_part = collection_url_map.get(collection_slug, collection_slug)
    
    # Create name slug (lowercase, dashes)
    name_slug = '-'.join([p.lower() for p in name_parts]) if sku_idx else color_slug
    
    # Build URL
    if code and sku:
        url = f"https://www.gerflor-cee.com/products/{collection_url_part}-{code}-{name_slug}-{sku}"
    else:
        url = f"https://www.gerflor-cee.com/products/{collection_url_part}-{color_slug}"
    
    product = {
        "id": f"gerflor-{collection_slug}-{color_slug}",
        "name": f"{collection_name_map.get(collection_slug, collection_slug.title())} {code} {name}",
        "slug": f"gerflor-{collection_slug}-{color_slug}",
        "sku": sku or "Unknown",
        "categoryId": "6",  # LVT category
        "brandId": "6",  # Gerflor brand
        "collection": collection_name_map.get(collection_slug, collection_slug.title()),
        "collection_slug": collection_slug,
        "code": code or "Unknown",
        "color_name": name,
        "shortDescription": f"{name} iz {collection_name_map.get(collection_slug, collection_slug)} kolekcije",
        "description": f"Gerflor {name} - Premium vinil pod iz {collection_name_map.get(collection_slug, collection_slug)} kolekcije. Luksuzni dizajn sa autentičnim izgledom i vrhunskom otpornošću.",
        "images": [
            {
                "id": f"{color_slug}-1",
                "url": image_url,
                "alt": f"{collection_name_map.get(collection_slug, collection_slug)} {name}",
                "isPrimary": True,
                "order": 1,
            }
        ],
        "url": url,
        "inStock": True,
        "featured": False,
    }
    
    all_products.append(product)

# Save results
output_path = "scripts/all_gerflor_products.json"
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

# Statistics by collection
collections_count = {}
for product in all_products:
    collection = product['collection']
    collections_count[collection] = collections_count.get(collection, 0) + 1

print("Po kolekcijama:")
for collection, count in sorted(collections_count.items()):
    print(f"  {collection}: {count}")
