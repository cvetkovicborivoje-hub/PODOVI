# -*- coding: utf-8 -*-
import json
import re
import sys
from pathlib import Path

# Postavi UTF-8 encoding za stdout
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

def update_gerflor_products_images():
    """Ažurira putanje do slika u gerflor-products-generated.ts za creation-30 proizvode"""
    
    json_path = Path('public/data/lvt_colors_complete.json')
    ts_path = Path('lib/data/gerflor-products-generated.ts')
    
    # Učitaj JSON fajl
    with open(json_path, 'r', encoding='utf-8') as f:
        json_data = json.load(f)
    
    # Kreiraj mapu: code -> texture_url
    image_map = {}
    for color in json_data['colors']:
        if color['collection'] == 'creation-30':
            code = color['code']
            image_map[code] = color['texture_url']
    
    print(f"Pronadjeno {len(image_map)} creation-30 proizvoda u JSON-u")
    
    # Učitaj TypeScript fajl
    with open(ts_path, 'r', encoding='utf-8') as f:
        ts_content = f.read()
    
    # Čitaj liniju po liniju i ažuriraj
    lines = ts_content.split('\n')
    new_lines = []
    i = 0
    updated_count = 0
    current_code = None
    in_creation_30 = False
    
    while i < len(lines):
        line = lines[i]
        
        # Proveri da li smo u creation-30 proizvodu
        if "id: 'creation-30-" in line:
            in_creation_30 = True
        
        # Pronađi liniju sa sku: 'code' za creation-30 proizvode
        if in_creation_30 and 'sku:' in line:
            sku_match = re.search(r"sku:\s*['\"](\d+)['\"]", line)
            if sku_match:
                current_code = sku_match.group(1)
        
        # Ako imamo kod i naidjemo na url liniju
        if in_creation_30 and current_code and 'url:' in line:
            # Pattern za URL - mora biti fleksibilniji
            old_url_match = re.search(r"url:\s*['\"]((?:/images/products/lvt/colors/creation-30/)[^'\"]+)['\"]", line)
            if old_url_match and current_code in image_map:
                old_url = old_url_match.group(1)
                new_url = image_map[current_code]
                # Zameni staru putanju novom
                new_line = line.replace(old_url, new_url)
                new_lines.append(new_line)
                updated_count += 1
                print(f"Ažuriran kod {current_code}")
                current_code = None  # Reset
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)
        
        # Reset kada završimo proizvod (zatvorena zagrada)
        if in_creation_30 and line.strip() == '},':
            in_creation_30 = False
            current_code = None
        
        i += 1
    
    new_content = '\n'.join(new_lines)
    
    # Sačuvaj ažurirani fajl
    with open(ts_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"\nAžurirano {updated_count} creation-30 proizvoda u gerflor-products-generated.ts")

if __name__ == "__main__":
    update_gerflor_products_images()
