# -*- coding: utf-8 -*-
"""
Preimenuje foldere proizvoda i slike u SVIM kolekcijama:
- Foldere preimenuje u format: code-name (npr. 0347-ballerina)
- Slike u pod/ folderu: dodaje -pod (npr. ime-pod.jpg)
- Slike u ilustracija/ folderu: dodaje -ilustracija (npr. ime-ilustracija.jpg)
"""

import json
import re
import sys
from pathlib import Path

# Postavi UTF-8 encoding za stdout
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

def sanitize_name(name):
    """Konvertuje ime u slug format (lowercase, zamenjuje space sa -)"""
    name = name.lower()
    name = name.replace(' ', '-')
    name = re.sub(r'[^a-z0-9\-_]', '', name)
    name = re.sub(r'-+', '-', name)
    name = name.strip('-')
    return name

def rename_collection(collection_name, json_data):
    """Preimenuje foldere i slike za datu kolekciju"""
    base_path = Path(f'public/images/products/lvt/colors/{collection_name}')
    
    if not base_path.exists():
        print(f"\n{collection_name}: Folder ne postoji, preskacem")
        return 0, 0
    
    # Filtriraj proizvode za ovu kolekciju
    colors = [c for c in json_data['colors'] if c['collection'] == collection_name]
    
    if not colors:
        print(f"\n{collection_name}: Nema proizvoda u JSON-u, preskacem")
        return 0, 0
    
    print(f"\n{collection_name}: {len(colors)} proizvoda")
    
    folders_renamed = 0
    images_renamed = 0
    
    for color in colors:
        old_slug = color['slug']
        code = color['code']
        name = color['name']
        
        # Kreiraj novo ime foldera: code-name
        clean_name = sanitize_name(name)
        new_folder_name = f"{code}-{clean_name}"
        
        old_folder = base_path / old_slug
        new_folder = base_path / new_folder_name
        
        if not old_folder.exists():
            # Možda je već preimenovan, proveri novo ime
            if new_folder.exists():
                # Folder već ima ispravno ime
                pass
            else:
                # Pokušaj da nađeš folder po kodu
                found_folder = None
                for folder in base_path.iterdir():
                    if folder.is_dir() and folder.name.startswith(f"{code}-"):
                        found_folder = folder
                        break
                if found_folder:
                    new_folder = found_folder
                else:
                    print(f"  WARNING: Folder ne postoji: {old_slug}")
                    continue
        else:
            # Preimenuj folder proizvoda
            if old_folder.name != new_folder_name:
                try:
                    old_folder.rename(new_folder)
                    folders_renamed += 1
                    if folders_renamed <= 5:  # Print prvih 5
                        print(f"  Preimenovan folder: {old_slug} -> {new_folder_name}")
                except Exception as e:
                    print(f"  Greska pri preimenovanju foldera {old_slug}: {e}")
                    continue
            else:
                # Folder već ima ispravno ime
                pass
        
        # Ako folder nije postojao pod starim imenom, koristi novo
        if not old_folder.exists() and new_folder.exists():
            pass  # Već koristimo new_folder
        
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
                        if images_renamed <= 10:  # Print prvih 10
                            print(f"    pod/{img_file.name} -> pod/{new_img_name}")
                    except Exception as e:
                        print(f"    Greska pri preimenovanju {img_file.name}: {e}")
        
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
                        if images_renamed <= 10:  # Print prvih 10
                            print(f"    ilustracija/{img_file.name} -> ilustracija/{new_img_name}")
                    except Exception as e:
                        print(f"    Greska pri preimenovanju {img_file.name}: {e}")
    
    return folders_renamed, images_renamed

def main():
    json_path = Path('public/data/lvt_colors_complete.json')
    
    # Učitaj JSON fajl
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Pronađi sve kolekcije u JSON-u
    collections = sorted(set(c['collection'] for c in data['colors']))
    
    print(f"Pronadjeno {len(collections)} kolekcija u JSON-u")
    
    total_folders = 0
    total_images = 0
    
    for collection in collections:
        folders, images = rename_collection(collection, data)
        total_folders += folders
        total_images += images
    
    print(f"\n{'='*50}")
    print(f"Gotovo!")
    print(f"Preimenovano foldera: {total_folders}")
    print(f"Preimenovano slika: {total_images}")

if __name__ == "__main__":
    main()
