#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generiše TypeScript kod za proizvode koje treba dodati u mock-data.ts
"""

import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

# Load products
with open("scripts/all_gerflor_products.json", 'r', encoding='utf-8') as f:
    data = json.load(f)

products = data['products']

# Specs by collection type (generic specs for LVT products)
def get_specs_for_collection(collection_slug):
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

# Generate TypeScript code
output_file = "lib/data/gerflor-products-generated.ts"

with open(output_file, 'w', encoding='utf-8') as f:
    f.write("import { Product } from '@/types';\n\n")
    f.write("// Auto-generated Gerflor products\n")
    f.write("export const gerflor_products: Product[] = [\n")
    
    for idx, product in enumerate(products):
        specs = get_specs_for_collection(product['collection_slug'])
        
        # Add installation type for clic/looselay
        if "clic" in product['collection_slug'].lower():
            specs.append({"key": "installation", "label": "Tip instalacije", "value": "Click sistem"})
        elif "looselay" in product['collection_slug'].lower():
            specs.append({"key": "installation", "label": "Tip instalacije", "value": "Loose lay"})
        else:
            specs.append({"key": "installation", "label": "Tip instalacije", "value": "Lepljenje"})
        
        # Add acoustic if applicable
        if "acoustic" in product['collection_slug'].lower():
            specs.insert(1, {"key": "acoustic", "label": "Akustična izolacija", "value": "Da"})
        
        f.write("  {\n")
        f.write(f"    id: '{product['id']}',\n")
        f.write(f"    name: '{product['name']}',\n")
        f.write(f"    slug: '{product['slug']}',\n")
        f.write(f"    sku: '{product['sku']}',\n")
        f.write(f"    categoryId: '{product['categoryId']}',\n")
        f.write(f"    brandId: '{product['brandId']}',\n")
        f.write(f"    shortDescription: '{product['shortDescription']}',\n")
        f.write(f"    description: `{product['description']}`,\n")
        f.write(f"    images: [\n")
        for img in product['images']:
            f.write(f"      {{\n")
            f.write(f"        id: '{img['id']}',\n")
            f.write(f"        url: '{img['url']}',\n")
            f.write(f"        alt: '{img['alt']}',\n")
            f.write(f"        isPrimary: {str(img['isPrimary']).lower()},\n")
            f.write(f"        order: {img['order']},\n")
            f.write(f"      }},\n")
        f.write(f"    ],\n")
        f.write(f"    specs: [\n")
        for spec in specs:
            f.write(f"      {{ key: '{spec['key']}', label: '{spec['label']}', value: '{spec['value']}' }},\n")
        f.write(f"    ],\n")
        f.write(f"    price: 3500,\n")
        f.write(f"    priceUnit: 'm²',\n")
        f.write(f"    inStock: {str(product['inStock']).lower()},\n")
        f.write(f"    featured: {str(product['featured']).lower()},\n")
        f.write(f"    createdAt: new Date('2024-01-01'),\n")
        f.write(f"    updatedAt: new Date('2024-01-01'),\n")
        f.write("  },\n")
    
    f.write("];\n")

print(f"✓ Generisano {len(products)} proizvoda u {output_file}")
