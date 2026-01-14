# -*- coding: utf-8 -*-
from pathlib import Path

base = Path('public/images/products/lvt/colors')
empty_count = 0
total_count = 0
empty_folders = []

for collection in base.iterdir():
    if collection.is_dir() and collection.name.startswith('creation'):
        for product_folder in collection.iterdir():
            if product_folder.is_dir() and product_folder.name not in ['pod', 'ilustracija']:
                ilustracija = product_folder / 'ilustracija'
                if ilustracija.exists() and ilustracija.is_dir():
                    total_count += 1
                    jpg_files = list(ilustracija.glob('*.jpg'))
                    if not jpg_files:
                        empty_count += 1
                        empty_folders.append(f"{collection.name}/{product_folder.name}")

print(f'\nPraznih foldera ilustracija: {empty_count} od {total_count} ukupno\n')

if empty_folders:
    print('Prazni folderi:')
    for folder in empty_folders[:30]:  # Prvih 30
        print(f'  - {folder}')
    if len(empty_folders) > 30:
        print(f'  ... i jos {len(empty_folders) - 30} foldera')
