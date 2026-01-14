# -*- coding: utf-8 -*-
import json
import re
import sys
from pathlib import Path

# Postavi UTF-8 encoding za stdout
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

def update_gerflor_products_images():
    """Ažurira putanje do slika u gerflor-products-generated.ts za sve kolekcije do creation-55"""
    
    json_path = Path('public/data/lvt_colors_complete.json')
    ts_path = Path('lib/data/gerflor-products-generated.ts')
    
    # Kolekcije do creation-55
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
        json_data = json.load(f)
    
    # Kreiraj mapu: (collection, code) -> texture_url
    image_map = {}
    for color in json_data['colors']:
        if color['collection'] in collections:
            code = color['code']
            collection = color['collection']
            image_map[(collection, code)] = color['texture_url']
    
    print(f"Pronadjeno {len(image_map)} proizvoda u kolekcijama do creation-55")
    
    # Učitaj TypeScript fajl
    with open(ts_path, 'r', encoding='utf-8') as f:
        ts_content = f.read()
    
    # Čitaj liniju po liniju i ažuriraj
    lines = ts_content.split('\n')
    new_lines = []
    i = 0
    updated_count = 0
    current_code = None
    current_collection = None
    in_product = False
    
    while i < len(lines):
        line = lines[i]
        
        # Proveri da li smo u nekoj od ovih kolekcija
        for collection in collections:
            collection_prefix = collection.replace('-', '-')
            if f"id: '{collection}-" in line or f"id: \"{collection}-" in line:
                in_product = True
                current_collection = collection
                break
        
        # Pronađi liniju sa sku: 'code'
        if in_product and 'sku:' in line:
            sku_match = re.search(r"sku:\s*['\"](\d+)['\"]", line)
            if sku_match:
                current_code = sku_match.group(1)
        
        # Ako imamo kolekciju, kod i naidjemo na url liniju
        if in_product and current_collection and current_code and 'url:' in line:
            old_url_match = re.search(r"url:\s*['\"]((?:/images/products/lvt/colors/[^'\"]+)/[^'\"]+)['\"]", line)
            if old_url_match and (current_collection, current_code) in image_map:
                old_url = old_url_match.group(1)
                new_url = image_map[(current_collection, current_code)]
                # Zameni staru putanju novom (samo base path, ne query params)
                new_url_base = new_url.split('?')[0]
                # Zameni ceo URL
                new_line = line
                if old_url_match.group(0) in line:
                    new_line = line.replace(old_url_match.group(1), new_url_base)
                    # Ako ima query params u novom URL-u, dodaj ih
                    if '?' in new_url:
                        # Već smo zamenili, ali možda treba dodati query param
                        if '?' not in new_line:
                            new_line = new_line.replace(new_url_base, new_url)
                        else:
                            # Ako već ima query param u liniji, zameni ceo URL
                            full_old_match = re.search(r"url:\s*['\"][^'\"]+['\"]", line)
                            if full_old_match:
                                new_line = line.replace(full_old_match.group(0), f"url: '{new_url}'")
                
                new_lines.append(new_line)
                updated_count += 1
                if updated_count <= 10:  # Print prvih 10
                    print(f"Ažuriran {current_collection} kod {current_code}")
                current_code = None  # Reset
                current_collection = None
                in_product = False
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)
        
        # Reset kada završimo proizvod (zatvorena zagrada)
        if in_product and line.strip() == '},':
            in_product = False
            current_code = None
            current_collection = None
        
        i += 1
    
    new_content = '\n'.join(new_lines)
    
    # Sačuvaj ažurirani fajl
    with open(ts_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"\nAžurirano {updated_count} proizvoda u gerflor-products-generated.ts")

if __name__ == "__main__":
    update_gerflor_products_images()
