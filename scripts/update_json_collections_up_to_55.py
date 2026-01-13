# -*- coding: utf-8 -*-
"""
Ažurira lvt_colors_complete.json sa novim putanjama do slika za kolekcije do creation-55
"""

import json
import sys
from pathlib import Path

# Postavi UTF-8 encoding za stdout
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

def update_collection_images(collection_name, json_data):
    """Ažurira putanje do slika za datu kolekciju"""
    base_path = Path(f'public/images/products/lvt/colors/{collection_name}')
    
    if not base_path.exists():
        print(f"{collection_name}: Folder ne postoji, preskacem")
        return 0, []
    
    colors = [c for c in json_data['colors'] if c['collection'] == collection_name]
    
    if not colors:
        print(f"{collection_name}: Nema proizvoda u JSON-u, preskacem")
        return 0, []
    
    print(f"\n{collection_name}: {len(colors)} proizvoda")
    
    updated_count = 0
    errors = []
    cache_version = 6  # Koristi istu verziju kao creation-30
    
    # Kreiraj mapu: code -> folder_name
    folder_map = {}
    for folder in base_path.iterdir():
        if folder.is_dir() and folder.name not in ['pod', 'ilustracija']:
            # Pokušaj da izvučeš kod iz imena foldera (npr. 0347-ballerina -> 0347)
            parts = folder.name.split('-', 1)
            if len(parts) >= 1 and parts[0].isdigit():
                code = parts[0]
                folder_map[code] = folder.name
    
    for color in colors:
        code = color['code']
        
        if code not in folder_map:
            errors.append(f"Ne postoji folder za kod {code} ({color['name']})")
            continue
        
        folder_name = folder_map[code]
        folder_path = base_path / folder_name
        
        pod_folder = folder_path / 'pod'
        ilustracija_folder = folder_path / 'ilustracija'
        
        pod_images = list(pod_folder.glob('*.jpg')) if pod_folder.exists() else []
        ilustracija_images = list(ilustracija_folder.glob('*.jpg')) if ilustracija_folder.exists() else []
        
        if not pod_images:
            errors.append(f"Nema slika u pod/ folderu za {code} ({color['name']})")
            continue
        
        pod_image_name = pod_images[0].name
        texture_url = f"/images/products/lvt/colors/{collection_name}/{folder_name}/pod/{pod_image_name}?v={cache_version}"
        
        lifestyle_url = None
        if ilustracija_images:
            ilustracija_image_name = ilustracija_images[0].name
            lifestyle_url = f"/images/products/lvt/colors/{collection_name}/{folder_name}/ilustracija/{ilustracija_image_name}?v={cache_version}"
        
        color['texture_url'] = texture_url
        color['image_url'] = texture_url
        
        if lifestyle_url:
            color['lifestyle_url'] = lifestyle_url
        elif 'lifestyle_url' in color:
            del color['lifestyle_url']
        
        updated_count += 1
    
    return updated_count, errors

def main():
    json_path = Path('public/data/lvt_colors_complete.json')
    
    # Učitaj JSON fajl
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    collections = [
        'creation-40',
        'creation-40-clic',
        'creation-40-clic-acoustic',
        'creation-40-zen',
        'creation-55',
    ]
    
    total_updated = 0
    all_errors = []
    
    for collection in collections:
        updated, errors = update_collection_images(collection, data)
        total_updated += updated
        all_errors.extend([f"{collection}: {e}" for e in errors])
    
    # Sačuvaj JSON
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"\n{'='*50}")
    print(f"Ažurirano {total_updated} proizvoda")
    if all_errors:
        print(f"\nGreške ({len(all_errors)}):")
        for error in all_errors[:20]:
            print(f"  - {error}")
        if len(all_errors) > 20:
            print(f"  ... i još {len(all_errors) - 20} grešaka")

if __name__ == "__main__":
    main()
