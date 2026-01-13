#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Koristi već download-ovane ZIP fajlove da ekstrauje prava imena
"""

import json
import sys
import os
import re

sys.stdout.reconfigure(encoding='utf-8')

print("="*80)
print("EKSTRAKCIJA PRAVIH IMENA IZ ZIP FAJLOVA")
print("="*80)
print()

# Load download results koji već ima URL-ove i imena iz ZIP fajlova
with open("downloads/gerflor_dialog/download_results.json", 'r', encoding='utf-8') as f:
    download_data = json.load(f)

# Parse imena direktno iz URL-ova jer URL sadrži puno ime
# Format: .../creation-40-new-collection-0347-ballerina-41840347

all_products = []

for collection in download_data['collections']:
    for color in collection['colors']:
        url = color.get('url', '')
        if not url:
            continue
        
        # Parse URL
        url_parts = url.split('/')[-1]  # "creation-40-new-collection-0347-ballerina-41840347"
        
        # Remove collection slug
        collection_slug = collection['slug']
        url_clean = url_parts.replace(collection_slug, '').replace('-new-collection', '')
        url_clean = url_clean.strip('-')
        
        # Split parts
        parts = url_clean.split('-')
        
        # Find 4-digit code
        code = None
        code_idx = None
        for i, part in enumerate(parts):
            if re.match(r'^\d{4}$', part):
                code = part
                code_idx = i
                break
        
        # Find 8-digit SKU
        sku = None
        for part in parts:
            if re.match(r'^\d{8}$', part):
                sku = part
                break
        
        # Name is between code and SKU
        if code_idx is not None:
            name_parts = []
            for i in range(code_idx + 1, len(parts)):
                part = parts[i]
                if re.match(r'^\d{8}$', part):
                    break
                name_parts.append(part)
            
            name = ' '.join(name_parts).title() if name_parts else color['name'].title()
        else:
            name = color['name'].title()
        
        all_products.append({
            'collection': collection['name'],
            'collection_slug': collection_slug,
            'code': code or "Unknown",
            'name': name,
            'sku': sku,
            'url': url,
            'color_slug': color['name']
        })

# Save
output_path = "scripts/products_with_real_names.json"
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump({
        "total": len(all_products),
        "products": all_products
    }, f, indent=2, ensure_ascii=False)

print(f"✓ Ekstrahovano {len(all_products)} proizvoda")
print(f"Sačuvano u: {output_path}")

# Show samples
print("\nPrimeri:")
for i in range(min(10, len(all_products))):
    p = all_products[i]
    print(f"  {p['code']} {p['name']} ({p['collection']})")
