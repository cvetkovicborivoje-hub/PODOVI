import sys
import zipfile
import shutil
from pathlib import Path
from PIL import Image
import io
sys.stdout.reconfigure(encoding='utf-8')

print("=" * 80)
print("EKSTRAKCIJA I KORIŠĆENJE ČISTIH GERFLOR SLIKA")
print("=" * 80)
print()

# Folder sa Gerflor zip fajlovima
gerflor_zips = Path('downloads/gerflor_dialog')
products_path = Path('public/images/products/lvt/colors')

if not gerflor_zips.exists():
    print("❌ Gerflor folder ne postoji!")
    sys.exit(1)

replaced = []
errors = []

# Prođi kroz sve kolekcije i proizvode
all_collections = sorted(products_path.glob('*'))

total = 0
for collection_dir in all_collections:
    if not collection_dir.is_dir():
        continue
    
    collection_name = collection_dir.name
    product_dirs = sorted(collection_dir.glob('*'))
    
    for product_dir in product_dirs:
        if not product_dir.is_dir():
            continue
        
        total += 1
        slug = product_dir.name
        main_image = product_dir / f"{slug}.jpg"
        
        if not main_image.exists():
            continue
        
        # Pronađi ZIP fajl za ovaj proizvod u odgovarajućoj kolekciji
        # ZIP-ovi su organizovani: downloads/gerflor_dialog/collection-name/*.zip
        collection_zip_folder = gerflor_zips / collection_name
        
        if collection_zip_folder.exists():
            # Traži ZIP fajl po slug-u
            zip_files = list(collection_zip_folder.glob(f'*{slug}*.zip'))
            
            if zip_files:
                try:
                    # Otvori ZIP
                    with zipfile.ZipFile(zip_files[0], 'r') as zip_ref:
                        # Lista svih JPG fajlova u ZIP-u
                        jpg_files = [f for f in zip_ref.namelist() if f.lower().endswith('.jpg')]
                        
                        if len(jpg_files) >= 2:
                            # Analiziraj obe slike - izaberi VEĆU (obično je čistija)
                            images_data = []
                            for jpg in jpg_files:
                                img_data = zip_ref.read(jpg)
                                size = len(img_data)
                                images_data.append((size, jpg, img_data))
                            
                            # Sortiraj po veličini - VEĆA je obično čist swatch
                            images_data.sort(key=lambda x: x[0], reverse=True)
                            
                            # Uzmi najveću sliku
                            largest_size, largest_name, largest_data = images_data[0]
                            
                            # Sačuvaj kao glavnu sliku
                            with open(main_image, 'wb') as f:
                                f.write(largest_data)
                            
                            replaced.append({
                                'product': f"{collection_name}/{slug}",
                                'zip': zip_files[0].name,
                                'image': largest_name,
                                'size': largest_size
                            })
                            
                            if total % 50 == 0:
                                print(f"[{total}] ✅ {collection_name}/{slug}")
                        
                except Exception as e:
                    errors.append(f"{collection_name}/{slug}: {e}")

print("\n" + "=" * 80)
print("REZULTATI:")
print(f"  📊 Obrađeno: {total}")
print(f"  ✅ Zamenjeno: {len(replaced)}")
print(f"  ❌ Greške: {len(errors)}")
print("=" * 80)

if replaced:
    print(f"\n🎯 Zamenjeno {len(replaced)} proizvoda sa čistim Gerflor slikama!")
    if len(replaced) <= 20:
        for item in replaced:
            print(f"  • {item['product']}")

# Sačuvaj log
with open('gerflor_extraction_log.txt', 'w', encoding='utf-8') as f:
    f.write(f"EKSTRAKCIJA ČISTIH GERFLOR SLIKA\n")
    f.write("=" * 80 + "\n\n")
    f.write(f"Zamenjeno: {len(replaced)}\n")
    f.write(f"Greške: {len(errors)}\n\n")
    
    f.write("ZAMENJENI:\n")
    f.write("-" * 80 + "\n")
    for item in replaced:
        f.write(f"{item['product']}\n")
        f.write(f"  ZIP: {item['zip']}\n")
        f.write(f"  Slika: {item['image']} ({item['size']} bytes)\n\n")

print("\n💾 Log: gerflor_extraction_log.txt")
print("✅ GOTOVO!")
