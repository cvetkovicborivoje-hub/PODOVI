# -*- coding: utf-8 -*-
"""
Briše visak slika iz proizvodnih foldera - slike direktno u root-u foldera (ne u pod/ ili ilustracija/)
i pod/ilustracija foldere koji nisu u produktnim folderima.
"""

import os
import sys
from pathlib import Path

# Postavi UTF-8 encoding za stdout
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

def clean_excess_images_in_collection(collection_path):
    """Briše visak slika iz kolekcije"""
    base_path = Path(collection_path)
    
    if not base_path.exists():
        print(f"Putanja ne postoji: {base_path}")
        return 0, 0
    
    deleted_files_count = 0
    deleted_folders_count = 0
    
    # Pronađi sve proizvodne foldere (na nivou 2 - npr. creation-30/0347-ballerina/)
    product_folders = []
    for item in base_path.iterdir():
        if item.is_dir() and item.name not in ['pod', 'ilustracija']:
            product_folders.append(item)
    
    files_to_delete = []
    folders_to_delete = []
    
    for folder in product_folders:
        # Slike direktno u proizvodnom folderu (koje nisu u pod/ ili ilustracija/)
        for img_file in folder.glob("*.jpg"):
            files_to_delete.append(img_file)
        
        # Proveri da li postoje pod/ilustracija folderi direktno u root-u kolekcije (što ne bi trebalo)
        # Ovo se dešava retko, ali proverimo
        pass
    
    # Takođe proveri root kolekcije za slike i pod/ilustracija foldere
    for jpg_file in base_path.glob("*.jpg"):
        files_to_delete.append(jpg_file)
    
    if (base_path / "pod").is_dir():
        folders_to_delete.append(base_path / "pod")
    if (base_path / "ilustracija").is_dir():
        folders_to_delete.append(base_path / "ilustracija")
    
    print(f"\n{base_path.name}:")
    print(f"  Pronadjeno {len(files_to_delete)} slika za brisanje")
    print(f"  Pronadjeno {len(folders_to_delete)} foldera za brisanje")
    
    if not files_to_delete and not folders_to_delete:
        print(f"  Nema viska za brisanje")
        return 0, 0
    
    # Delete JPG files
    for i, file_path in enumerate(files_to_delete):
        try:
            os.remove(file_path)
            deleted_files_count += 1
        except OSError as e:
            print(f"  Greska pri brisanju {file_path.name}: {e}")
    
    # Delete folders
    import shutil
    for folder_path in folders_to_delete:
        try:
            shutil.rmtree(folder_path)
            deleted_folders_count += 1
            print(f"  Obrisan folder: {folder_path.name}")
        except OSError as e:
            print(f"  Greska pri brisanju foldera {folder_path}: {e}")
    
    return deleted_files_count, deleted_folders_count

def main():
    base_path = Path('public/images/products/lvt/colors')
    
    if not base_path.exists():
        print(f"Bazna putanja ne postoji: {base_path}")
        return
    
    # Pronađi sve creation kolekcije
    collections = [d for d in base_path.iterdir() if d.is_dir() and d.name.startswith('creation')]
    
    total_files = 0
    total_folders = 0
    
    for collection in sorted(collections):
        files, folders = clean_excess_images_in_collection(collection)
        total_files += files
        total_folders += folders
    
    print(f"\n{'='*50}")
    print(f"Gotovo!")
    print(f"Obrisano slika: {total_files}")
    print(f"Obrisano foldera: {total_folders}")

if __name__ == "__main__":
    main()
