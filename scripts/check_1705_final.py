# -*- coding: utf-8 -*-
import json
from pathlib import Path

json_path = Path('public/data/lvt_colors_complete.json')
data = json.load(open(json_path, 'r', encoding='utf-8'))
color = [c for c in data['colors'] if c['code'] == '1705' and c['collection'] == 'creation-30'][0]

print('1705 AQUINOAH BROWN:')
print(f'texture_url: {color.get("texture_url", "N/A")}')

# Proveri da li fajl postoji
folder = Path('public/images/products/lvt/colors/creation-30/1705-aquinoah-brown/pod')
if folder.exists():
    images = list(folder.glob('*.jpg'))
    print(f'\nSlike u pod/ folderu:')
    for img in images:
        print(f'  - {img.name}')
        print(f'    Postoji: {img.exists()}')
