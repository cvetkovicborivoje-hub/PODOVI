# -*- coding: utf-8 -*-
"""
Standardizuje imena slika: code-name-pod.jpg ili code-name-ilustracija.jpg
Npr: 0347-ballerina-pod.jpg, 0347-ballerina-ilustracija.jpg
"""

import json
import sys
from pathlib import Path

# Postavi UTF-8 encoding za stdout
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

def sanitize_for_filename(text):
    """Konvertuje tekst u siguran format za ime fajla"""
    import re
    text = text.lower()
    text = text.replace(' ', '-')
    text = re.sub(r'[^a-z0-9\-]', '', text)
    text = re.sub(r'-+', '-', text)
    text = text.strip('-')
    return text

def standardize_collection_images(collection_name, json_data):
    """Standardizuje imena slika za datu kolekciju"""
    base_path = Path(f'public/images/products/lvt/colors/{collection_name}')
    
    if not base_path.exists():
        print(f"{collection_name}: Folder ne postoji, preskacem")
        return 0, []
    
    colors = [c for c in json_data['colors'] if c['collection'] == collection_name]
    
    if not colors:
        print(f"{collection_name}: Nema proizvoda u JSON-u, preskacem")
        return 0, []
    
    print(f"\n{collection_name}: {len(colors)} proizvoda")
    
    renamed_count = 0
    errors = []
    
    # Kreiraj mapu: code -> folder_name
    folder_map = {}
    for folder in base_path.iterdir():
        if folder.is_dir() and folder.name not in ['pod', 'ilustracija']:
            parts = folder.name.split('-', 1)
            if len(parts) >= 1 and parts[0].isdigit():
                code = parts[0]
                folder_map[code] = folder.name
    
    for color in colors:
        code = color['code']
        name = color['name']
        
        if code not in folder_map:
            errors.append(f"Ne postoji folder za kod {code} ({name})")
            continue
        
        folder_name = folder_map[code]
        folder_path = base_path / folder_name
        
        # Standardno ime: code-name-pod.jpg
        clean_name = sanitize_for_filename(name)
        standard_pod_name = f"{code}-{clean_name}-pod.jpg"
        standard_ilustracija_name = f"{code}-{clean_name}-ilustracija.jpg"
        
        # Preimenuj slike u pod/ folderu
        pod_folder = folder_path / 'pod'
        if pod_folder.exists():
            pod_images = list(pod_folder.glob('*.jpg'))
            if pod_images:
                old_pod = pod_images[0]
                new_pod = pod_folder / standard_pod_name
                if old_pod.name != standard_pod_name:
                    try:
                        old_pod.rename(new_pod)
                        renamed_count += 1
                        print(f"  {code}: pod/{old_pod.name} -> pod/{standard_pod_name}")
                    except Exception as e:
                        errors.append(f"Greska pri preimenovanju pod/{old_pod.name}: {e}")
        
        # Preimenuj slike u ilustracija/ folderu
        ilustracija_folder = folder_path / 'ilustracija'
        if ilustracija_folder.exists():
            ilustracija_images = list(ilustracija_folder.glob('*.jpg'))
            if ilustracija_images:
                old_il = ilustracija_images[0]
                new_il = ilustracija_folder / standard_ilustracija_name
                if old_il.name != standard_ilustracija_name:
                    try:
                        old_il.rename(new_il)
                        renamed_count += 1
                        print(f"  {code}: ilustracija/{old_il.name} -> ilustracija/{standard_ilustracija_name}")
                    except Exception as e:
                        errors.append(f"Greska pri preimenovanju ilustracija/{old_il.name}: {e}")
    
    return renamed_count, errors

def main():
    json_path = Path('public/data/lvt_colors_complete.json')
    
    # Učitaj JSON fajl
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    collections = [
        'creation-30',
        'creation-40',
        'creation-40-clic',
        'creation-40-clic-acoustic',
        'creation-40-zen',
        'creation-55',
    ]
    
    total_renamed = 0
    all_errors = []
    
    for collection in collections:
        renamed, errors = standardize_collection_images(collection, data)
        total_renamed += renamed
        all_errors.extend([f"{collection}: {e}" for e in errors])
    
    print(f"\n{'='*50}")
    print(f"Preimenovano {total_renamed} slika")
    if all_errors:
        print(f"\nGreške ({len(all_errors)}):")
        for error in all_errors[:20]:
            print(f"  - {error}")
        if len(all_errors) > 20:
            print(f"  ... i još {len(all_errors) - 20} grešaka")

if __name__ == "__main__":
    main()
