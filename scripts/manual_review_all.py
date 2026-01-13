import sys
import shutil
from pathlib import Path
import webbrowser
import time
sys.stdout.reconfigure(encoding='utf-8')

# Prikupljanje svih proizvoda
base_path = Path('public/images/products/lvt/colors')
all_products = []

print("=" * 80)
print("INTERAKTIVNI PREGLED SLIKA")
print("=" * 80)
print("\n📊 Prikupljam proizvode...")

for collection_dir in sorted(base_path.iterdir()):
    if not collection_dir.is_dir():
        continue
    for product_dir in sorted(collection_dir.iterdir()):
        if product_dir.is_dir():
            slug = product_dir.name
            main_image = product_dir / f"{slug}.jpg"
            if main_image.exists():
                all_images = list(product_dir.glob('*.jpg'))
                if len(all_images) >= 2:  # Mora da ima bar 2 slike
                    all_products.append({
                        'collection': collection_dir.name,
                        'slug': slug,
                        'main_image': main_image,
                        'all_images': [img for img in all_images if img != main_image]
                    })

print(f"✅ Pronađeno {len(all_products)} proizvoda sa više slika")
print()
print("=" * 80)
print("INSTRUKCIJE:")
print("  - Za svaki proizvod ću otvoriti sliku u browser-u")
print("  - Unesi 'y' ako IMA nameštaj (zameniću sa drugom slikom)")
print("  - Unesi 'n' ako NEMA nameštaj (ostaviću)")
print("  - Unesi 's' da preskočiš")
print("  - Unesi 'q' da završiš")
print("=" * 80)
print("\n🚀 POČINJEM...\n")

replaced = []
skipped = []

for i, product in enumerate(all_products, 1):
    print(f"\n[{i}/{len(all_products)}] {product['collection']}/{product['slug']}")
    
    # Otvori sliku u browser-u
    file_url = f"file:///{product['main_image'].absolute().as_posix()}"
    webbrowser.open(file_url)
    
    # Čekaj malo da se učita
    time.sleep(0.5)
    
    # Pitaj korisnika
    while True:
        answer = input("  Ima nameštaj? (y/n/s/q): ").strip().lower()
        
        if answer == 'q':
            print("\n🛑 Prekinuto!")
            break
        elif answer == 's':
            skipped.append(product['slug'])
            print("  ⏭️  Preskočeno")
            break
        elif answer == 'n':
            print("  ✅ OK - ostavljeno")
            break
        elif answer == 'y':
            # Pronađi najbolju zamenu
            if product['all_images']:
                # Uzmi prvu dostupnu sliku
                replacement = product['all_images'][0]
                print(f"  🔧 Zamenjujem sa: {replacement.name}")
                shutil.copy(replacement, product['main_image'])
                replaced.append({
                    'collection': product['collection'],
                    'slug': product['slug'],
                    'old': product['main_image'].name,
                    'new': replacement.name
                })
                print("  ✅ Zamenjeno!")
            else:
                print("  ⚠️  Nema druge slike za zamenu!")
            break
        else:
            print("  ⚠️  Unesi y, n, s ili q!")
    
    if answer == 'q':
        break

# Rezultati
print()
print("=" * 80)
print("REZULTATI:")
print(f"  ✅ Pregledano: {i}")
print(f"  🔧 Zamenjeno: {len(replaced)}")
print(f"  ⏭️  Preskočeno: {len(skipped)}")
print("=" * 80)

if replaced:
    print("\n📋 LISTA ZAMENA:")
    for item in replaced:
        print(f"  • {item['collection']}/{item['slug']}: {item['old']} → {item['new']}")

# Sačuvaj log
with open('manual_replacements_log.txt', 'w', encoding='utf-8') as f:
    f.write("RUČNE ZAMENE SLIKA\n")
    f.write("=" * 80 + "\n\n")
    for item in replaced:
        f.write(f"{item['collection']}/{item['slug']}: {item['old']} → {item['new']}\n")

print(f"\n💾 Log sačuvan u: manual_replacements_log.txt")
print("\n✅ GOTOVO!")
