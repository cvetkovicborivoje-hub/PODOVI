# -*- coding: utf-8 -*-
"""
Ažurira JSON sa standardizovanim imenima slika: code-name-pod.jpg
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

def update_json_with_standard_names():
    """Ažurira JSON sa standardizovanim imenima slika"""
    json_path = Path('public/data/lvt_colors_complete.json')
    
    collections = [
        'creation-30',
        'creation-40',
        'creation-40-clic',
        'creation-40-clic-acoustic',
        'creation-40-zen',
        'creation-55',
    ]
    
    # Učitaj JSON fajl
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    updated_count = 0
    errors = []
    cache_version = 7  # Povećaj verziju za cache busting
    
    for collection in collections:
        base_path = Path(f'public/images/products/lvt/colors/{collection}')
        
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
            
            # Koristi standardno ime (ne zanima nas stvarno ime fajla, koristimo standardno)
            # Ali prvo proveri da li fajl sa tim imenom postoji
            standard_pod_path = pod_folder / standard_pod_name
            if not standard_pod_path.exists():
                # Ako standardno ime ne postoji, koristi prvu sliku koja postoji
                pod_image_name = pod_images[0].name
            else:
                pod_image_name = standard_pod_name
            
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
        for error in errors[:20]:
            print(f"  - {error}")
        if len(errors) > 20:
            print(f"  ... i još {len(errors) - 20} grešaka")

if __name__ == "__main__":
    update_json_with_standard_names()
