import sys
import json
import shutil
from pathlib import Path
from PIL import Image
import numpy as np
sys.stdout.reconfigure(encoding='utf-8')

# KLJUČNE REČI ZA NAMEŠTAJ/OBJEKTE - ove slike OBAVEZNO ISKLJUČITI
FURNITURE_KEYWORDS = [
    'sky view', 'skyview', 'room scene', 'chambre', 'kitchen', 'bathroom', 
    'bedroom', 'living room', 'office', 'restaurant', 'lounge', 'hall', 
    'hotel', 'vdc', 'rs78', 'rs75', 'rs74', 'rs76', 'rs77',
    'room', 'scene', 'view', 'interior', 'decor'
]

def has_furniture_keywords(filename):
    """Proverava da li fajl IMA nameštaj/objekte po imenu."""
    filename_lower = filename.lower()
    for keyword in FURNITURE_KEYWORDS:
        if keyword in filename_lower:
            return True
    return False

def calculate_simplicity_score(image_path):
    """
    Računa koliko je slika JEDNOSTAVNA (čista tekstura).
    MANJI score = jednostavnija = bolja za swatch.
    """
    try:
        img = Image.open(image_path).convert('RGB')
        img_array = np.array(img)
        gray = img.convert('L')
        gray_array = np.array(gray)
        
        # Čista tekstura treba da ima:
        # 1. MALO ivica (nema objekata)
        edges_h = np.abs(np.diff(gray_array, axis=0))
        edges_v = np.abs(np.diff(gray_array, axis=1))
        edge_count = (np.sum(edges_h > 30) + np.sum(edges_v > 30)) / gray_array.size
        
        # 2. UNIFORMNU svetlost (nema senki)
        brightness_std = np.std(gray_array)
        
        # 3. JEDNOSTAVNU paletu boja (samo tekstura)
        color_std = np.mean(np.std(img_array, axis=(0,1)))
        
        # Score: manji = bolji
        score = (edge_count * 100) + (brightness_std / 10) + (color_std / 2)
        
        return score
        
    except Exception as e:
        return 9999  # Greška = najgori score

def find_best_clean_swatch(product_dir, main_image):
    """
    Pronalazi NAJČISTIJU teksturu:
    1. Prvo eliminiše SVE slike sa ključnim rečima
    2. Od preostalih bira najjednostavniju
    """
    all_images = list(product_dir.glob('*.jpg'))
    
    # KORAK 1: Filtriraj - ukloni SVE sa ključnim rečima
    clean_candidates = []
    for img in all_images:
        if img == main_image:
            continue
        
        if has_furniture_keywords(img.name):
            continue  # PRESKAČI slike sa nameštajem
        
        clean_candidates.append(img)
    
    if not clean_candidates:
        return None, "Nema slika bez ključnih reči"
    
    # KORAK 2: Od čistih, nađi najjednostavniju
    scored_images = []
    for img in clean_candidates:
        score = calculate_simplicity_score(img)
        scored_images.append((score, img))
    
    # Sortiraj - najmanji score = najbolji
    scored_images.sort(key=lambda x: x[0])
    
    return scored_images[0][1], None

print("=" * 80)
print("PRAVILAN IZBOR SWATCH-EVA")
print("=" * 80)
print()

# Učitaj rezultate
try:
    with open('furniture_review_results.json', 'r', encoding='utf-8') as f:
        results = json.load(f)
    print(f"✅ Analiziram {len(results)} proizvoda\n")
except FileNotFoundError:
    print("❌ furniture_review_results.json nije pronađen!")
    sys.exit(1)

base_path = Path('public/images/products/lvt/colors')
replaced = []
no_clean_images = []
errors = []

for i, product in enumerate(results, 1):
    collection = product['collection']
    slug = product['slug']
    
    print(f"[{i}/{len(results)}] {collection}/{slug}")
    
    product_dir = base_path / collection / slug
    main_image = product_dir / f"{slug}.jpg"
    
    if not product_dir.exists() or not main_image.exists():
        errors.append(f"{collection}/{slug}")
        print(f"  ❌ Fajlovi ne postoje!")
        continue
    
    # Proveri trenutnu sliku
    if has_furniture_keywords(main_image.name):
        print(f"  ⚠️  TRENUTNA slika ima ključne reči u imenu!")
    
    # Nađi najbolju čistu
    best_image, error = find_best_clean_swatch(product_dir, main_image)
    
    if error:
        no_clean_images.append(f"{collection}/{slug}: {error}")
        print(f"  🔴 {error}")
        continue
    
    if best_image:
        try:
            shutil.copy(best_image, main_image)
            replaced.append({
                'collection': collection,
                'slug': slug,
                'new_image': best_image.name
            })
            print(f"  ✅ Zamenjeno: {best_image.name[:60]}")
        except Exception as e:
            errors.append(f"{collection}/{slug}: {e}")
            print(f"  ❌ Greška: {e}")

# Rezultati
print("\n" + "=" * 80)
print("REZULTATI:")
print(f"  ✅ ZAMENJENO: {len(replaced)}")
print(f"  🔴 NEMA ČISTIH SLIKA: {len(no_clean_images)}")
print(f"  ❌ GREŠKE: {len(errors)}")
print("=" * 80)

# Sačuvaj log
with open('proper_replacement_log.txt', 'w', encoding='utf-8') as f:
    f.write("PRAVILNA ZAMENA - SAMO ČISTE TEKSTURE\n")
    f.write("=" * 80 + "\n\n")
    f.write(f"Zamenjeno: {len(replaced)}\n")
    f.write(f"Nema čistih slika: {len(no_clean_images)}\n")
    f.write(f"Greške: {len(errors)}\n\n")
    
    f.write("ZAMENJENI:\n")
    f.write("-" * 80 + "\n")
    for item in replaced:
        f.write(f"{item['collection']}/{item['slug']}\n")
        f.write(f"  → {item['new_image']}\n\n")
    
    if no_clean_images:
        f.write("\n\nNEMA ČISTIH SLIKA (ručna provera!):\n")
        f.write("-" * 80 + "\n")
        for item in no_clean_images:
            f.write(f"{item}\n")

print(f"\n💾 Log: proper_replacement_log.txt")
print("\n✅ GOTOVO!")
