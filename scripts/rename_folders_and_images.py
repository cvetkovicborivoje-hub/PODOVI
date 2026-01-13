#!/usr/bin/env python3
"""
Preimenuje foldere proizvoda i slike u creation-30 kolekciji:
- Foldere preimenuje u format: code-name (npr. 0347-ballerina)
- Slike u pod/ folderu: dodaje -pod (npr. ime-pod.jpg)
- Slike u ilustracija/ folderu: dodaje -ilustracija (npr. ime-ilustracija.jpg)
"""

import json
import re
from pathlib import Path

def sanitize_name(name):
    """Konvertuje ime u slug format (lowercase, zamenjuje space sa -)"""
    # Konvertuj u lowercase
    name = name.lower()
    # Zameni razmake sa crticama
    name = name.replace(' ', '-')
    # Ukloni nevalidne karaktere (ostavi samo alfanumerike, crtice i podvlačenja)
    name = re.sub(r'[^a-z0-9\-_]', '', name)
    # Ukloni višestruke crtice
    name = re.sub(r'-+', '-', name)
    # Ukloni crtice sa početka/kraja
    name = name.strip('-')
    return name

def rename_folders_and_images():
    base_path = Path('public/images/products/lvt/colors/creation-30')
    json_path = Path('public/data/lvt_colors_complete.json')
    
    # Učitaj JSON fajl
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Filtriraj samo creation-30 proizvode
    creation_30_colors = [c for c in data['colors'] if c['collection'] == 'creation-30']
    
    print(f"Pronadjeno {len(creation_30_colors)} proizvoda u creation-30 kolekciji\n")
    
    folders_renamed = 0
    images_renamed = 0
    
    for color in creation_30_colors:
        old_slug = color['slug']
        code = color['code']
        name = color['name']
        
        # Kreiraj novo ime foldera: code-name
        clean_name = sanitize_name(name)
        new_folder_name = f"{code}-{clean_name}"
        
        old_folder = base_path / old_slug
        new_folder = base_path / new_folder_name
        
        if not old_folder.exists():
            print(f"WARNING: Folder ne postoji: {old_folder.name}")
            continue
        
        # Preimenuj folder proizvoda
        if old_folder.name != new_folder_name:
            try:
                old_folder.rename(new_folder)
                folders_renamed += 1
                print(f"Preimenovan folder: {old_slug} -> {new_folder_name}")
            except Exception as e:
                print(f"Greska pri preimenovanju foldera {old_slug}: {e}")
                continue
        else:
            print(f"Folder vec ima ispravno ime: {new_folder_name}")
        
        # Preimenuj slike u pod/ folderu
        pod_folder = new_folder / 'pod'
        if pod_folder.exists():
            for img_file in pod_folder.glob('*.jpg'):
                if not img_file.name.endswith('-pod.jpg'):
                    # Dodaj -pod pre ekstenzije
                    new_img_name = img_file.stem + '-pod.jpg'
                    new_img_path = pod_folder / new_img_name
                    try:
                        img_file.rename(new_img_path)
                        images_renamed += 1
                        print(f"  pod/{img_file.name} -> pod/{new_img_name}")
                    except Exception as e:
                        print(f"  Greska pri preimenovanju {img_file.name}: {e}")
        
        # Preimenuj slike u ilustracija/ folderu
        ilustracija_folder = new_folder / 'ilustracija'
        if ilustracija_folder.exists():
            for img_file in ilustracija_folder.glob('*.jpg'):
                if not img_file.name.endswith('-ilustracija.jpg'):
                    # Dodaj -ilustracija pre ekstenzije
                    new_img_name = img_file.stem + '-ilustracija.jpg'
                    new_img_path = ilustracija_folder / new_img_name
                    try:
                        img_file.rename(new_img_path)
                        images_renamed += 1
                        print(f"  ilustracija/{img_file.name} -> ilustracija/{new_img_name}")
                    except Exception as e:
                        print(f"  Greska pri preimenovanju {img_file.name}: {e}")
    
    print(f"\nGotovo!")
    print(f"Preimenovano foldera: {folders_renamed}")
    print(f"Preimenovano slika: {images_renamed}")

if __name__ == "__main__":
    rename_folders_and_images()
