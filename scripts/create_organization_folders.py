#!/usr/bin/env python3
"""
Kreira dodatne foldere 'pod' i 'ilustracija' u svakom proizvodnom folderu
koji ima tačno 2 JPG slike, kako bi korisnik mogao ručno da rasporedi slike.
"""

import os
from pathlib import Path

def create_organization_folders():
    base_path = Path("public/images/products/lvt/colors")
    
    if not base_path.exists():
        print(f"Putanja ne postoji: {base_path}")
        return
    
    folders_processed = 0
    folders_created = 0
    
    # Prođi kroz sve foldere rekurzivno
    for folder in base_path.rglob("*"):
        if not folder.is_dir():
            continue
        
        # Preskoči ako već ima "pod" ili "ilustracija" podfolder (znači da je parent folder)
        if folder.name in ["pod", "ilustracija"]:
            continue
        
        # Preskoči root i kolekcijske foldere - traži samo proizvodne foldere
        # Proizvodni folderi su na nivou 2 (npr. creation-30/ballerina-41870347/)
        relative_depth = len(folder.relative_to(base_path).parts)
        if relative_depth != 2:  # Samo folderi na nivou 2 (proizvodni folderi)
            continue
        
        # Proveri da li folder ima barem 2 JPG fajla
        jpg_files = list(folder.glob("*.jpg"))
        
        if len(jpg_files) >= 2:
            folders_processed += 1
            
            # Kreiraj folder 'pod' ako ne postoji
            pod_folder = folder / "pod"
            if not pod_folder.exists():
                pod_folder.mkdir(parents=False, exist_ok=True)
                folders_created += 1
                rel_path = os.path.relpath(pod_folder, Path.cwd())
                print(f"Kreiran folder: {rel_path}")
            
            # Kreiraj folder 'ilustracija' ako ne postoji
            ilustracija_folder = folder / "ilustracija"
            if not ilustracija_folder.exists():
                ilustracija_folder.mkdir(parents=False, exist_ok=True)
                folders_created += 1
                rel_path = os.path.relpath(ilustracija_folder, Path.cwd())
                print(f"Kreiran folder: {rel_path}")
    
    print(f"\nProcesirano foldera sa 2+ slika: {folders_processed}")
    print(f"Kreirano novih foldera: {folders_created}")
    print(f"\nSada mozete rucno da rasporedite slike prevlacenjem u 'pod' ili 'ilustracija' foldere.")

if __name__ == "__main__":
    create_organization_folders()
