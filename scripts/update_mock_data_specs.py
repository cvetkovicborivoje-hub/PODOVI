#!/usr/bin/env python3
"""
Update mock-data.ts with specifications from extracted JSON
"""

import json
import re

# Load extracted specs
with open('scripts/lvt_specs_extracted.json', 'r', encoding='utf-8') as f:
    specs_data = json.load(f)

# Product ID mapping (folder-name -> product-id)
product_mapping = {
    'creation-30': '8',
    'creation-40': '9',
    'creation-40-clic': '10',
    'creation-40-clic-acoustic': '11',
    'creation-40-zen': '12',
    'creation-55': '13',
    'creation-55-clic': '14',
    'creation-55-clic-acoustic': '15',
    'creation-55-looselay': '16',
    'creation-55-looselay-acoustic': '17',
    'creation-55-zen': '18',
    'creation-70': '19',
    'creation-70-clic': '20',
    'creation-70-connect': '21',
    'creation-70-megaclic': '22',
    'creation-70-zen': '23',
    'creation-saga': '24',
    'creation-70-looselay': '25',
}

# Generate specs arrays for each product
def generate_specs_array(folder_name):
    """Generate TypeScript specs array from JSON data"""
    if folder_name not in specs_data:
        return None
    
    data = specs_data[folder_name]
    specs = []
    
    # Add thickness if available
    if data.get('thickness'):
        specs.append(f"      {{ key: 'thickness', label: 'Ukupna debljina', value: '{data['thickness']}' }}")
    
    # Add wear layer if available
    if data.get('wear_layer'):
        specs.append(f"      {{ key: 'wear_layer', label: 'Sloj habanja', value: '{data['wear_layer']}' }}")
    
    # Add format if available
    if data.get('format'):
        format_value = 'Plank' if data['format'] == 'plank' else 'Tile'
        specs.append(f"      {{ key: 'format', label: 'Format', value: '{format_value}' }}")
    
    # Add usage class if available
    if data.get('usage_class'):
        specs.append(f"      {{ key: 'usage_class', label: 'Klasa upotrebe', value: '{data['usage_class']}' }}")
    
    # Add fire classification if available
    if data.get('fire_class'):
        specs.append(f"      {{ key: 'fire_class', label: 'Protivpožarna klasifikacija', value: '{data['fire_class']}' }}")
    
    # Add acoustic if available (only if meaningful value)
    if data.get('acoustic') and data['acoustic'] not in ['2', '31074', '30174']:
        acoustic_val = data['acoustic']
        if acoustic_val == 'Yes':
            specs.append(f"      {{ key: 'acoustic', label: 'Akustična izolacija', value: 'Da' }}")
        elif 'dB' not in acoustic_val and acoustic_val.isdigit():
            specs.append(f"      {{ key: 'acoustic', label: 'Akustična izolacija', value: '{acoustic_val} dB' }}")
    
    # Add installation type
    if data.get('installation'):
        install_mapping = {
            'glue down': 'Lepljenje',
            'click system': 'Click sistem',
            'loose lay': 'Loose lay',
            'connect system': 'Connect sistem',
        }
        install_value = install_mapping.get(data['installation'], data['installation'])
        specs.append(f"      {{ key: 'installation', label: 'Tip instalacije', value: '{install_value}' }}")
    
    # Always add surface treatment for LVT
    specs.append(f"      {{ key: 'surface', label: 'Površinska obrada', value: 'Protecshield® PUR' }}")
    
    return ',\n'.join(specs) if specs else None

# Output to file instead of terminal to avoid encoding issues
output = []
output.append("// Generated specs for LVT products\n")
output.append("=" * 60 + "\n\n")

for folder_name, product_id in product_mapping.items():
    specs_array = generate_specs_array(folder_name)
    if specs_array:
        output.append(f"Product ID {product_id} ({folder_name}):\n")
        output.append("    specs: [\n")
        output.append(specs_array + "\n")
        output.append("    ],\n\n")
    else:
        output.append(f"Product ID {product_id} ({folder_name}): NO SPECS FOUND\n\n")

output.append("=" * 60 + "\n")

# Write to file
with open('scripts/lvt_specs_output.txt', 'w', encoding='utf-8') as f:
    f.write(''.join(output))

print("Success! Specs written to scripts/lvt_specs_output.txt")
