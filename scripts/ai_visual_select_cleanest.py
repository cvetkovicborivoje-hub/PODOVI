import sys
import os
from pathlib import Path
from PIL import Image
import shutil
sys.stdout.reconfigure(encoding='utf-8')

print("=" * 80)
print("AI VIZUELNA SELEKCIJA NAJČISTIJIH SLIKA")
print("=" * 80)
print()

# Jednostavna vizuelna analiza
def analyze_image_simplicity(image_path):
    """Analiziraj sliku i vrati ocenu čistoće (veći broj = čistija)"""
    try:
        img = Image.open(image_path)
        width, height = img.size
        
        # Konvertuj u RGB
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Uzmi centralni region (sredina slike - tu ne treba da bude ništa)
        center_x = width // 2
        center_y = height // 2
        box_size = min(width, height) // 4
        
        center_region = img.crop((
            center_x - box_size // 2,
            center_y - box_size // 2,
            center_x + box_size // 2,
            center_y + box_size // 2
        ))
        
        # Analiziraj kompleksnost u centru
        pixels = list(center_region.getdata())
        
        # Izračunaj varijanse boja
        r_values = [p[0] for p in pixels]
        g_values = [p[1] for p in pixels]
        b_values = [p[2] for p in pixels]
        
        r_var = sum((x - sum(r_values) / len(r_values)) ** 2 for x in r_values) / len(r_values)
        g_var = sum((x - sum(g_values) / len(g_values)) ** 2 for x in g_values) / len(g_values)
        b_var = sum((x - sum(b_values) / len(b_values)) ** 2 for x in b_values) / len(b_values)
        
        total_var = r_var + g_var + b_var
        
        # Manji variance = čistija slika (jednolična tekstura poda)
        # Veći variance = kompleksnija slika (verovatno nameštaj)
        
        # Takođe proveri aspect ratio - swatch slike su često kvadratne ili landscape
        aspect_ratio = width / height
        aspect_score = 1.0 if 0.8 <= aspect_ratio <= 1.5 else 0.5
        
        # Finalna ocena (INVERZ variance + aspect bonus)
        # Delimo sa 10000 da normalizujemo
        simplicity_score = (1000000 / (total_var + 1)) * aspect_score
        
        return {
            'score': simplicity_score,
            'variance': total_var,
            'aspect_ratio': aspect_ratio,
            'size': os.path.getsize(image_path)
        }
    
    except Exception as e:
        return {'score': 0, 'error': str(e)}

# Pronađi sve proizvode
products_path = Path('public/images/products/lvt/colors')
all_collections = sorted(products_path.glob('*'))

replaced = []
skipped = []
total = 0

for collection_dir in all_collections:
    if not collection_dir.is_dir():
        continue
    
    product_dirs = sorted(collection_dir.glob('*'))
    
    for product_dir in product_dirs:
        if not product_dir.is_dir():
            continue
        
        total += 1
        slug = product_dir.name
        main_image = product_dir / f"{slug}.jpg"
        
        if not main_image.exists():
            continue
        
        # Pronađi SVE jpg slike u folderu
        all_images = sorted(product_dir.glob('*.jpg'))
        
        if len(all_images) <= 1:
            # Samo glavna slika, skip
            continue
        
        # Analiziraj SVE slike
        image_scores = []
        for img_path in all_images:
            analysis = analyze_image_simplicity(img_path)
            image_scores.append({
                'path': img_path,
                'name': img_path.name,
                'analysis': analysis
            })
        
        # Sortiraj po oceni - NAJVIŠA ocena = NAJČISTIJA
        image_scores.sort(key=lambda x: x['analysis']['score'], reverse=True)
        
        # Najbolja slika
        best_image = image_scores[0]
        
        # Da li je najbolja slika već glavna?
        if best_image['path'] == main_image:
            # Već je dobra
            continue
        
        # ZAMENI glavnu sliku sa najboljom
        print(f"\n[{total}] {collection_dir.name}/{slug}")
        print(f"  Kandidati:")
        for idx, img in enumerate(image_scores[:3]):  # Top 3
            marker = "✅ IZABRANA" if idx == 0 else ""
            print(f"    {idx+1}. {img['name']}")
            print(f"       Score: {img['analysis']['score']:.1f}, Var: {img['analysis']['variance']:.1f}, "
                  f"Aspect: {img['analysis']['aspect_ratio']:.2f}, Size: {img['analysis']['size']} bytes {marker}")
        
        # Zameni
        shutil.copy2(best_image['path'], main_image)
        
        replaced.append({
            'product': f"{collection_dir.name}/{slug}",
            'from': best_image['name'],
            'score': best_image['analysis']['score']
        })

print("\n" + "=" * 80)
print("REZULTATI:")
print(f"  📊 Obrađeno: {total} proizvoda")
print(f"  ✅ Zamenjeno: {len(replaced)} slika")
print("=" * 80)

if replaced:
    print(f"\n🎯 Zamenjeno {len(replaced)} proizvoda!")
    if len(replaced) <= 30:
        for item in replaced:
            print(f"  • {item['product']} ← {item['from']} (score: {item['score']:.1f})")

# Sačuvaj log
with open('ai_visual_selection_log.txt', 'w', encoding='utf-8') as f:
    f.write(f"AI VIZUELNA SELEKCIJA\n")
    f.write("=" * 80 + "\n\n")
    f.write(f"Zamenjeno: {len(replaced)}\n\n")
    
    for item in replaced:
        f.write(f"{item['product']}\n")
        f.write(f"  Izabrana: {item['from']}\n")
        f.write(f"  Score: {item['score']:.1f}\n\n")

print("\n💾 Log: ai_visual_selection_log.txt")
print("✅ GOTOVO!")
