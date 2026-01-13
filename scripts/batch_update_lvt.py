#!/usr/bin/env python3
import json
import re

# Load specs
with open('scripts/lvt_specs_extracted.json', 'r', encoding='utf-8') as f:
    specs_data = json.load(f)

# Load mock-data.ts
with open('lib/data/mock-data.ts', 'r', encoding='utf-8') as f:
    content = f.read()

# Product ID to folder mapping
products = {
    '10': ('creation-40-clic', 'Creation 40 Clic LVT sa click sistemom za brzu ugradnju'),
    '11': ('creation-40-clic-acoustic', 'Creation 40 Clic Acoustic LVT sa click sistemom i zvučnom izolacijom'),
    '12': ('creation-40-zen', 'Creation 40 Zen LVT sa teksturiranim površinama'),
    '13': ('creation-55', 'Creation 55 LVT sa 0.55mm slojem habanja'),
    '14': ('creation-55-clic', 'Creation 55 Clic LVT sa click sistemom'),
    '15': ('creation-55-clic-acoustic', 'Creation 55 Clic Acoustic LVT sa click sistemom i akustikom'),
    '16': ('creation-55-looselay', 'Creation 55 Looselay LVT sa loose lay instalacijom'),
    '17': ('creation-55-looselay-acoustic', 'Creation 55 Looselay Acoustic LVT sa loose lay i akustikom'),
    '18': ('creation-55-zen', 'Creation 55 Zen LVT sa teksturiranim površinama'),
    '19': ('creation-70', 'Creation 70 LVT sa 0.70mm slojem habanja'),
    '20': ('creation-70-clic', 'Creation 70 Clic LVT sa click sistemom'),
    '21': ('creation-70-connect', 'Creation 70 Connect LVT sa connect sistemom'),
    '22': ('creation-70-megaclic', 'Creation 70 Megaclic LVT sa megaclic sistemom'),
    '23': ('creation-70-zen', 'Creation 70 Zen LVT sa teksturiranim površinama'),
    '24': ('creation-saga', 'Creation Saga² LVT sa kvadratnim formatom'),
    '25': ('creation-70-looselay', 'Creation 70 Looselay LVT sa loose lay instalacijom'),
}

def generate_specs(folder_name):
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
        fmt = 'Planka' if data['format'] == 'plank' else 'Pločica'
        specs.append(f"      {{ key: 'format', label: 'Format', value: '{fmt}' }},")
    if data.get('usage_class'):
        specs.append(f"      {{ key: 'usage_class', label: 'Klasa upotrebe', value: '{data['usage_class']}' }},")
    if data.get('fire_class'):
        specs.append(f"      {{ key: 'fire_class', label: 'Protivpožarna klasifikacija', value: '{data['fire_class']}' }},")
    if data.get('acoustic') and data['acoustic'] not in ['2', '31074', '30174']:
        acoustic = data['acoustic']
        if acoustic == 'Yes':
            specs.append(f"      {{ key: 'acoustic', label: 'Akustična izolacija', value: 'Da' }},")
        elif str(acoustic).isdigit():
            specs.append(f"      {{ key: 'acoustic', label: 'Akustična izolacija', value: '{acoustic} dB' }},")
    if data.get('installation'):
        inst_map = {'glue down': 'Lepljenje', 'click system': 'Click sistem', 'loose lay': 'Loose lay', 'connect system': 'Connect sistem'}
        inst = inst_map.get(data['installation'], data['installation'])
        specs.append(f"      {{ key: 'installation', label: 'Tip instalacije', value: '{inst}' }},")
    specs.append(f"      {{ key: 'surface', label: 'Površinska obrada', value: 'Protecshield® PUR' }},")
    return '\n'.join(specs)

# Update each product
for product_id, (folder_name, short_desc) in products.items():
    pattern = rf"(    id: '{product_id}',.*?specs: \[)[^\]]+(\],)"
    new_specs = generate_specs(folder_name)
    if new_specs:
        replacement = rf"\1\n{new_specs}\n    \2"
        content = re.sub(pattern, replacement, content, flags=re.DOTALL)
        print(f"Updated ID {product_id}: {folder_name}")

# Write back
with open('lib/data/mock-data.ts', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\nDONE! Updated {len(products)} LVT products!")
