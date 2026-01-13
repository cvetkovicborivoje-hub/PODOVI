import sys
import shutil
from pathlib import Path
from PIL import Image
import numpy as np
sys.stdout.reconfigure(encoding='utf-8')

def detect_furniture(image_path):
    """
    Napredna detekcija nameštaja na slici.
    Vraća True ako slika ima nameštaj (lifestyle), False ako je swatch.
    """
    try:
        img = Image.open(image_path).convert('RGB')
        img_array = np.array(img)
        
        # 1. KOMPLEKSNOST BOJA - swatch ima malo različitih boja
        unique_colors = len(np.unique(img_array.reshape(-1, img_array.shape[2]), axis=0))
        color_complexity = unique_colors / (img.size[0] * img.size[1])
        
        # 2. EDGE DETECTION - nameštaj ima mnogo ivica
        gray = img.convert('L')
        gray_array = np.array(gray)
        edges_h = np.abs(np.diff(gray_array, axis=0))
        edges_v = np.abs(np.diff(gray_array, axis=1))
        edge_ratio = (np.sum(edges_h > 30) + np.sum(edges_v > 30)) / gray_array.size
        
        # 3. BRIGHTNESS VARIANCE - swatch je ravnomerniji
        brightness_variance = np.var(gray_array)
        
        # 4. HISTOGRAM UNIFORMNOST - swatch ima uniformniji histogram
        hist, _ = np.histogram(gray_array, bins=50)
        hist_std = np.std(hist)
        
        # 5. ASPECT RATIO - lifestyle slike često imaju specifičan aspect ratio
        aspect_ratio = img.size[0] / img.size[1]
        
        # SCORING SYSTEM
        score = 0
        reasons = []
        
        # Visoka kompleksnost boja = lifestyle
        if color_complexity > 0.15:
            score += 2
            reasons.append(f"high_color_complexity={color_complexity:.3f}")
        
        # Mnogo ivica = lifestyle
        if edge_ratio > 0.15:
            score += 3
            reasons.append(f"high_edges={edge_ratio:.3f}")
        
        # Visoka variance = lifestyle
        if brightness_variance > 2000:
            score += 2
            reasons.append(f"high_variance={brightness_variance:.0f}")
        
        # Neravnomeran histogram = lifestyle
        if hist_std > 200:
            score += 2
            reasons.append(f"uneven_hist={hist_std:.0f}")
        
        # Čudan aspect ratio = možda lifestyle
        if aspect_ratio < 0.8 or aspect_ratio > 1.2:
            score += 1
            reasons.append(f"aspect={aspect_ratio:.2f}")
        
        # Ako score >= 5, verovatno je lifestyle (ima nameštaj)
        has_furniture = score >= 5
        
        return {
            'has_furniture': has_furniture,
            'score': score,
            'reasons': reasons,
            'metrics': {
                'color_complexity': color_complexity,
                'edge_ratio': edge_ratio,
                'brightness_variance': brightness_variance,
                'hist_std': hist_std,
                'aspect_ratio': aspect_ratio
            }
        }
    
    except Exception as e:
        print(f"  ⚠️  Greška: {e}")
        return {'has_furniture': False, 'score': 0, 'reasons': [], 'metrics': {}}

# Glavna putanja
base_path = Path('public/images/products/lvt/colors')
products_to_fix = []
total_products = 0
already_ok = 0
false_positives = []

print("=" * 80)
print("NAPREDNA AI DETEKCIJA NAMEŠTAJA")
print("=" * 80)
print()

# Prolazi kroz sve kolekcije
for collection_dir in sorted(base_path.iterdir()):
    if not collection_dir.is_dir():
        continue
    
    collection = collection_dir.name
    print(f"\n🔍 Kolekcija: {collection}")
    
    # Prolazi kroz sve proizvode
    for idx, product_dir in enumerate(sorted(collection_dir.iterdir()), 1):
        if not product_dir.is_dir():
            continue
        
        total_products += 1
        slug = product_dir.name
        
        # Progress indicator
        if idx % 10 == 0:
            print(f"  📊 Proverio {idx} proizvoda u {collection}...", flush=True)
        
        # Sve slike
        all_images = list(product_dir.glob('*.jpg'))
        main_image = product_dir / f"{slug}.jpg"
        
        if not main_image.exists() or len(all_images) < 2:
            already_ok += 1
            continue
        
        # Testiraj glavnu sliku
        main_result = detect_furniture(main_image)
        
        if main_result['has_furniture']:
            # Pronađi najbolji swatch
            original_images = [img for img in all_images if img != main_image]
            best_swatch = None
            min_score = 999
            
            for img in original_images:
                result = detect_furniture(img)
                if not result['has_furniture'] and result['score'] < min_score:
                    best_swatch = img
                    min_score = result['score']
            
            if best_swatch:
                products_to_fix.append({
                    'collection': collection,
                    'slug': slug,
                    'current': main_image,
                    'replace_with': best_swatch,
                    'score': main_result['score'],
                    'reasons': main_result['reasons']
                })
                print(f"  ❌ {slug}: score={main_result['score']} ({', '.join(main_result['reasons'][:2])})")
            else:
                false_positives.append(slug)
                print(f"  ⚠️  {slug}: detektovan nameštaj ali nema swatch zamenu")
        else:
            already_ok += 1

print()
print("=" * 80)
print(f"📊 STATISTIKA:")
print(f"   Ukupno: {total_products}")
print(f"   ✅ Već OK: {already_ok}")
print(f"   ❌ Treba popraviti: {len(products_to_fix)}")
print(f"   ⚠️  False positives: {len(false_positives)}")
print("=" * 80)
print()

if products_to_fix:
    print(f"🔧 ZAMENJUJEM {len(products_to_fix)} SLIKA...")
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
