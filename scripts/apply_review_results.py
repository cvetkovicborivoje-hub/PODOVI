import sys
import json
import shutil
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')

print("=" * 80)
print("PRIMENA RUČNOG PREGLEDA")
print("=" * 80)
print()

# Učitaj rezultate
try:
    with open('furniture_review_results.json', 'r', encoding='utf-8') as f:
        results = json.load(f)
    print(f"✅ Učitano {len(results)} proizvoda za zamenu\n")
except FileNotFoundError:
    print("❌ Fajl 'furniture_review_results.json' nije pronađen!")
    print("   Preuzmi JSON iz HTML stranice i sačuvaj kao 'furniture_review_results.json'")
    sys.exit(1)

if not results:
    print("✅ Nema proizvoda za zamenu!")
    sys.exit(0)

# Primeni zamene
base_path = Path('public/images/products/lvt/colors')
replaced = []
errors = []

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
    
    # Pronađi alternativne slike
    all_images = list(product_dir.glob('*.jpg'))
    alternative_images = [img for img in all_images if img != main_image]
    
    if not alternative_images:
        errors.append(f"{collection}/{slug}: Nema alternativnih slika")
        print(f"  ⚠️  Nema alternativnih slika!")
        continue
    
    # Uzmi prvu alternativnu sliku
    replacement = alternative_images[0]
    
    # Zameni
    try:
        shutil.copy(replacement, main_image)
        replaced.append({
            'collection': collection,
            'slug': slug,
            'replacement': replacement.name
        })
        print(f"  ✅ Zamenjeno sa: {replacement.name}")
    except Exception as e:
        errors.append(f"{collection}/{slug}: {str(e)}")
        print(f"  ❌ Greška: {e}")

# Rezultati
print()
print("=" * 80)
print("REZULTATI:")
print(f"  ✅ Uspešno zamenjeno: {len(replaced)}")
print(f"  ❌ Greške: {len(errors)}")
print("=" * 80)

if errors:
    print("\n⚠️  GREŠKE:")
    for error in errors[:10]:  # Prikaži prvih 10
        print(f"  • {error}")
    if len(errors) > 10:
        print(f"  ... i još {len(errors) - 10} grešaka")

# Sačuvaj log
with open('replacement_log.txt', 'w', encoding='utf-8') as f:
    f.write("AUTOMATSKE ZAMENE SLIKA NA OSNOVU RUČNOG PREGLEDA\n")
    f.write("=" * 80 + "\n\n")
    f.write(f"Zamenjeno: {len(replaced)}\n")
    f.write(f"Greške: {len(errors)}\n\n")
    f.write("LISTA ZAMENA:\n")
    f.write("-" * 80 + "\n")
    for item in replaced:
        f.write(f"{item['collection']}/{item['slug']} → {item['replacement']}\n")
    if errors:
        f.write("\n\nGREŠKE:\n")
        f.write("-" * 80 + "\n")
        for error in errors:
            f.write(f"{error}\n")

print(f"\n💾 Log sačuvan: replacement_log.txt")
print("\n✅ GOTOVO! Sada commit-uj i push-uj izmene!")
