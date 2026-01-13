#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generise TS fajl sa PRAVILNIM imenima
"""

import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

print("="*80)
print("GENERISANJE TS FAJLA SA PRAVILNIM IMENIMA")
print("="*80)
print()

# Load all products with correct names
with open("scripts/all_products_smart_names.json", 'r', encoding='utf-8') as f:
    data = json.load(f)

products = data['products']
print(f"Ukupno proizvoda: {len(products)}\n")

# Generate TS file
ts_content = """// Auto-generated from scripts/all_products_smart_names.json
// DO NOT EDIT MANUALLY

import { Product } from '@/types';

export const gerflor_products: Product[] = [
"""

for product in products:
    collection = product['collection']
    color_slug = product['color_slug']
    code = product['code']
    name = product['name']
    image_url = product['image_url']
    
    # Determine category and subcategory based on collection
    if 'clic' in collection or 'connect' in collection or 'megaclic' in collection:
        category = 'LVT/SPC klik sistem'
        subcategory = f'Gerflor {collection.replace("-", " ").title()}'
    elif 'looselay' in collection:
        category = 'LVT looselay'
        subcategory = f'Gerflor {collection.replace("-", " ").title()}'
    elif 'saga' in collection:
        category = 'LVT'
        subcategory = 'Gerflor Creation Saga2'
    elif 'zen' in collection:
        category = 'LVT/SPC klik sistem'
        subcategory = f'Gerflor {collection.replace("-", " ").title()}'
    else:
        category = 'LVT'
        subcategory = f'Gerflor {collection.replace("-", " ").title()}'
    
    # Generate product entry (PRAVILNI Product format)
    ts_content += f"""  {{
    id: '{collection}-{color_slug}',
    name: '{code} {name}',
    slug: '{collection}-{color_slug}',
    sku: '{code}',
    categoryId: '6',  // LVT category
    brandId: '6',  // Gerflor brand
    shortDescription: 'Gerflor {collection.replace("-", " ").title()} - {name}',
    description: 'Gerflor {collection.replace("-", " ").title()} - {name} (Šifra: {code})',
    images: [{{
      id: '{collection}-{color_slug}-img-1',
      url: '{image_url}',
      alt: '{name}',
      isPrimary: true,
      order: 1,
    }}],
    specs: [
      {{ key: 'collection', label: 'Kolekcija', value: '{collection.replace("-", " ").title()}' }},
      {{ key: 'code', label: 'Šifra', value: '{code}' }},
      {{ key: 'color', label: 'Boja', value: '{name}' }},
    ],
    inStock: true,
    featured: false,
    externalLink: 'https://www.gerflor-cee.com/products/{collection}',
    createdAt: new Date('2024-01-01'),
    updatedAt: new Date('2024-01-01'),
  }},
"""

ts_content += """];

export default gerflor_products;
"""

# Save
output_path = "lib/data/gerflor-products-generated.ts"
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(ts_content)

print(f"✅ TS fajl generisan: {output_path}")
print(f"📊 Broj proizvoda: {len(products)}")
print("\nGotovo!")
