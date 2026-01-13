import sys
import shutil
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')

# Ključne reči za lifestyle slike (SA NAMEŠTAJEM)
FURNITURE_KEYWORDS = [
    'sky view', 'sky-view', 'skyview',
    'room scene', 'room-scene', 'roomscene',
    'kitchen', 'chambre', 'bedroom', 'living room',
    'terra-nova', 'living', 'scene',
    'rs78', 'rs74', 'vdc'  # Često u lifestyle slikama
]

def has_furniture_in_name(filename):
    """Proverava da li ime fajla ukazuje na lifestyle sliku"""
    filename_lower = filename.lower()
    return any(keyword in filename_lower for keyword in FURNITURE_KEYWORDS)

# Glavna putanja
base_path = Path('public/images/products/lvt/colors')
products_to_fix = []
total_products = 0
already_ok = 0

print("=" * 80)
print("AUTOMATSKI PREGLED SVIH PROIZVODA")
print("=" * 80)
print()

# Prolazi kroz sve kolekcije
for collection_dir in sorted(base_path.iterdir()):
    if not collection_dir.is_dir():
        continue
    
    collection = collection_dir.name
    print(f"\n🔍 Kolekcija: {collection}")
    
    # Prolazi kroz sve proizvode u kolekciji
    for product_dir in sorted(collection_dir.iterdir()):
        if not product_dir.is_dir():
            continue
        
        total_products += 1
        slug = product_dir.name
        
        # Pronalazi sve slike u folderu
        all_images = list(product_dir.glob('*.jpg'))
        
        # Glavni fajl
        main_image = product_dir / f"{slug}.jpg"
        
        if not main_image.exists():
            continue
        
        # Originalne slike (bez glavne)
        original_images = [img for img in all_images if img != main_image]
        
        if len(original_images) < 2:
            already_ok += 1
            continue
        
        # Pronalazi lifestyle i swatch slike
        lifestyle_images = [img for img in original_images if has_furniture_in_name(img.name)]
        swatch_images = [img for img in original_images if not has_furniture_in_name(img.name)]
        
        if not swatch_images:
            print(f"  ⚠️  {slug}: Nema swatch sliku!")
            continue
        
        # Proverava da li glavna slika koristi lifestyle
        main_size = main_image.stat().st_size
        
        # Da li glavna slika odgovara nekoj od lifestyle slika?
        uses_lifestyle = False
        for lifestyle_img in lifestyle_images:
            if lifestyle_img.stat().st_size == main_size:
                uses_lifestyle = True
                break
        
        if uses_lifestyle:
            # Treba zameniti sa swatch slikom
            best_swatch = swatch_images[0]  # Uzmi prvu swatch sliku
            products_to_fix.append({
                'collection': collection,
                'slug': slug,
                'current': main_image,
                'replace_with': best_swatch
            })
            print(f"  ❌ {slug}: Koristi lifestyle → zameni sa {best_swatch.name}")
        else:
            already_ok += 1

print()
print("=" * 80)
print(f"📊 STATISTIKA:")
print(f"   Ukupno proizvoda: {total_products}")
print(f"   ✅ Već OK: {already_ok}")
print(f"   ❌ Treba popraviti: {len(products_to_fix)}")
print("=" * 80)
print()

if products_to_fix:
    print("🔧 ZAMENJUJEM SLIKE...")
    print()
    
    for i, product in enumerate(products_to_fix, 1):
        print(f"[{i}/{len(products_to_fix)}] {product['collection']}/{product['slug']}")
        shutil.copy(product['replace_with'], product['current'])
    
    print()
    print("=" * 80)
    print(f"✅ GOTOVO! Zamenjeno {len(products_to_fix)} slika!")
    print("=" * 80)
else:
    print("✅ Sve slike su već dobre!")
