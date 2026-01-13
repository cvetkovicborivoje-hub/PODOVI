import sys
import json
import shutil
from pathlib import Path
from PIL import Image
import numpy as np
sys.stdout.reconfigure(encoding='utf-8')

def detect_furniture_score(image_path):
    """
    AI detekcija nameštaja - vraća score (0-10).
    Viši score = više nameštaja.
    """
    try:
        img = Image.open(image_path).convert('RGB')
        img_array = np.array(img)
        
        # 1. KOMPLEKSNOST BOJA
        unique_colors = len(np.unique(img_array.reshape(-1, img_array.shape[2]), axis=0))
        color_complexity = unique_colors / (img.size[0] * img.size[1])
        
        # 2. EDGE DETECTION
        gray = img.convert('L')
        gray_array = np.array(gray)
        edges_h = np.abs(np.diff(gray_array, axis=0))
        edges_v = np.abs(np.diff(gray_array, axis=1))
        edge_ratio = (np.sum(edges_h > 30) + np.sum(edges_v > 30)) / gray_array.size
        
        # 3. BRIGHTNESS VARIANCE
        brightness_variance = np.var(gray_array)
        
        # SCORING
        score = 0
        
        if edge_ratio > 0.15:
            score += 3
        
        if brightness_variance > 2000:
            score += 2
        
        if color_complexity > 0.15:
            score += 2
        
        # Dodatni faktori
        if edge_ratio > 0.20:
            score += 2
        
        if brightness_variance > 3000:
            score += 1
        
        return score
        
    except Exception as e:
        print(f"  ⚠️  Greška pri analizi: {e}")
        return 999  # Maksimalan score ako ne može da analizira

def find_cleanest_image(product_dir, main_image):
    """Pronalazi sliku sa najmanje nameštaja koristeći AI."""
    all_images = list(product_dir.glob('*.jpg'))
    
    candidates = []
    for img in all_images:
        if img == main_image:
            continue
        
        score = detect_furniture_score(img)
        candidates.append((score, img))
    
    # Sortiraj po score-u (manji = čistiji)
    candidates.sort(key=lambda x: x[0])
    
    return candidates[0] if candidates else None

print("=" * 80)
print("AI ZAMENA SLIKA - Computer Vision Detekcija Nameštaja")
print("=" * 80)
print()

# Učitaj rezultate
try:
    with open('furniture_review_results.json', 'r', encoding='utf-8') as f:
        results = json.load(f)
    print(f"✅ Učitano {len(results)} proizvoda za analizu\n")
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
    
    # Analiziraj trenutnu sliku
    current_score = detect_furniture_score(main_image)
    print(f"  📊 Trenutna slika score: {current_score}")
    
    # Pronađi najčistiju alternativu
    result = find_cleanest_image(product_dir, main_image)
    
    if not result:
        skipped.append(f"{collection}/{slug}: Nema alternativnih slika")
        print(f"  ⚠️  Nema alternativnih slika!")
        continue
    
    new_score, clean_image = result
    print(f"  🎯 Najbolja alternativa score: {new_score} - {clean_image.name}")
    
    # Zameni samo ako je nova slika čistija
    if new_score < current_score:
        try:
            shutil.copy(clean_image, main_image)
            replaced.append({
                'collection': collection,
                'slug': slug,
                'replacement': clean_image.name,
                'old_score': current_score,
                'new_score': new_score
            })
            print(f"  ✅ ZAMENJENO! {current_score} → {new_score} ({clean_image.name})")
        except Exception as e:
            errors.append(f"{collection}/{slug}: {str(e)}")
            print(f"  ❌ Greška: {e}")
    else:
        skipped.append(f"{collection}/{slug}: Trenutna slika je najbolja ({current_score} vs {new_score})")
        print(f"  ⏭️  Trenutna slika je već najbolja opcija")

# Rezultati
print()
print("=" * 80)
print("REZULTATI:")
print(f"  ✅ Uspešno zamenjeno: {len(replaced)}")
print(f"  ⏭️  Preskočeno (već najbolja): {len(skipped)}")
print(f"  ❌ Greške: {len(errors)}")
print("=" * 80)

# Sačuvaj log
with open('ai_replacement_log.txt', 'w', encoding='utf-8') as f:
    f.write("AI ZAMENA SLIKA - COMPUTER VISION ANALIZA\n")
    f.write("=" * 80 + "\n\n")
    f.write(f"Zamenjeno: {len(replaced)}\n")
    f.write(f"Preskočeno: {len(skipped)}\n")
    f.write(f"Greške: {len(errors)}\n\n")
    f.write("LISTA ZAMENA (sa AI score-ovima):\n")
    f.write("-" * 80 + "\n")
    for item in replaced:
        f.write(f"{item['collection']}/{item['slug']}\n")
        f.write(f"  Score: {item['old_score']} → {item['new_score']}\n")
        f.write(f"  Nova slika: {item['replacement']}\n\n")

print(f"\n💾 Log sačuvan: ai_replacement_log.txt")
print("\n✅ GOTOVO!")
