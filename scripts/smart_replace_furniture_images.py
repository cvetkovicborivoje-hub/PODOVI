import sys
import json
import shutil
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')

# Ključne reči koje ukazuju na nameštaj u imenu slike
FURNITURE_KEYWORDS = [
    'sky view', 'room scene', 'chambre', 'kitchen', 'bathroom', 'bedroom',
    'living room', 'office', 'restaurant', 'vdc', 'rs78', 'rs75',
    'lounge', 'hall', 'hotel', 'rs74', 'rs76'
]

def has_furniture_keyword(filename):
    """Proverava da li ime fajla sadrži ključne reči za nameštaj."""
    filename_lower = filename.lower()
    return any(keyword in filename_lower for keyword in FURNITURE_KEYWORDS)

def find_clean_swatch(product_dir, main_image):
    """Pronalazi najčistiju swatch sliku bez nameštaja."""
    all_images = list(product_dir.glob('*.jpg'))
    
    # Sortiraj po prioritetu - kraći nazivi su obično čistiji swatch-evi
    candidates = []
    for img in all_images:
        if img == main_image:
            continue
        
        # Preskoči slike sa nameštajem u imenu
        if has_furniture_keyword(img.name):
            continue
        
        # Preferiraj kraće nazive (obično su to čisti swatch-evi)
        priority = len(img.name)
        candidates.append((priority, img))
    
    # Sortiraj po prioritetu (kraće ime = bolji prioritet)
    candidates.sort(key=lambda x: x[0])
    
    return candidates[0][1] if candidates else None

print("=" * 80)
print("PAMETNA ZAMENA SLIKA - Samo čisti swatch-evi")
print("=" * 80)
print()

# Učitaj rezultate
try:
    with open('furniture_review_results.json', 'r', encoding='utf-8') as f:
        results = json.load(f)
    print(f"✅ Učitano {len(results)} proizvoda za proveru\n")
except FileNotFoundError:
    print("❌ Fajl 'furniture_review_results.json' nije pronađen!")
    sys.exit(1)

# Primeni zamene
base_path = Path('public/images/products/lvt/colors')
replaced = []
errors = []
skipped = []

for i, product in enumerate(results, 1):
    collection = product['collection']
    slug = product['slug']
    
    print(f"[{i}/{len(results)}] {collection}/{slug}")
    
    product_dir = base_path / collection / slug
    main_image = product_dir / f"{slug}.jpg"
    
    if not product_dir.exists():
        errors.append(f"{collection}/{slug}: Folder ne postoji")
        print(f"  ❌ Folder ne postoji!")
        continue
    
    if not main_image.exists():
        errors.append(f"{collection}/{slug}: Glavna slika ne postoji")
        print(f"  ❌ Glavna slika ne postoji!")
        continue
    
    # Pronađi čist swatch
    clean_swatch = find_clean_swatch(product_dir, main_image)
    
    if not clean_swatch:
        skipped.append(f"{collection}/{slug}: Nema čistog swatch-a")
        print(f"  ⚠️  Nema čistog swatch-a (sve imaju nameštaj)!")
        continue
    
    # Zameni
    try:
        shutil.copy(clean_swatch, main_image)
        replaced.append({
            'collection': collection,
            'slug': slug,
            'replacement': clean_swatch.name
        })
        print(f"  ✅ Zamenjeno sa: {clean_swatch.name}")
    except Exception as e:
        errors.append(f"{collection}/{slug}: {str(e)}")
        print(f"  ❌ Greška: {e}")

# Rezultati
print()
print("=" * 80)
print("REZULTATI:")
print(f"  ✅ Uspešno zamenjeno: {len(replaced)}")
print(f"  ⚠️  Preskočeno (nema čistog): {len(skipped)}")
print(f"  ❌ Greške: {len(errors)}")
print("=" * 80)

if skipped:
    print("\n⚠️  PRESKOČENI PROIZVODI (trebaju ručnu proveru):")
    for item in skipped[:20]:
        print(f"  • {item}")
    if len(skipped) > 20:
        print(f"  ... i još {len(skipped) - 20}")

if errors:
    print("\n❌ GREŠKE:")
    for error in errors[:10]:
        print(f"  • {error}")
    if len(errors) > 10:
        print(f"  ... i još {len(errors) - 10} grešaka")

# Sačuvaj log
with open('smart_replacement_log.txt', 'w', encoding='utf-8') as f:
    f.write("PAMETNA ZAMENA SLIKA - SAMO ČISTI SWATCH-EVI\n")
    f.write("=" * 80 + "\n\n")
    f.write(f"Zamenjeno: {len(replaced)}\n")
    f.write(f"Preskočeno: {len(skipped)}\n")
    f.write(f"Greške: {len(errors)}\n\n")
    f.write("LISTA ZAMENA:\n")
    f.write("-" * 80 + "\n")
    for item in replaced:
        f.write(f"{item['collection']}/{item['slug']} → {item['replacement']}\n")
    
    if skipped:
        f.write("\n\nPRESKOČENI (Nema čistog swatch-a):\n")
        f.write("-" * 80 + "\n")
        for item in skipped:
            f.write(f"{item}\n")
    
    if errors:
        f.write("\n\nGREŠKE:\n")
        f.write("-" * 80 + "\n")
        for error in errors:
            f.write(f"{error}\n")

print(f"\n💾 Log sačuvan: smart_replacement_log.txt")
print("\n✅ GOTOVO!")
