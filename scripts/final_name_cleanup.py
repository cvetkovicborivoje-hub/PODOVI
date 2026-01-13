#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Finalno čišćenje imena
"""

import json
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

with open("scripts/products_final_clean_names.json", 'r', encoding='utf-8') as f:
    data = json.load(f)

products = data['products']

final_products = []

for product in products:
    name = product['name']
    code = product['code']
    
    # Remove code if it's at the beginning (duplicate)
    name = re.sub(rf'^{code}\s+', '', name)
    
    # Remove any 4-5 digit numbers at start
    name = re.sub(r'^\d{4,5}\s+', '', name)
    
    # Remove "RS" + numbers
    name = re.sub(r'RS\d+\s*', '', name)
    
    # Remove "JPG" related
    name = re.sub(r'JPG.*?DPI\s*', '', name, flags=re.IGNORECASE)
    
    # Remove "Sky View"
    name = re.sub(r'\s*SKY\s*VIEW\s*', '', name, flags=re.IGNORECASE)
    
    # Remove VDC and similar
    name = re.sub(r'\s*VDC.*', '', name, flags=re.IGNORECASE)
    
    # Remove numbers in brackets
    name = re.sub(r'\s*\(\d+\)', '', name)
    name = re.sub(r'\s*\[\d+\]', '', name)
    
    # Remove "Creation" word
    name = re.sub(r'CREATION\s+', '', name, flags=re.IGNORECASE)
    
    # Clean multiple spaces
    name = ' '.join(name.split())
    
    # Remove trailing/leading special chars
    name = name.strip(' -_.')
    
    final_products.append({
        **product,
        'name': name
    })

# Save
output_path = "scripts/products_ultra_clean.json"
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump({
        "total": len(final_products),
        "products": final_products
    }, f, indent=2, ensure_ascii=False)

print(f"✓ Finalno očišćeno {len(final_products)} proizvoda")
print(f"Sačuvano u: {output_path}")

print("\nPrimeri proizvoda:")
for i in range(min(30, len(final_products))):
    p = final_products[i]
    print(f"  {p['code']} {p['name']}")
