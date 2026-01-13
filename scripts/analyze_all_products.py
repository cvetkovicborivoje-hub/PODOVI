import sys
import shutil
from pathlib import Path
from PIL import Image
import numpy as np
from scipy import ndimage
sys.stdout.reconfigure(encoding='utf-8')

def detect_objects_visual(image_path):
    """ČISTA VIZUELNA DETEKCIJA - bez gledanja naziva."""
    try:
        img = Image.open(image_path).convert('RGB')
        img_array = np.array(img)
        gray = img.convert('L')
        gray_array = np.array(gray)
        
        score = 0
        
        # 1. DUBINA - 3D scene imaju gradijent
        try:
            vertical_gradient = np.abs(np.gradient(gray_array.mean(axis=1)))
            horizontal_gradient = np.abs(np.gradient(gray_array.mean(axis=0)))
            depth_indicator = np.mean(vertical_gradient) + np.mean(horizontal_gradient)
            if depth_indicator > 10:
                score += 50
        except:
            pass
        
        # 2. JAČINA IVICA - objekti
        edges = ndimage.sobel(gray_array)
        strong_edges = np.sum(np.abs(edges) > 100)
        edge_density = strong_edges / gray_array.size
        if edge_density > 0.05:
            score += 40
        
        # 3. REGIONALNA VARIJANSA
        try:
            h, w = gray_array.shape
            regions = []
            for i in range(4):
                for j in range(4):
                    region = gray_array[i*h//4:(i+1)*h//4, j*w//4:(j+1)*w//4]
                    regions.append(np.mean(region))
            region_variance = np.var(regions)
            if region_variance > 500:
                score += 30
        except:
            pass
        
        # 4. RASPON BOJA
        r, g, b = img_array[:,:,0], img_array[:,:,1], img_array[:,:,2]
        color_ranges = (np.max(r) - np.min(r)) + (np.max(g) - np.min(g)) + (np.max(b) - np.min(b))
        if color_ranges > 400:
            score += 25
        
        # 5. HISTOGRAM
        hist, _ = np.histogram(gray_array, bins=32)
        peaks = np.where(hist > np.max(hist) * 0.3)[0]
        if len(peaks) > 3:
            score += 20
        
        # 6. LOKALNA KOMPLEKSNOST
        try:
            h, w = gray_array.shape
            quadrants = [
                gray_array[:h//2, :w//2],
                gray_array[:h//2, w//2:],
                gray_array[h//2:, :w//2],
                gray_array[h//2:, w//2:]
            ]
            complexities = [np.std(q) for q in quadrants]
            complexity_variance = np.var(complexities)
            if complexity_variance > 200:
                score += 15
        except:
            pass
        
        return score
        
    except Exception as e:
        return 9999

print("=" * 80)
print("ANALIZA SVIH 583 PROIZVODA - Vizuelna detekcija")
print("=" * 80)
print()

base_path = Path('public/images/products/lvt/colors')
all_collections = sorted(base_path.glob('*'))

total_products = 0
replaced = []
unchanged = []
errors = []

for collection_dir in all_collections:
    if not collection_dir.is_dir():
        continue
    
    collection_name = collection_dir.name
    product_dirs = sorted(collection_dir.glob('*'))
    
    for product_dir in product_dirs:
        if not product_dir.is_dir():
            continue
        
        total_products += 1
        slug = product_dir.name
        main_image = product_dir / f"{slug}.jpg"
        
        if not main_image.exists():
            errors.append(f"{collection_name}/{slug}: Nema glavne slike")
            continue
        
        # Analiziraj sve slike
        all_images = list(product_dir.glob('*.jpg'))
        if len(all_images) <= 1:
            unchanged.append(f"{collection_name}/{slug}")
            continue
        
        # Score sve slike
        scored = []
        for img in all_images:
            score = detect_objects_visual(img)
            scored.append((score, img))
        
        scored.sort(key=lambda x: x[0])
        
        # Trenutna slika
        current_score = next(s for s, im in scored if im == main_image)
        best_score, best_image = scored[0]
        
        # Zameni ako je bolja (razlika > 20)
        if best_image != main_image and best_score < current_score - 20:
            try:
                shutil.copy(best_image, main_image)
                replaced.append({
                    'collection': collection_name,
                    'slug': slug,
                    'old': current_score,
                    'new': best_score,
                    'improvement': current_score - best_score
                })
                print(f"[{total_products}] ✅ {collection_name}/{slug}: {current_score}→{best_score}")
            except Exception as e:
                errors.append(f"{collection_name}/{slug}: {e}")
                print(f"[{total_products}] ❌ {collection_name}/{slug}: GREŠKA")
        else:
            unchanged.append(f"{collection_name}/{slug}")
            if total_products % 50 == 0:
                print(f"[{total_products}] Obrađeno...")

print("\n" + "=" * 80)
print("FINALNI REZULTATI:")
print(f"  📊 UKUPNO PROIZVODA: {total_products}")
print(f"  ✅ ZAMENJENO: {len(replaced)}")
print(f"  ⏭️  OSTAVLJENO: {len(unchanged)}")
print(f"  ❌ GREŠKE: {len(errors)}")
print("=" * 80)

if replaced:
    print("\n🎯 TOP 20 POBOLJŠANJA:")
    replaced.sort(key=lambda x: x['improvement'], reverse=True)
    for item in replaced[:20]:
        print(f"  {item['collection']}/{item['slug']}: {item['old']}→{item['new']} (↓{item['improvement']})")

# Sačuvaj log
with open('all_products_analysis.txt', 'w', encoding='utf-8') as f:
    f.write(f"ANALIZA SVIH {total_products} PROIZVODA\n")
    f.write("=" * 80 + "\n\n")
    f.write(f"Zamenjeno: {len(replaced)}\n")
    f.write(f"Ostavljeno: {len(unchanged)}\n")
    f.write(f"Greške: {len(errors)}\n\n")
    
    f.write("ZAMENJENI:\n")
    f.write("-" * 80 + "\n")
    for item in replaced:
        f.write(f"{item['collection']}/{item['slug']}: {item['old']}→{item['new']}\n")

print("\n💾 Log: all_products_analysis.txt")
print("✅ GOTOVO!")
