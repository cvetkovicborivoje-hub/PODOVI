#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Koristi PUNA imena iz ZIP fajlova bez traženja koda
"""

import json
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

# Load original names from ZIPs
with open("scripts/products_real_names_final.json", 'r', encoding='utf-8') as f:
    data = json.load(f)

products = data['products']

fixed_products = []

for product in products:
    sku = product['sku']
    name = product['name']
    
    # Extract 4-digit code from SKU
    code = sku[-4:] if sku else product['code']
    
    # Clean the name from ZIP file
    clean_name = name
    
    # Remove leading dash and spaces
    clean_name = re.sub(r'^[-\s]+', '', clean_name)
    
    # Remove "JPG XX dpi" prefix
    clean_name = re.sub(r'^JPG\s+\d+\s+dpi[-\s]*', '', clean_name, flags=re.IGNORECASE)
    
    # Remove "Creation XX" prefix
    clean_name = re.sub(r'^Creation\s+\d+\s+', '', clean_name, flags=re.IGNORECASE)
    
    # Remove "Sky View" suffix
    clean_name = re.sub(r'\s+Sky\s+View$', '', clean_name, flags=re.IGNORECASE)
    
    # Remove "VDC" and similar suffixes
    clean_name = re.sub(r'\s+[-_]\s*VDC.*$', '', clean_name, flags=re.IGNORECASE)
    clean_name = re.sub(r'\s+[-_]\s*RS\d+.*$', '', clean_name, flags=re.IGNORECASE)
    
    # Remove "500x500" and similar
    clean_name = re.sub(r'\s+\d+x\d+', '', clean_name, flags=re.IGNORECASE)
    
    # Remove file-related text
    clean_name = re.sub(r'\[\d+\]$', '', clean_name)
    
    # Remove trailing/leading dashes and underscores
    clean_name = clean_name.strip(' -_.')
    
    # Convert to uppercase and replace dashes/underscores with spaces
    clean_name = clean_name.replace('-', ' ').replace('_', ' ')
    clean_name = ' '.join(clean_name.split())  # Normalize whitespace
    clean_name = clean_name.upper()
    
    fixed_products.append({
        **product,
        'code': code,
        'name': clean_name
    })

# Save
output_path = "scripts/products_final_clean_names.json"
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump({
        "total": len(fixed_products),
        "products": fixed_products
    }, f, indent=2, ensure_ascii=False)

print(f"✓ Očišćeno {len(fixed_products)} proizvoda")
print(f"Sačuvano u: {output_path}")

# Show samples
print("\nPrimeri proizvoda:")
for i in range(min(20, len(fixed_products))):
    p = fixed_products[i]
    print(f"  {p['code']} {p['name']}")
