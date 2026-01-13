# -*- coding: utf-8 -*-
import json
import sys
from pathlib import Path
from urllib.parse import quote

# Postavi UTF-8 encoding za stdout
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

def update_single_product_image(code='1705'):
    """Ažurira sliku za pojedinačan proizvod (1705 - AQUINOAH BROWN)"""
    
    json_path = Path('public/data/lvt_colors_complete.json')
    base_path = Path('public/images/products/lvt/colors/creation-30')
    
    # Učitaj JSON fajl
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Pronađi proizvod
    color = None
    for c in data['colors']:
        if c['code'] == code and c['collection'] == 'creation-30':
            color = c
            break
    
    if not color:
        print(f"Proizvod sa kodom {code} nije pronadjen!")
        return
    
    print(f"Pronadjen proizvod: {color['name']} (Šifra: {code})")
    
    # Pronađi folder
    folder_name = f"{code}-{color['name'].lower().replace(' ', '-')}"
    # Ili jednostavnije - nađi folder koji počinje sa kodom
    folder = None
    for f in base_path.iterdir():
        if f.is_dir() and f.name.startswith(f"{code}-"):
            folder = f
            break
    
    if not folder:
        print(f"Folder za kod {code} nije pronadjen!")
        return
    
    print(f"Pronadjen folder: {folder.name}")
    
    # Pronađi sliku u pod/ folderu
    pod_folder = folder / 'pod'
    if not pod_folder.exists():
        print(f"Pod folder ne postoji: {pod_folder}")
        return
    
    pod_images = list(pod_folder.glob('*.jpg'))
    if not pod_images:
        print(f"Nema slika u pod/ folderu: {pod_folder}")
        return
    
    # Uzmi prvu sliku
    pod_image = pod_images[0]
    print(f"Pronadjena slika: {pod_image.name}")
    
    # Kreiraj novu URL putanju
    cache_version = 5
    folder_name = folder.name
    texture_url = f"/images/products/lvt/colors/creation-30/{folder_name}/pod/{quote(pod_image.name)}?v={cache_version}"
    
    # Ažuriraj JSON
    color['texture_url'] = texture_url
    color['image_url'] = texture_url
    
    # Proveri ilustraciju
    ilustracija_folder = folder / 'ilustracija'
    if ilustracija_folder.exists():
        ilustracija_images = list(ilustracija_folder.glob('*.jpg'))
        if ilustracija_images:
            ilustracija_image = ilustracija_images[0]
            lifestyle_url = f"/images/products/lvt/colors/creation-30/{folder_name}/ilustracija/{quote(ilustracija_image.name)}?v={cache_version}"
            color['lifestyle_url'] = lifestyle_url
            print(f"Pronadjena ilustracija: {ilustracija_image.name}")
        else:
            if 'lifestyle_url' in color:
                del color['lifestyle_url']
    else:
        if 'lifestyle_url' in color:
            del color['lifestyle_url']
    
    # Sačuvaj JSON
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"\nAžurirana texture_url: {texture_url}")
    print(f"Ažuriran JSON fajl!")

if __name__ == "__main__":
    update_single_product_image('1705')
