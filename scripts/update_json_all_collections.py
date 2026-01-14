# -*- coding: utf-8 -*-
"""
Ažurira JSON sa standardizovanim imenima slika za SVE kolekcije: code-name-pod.jpg
"""

import json
import sys
from pathlib import Path
from urllib.parse import quote

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

def update_json_all_collections():
    """Ažurira JSON sa standardizovanim imenima slika za SVE kolekcije"""
    json_path = Path('public/data/lvt_colors_complete.json')
    
    # Učitaj JSON fajl
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Pronađi sve kolekcije u JSON-u
    collections = sorted(set(c['collection'] for c in data['colors']))
    
    base_images_path = Path('public/images/products/lvt/colors')
    
    updated_count = 0
    errors = []
    cache_version = 8  # Povećaj verziju za cache busting
    
    for collection in collections:
        base_path = base_images_path / collection
        
        if not base_path.exists():
            continue
        
        colors = [c for c in data['colors'] if c['collection'] == collection]
        
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
                errors.append(f"{collection}: Ne postoji folder za kod {code} ({name})")
                continue
            
            folder_name = folder_map[code]
            folder_path = base_path / folder_name
            
            # Standardno ime: code-name-pod.jpg
            clean_name = sanitize_for_filename(name)
            standard_pod_name = f"{code}-{clean_name}-pod.jpg"
            standard_ilustracija_name = f"{code}-{clean_name}-ilustracija.jpg"
            
            pod_folder = folder_path / 'pod'
            ilustracija_folder = folder_path / 'ilustracija'
            
            pod_images = list(pod_folder.glob('*.jpg')) if pod_folder.exists() else []
            
            if not pod_images:
                errors.append(f"{collection}: Nema slika u pod/ folderu za {code} ({name})")
                continue
            
            # Koristi standardno ime (proveri da li postoji, ako ne, koristi prvu dostupnu)
            standard_pod_path = pod_folder / standard_pod_name
            if standard_pod_path.exists():
                pod_image_name = standard_pod_name
            else:
                pod_image_name = pod_images[0].name
            
            texture_url = f"/images/products/lvt/colors/{collection}/{folder_name}/pod/{pod_image_name}?v={cache_version}"
            
            lifestyle_url = None
            if ilustracija_folder.exists():
                ilustracija_images = list(ilustracija_folder.glob('*.jpg'))
                if ilustracija_images:
                    standard_il_path = ilustracija_folder / standard_ilustracija_name
                    if standard_il_path.exists():
                        ilustracija_image_name = standard_ilustracija_name
                    else:
                        ilustracija_image_name = ilustracija_images[0].name
                    lifestyle_url = f"/images/products/lvt/colors/{collection}/{folder_name}/ilustracija/{ilustracija_image_name}?v={cache_version}"
            
            color['texture_url'] = texture_url
            color['image_url'] = texture_url
            
            if lifestyle_url:
                color['lifestyle_url'] = lifestyle_url
            elif 'lifestyle_url' in color:
                del color['lifestyle_url']
            
            updated_count += 1
    
    # Sačuvaj JSON
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"Ažurirano {updated_count} proizvoda")
    if errors:
        print(f"\nGreške ({len(errors)}):")
        for error in errors[:30]:
            print(f"  - {error}")
        if len(errors) > 30:
            print(f"  ... i još {len(errors) - 30} grešaka")

if __name__ == "__main__":
    update_json_all_collections()
