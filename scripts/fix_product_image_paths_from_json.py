# -*- coding: utf-8 -*-
"""
Fix image paths in gerflor-products-generated.ts by syncing with lvt_colors_complete.json
This script will:
1. Load color data from JSON
2. Match products by code and collection name
3. Update image URLs in TypeScript file to use correct paths from JSON
4. Update version to v=9
"""
import json
import sys
import re
from pathlib import Path

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

json_path = Path('public/data/lvt_colors_complete.json')
ts_path = Path('lib/data/gerflor-products-generated.ts')

print("Loading color JSON data...")
with open(json_path, 'r', encoding='utf-8') as f:
    color_data = json.load(f)

print(f"Loaded {len(color_data['colors'])} color entries\n")

# Create lookup map: collection + code -> color entry
color_map = {}
for color in color_data['colors']:
    collection = color['collection']
    code = color['code']
    key = f"{collection}|{code}"
    if key not in color_map:
        color_map[key] = []
    color_map[key].append(color)

print(f"Created color lookup map with {len(color_map)} unique keys\n")

# Read TypeScript file
print("Reading TypeScript file...")
with open(ts_path, 'r', encoding='utf-8') as f:
    ts_content = f.read()

print(f"File size: {len(ts_content)} characters\n")

# Find all product entries and update them
updated_count = 0
not_found = []

# Pattern to match product entries with image URLs
# Look for: url: '/images/products/lvt/colors/...'
product_pattern = r"(\{\s*id:\s*'([^']+)',\s*name:\s*'([^']+)',\s*slug:\s*'([^']+)',\s*sku:\s*'([^']+)',[^}]*?images:\s*\[\{\s*id:\s*'([^']+)',\s*url:\s*)'([^']+)'"

def extract_collection_from_slug(slug):
    """Extract collection name from product slug"""
    # Remove 'gerflor-' prefix if present
    slug = slug.replace('gerflor-', '')
    
    # Extract collection name (same logic as ColorGrid)
    if slug.startswith('creation-'):
        parts = slug.split('-')
        if len(parts) >= 2:
            # Handle 4-part collections
            if len(parts) >= 4 and parts[2] == 'clic' and parts[3] == 'acoustic':
                return '-'.join(parts[:4])
            # Handle 3-part collections
            elif len(parts) >= 3 and parts[2] in ['looselay', 'clic', 'zen', 'connect', 'megaclic', 'saga2']:
                return '-'.join(parts[:3])
            # Handle 2-part collections
            else:
                return '-'.join(parts[:2])
    return None

def find_color_entry(collection, code):
    """Find color entry in JSON by collection and code"""
    key = f"{collection}|{code}"
    if key in color_map:
        # Return first match (usually there's only one)
        return color_map[key][0]
    
    # Try without Unknown prefix
    if code == 'Unknown':
        return None
    
    # Try variations
    for color in color_data['colors']:
        if color['collection'] == collection:
            # Try matching by code
            if color['code'] == code:
                return color
    
    return None

# Find all product entries
# Better approach: find each product block and update images
print("Finding and updating product entries...\n")

# Split into individual product entries
# Products are separated by }, with { at start
products = re.split(r"(?=\{\s*id:\s*')", ts_content)

if len(products) <= 1:
    # Try different splitting
    products = re.findall(r"\{\s*id:\s*'[^']+',.*?\}", ts_content, re.DOTALL)

print(f"Found {len(products)} potential product blocks\n")

# Process each product
new_content_parts = [products[0]]  # Keep the initial part (imports, etc.)
updated_products = 0

for i, product in enumerate(products[1:], 1):
    # Extract slug and sku from product
    slug_match = re.search(r"slug:\s*'([^']+)'", product)
    sku_match = re.search(r"sku:\s*'([^']+)'", product)
    
    if not slug_match or not sku_match:
        new_content_parts.append(product)
        continue
    
    slug = slug_match.group(1)
    sku = sku_match.group(1)
    
    # Extract collection name from slug
    collection = extract_collection_from_slug(slug)
    
    if not collection:
        new_content_parts.append(product)
        continue
    
    # Find color entry in JSON
    color_entry = find_color_entry(collection, sku)
    
    if not color_entry:
        # Try with different code matching
        # Sometimes code might be in name
        not_found.append({
            'slug': slug,
            'sku': sku,
            'collection': collection
        })
        new_content_parts.append(product)
        continue
    
    # Get image URL from color entry
    image_url = color_entry.get('texture_url') or color_entry.get('image_url')
    
    if not image_url:
        new_content_parts.append(product)
        continue
    
    # Update version to v=9
    if '?v=' in image_url:
        image_url = re.sub(r'\?v=\d+', '?v=9', image_url)
    else:
        image_url += '?v=9'
    
    # Find and replace image URL in product
    url_pattern = r"(url:\s*')([^']+)(')"
    if re.search(url_pattern, product):
        updated_product = re.sub(
            url_pattern,
            lambda m: f"{m.group(1)}{image_url}{m.group(3)}",
            product,
            count=1  # Only replace first occurrence (the primary image)
        )
        new_content_parts.append(updated_product)
        updated_products += 1
    else:
        new_content_parts.append(product)

print(f"Updated {updated_products} products")
print(f"Not found: {len(not_found)}")

if not_found:
    print("\nProducts not found in color JSON (first 10):")
    for item in not_found[:10]:
        print(f"  {item['collection']} / {item['sku']} - {item['slug']}")

# Join content back
new_content = ''.join(new_content_parts)

# Write updated file
if updated_products > 0:
    with open(ts_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"\n✅ Updated {ts_path}")
    print(f"   Updated {updated_products} product image URLs")
    print(f"   All URLs now use version v=9")
else:
    print("\n⚠️  No updates made")
