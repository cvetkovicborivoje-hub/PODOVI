#!/usr/bin/env python3
"""
Update all LVT products in mock-data.ts with extracted specifications
"""

import json
import re

# Load extracted specs
with open('scripts/lvt_specs_extracted.json', 'r', encoding='utf-8') as f:
    specs_data = json.load(f)

# Load current mock-data.ts
with open('lib/data/mock-data.ts', 'r', encoding='utf-8') as f:
    mock_data = f.read()

# Product mapping: folder-name -> (product-id, product-slug)
product_mapping = {
    'creation-30': ('8', 'gerflor-creation-30'),
    'creation-40': ('9', 'gerflor-creation-40'),
    'creation-40-clic': ('10', 'gerflor-creation-40-clic'),
    'creation-40-clic-acoustic': ('11', 'gerflor-creation-40-clic-acoustic'),
    'creation-40-zen': ('12', 'gerflor-creation-40-zen'),
    'creation-55': ('13', 'gerflor-creation-55'),
    'creation-55-clic': ('14', 'gerflor-creation-55-clic'),
    'creation-55-clic-acoustic': ('15', 'gerflor-creation-55-clic-acoustic'),
    'creation-55-looselay': ('16', 'gerflor-creation-55-looselay'),
    'creation-55-looselay-acoustic': ('17', 'gerflor-creation-55-looselay-acoustic'),
    'creation-55-zen': ('18', 'gerflor-creation-55-zen'),
    'creation-70': ('19', 'gerflor-creation-70'),
    'creation-70-clic': ('20', 'gerflor-creation-70-clic'),
    'creation-70-connect': ('21', 'gerflor-creation-70-connect'),
    'creation-70-megaclic': ('22', 'gerflor-creation-70-megaclic'),
    'creation-70-zen': ('23', 'gerflor-creation-70-zen'),
    'creation-saga': ('24', 'gerflor-creation-saga'),
    'creation-70-looselay': ('25', 'gerflor-creation-70-looselay'),
}

def generate_specs_ts(folder_name):
    """Generate TypeScript specs array"""
    if folder_name not in specs_data:
        return None
    
    data = specs_data[folder_name]
    specs = []
    
    if data.get('thickness'):
        specs.append(f"      {{ key: 'thickness', label: 'Ukupna debljina', value: '{data['thickness']}' }},")
    
    if data.get('wear_layer'):
        wear = data['wear_layer'].replace(',', '.')
        specs.append(f"      {{ key: 'wear_layer', label: 'Sloj habanja', value: '{wear}' }},")
    
    if data.get('format'):
        format_value = 'Planka' if data['format'] == 'plank' else 'Pločica'
        specs.append(f"      {{ key: 'format', label: 'Format', value: '{format_value}' }},")
    
    if data.get('usage_class'):
        specs.append(f"      {{ key: 'usage_class', label: 'Klasa upotrebe', value: '{data['usage_class']}' }},")
    
    if data.get('fire_class'):
        specs.append(f"      {{ key: 'fire_class', label: 'Protivpožarna klasifikacija', value: '{data['fire_class']}' }},")
    
    if data.get('acoustic') and data['acoustic'] not in ['2', '31074', '30174']:
        acoustic_val = data['acoustic']
        if acoustic_val == 'Yes':
            specs.append(f"      {{ key: 'acoustic', label: 'Akustična izolacija', value: 'Da' }},")
        elif 'dB' not in str(acoustic_val) and str(acoustic_val).isdigit():
            specs.append(f"      {{ key: 'acoustic', label: 'Akustična izolacija', value: '{acoustic_val} dB' }},")
    
    if data.get('installation'):
        install_mapping = {
            'glue down': 'Lepljenje',
            'click system': 'Click sistem',
            'loose lay': 'Loose lay',
            'connect system': 'Connect sistem',
        }
        install_value = install_mapping.get(data['installation'], data['installation'])
        specs.append(f"      {{ key: 'installation', label: 'Tip instalacije', value: '{install_value}' }},")
    
    specs.append(f"      {{ key: 'surface', label: 'Površinska obrada', value: 'Protecshield® PUR' }},")
    
    return '\n'.join(specs)

# Update each product
updated_count = 0
for folder_name, (product_id, slug) in product_mapping.items():
    # Find the product in mock-data.ts
    pattern = rf"(  {{\n    id: '{product_id}',\n    name: '[^']+',\n    slug: '{slug}'[^}}]+specs: \[)([^\]]+)(\],)"
    
    match = re.search(pattern, mock_data, re.DOTALL)
    
    if match:
        new_specs = generate_specs_ts(folder_name)
        if new_specs:
            # Replace old specs with new specs
            replacement = f"{match.group(1)}\n{new_specs}\n    {match.group(3)}"
            mock_data = mock_data[:match.start()] + replacement + mock_data[match.end():]
            updated_count += 1
            print(f"Updated: {slug}")
        else:
            print(f"No specs data for: {slug}")
    else:
        print(f"NOT FOUND in file: {slug} (id: {product_id})")

# Write updated mock-data.ts
with open('lib/data/mock-data.ts', 'w', encoding='utf-8') as f:
    f.write(mock_data)

print(f"\nTotal updated: {updated_count} / {len(product_mapping)} products")
