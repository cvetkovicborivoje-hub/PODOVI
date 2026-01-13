#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generiše TypeScript fajl sa PRAVIM imenima
"""

import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

# Load fixed names
with open("scripts/products_fixed_names.json", 'r', encoding='utf-8') as f:
    data = json.load(f)

products = data['products']

# Specs by collection
def get_specs(collection_slug):
    if "30" in collection_slug:
        return [
            {"key": "thickness", "label": "Ukupna debljina", "value": "2mm"},
            {"key": "wear_layer", "label": "Sloj habanja", "value": "0.30mm"},
            {"key": "format", "label": "Format", "value": "Ploča"},
            {"key": "dimension", "label": "Dimenzije", "value": "18.4 cm x 121.9 cm"},
            {"key": "usage_class", "label": "Klasa upotrebe", "value": "23-31"},
        ]
    elif "40" in collection_slug:
        return [
            {"key": "thickness", "label": "Ukupna debljina", "value": "2mm"},
            {"key": "wear_layer", "label": "Sloj habanja", "value": "0.40mm"},
            {"key": "format", "label": "Format", "value": "Ploča"},
            {"key": "dimension", "label": "Dimenzije", "value": "18.4 cm x 121.9 cm"},
            {"key": "usage_class", "label": "Klasa upotrebe", "value": "23-32"},
        ]
    elif "55" in collection_slug:
        return [
            {"key": "thickness", "label": "Ukupna debljina", "value": "2.5mm"},
            {"key": "wear_layer", "label": "Sloj habanja", "value": "0.55mm"},
            {"key": "format", "label": "Format", "value": "Ploča"},
            {"key": "dimension", "label": "Dimenzije", "value": "18.4 cm x 121.9 cm"},
            {"key": "usage_class", "label": "Klasa upotrebe", "value": "23-33/42"},
        ]
    elif "70" in collection_slug:
        return [
            {"key": "thickness", "label": "Ukupna debljina", "value": "2.5mm"},
            {"key": "wear_layer", "label": "Sloj habanja", "value": "0.70mm"},
            {"key": "format", "label": "Format", "value": "Ploča"},
            {"key": "dimension", "label": "Dimenzije", "value": "18.4 cm x 121.9 cm"},
            {"key": "usage_class", "label": "Klasa upotrebe", "value": "34-43"},
        ]
    else:
        return [
            {"key": "format", "label": "Format", "value": "Ploča"},
            {"key": "surface", "label": "Površinska obrada", "value": "Protecshield® PUR"},
        ]

output_file = "lib/data/gerflor-products-generated.ts"

with open(output_file, 'w', encoding='utf-8') as f:
    f.write("import { Product } from '@/types';\n\n")
    f.write("// Auto-generated Gerflor products with REAL names\n")
    f.write("export const gerflor_products: Product[] = [\n")
    
    for product in products:
        specs = get_specs(product['collection_slug'])
        
        # Add installation type
        if "clic" in product['collection_slug'].lower():
            specs.append({"key": "installation", "label": "Tip instalacije", "value": "Click sistem"})
        elif "looselay" in product['collection_slug'].lower():
            specs.append({"key": "installation", "label": "Tip instalacije", "value": "Loose lay"})
        else:
            specs.append({"key": "installation", "label": "Tip instalacije", "value": "Lepljenje"})
        
        # Add acoustic if applicable
        if "acoustic" in product['collection_slug'].lower():
            specs.insert(1, {"key": "acoustic", "label": "Akustična izolacija", "value": "Da"})
        
        # Build full product name
        full_name = f"{product['collection']} {product['code']} {product['name']}"
        slug = f"gerflor-{product['collection_slug']}-{product['color_slug']}"
        
        f.write("  {\n")
        f.write(f"    id: '{slug}',\n")
        f.write(f"    name: '{full_name}',\n")
        f.write(f"    slug: '{slug}',\n")
        f.write(f"    sku: '{product['sku']}',\n")
        f.write(f"    categoryId: '6',\n")
        f.write(f"    brandId: '6',\n")
        f.write(f"    shortDescription: '{product['name']} iz {product['collection']} kolekcije',\n")
        f.write(f"    description: `Gerflor {product['name']} - Premium vinil pod iz {product['collection']} kolekcije. Luksuzni dizajn sa autentičnim izgledom i vrhunskom otpornošću.`,\n")
        f.write(f"    images: [\n")
        f.write(f"      {{\n")
        f.write(f"        id: '{product['color_slug']}-1',\n")
        f.write(f"        url: '{product['image_url']}',\n")
        f.write(f"        alt: '{full_name}',\n")
        f.write(f"        isPrimary: true,\n")
        f.write(f"        order: 1,\n")
        f.write(f"      }},\n")
        f.write(f"    ],\n")
        f.write(f"    specs: [\n")
        for spec in specs:
            f.write(f"      {{ key: '{spec['key']}', label: '{spec['label']}', value: '{spec['value']}' }},\n")
        f.write(f"    ],\n")
        f.write(f"    price: 3500,\n")
        f.write(f"    priceUnit: 'm²',\n")
        f.write(f"    inStock: true,\n")
        f.write(f"    featured: false,\n")
        f.write(f"    createdAt: new Date('2024-01-01'),\n")
        f.write(f"    updatedAt: new Date('2024-01-01'),\n")
        f.write("  },\n")
    
    f.write("];\n")

print(f"✓ Generisano {len(products)} proizvoda u {output_file}")
print("\nPrimeri proizvoda:")
for i in range(min(10, len(products))):
    p = products[i]
    print(f"  {p['collection']} {p['code']} {p['name']}")
