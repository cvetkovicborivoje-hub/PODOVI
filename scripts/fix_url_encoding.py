# -*- coding: utf-8 -*-
import json
import sys
from pathlib import Path
from urllib.parse import unquote

# Postavi UTF-8 encoding za stdout
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

def fix_url_encoding():
    """Uklanja URL encoding iz URL-ova u JSON-u (URL-ovi treba da budu plain stringovi)"""
    
    json_path = Path('public/data/lvt_colors_complete.json')
    
    # Učitaj JSON fajl
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    updated_count = 0
    
    # Ažuriraj sve creation-30 proizvode
    for color in data['colors']:
        if color['collection'] == 'creation-30':
            changed = False
            
            if 'texture_url' in color:
                old_url = color['texture_url']
                # Dekoduj URL (ukloni encoding)
                if '%' in old_url:
                    # Dekoduj samo deo URL-a pre query parametara
                    if '?' in old_url:
                        base_url, query = old_url.split('?', 1)
                        decoded_url = unquote(base_url) + '?' + query
                    else:
                        decoded_url = unquote(old_url)
                    color['texture_url'] = decoded_url
                    changed = True
            
            if 'image_url' in color:
                old_url = color['image_url']
                if '%' in old_url:
                    if '?' in old_url:
                        base_url, query = old_url.split('?', 1)
                        decoded_url = unquote(base_url) + '?' + query
                    else:
                        decoded_url = unquote(old_url)
                    color['image_url'] = decoded_url
                    changed = True
            
            if 'lifestyle_url' in color:
                old_url = color['lifestyle_url']
                if '%' in old_url:
                    if '?' in old_url:
                        base_url, query = old_url.split('?', 1)
                        decoded_url = unquote(base_url) + '?' + query
                    else:
                        decoded_url = unquote(old_url)
                    color['lifestyle_url'] = decoded_url
                    changed = True
            
            if changed:
                updated_count += 1
    
    # Sačuvaj JSON
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"Ažurirano {updated_count} creation-30 proizvoda - uklonjen URL encoding")

if __name__ == "__main__":
    fix_url_encoding()
