#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Popravlja nazive koristeći SKU za ekstrakciju koda
"""

import json
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

# Load existing data
with open("scripts/products_real_names_final.json", 'r', encoding='utf-8') as f:
    data = json.load(f)

products = data['products']

fixed_products = []

for product in products:
    sku = product['sku']
    name = product['name']
    
    # Extract 4-digit code from SKU (last 4 digits)
    if sku:
        code = sku[-4:]
    else:
        code = product['code']
    
    # Try to find this code in the name and extract the real name after it
    # Pattern: look for "0347 Something" in name
    real_name = None
    
    # Try to find pattern "0XXX Name" where 0XXX is our code
    match = re.search(rf'{code}\s+(.+)', name, re.IGNORECASE)
    if match:
        real_name = match.group(1).strip()
    else:
        # Try to find code with dash: "0XXX-name" or "0XXX - name"
        match = re.search(rf'{code}[\s-]+(.+)', name, re.IGNORECASE)
        if match:
            real_name = match.group(1).strip()
    
    # Clean up real_name
    if real_name:
        # Remove "JPG 72 dpi-" prefix
        real_name = re.sub(r'^JPG\s+\d+\s+dpi[-\s]*', '', real_name, flags=re.IGNORECASE)
        # Remove "Creation" prefix if followed by code
        real_name = re.sub(r'^Creation\s+\d+\s+', '', real_name, flags=re.IGNORECASE)
        # Remove "Sky View" suffix
        real_name = re.sub(r'\s+Sky\s+View$', '', real_name, flags=re.IGNORECASE)
        # Remove VDC suffix
        real_name = re.sub(r'\s+[-_]\s*VDC.*$', '', real_name, flags=re.IGNORECASE)
        # Remove trailing dashes and underscores
        real_name = real_name.strip(' -_')
        # Convert to title case
        real_name = real_name.title()
    else:
        # Fallback to original name but clean it
        real_name = product['color_slug'].split('-')[0].title()
    
    fixed_products.append({
        **product,
        'code': code,
        'name': real_name.upper()
    })

# Save
output_path = "scripts/products_fixed_names.json"
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump({
        "total": len(fixed_products),
        "products": fixed_products
    }, f, indent=2, ensure_ascii=False)

print(f"✓ Popravljeno {len(fixed_products)} proizvoda")
print(f"Sačuvano u: {output_path}")

# Show samples
print("\nPrimeri:")
for i in range(min(20, len(fixed_products))):
    p = fixed_products[i]
    print(f"  {p['code']} {p['name']}")
