import sys
import json
sys.stdout.reconfigure(encoding='utf-8')

# Učitava pravilna imena
with open('scripts/all_products_smart_names.json', 'r', encoding='utf-8') as f:
    products_data = json.load(f)

products = products_data['products']

# Kreira novi colors array
colors = []

for prod in products:
    collection = prod['collection']
    code = prod['code']
    name = prod['name']
    full_name = f"{code} {name}"
    slug = prod['color_slug']
    
    # Kreira collection_name iz collection slug-a
    collection_name = collection.replace('-', ' ').title()
    
    # Nova putanja do slike sa cache bust
    image_url = f"/images/products/lvt/colors/{collection}/{slug}/{slug}.jpg?v=2"
    
    colors.append({
        "collection": collection,
        "collection_name": collection_name,
        "code": code,
        "name": name,
        "full_name": full_name,
        "slug": slug,
        "image_url": image_url,
        "texture_url": image_url,
        "image_count": 1
    })

# Pravi finalni JSON
output = {
    "total": len(colors),
    "collections": len(set(p['collection'] for p in products)),
    "colors": colors
}

# Piše JSON
with open('public/data/lvt_colors_complete.json', 'w', encoding='utf-8') as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f"✅ Regenerisan JSON sa {len(colors)} boja!")
print(f"✅ Prava imena: {colors[0]['full_name']}, {colors[1]['full_name']}, ...")
print(f"✅ Nove slike: {colors[0]['image_url']}")
