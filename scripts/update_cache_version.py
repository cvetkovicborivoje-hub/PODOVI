# -*- coding: utf-8 -*-
import json
import sys
from pathlib import Path

# Postavi UTF-8 encoding za stdout
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

def update_cache_version():
    """Povećava cache-bust verziju za sve creation-30 proizvode"""
    
    json_path = Path('public/data/lvt_colors_complete.json')
    
    # Učitaj JSON fajl
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Pronađi trenutnu verziju (proveri prvi creation-30 proizvod)
    current_version = 5
    for color in data['colors']:
        if color['collection'] == 'creation-30' and 'texture_url' in color:
            if '?v=' in color['texture_url']:
                version_str = color['texture_url'].split('?v=')[1]
                try:
                    current_version = int(version_str)
                except:
                    pass
            break
    
    new_version = current_version + 1
    print(f"Trenutna verzija: {current_version}")
    print(f"Nova verzija: {new_version}")
    
    updated_count = 0
    
    # Ažuriraj sve creation-30 proizvode
    for color in data['colors']:
        if color['collection'] == 'creation-30':
            if 'texture_url' in color:
                old_url = color['texture_url']
                if '?v=' in old_url:
                    base_url = old_url.split('?v=')[0]
                    color['texture_url'] = f"{base_url}?v={new_version}"
                    updated_count += 1
                else:
                    color['texture_url'] = f"{old_url}?v={new_version}"
                    updated_count += 1
            
            if 'image_url' in color:
                old_url = color['image_url']
                if '?v=' in old_url:
                    base_url = old_url.split('?v=')[0]
                    color['image_url'] = f"{base_url}?v={new_version}"
                else:
                    color['image_url'] = f"{old_url}?v={new_version}"
            
            if 'lifestyle_url' in color:
                old_url = color['lifestyle_url']
                if '?v=' in old_url:
                    base_url = old_url.split('?v=')[0]
                    color['lifestyle_url'] = f"{base_url}?v={new_version}"
                else:
                    color['lifestyle_url'] = f"{old_url}?v={new_version}"
    
    # Sačuvaj JSON
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"\nAžurirano {updated_count} creation-30 proizvoda sa cache verzijom {new_version}")

if __name__ == "__main__":
    update_cache_version()
