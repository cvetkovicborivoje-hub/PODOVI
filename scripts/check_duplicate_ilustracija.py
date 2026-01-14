# -*- coding: utf-8 -*-
from pathlib import Path
import json

# Učitaj JSON da znamo koje boje postoje
json_path = Path('public/data/lvt_colors_complete.json')
with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Kreiraj mapu: code -> lista kolekcija gde postoji
code_collections = {}
for color in data['colors']:
    code = color['code']
    collection = color['collection']
    if code not in code_collections:
        code_collections[code] = []
    code_collections[code].append(collection)

base = Path('public/images/products/lvt/colors')
empty_ilustracija = {}  # collection -> {code: folder_name}
has_ilustracija = {}    # collection -> {code: folder_name}

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
                            empty_ilustracija[collection_name][code] = product_folder.name
                        else:
                            has_ilustracija[collection_name][code] = product_folder.name

# Pronađi proizvode koji nemaju ilustraciju u jednoj kolekciji, ali imaju u drugoj
matches = []

for collection_name, empty_codes in empty_ilustracija.items():
    for code, folder_name in empty_codes.items():
        # Proveri da li isti kod ima ilustraciju u drugoj kolekciji
        for other_collection, has_codes in has_ilustracija.items():
            if other_collection != collection_name and code in has_codes:
                matches.append({
                    'code': code,
                    'empty_in': collection_name,
                    'empty_folder': folder_name,
                    'has_in': other_collection,
                    'has_folder': has_codes[code]
                })
                break  # Našli smo jedan, ne treba više tražiti

print(f'\nPronadjeno {len(matches)} proizvoda koji nemaju ilustraciju u jednoj kolekciji, ali imaju u drugoj:\n')

if matches:
    for match in matches[:50]:  # Prvih 50
        print(f"Kod {match['code']}:")
        print(f"  NEMA ilustracije u: {match['empty_in']}/{match['empty_folder']}")
        print(f"  IMA ilustraciju u: {match['has_in']}/{match['has_folder']}")
        print()
    
    if len(matches) > 50:
        print(f'... i jos {len(matches) - 50} proizvoda')
else:
    print('Nema takvih proizvoda.')

print(f'\nUkupno: {len(matches)} proizvoda')
