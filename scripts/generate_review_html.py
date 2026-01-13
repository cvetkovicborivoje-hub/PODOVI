import sys
import json
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')

# Prikupljanje svih proizvoda
base_path = Path('public/images/products/lvt/colors')
products_data = []

print("=" * 80)
print("GENERISANJE HTML ZA PREGLED SLIKA")
print("=" * 80)
print("\n📊 Prikupljam proizvode...")

for collection_dir in sorted(base_path.iterdir()):
    if not collection_dir.is_dir():
        continue
    
    collection = collection_dir.name
    
    for product_dir in sorted(collection_dir.iterdir()):
        if not product_dir.is_dir():
            continue
        
        slug = product_dir.name
        main_image = product_dir / f"{slug}.jpg"
        
        if main_image.exists():
            all_images = list(product_dir.glob('*.jpg'))
            if len(all_images) >= 2:
                # Relativna putanja za HTML
                image_path = f"public/images/products/lvt/colors/{collection}/{slug}/{slug}.jpg"
                
                products_data.append({
                    'collection': collection,
                    'slug': slug,
                    'image': image_path,
                    'alternativeImages': [img.name for img in all_images if img != main_image]
                })

print(f"✅ Pronađeno {len(products_data)} proizvoda\n")

# Učitaj HTML template
with open('review_images.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# Ubaci JSON podatke
json_data = json.dumps(products_data, ensure_ascii=False, indent=2)
html_content = html_content.replace(
    '<script id="productsData" type="application/json">\n        []\n    </script>',
    f'<script id="productsData" type="application/json">\n{json_data}\n    </script>'
)

# Sačuvaj novi HTML
output_file = 'review_images_generated.html'
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"✅ HTML generisan: {output_file}")
print(f"📊 Ukupno proizvoda: {len(products_data)}")
print()
print("=" * 80)
print("SLEDEĆI KORACI:")
print(f"  1. Otvori: {output_file}")
print("  2. Pregledaj SVE slike i označi one SA NAMEŠTAJEM")
print("  3. Klikni '💾 Preuzmi JSON' kada završiš")
print("  4. Pokreni: python scripts/apply_review_results.py")
print("=" * 80)
