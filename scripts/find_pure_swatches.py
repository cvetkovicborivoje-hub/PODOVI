import sys
import json
import shutil
from pathlib import Path
from PIL import Image
import numpy as np
sys.stdout.reconfigure(encoding='utf-8')

def analyze_image_purity(image_path):
    """
    Analizira da li je slika ČISTA TEKSTURA ili ima objekte.
    Vraća score (0-100): niži = čistija tekstura, viši = ima objekte/scenu.
    """
    try:
        img = Image.open(image_path).convert('RGB')
        img_array = np.array(img)
        gray = img.convert('L')
        gray_array = np.array(gray)
        
        score = 0
        details = []
        
        # 1. EDGE COMPLEXITY - objekti imaju mnogo različitih ivica
        edges_h = np.abs(np.diff(gray_array, axis=0))
        edges_v = np.abs(np.diff(gray_array, axis=1))
        strong_edges = (np.sum(edges_h > 30) + np.sum(edges_v > 30)) / gray_array.size
        
        if strong_edges > 0.20:
            score += 40
            details.append(f"high_edges={strong_edges:.3f}")
        elif strong_edges > 0.15:
            score += 30
            details.append(f"med_edges={strong_edges:.3f}")
        elif strong_edges > 0.10:
            score += 15
            details.append(f"low_edges={strong_edges:.3f}")
        
        # 2. COLOR VARIANCE - scene imaju veliku varijansu boja
        color_std = np.std(img_array, axis=(0,1))
        avg_color_std = np.mean(color_std)
        
        if avg_color_std > 60:
            score += 25
            details.append(f"high_color_var={avg_color_std:.1f}")
        elif avg_color_std > 40:
            score += 15
            details.append(f"med_color_var={avg_color_std:.1f}")
        
        # 3. BRIGHTNESS VARIANCE - objekti i senke kreiraju veliku varijansu
        brightness_var = np.var(gray_array)
        
        if brightness_var > 3000:
            score += 20
            details.append(f"high_brightness_var={brightness_var:.0f}")
        elif brightness_var > 2000:
            score += 10
            details.append(f"med_brightness_var={brightness_var:.0f}")
        
        # 4. SPATIAL FREQUENCY - objekti imaju više različitih frekvencija
        # Čista tekstura ima uniforman pattern
        fft = np.fft.fft2(gray_array)
        fft_magnitude = np.abs(fft)
        high_freq_energy = np.sum(fft_magnitude[fft_magnitude > np.percentile(fft_magnitude, 95)])
        
        if high_freq_energy > 1e9:
            score += 15
            details.append(f"high_freq")
        
        # 5. ASPECT RATIO - čiste teksture obično imaju specifične ratio-e
        aspect_ratio = img.size[0] / img.size[1]
        if aspect_ratio > 2.5 or aspect_ratio < 0.4:
            score += 10
            details.append(f"unusual_ratio={aspect_ratio:.2f}")
        
        # 6. CONTRAST RANGE - scene imaju veliki raspon kontrasta
        min_brightness = np.min(gray_array)
        max_brightness = np.max(gray_array)
        contrast_range = max_brightness - min_brightness
        
        if contrast_range > 200:
            score += 15
            details.append(f"high_contrast={contrast_range}")
        elif contrast_range > 150:
            score += 5
            details.append(f"med_contrast={contrast_range}")
        
        return score, details
        
    except Exception as e:
        print(f"  ⚠️  Greška: {e}")
        return 999, [f"error: {e}"]

def find_purest_swatch(product_dir, main_image):
    """Pronalazi najčistiju teksturu bez ikakvih objekata."""
    all_images = list(product_dir.glob('*.jpg'))
    
    if len(all_images) <= 1:
        return None
    
    results = []
    print(f"    Analiziram {len(all_images)} slika...")
    
    for img in all_images:
        score, details = analyze_image_purity(img)
        results.append((score, img, details))
        print(f"      {img.name[:50]:50} | Score: {score:3} | {', '.join(details[:2])}")
    
    # Sortiraj po score-u (najniži = najčistiji)
    results.sort(key=lambda x: x[0])
    
    return results[0] if results else None

print("=" * 80)
print("TRAŽIM ČISTE TEKSTURE - Bez ikakvih objekata")
print("=" * 80)
print()

# Učitaj rezultate
try:
    with open('furniture_review_results.json', 'r', encoding='utf-8') as f:
        results = json.load(f)
    print(f"✅ Analiziram {len(results)} proizvoda\n")
except FileNotFoundError:
    print("❌ Fajl 'furniture_review_results.json' nije pronađen!")
    sys.exit(1)

# Analiza i zamena
base_path = Path('public/images/products/lvt/colors')
replaced = []
errors = []
skipped = []

for i, product in enumerate(results, 1):  # SVE proizvode
    collection = product['collection']
    slug = product['slug']
    
    print(f"\n[{i}/{len(results)}] {collection}/{slug}")
    
    product_dir = base_path / collection / slug
    main_image = product_dir / f"{slug}.jpg"
    
    if not product_dir.exists() or not main_image.exists():
        errors.append(f"{collection}/{slug}: Nedostaju fajlovi")
        print(f"  ❌ Nedostaju fajlovi!")
        continue
    
    # Analiziraj trenutnu sliku
    current_score, current_details = analyze_image_purity(main_image)
    print(f"  📊 TRENUTNA: {main_image.name[:40]:40} | Score: {current_score}")
    print(f"      {', '.join(current_details)}")
    
    # Pronađi najčistiju
    result = find_purest_swatch(product_dir, main_image)
    
    if not result:
        skipped.append(f"{collection}/{slug}: Nema alternativa")
        print(f"  ⚠️  Nema alternativa!")
        continue
    
    best_score, best_image, best_details = result
    
    # Zameni samo ako je nova ZNAČAJNO čistija (razlika > 10)
    if best_score < current_score - 10:
        try:
            print(f"  ✅ ZAMENJUJEM: {current_score} → {best_score}")
            print(f"      Nova: {best_image.name}")
            shutil.copy(best_image, main_image)
            replaced.append({
                'collection': collection,
                'slug': slug,
                'old_score': current_score,
                'new_score': best_score,
                'new_image': best_image.name
            })
        except Exception as e:
            errors.append(f"{collection}/{slug}: {str(e)}")
            print(f"  ❌ Greška: {e}")
    else:
        skipped.append(f"{collection}/{slug}: Trenutna je najbolja")
        print(f"  ⏭️  Trenutna je već najbolja (score {current_score})")

# Rezultati
print("\n" + "=" * 80)
print("REZULTATI (SVE PROIZVODE):")
print(f"  ✅ Zamenjeno: {len(replaced)}")
print(f"  ⏭️  Preskočeno: {len(skipped)}")
print(f"  ❌ Greške: {len(errors)}")
print("=" * 80)

if replaced:
    print("\n🎉 ZAMENJENI PROIZVODI:")
    for item in replaced:
        print(f"  • {item['collection']}/{item['slug']}")
        print(f"    Score: {item['old_score']} → {item['new_score']} (-{item['old_score'] - item['new_score']})")
        print(f"    Nova: {item['new_image']}")

print("\n✅ Analiza završena na SVIM proizvodima!")
