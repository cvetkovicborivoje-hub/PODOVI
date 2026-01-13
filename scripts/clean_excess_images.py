#!/usr/bin/env python3
"""
Briše visak slika iz glavnih foldera kolekcije creation-30.
Briše sve JPG fajlove koji nisu u pod/ ili ilustracija/ folderima.
"""

from pathlib import Path

base = Path('public/images/products/lvt/colors/creation-30')

folders_cleaned = 0
images_deleted = 0
images_to_delete = []

# Prvo prikupi sve slike koje će biti obrisane (bez brisanja)
for folder in base.iterdir():
    if not folder.is_dir() or folder.name in ['pod', 'ilustracija']:
        continue
    
    pod_folder = folder / 'pod'
    ilustracija_folder = folder / 'ilustracija'
    
    # Pronađi sve JPG fajlove u glavnom folderu
    main_images = list(folder.glob('*.jpg'))
    
    # Pronađi slike koje NISU u pod/ ili ilustracija/ folderima
    for img in main_images:
        in_pod = (pod_folder / img.name).exists() if pod_folder.exists() else False
        in_ilustracija = (ilustracija_folder / img.name).exists() if ilustracija_folder.exists() else False
        
        if not in_pod and not in_ilustracija:
            images_to_delete.append((folder.name, img))

print(f"Pronadjeno {len(images_to_delete)} slika za brisanje u {len(set(f[0] for f in images_to_delete))} folderima\n")

# Prikaži prvih 10
for folder_name, img in images_to_delete[:10]:
    print(f"{folder_name}: {img.name}")

if len(images_to_delete) > 10:
    print(f"\n... i jos {len(images_to_delete) - 10} slika")

# Obriši slike
print(f"\nUkupno slika za brisanje: {len(images_to_delete)}")
print("Brisanje slika...\n")

for folder_name, img in images_to_delete:
    try:
        img.unlink()
        images_deleted += 1
        if images_deleted % 10 == 0:
            print(f"Obrisano {images_deleted} slika...")
    except Exception as e:
        print(f"Greska pri brisanju {img}: {e}")

folders_cleaned = len(set(f[0] for f in images_to_delete))
print(f"\nObrisano {images_deleted} slika iz {folders_cleaned} foldera.")
