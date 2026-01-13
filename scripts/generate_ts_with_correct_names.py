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
    
    # Generate product entry
    ts_content += f"""  {{
    id: '{collection}-{color_slug}',
    name: '{name}',
    code: '{code}',
    brand: 'gerflor',
    category: '{category}',
    subcategory: '{subcategory}',
    image: {{
      url: '{image_url}',
      alt: '{name}',
    }},
    description: 'Gerflor {collection.replace("-", " ").title()} - {name}',
    specifications: {{
      'Kolekcija': '{collection.replace("-", " ").title()}',
      'Šifra': '{code}',
      'Boja': '{name}',
    }},
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
