# -*- coding: utf-8 -*-
from pathlib import Path

def check_collection_structure(collection_name):
    """Proverava strukturu foldera za datu kolekciju"""
    base = Path(f'public/images/products/lvt/colors/{collection_name}')
    
    if not base.exists():
        print(f"{collection_name}: Folder ne postoji")
        return
    
    folders = [f for f in base.iterdir() if f.is_dir() and f.name not in ['pod', 'ilustracija']]
    print(f"\n{collection_name}: {len(folders)} proizvodnih foldera")
    
    # Proveri prvih 3 foldera
    for folder in folders[:3]:
        pod = folder / 'pod'
        il = folder / 'ilustracija'
        pod_images = list(pod.glob('*.jpg')) if pod.exists() else []
        il_images = list(il.glob('*.jpg')) if il.exists() else []
        print(f"  {folder.name}: pod/{len(pod_images)} slika, ilustracija/{len(il_images)} slika")

if __name__ == "__main__":
    collections = [
        'creation-40',
        'creation-40-clic',
        'creation-40-clic-acoustic',
        'creation-40-zen',
        'creation-55',
        'creation-55-clic',
        'creation-55-clic-acoustic',
        'creation-55-looselay',
        'creation-55-looselay-acoustic',
        'creation-55-zen'
    ]
    
    for col in collections:
        check_collection_structure(col)
