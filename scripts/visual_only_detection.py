import sys
import json
import shutil
from pathlib import Path
from PIL import Image
import numpy as np
from scipy import ndimage
sys.stdout.reconfigure(encoding='utf-8')

def detect_objects_visual(image_path):
    """
    ČISTA VIZUELNA DETEKCIJA - detektuje da li slika ima objekte.
    Vraća score: VEĆI = više objekata, MANJI = čistija tekstura
    """
    try:
        img = Image.open(image_path).convert('RGB')
        img_array = np.array(img)
        gray = img.convert('L')
        gray_array = np.array(gray)
        
        score = 0
        
        # 1. DUBINA DETEKCIJA - 3D scene imaju gradijent svetlosti (senke, perspektiva)
        # Čista tekstura je RAVNA - uniformna svetlost
        vertical_gradient = np.abs(np.gradient(gray_array.mean(axis=1)))
        horizontal_gradient = np.abs(np.gradient(gray_array.mean(axis=0)))
        depth_indicator = np.mean(vertical_gradient) + np.mean(horizontal_gradient)
        
        if depth_indicator > 10:  # Ima dubinu = scena
            score += 50
        
        # 2. DISTINCT EDGES - objekti imaju jasne, definisane ivice
        # Tekstura ima samo ponavljajući pattern
        edges = ndimage.sobel(gray_array)
        strong_edges = np.sum(np.abs(edges) > 100)
        edge_density = strong_edges / gray_array.size
        
        if edge_density > 0.05:  # Mnogo jakih ivica = objekti
            score += 40
        
        # 3. KONTRASTNA REGIONA - objekti kreiraju različite regione
        # Čista tekstura je uniformna
        regions = gray_array.reshape(-1, gray_array.shape[1] // 4, 4).mean(axis=2)
        region_variance = np.var([np.mean(regions[i]) for i in range(len(regions))])
        
        if region_variance > 500:  # Velika varijansa između regiona = objekti
            score += 30
        
        # 4. COLOR DIVERSITY - objekti imaju različite boje
        # Tekstura ima samo boju materijala
        r, g, b = img_array[:,:,0], img_array[:,:,1], img_array[:,:,2]
        color_ranges = (np.max(r) - np.min(r)) + (np.max(g) - np.min(g)) + (np.max(b) - np.min(b))
        
        if color_ranges > 400:  # Veliki raspon boja = razni objekti
            score += 25
        
        # 5. HISTOGRAM ANALIZA - objekti imaju multi-modal histogram
        # Tekstura ima jednostavan histogram
        hist, _ = np.histogram(gray_array, bins=32)
        peaks = np.where(hist > np.max(hist) * 0.3)[0]
        
        if len(peaks) > 3:  # Više pikova = različiti objekti/svetla
            score += 20
        
        # 6. LOCAL COMPLEXITY - objekti kreiraju različitu kompleksnost u različitim delovima
        # Tekstura je uniformno kompleksna svuda
        h, w = gray_array.shape
        quadrants = [
            gray_array[:h//2, :w//2],
            gray_array[:h//2, w//2:],
            gray_array[h//2:, :w//2],
            gray_array[h//2:, w//2:]
        ]
        complexities = [np.std(q) for q in quadrants]
        complexity_variance = np.var(complexities)
        
        if complexity_variance > 200:  # Različita kompleksnost = objekti u nekim delovima
            score += 15
        
        return score
        
    except Exception as e:
        print(f"    GREŠKA pri analizi: {e}")
        return 9999

def find_flattest_texture(product_dir, main_image):
    """Pronalazi sliku sa NAJMANJE objekata - samo flat tekstura."""
    all_images = list(product_dir.glob('*.jpg'))
    
    if len(all_images) <= 1:
        return None
    
    results = []
    for img in all_images:
        score = detect_objects_visual(img)
        results.append((score, img))
    
    # Sortiraj - najmanji score = najčistija
    results.sort(key=lambda x: x[0])
    
    return results

print("=" * 80)
print("VIZUELNA DETEKCIJA OBJEKATA - Samo gledamo slike!")
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
unchanged = []

print("OBRAĐUJEM SVE PROIZVODE:\n")

for i, product in enumerate(results, 1):
    collection = product['collection']
    slug = product['slug']
    
    print(f"[{i}/{len(results)}] {collection}/{slug}")
    
    product_dir = base_path / collection / slug
    main_image = product_dir / f"{slug}.jpg"
    
    if not product_dir.exists() or not main_image.exists():
        print(f"  ❌ Nedostaju fajlovi!\n")
        continue
    
    # Analiziraj SVE slike
    scored_images = find_flattest_texture(product_dir, main_image)
    
    if not scored_images:
        print(f"  ⚠️  Nema alternativa\n")
        continue
    
    # Prikaži top 3
    print(f"  📊 TOP 3 najčistije:")
    for score, img in scored_images[:3]:
        current_marker = " <- TRENUTNA" if img == main_image else ""
        print(f"      Score {score:3}: {img.name[:50]}{current_marker}")
    
    # Trenutna slika
    current_score = next(s for s, im in scored_images if im == main_image)
    best_score, best_image = scored_images[0]
    
    # Zameni ako postoji bolja (razlika > 20)
    if best_image != main_image and best_score < current_score - 20:
        try:
            shutil.copy(best_image, main_image)
            replaced.append({
                'collection': collection,
                'slug': slug,
                'old_score': current_score,
                'new_score': best_score,
                'improvement': current_score - best_score
            })
            print(f"  ✅ ZAMENJENO: {current_score} → {best_score} (poboljšanje: {current_score - best_score})")
        except Exception as e:
            print(f"  ❌ Greška: {e}")
    else:
        unchanged.append(f"{collection}/{slug}")
        print(f"  ⏭️  Trenutna je OK (score: {current_score})")
    
    print()

# Rezultati
print("=" * 80)
print("FINALNI REZULTATI (SVI PROIZVODI):")
print(f"  ✅ ZAMENJENO: {len(replaced)}")
print(f"  ⏭️  OSTAVLJENO: {len(unchanged)}")
print("=" * 80)

if replaced:
    print("\n🎯 TOP 10 ZAMENJENIH (najveća poboljšanja):")
    replaced.sort(key=lambda x: x['improvement'], reverse=True)
    for item in replaced[:10]:
        print(f"  • {item['collection']}/{item['slug']}")
        print(f"    {item['old_score']} → {item['new_score']} (↓{item['improvement']})")

print("\n✅ GOTOVO! Sve zamene izvršene.")
