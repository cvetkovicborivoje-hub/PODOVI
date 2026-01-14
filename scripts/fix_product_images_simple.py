# -*- coding: utf-8 -*-
"""
Fix image paths in gerflor-products-generated.ts by syncing with lvt_colors_complete.json
Simple approach: Find products by slug/code and replace image URLs
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

# Create lookup: (collection, code) -> image_url
color_lookup = {}
for color in color_data['colors']:
    collection = color['collection']
    code = color['code']
    if code and code != 'Unknown':
        key = (collection, code)
        image_url = color.get('texture_url') or color.get('image_url')
        if image_url:
            # Ensure v=9
            if '?v=' in image_url:
                image_url = re.sub(r'\?v=\d+', '?v=9', image_url)
            else:
                image_url += '?v=9'
            color_lookup[key] = image_url

print(f"Created lookup for {len(color_lookup)} color entries\n")

# Read TypeScript file
print("Reading TypeScript file...")
with open(ts_path, 'r', encoding='utf-8') as f:
    ts_content = f.read()

def extract_collection_from_slug(slug):
    """Extract collection name from product slug"""
    slug = slug.replace('gerflor-', '')
    if slug.startswith('creation-'):
        parts = slug.split('-')
        if len(parts) >= 2:
            if len(parts) >= 4 and parts[2] == 'clic' and parts[3] == 'acoustic':
                return '-'.join(parts[:4])
            elif len(parts) >= 3 and parts[2] in ['looselay', 'clic', 'zen', 'connect', 'megaclic', 'saga2']:
                return '-'.join(parts[:3])
            else:
                return '-'.join(parts[:2])
    return None

# Find all product entries with their slugs and codes
# Pattern: slug: '...', sku: '...', ... images: [{ ... url: '...'
pattern = r"slug:\s*'([^']+)',\s*sku:\s*'([^']+)',(.*?)url:\s*'([^']+)'"

def replace_url(match):
    slug = match.group(1)
    sku = match.group(2)
    before_url = match.group(3)
    old_url = match.group(4)
    
    # Extract collection from slug
    collection = extract_collection_from_slug(slug)
    
    if not collection:
        return match.group(0)  # No change
    
    # Look up in color data
    key = (collection, sku)
    if key in color_lookup:
        new_url = color_lookup[key]
        if old_url != new_url:
            # Replace only the URL part
            return f"slug: '{slug}', sku: '{sku}',{before_url}url: '{new_url}'"
    
    return match.group(0)  # No change

# Replace all matching patterns
print("Finding and replacing image URLs...")
new_content = re.sub(pattern, replace_url, ts_content, flags=re.DOTALL)

# Check if changes were made
if new_content != ts_content:
    # Count how many URLs were changed
    changes = 0
    for match in re.finditer(pattern, ts_content, flags=re.DOTALL):
        slug = match.group(1)
        sku = match.group(2)
        old_url = match.group(4)
        collection = extract_collection_from_slug(slug)
        if collection:
            key = (collection, sku)
            if key in color_lookup:
                new_url = color_lookup[key]
                if old_url != new_url:
                    changes += 1
    
    print(f"Found {changes} products to update")
    
    # Write updated file
    with open(ts_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"\n✅ Updated {ts_path}")
    print(f"   Updated {changes} product image URLs")
    print(f"   All URLs now use version v=9")
else:
    print("\n⚠️  No changes detected - URLs may already be correct")
