# -*- coding: utf-8 -*-
"""
Ažurira JSON sa novim ilustracijama koje su kopirane
"""

import json
import sys
from pathlib import Path
from urllib.parse import quote

# Postavi UTF-8 encoding za stdout
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

json_path = Path('public/data/lvt_colors_complete.json')
base_images_path = Path('public/images/products/lvt/colors')

# Učitaj JSON fajl
with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

updated_count = 0
cache_version = 9  # Povećaj verziju za cache busting

for color in data['colors']:
    collection = color['collection']
    code = color['code']
    
    base_path = base_images_path / collection
    if not base_path.exists():
        continue
    
    # Pronađi folder proizvoda po kodu
    folder_name = None
    for folder in base_path.iterdir():
        if folder.is_dir() and folder.name not in ['pod', 'ilustracija']:
            folder_parts = folder.name.split('-', 1)
            if folder_parts and folder_parts[0] == code:
                folder_name = folder.name
                break
    
    if not folder_name:
        continue
    
    folder_path = base_path / folder_name
    ilustracija_folder = folder_path / 'ilustracija'
    
    # Proveri da li ilustracija folder postoji i ima slike
    if ilustracija_folder.exists():
        ilustracija_images = list(ilustracija_folder.glob('*.jpg'))
        if ilustracija_images:
            ilustracija_image_name = ilustracija_images[0].name
            lifestyle_url = f"/images/products/lvt/colors/{collection}/{folder_name}/ilustracija/{quote(ilustracija_image_name)}?v={cache_version}"
            
            # Ažuriraj lifestyle_url i texture_url/image_url ako već nisu ažurirani
            if 'lifestyle_url' not in color or color['lifestyle_url'] != lifestyle_url:
                color['lifestyle_url'] = lifestyle_url
                updated_count += 1
    
    # Takođe ažuriraj texture_url i image_url sa novom cache verzijom
    if 'texture_url' in color:
        clean_url = color['texture_url'].split('?')[0]
        color['texture_url'] = f"{clean_url}?v={cache_version}"
    if 'image_url' in color:
        clean_url = color['image_url'].split('?')[0]
        color['image_url'] = f"{clean_url}?v={cache_version}"
    if 'lifestyle_url' in color:
        clean_url = color['lifestyle_url'].split('?')[0]
        color['lifestyle_url'] = f"{clean_url}?v={cache_version}"

# Sačuvaj JSON
with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Ažurirano {updated_count} proizvoda sa novim ilustracijama")
print(f"Cache verzija ažurirana na v={cache_version}")
