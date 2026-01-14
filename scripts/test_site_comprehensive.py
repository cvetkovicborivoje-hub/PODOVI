# -*- coding: utf-8 -*-
"""
Comprehensive site testing script
Tests all products, images, and ColorGrid logic
"""
import json
import sys
from pathlib import Path
from urllib.parse import unquote

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

base_images_path = Path('public/images/products/lvt/colors')
json_path = Path('public/data/lvt_colors_complete.json')
products_path = Path('lib/data/gerflor-products-generated.ts')

# Load JSON
print("Loading JSON data...")
with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Total colors in JSON: {len(data['colors'])}\n")

# Get all unique collections
all_collections = sorted(set(c['collection'] for c in data['colors']))
print(f"Collections found: {len(all_collections)}\n")

# Test 1: Check if all images exist
print("=" * 80)
print("TEST 1: Image File Existence")
print("=" * 80)

missing_images = []
broken_urls = []

for color in data['colors']:
    collection = color['collection']
    code = color['code']
    name = color['name']
    
    # Check texture_url
    texture_url = color.get('texture_url', '')
    if texture_url:
        # Remove query string
        clean_url = texture_url.split('?')[0]
        # Remove /images/products/lvt/colors/ prefix
        if clean_url.startswith('/images/products/lvt/colors/'):
            rel_path = clean_url[len('/images/products/lvt/colors/'):]
            image_path = base_images_path / rel_path
            
            if not image_path.exists():
                missing_images.append({
                    'collection': collection,
                    'code': code,
                    'name': name,
                    'url': texture_url,
                    'expected_path': str(image_path),
                    'type': 'texture_url'
                })
    
    # Check lifestyle_url
    lifestyle_url = color.get('lifestyle_url', '')
    if lifestyle_url:
        clean_url = lifestyle_url.split('?')[0]
        if clean_url.startswith('/images/products/lvt/colors/'):
            rel_path = clean_url[len('/images/products/lvt/colors/'):]
            image_path = base_images_path / rel_path
            
            if not image_path.exists():
                missing_images.append({
                    'collection': collection,
                    'code': code,
                    'name': name,
                    'url': lifestyle_url,
                    'expected_path': str(image_path),
                    'type': 'lifestyle_url'
                })

print(f"\nMissing images: {len(missing_images)}")
if missing_images:
    print("\nFirst 20 missing images:")
    for item in missing_images[:20]:
        print(f"  {item['collection']}/{item['code']} {item['name']}")
        print(f"    URL: {item['url']}")
        print(f"    Expected: {item['expected_path']}")
        print(f"    Type: {item['type']}")
        print()

# Test 2: Check collection name extraction logic
print("=" * 80)
print("TEST 2: Collection Name Extraction Logic")
print("=" * 80)

test_slugs = [
    'creation-saga2-terra-35021566',
    'creation-55-looselay-terra-39741566',
    'creation-55-clic-acoustic-ball-39750555',
    'creation-40-clic-acoustic-twist-39750417',
    'creation-70-megaclic-quartet-39750545',
    'gerflor-creation-30',
    'creation-30-ballerina-41870347',
]

extraction_errors = []

for slug in test_slugs:
    collectionName = slug.replace('gerflor-', '')
    
    # Simulate ColorGrid logic
    if collectionName.startswith('creation-'):
        parts = collectionName.split('-')
        if len(parts) >= 2:
            # Handle 4-part collections
            if len(parts) >= 4 and parts[2] == 'clic' and parts[3] == 'acoustic':
                collectionName = '-'.join(parts[:4])
            # Handle 3-part collections
            elif len(parts) >= 3 and parts[2] in ['looselay', 'clic', 'zen', 'connect', 'megaclic', 'saga2']:
                collectionName = '-'.join(parts[:3])
            # Handle 2-part collections
            else:
                collectionName = '-'.join(parts[:2])
    
    exists = collectionName in all_collections
    matching = [c for c in data['colors'] if c['collection'] == collectionName]
    
    if not exists or len(matching) == 0:
        extraction_errors.append({
            'slug': slug,
            'extracted': collectionName,
            'exists': exists,
            'matching_count': len(matching)
        })
        print(f"❌ FAILED: {slug}")
        print(f"   Extracted: {collectionName}")
        print(f"   Exists: {exists}")
        print(f"   Matching colors: {len(matching)}")
        print()
    else:
        print(f"✅ OK: {slug} → {collectionName} ({len(matching)} colors)")

print(f"\nExtraction errors: {len(extraction_errors)}")

# Test 3: Check if all collections can be matched
print("\n" + "=" * 80)
print("TEST 3: Collection Matching Test")
print("=" * 80)

unmatched_collections = []

for collection in all_collections:
    matching_colors = [c for c in data['colors'] if c['collection'] == collection]
    
    # Try to find a product slug that would match this collection
    # Test different slug patterns
    test_patterns = [
        collection,  # Direct match
        f'gerflor-{collection}',  # With gerflor prefix
        f'{collection}-test-123456',  # With suffix
    ]
    
    matched = False
    for pattern in test_patterns:
        # Simulate extraction
        test_collection = pattern.replace('gerflor-', '')
        if test_collection.startswith('creation-'):
            parts = test_collection.split('-')
            if len(parts) >= 2:
                if len(parts) >= 4 and parts[2] == 'clic' and parts[3] == 'acoustic':
                    test_collection = '-'.join(parts[:4])
                elif len(parts) >= 3 and parts[2] in ['looselay', 'clic', 'zen', 'connect', 'megaclic', 'saga2']:
                    test_collection = '-'.join(parts[:3])
                else:
                    test_collection = '-'.join(parts[:2])
        
        if test_collection == collection:
            matched = True
            break
    
    if not matched:
        unmatched_collections.append(collection)
        print(f"⚠️  Collection '{collection}' might not be matchable from product slugs")

print(f"\nUnmatched collections: {len(unmatched_collections)}")

# Test 4: Check product slugs from gerflor-products-generated.ts
print("\n" + "=" * 80)
print("TEST 4: Product Slugs from TypeScript File")
print("=" * 80)

# Read TypeScript file and extract product slugs
try:
    with open(products_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract slugs (simplified regex - looking for slug: 'pattern')
    import re
    slug_pattern = r"slug:\s*['\"]([^'\"]+)['\"]"
    product_slugs = re.findall(slug_pattern, content)
    
    # Filter for creation slugs
    creation_slugs = [s for s in product_slugs if 'creation' in s.lower()][:20]
    
    print(f"Found {len(creation_slugs)} creation product slugs (showing first 20)")
    
    slug_extraction_errors = []
    
    for slug in creation_slugs:
        collectionName = slug.replace('gerflor-', '')
        
        # Simulate ColorGrid logic
        if collectionName.startswith('creation-'):
            parts = collectionName.split('-')
            if len(parts) >= 2:
                if len(parts) >= 4 and parts[2] == 'clic' and parts[3] == 'acoustic':
                    collectionName = '-'.join(parts[:4])
                elif len(parts) >= 3 and parts[2] in ['looselay', 'clic', 'zen', 'connect', 'megaclic', 'saga2']:
                    collectionName = '-'.join(parts[:3])
                else:
                    collectionName = '-'.join(parts[:2])
        
        exists = collectionName in all_collections
        matching = [c for c in data['colors'] if c['collection'] == collectionName]
        
        if not exists or len(matching) == 0:
            slug_extraction_errors.append({
                'slug': slug,
                'extracted': collectionName,
                'exists': exists,
                'matching_count': len(matching)
            })
            print(f"❌ {slug} → {collectionName} ({len(matching)} colors)")
        else:
            print(f"✅ {slug} → {collectionName} ({len(matching)} colors)")
    
    print(f"\nSlug extraction errors: {len(slug_extraction_errors)}")
    
except Exception as e:
    print(f"Error reading TypeScript file: {e}")

# Summary
print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)
print(f"Missing images: {len(missing_images)}")
print(f"Extraction errors: {len(extraction_errors)}")
print(f"Unmatched collections: {len(unmatched_collections)}")
if 'slug_extraction_errors' in locals():
    print(f"Slug extraction errors: {len(slug_extraction_errors)}")

# Save detailed report
report_path = Path('test_report.json')
report = {
    'missing_images': missing_images,
    'extraction_errors': extraction_errors,
    'unmatched_collections': unmatched_collections,
    'summary': {
        'total_colors': len(data['colors']),
        'total_collections': len(all_collections),
        'missing_images_count': len(missing_images),
        'extraction_errors_count': len(extraction_errors),
    }
}

if 'slug_extraction_errors' in locals():
    report['slug_extraction_errors'] = slug_extraction_errors

with open(report_path, 'w', encoding='utf-8') as f:
    json.dump(report, f, ensure_ascii=False, indent=2)

print(f"\nDetailed report saved to: {report_path}")
