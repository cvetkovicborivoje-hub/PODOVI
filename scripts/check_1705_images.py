# -*- coding: utf-8 -*-
from pathlib import Path

folder = Path('public/images/products/lvt/colors/creation-30/1705-aquinoah-brown')
print(f'Folder postoji: {folder.exists()}')

if folder.exists():
    pod = folder / 'pod'
    il = folder / 'ilustracija'
    
    pod_imgs = list(pod.glob('*.jpg')) if pod.exists() else []
    il_imgs = list(il.glob('*.jpg')) if il.exists() else []
    
    print(f'\nPod slike ({len(pod_imgs)}):')
    for img in pod_imgs:
        print(f'  - {img.name}')
    
    print(f'\nIlustracija slike ({len(il_imgs)}):')
    for img in il_imgs:
        print(f'  - {img.name}')
