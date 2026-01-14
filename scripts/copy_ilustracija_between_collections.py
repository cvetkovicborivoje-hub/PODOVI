# -*- coding: utf-8 -*-
from pathlib import Path
import shutil
import sys

# Postavi UTF-8 encoding za stdout
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

base = Path('public/images/products/lvt/colors')
empty_ilustracija = {}  # collection -> {code: (folder_path, folder_name)}
has_ilustracija = {}    # collection -> {code: (folder_path, folder_name, image_path)}

# Prođi kroz sve kolekcije i proizvode
for collection in base.iterdir():
    if collection.is_dir() and collection.name.startswith('creation'):
        collection_name = collection.name
        empty_ilustracija[collection_name] = {}
        has_ilustracija[collection_name] = {}
        
        for product_folder in collection.iterdir():
            if product_folder.is_dir() and product_folder.name not in ['pod', 'ilustracija']:
                # Izvuci kod iz imena foldera (prvi deo pre -)
                folder_parts = product_folder.name.split('-', 1)
                if folder_parts and folder_parts[0].isdigit():
                    code = folder_parts[0]
                    ilustracija = product_folder / 'ilustracija'
                    
                    if ilustracija.exists() and ilustracija.is_dir():
                        jpg_files = list(ilustracija.glob('*.jpg'))
                        if not jpg_files:
                            empty_ilustracija[collection_name][code] = (ilustracija, product_folder.name)
                        else:
                            # Uzmi prvu sliku
                            has_ilustracija[collection_name][code] = (ilustracija, product_folder.name, jpg_files[0])

# Pronađi i kopiraj ilustracije
copied_count = 0
errors = []

for collection_name, empty_codes in empty_ilustracija.items():
    for code, (target_ilustracija, target_folder_name) in empty_codes.items():
        # Proveri da li isti kod ima ilustraciju u drugoj kolekciji
        for other_collection, has_codes in has_ilustracija.items():
            if other_collection != collection_name and code in has_codes:
                source_ilustracija, source_folder_name, source_image = has_codes[code]
                
                # Kopiraj sliku
                try:
                    # Kreiraj novo ime fajla - zadrži ekstenziju i dodaj -ilustracija ako već nije
                    source_image_name = source_image.name
                    if not source_image_name.endswith('-ilustracija.jpg'):
                        # Ako ime već ima -ilustracija, zadrži ga, inače dodaj
                        name_part = source_image_name.rsplit('.', 1)[0]
                        ext = source_image_name.rsplit('.', 1)[1]
                        if not name_part.endswith('-ilustracija'):
                            new_name = f"{name_part}-ilustracija.{ext}"
                        else:
                            new_name = source_image_name
                    else:
                        new_name = source_image_name
                    
                    target_image = target_ilustracija / new_name
                    
                    # Kopiraj fajl
                    shutil.copy2(source_image, target_image)
                    copied_count += 1
                    
                    if copied_count <= 20:  # Print prvih 20
                        print(f"Kopirano: {code}")
                        print(f"  Iz: {other_collection}/{source_folder_name}/ilustracija/{source_image.name}")
                        print(f"  U: {collection_name}/{target_folder_name}/ilustracija/{new_name}")
                        print()
                    
                    break  # Našli smo jedan, ne treba više tražiti
                except Exception as e:
                    errors.append(f"Greška pri kopiranju {code} iz {other_collection} u {collection_name}: {e}")

print(f"\n{'='*50}")
print(f"Kopirano ilustracija: {copied_count}")

if errors:
    print(f"\nGreške ({len(errors)}):")
    for error in errors[:10]:
        print(f"  - {error}")
    if len(errors) > 10:
        print(f"  ... i još {len(errors) - 10} grešaka")
