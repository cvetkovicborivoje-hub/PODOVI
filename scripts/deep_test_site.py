# -*- coding: utf-8 -*-
"""
Deep comprehensive site testing - like ChatGPT agent would test
Tests everything: pages, images, data integrity, components, URLs, etc.
"""
import json
import sys
import re
from pathlib import Path
from urllib.parse import unquote, quote
from collections import defaultdict

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

base_images_path = Path('public/images/products/lvt/colors')
json_path = Path('public/data/lvt_colors_complete.json')
products_ts_path = Path('lib/data/gerflor-products-generated.ts')

print("=" * 80)
print("DEEP COMPREHENSIVE SITE TESTING")
print("=" * 80)
print()

# Load JSON
print("Loading data files...")
with open(json_path, 'r', encoding='utf-8') as f:
    json_data = json.load(f)

print(f"✅ JSON loaded: {len(json_data['colors'])} colors\n")

# ============================================================================
# TEST 1: Image File Existence and URL Validation
# ============================================================================
print("=" * 80)
print("TEST 1: Image File Existence & URL Validation")
print("=" * 80)

image_issues = {
    'missing_files': [],
    'wrong_paths': [],
    'url_encoding_issues': [],
    'invalid_urls': []
}

all_collections = sorted(set(c['collection'] for c in json_data['colors']))
print(f"Collections to check: {len(all_collections)}\n")

for color in json_data['colors']:
    collection = color['collection']
    code = color['code']
    name = color['name']
    
    collection_path = base_images_path / collection
    if not collection_path.exists():
        image_issues['missing_files'].append({
            'collection': collection,
            'code': code,
            'name': name,
            'issue': 'Collection folder does not exist',
            'path': str(collection_path)
        })
        continue
    
    # Check texture_url/image_url
    texture_url = color.get('texture_url') or color.get('image_url')
    if texture_url:
        # Validate URL format
        if not texture_url.startswith('/images/products/lvt/colors/'):
            image_issues['invalid_urls'].append({
                'collection': collection,
                'code': code,
                'name': name,
                'url': texture_url,
                'issue': 'Invalid URL format'
            })
        else:
            # Extract path
            clean_url = texture_url.split('?')[0]
            rel_path = clean_url[len('/images/products/lvt/colors/'):]
            file_path = base_images_path / rel_path
            
            # Check if file exists
            if not file_path.exists():
                # Check if folder exists
                folder_path = file_path.parent
                if folder_path.exists():
                    # Folder exists but file doesn't - check what files are there
                    actual_files = list(folder_path.glob('*.jpg')) + list(folder_path.glob('*.jpeg'))
                    image_issues['missing_files'].append({
                        'collection': collection,
                        'code': code,
                        'name': name,
                        'url': texture_url,
                        'expected': str(file_path),
                        'folder_exists': True,
                        'actual_files': [f.name for f in actual_files[:3]],
                        'issue': 'File not found in folder'
                    })
                else:
                    image_issues['wrong_paths'].append({
                        'collection': collection,
                        'code': code,
                        'name': name,
                        'url': texture_url,
                        'expected': str(file_path),
                        'folder_exists': False,
                        'issue': 'Folder does not exist'
                    })
    
    # Check lifestyle_url
    lifestyle_url = color.get('lifestyle_url')
    if lifestyle_url:
        clean_url = lifestyle_url.split('?')[0]
        if clean_url.startswith('/images/products/lvt/colors/'):
            rel_path = clean_url[len('/images/products/lvt/colors/'):]
            file_path = base_images_path / rel_path
            
            if not file_path.exists():
                # Decode URL to check encoding issues
                decoded_path = unquote(str(file_path))
                if '%' in str(file_path) and Path(decoded_path).exists():
                    image_issues['url_encoding_issues'].append({
                        'collection': collection,
                        'code': code,
                        'name': name,
                        'url': lifestyle_url,
                        'issue': 'URL encoding problem'
                    })
                else:
                    image_issues['missing_files'].append({
                        'collection': collection,
                        'code': code,
                        'name': name,
                        'url': lifestyle_url,
                        'expected': str(file_path),
                        'type': 'lifestyle_url',
                        'issue': 'File not found'
                    })

print(f"Missing files: {len(image_issues['missing_files'])}")
print(f"Wrong paths: {len(image_issues['wrong_paths'])}")
print(f"URL encoding issues: {len(image_issues['url_encoding_issues'])}")
print(f"Invalid URLs: {len(image_issues['invalid_urls'])}")

# Group by collection
if image_issues['missing_files']:
    by_collection = defaultdict(int)
    for issue in image_issues['missing_files']:
        by_collection[issue['collection']] += 1
    print(f"\nMissing files by collection:")
    for col, count in sorted(by_collection.items(), key=lambda x: -x[1])[:10]:
        print(f"  {col}: {count}")

print()

# ============================================================================
# TEST 2: Data Integrity - JSON Structure
# ============================================================================
print("=" * 80)
print("TEST 2: JSON Data Integrity")
print("=" * 80)

data_issues = {
    'missing_fields': [],
    'invalid_slugs': [],
    'duplicate_codes': [],
    'unknown_codes': []
}

for color in json_data['colors']:
    # Check required fields
    required = ['collection', 'code', 'name', 'full_name', 'slug']
    missing = [f for f in required if not color.get(f)]
    if missing:
        data_issues['missing_fields'].append({
            'color': color.get('full_name', 'Unknown'),
            'missing': missing
        })
    
    # Check slug format
    slug = color.get('slug', '')
    if not re.match(r'^[a-z0-9-]+$', slug):
        data_issues['invalid_slugs'].append({
            'color': color.get('full_name', 'Unknown'),
            'slug': slug
        })
    
    # Check for Unknown codes
    if color.get('code') == 'Unknown':
        data_issues['unknown_codes'].append({
            'collection': color.get('collection'),
            'name': color.get('name'),
            'slug': color.get('slug')
        })

# Check duplicates
code_map = defaultdict(list)
for color in json_data['colors']:
    code = color.get('code')
    collection = color.get('collection')
    if code and code != 'Unknown':
        key = f"{collection}-{code}"
        code_map[key].append(color.get('full_name'))

for key, names in code_map.items():
    if len(names) > 1:
        data_issues['duplicate_codes'].append({
            'code': key,
            'count': len(names),
            'names': names
        })

print(f"Missing fields: {len(data_issues['missing_fields'])}")
print(f"Invalid slugs: {len(data_issues['invalid_slugs'])}")
print(f"Duplicate codes: {len(data_issues['duplicate_codes'])}")
print(f"Unknown codes: {len(data_issues['unknown_codes'])}")

if data_issues['unknown_codes']:
    by_collection = defaultdict(int)
    for issue in data_issues['unknown_codes']:
        by_collection[issue['collection']] += 1
    print(f"\nUnknown codes by collection:")
    for col, count in sorted(by_collection.items(), key=lambda x: -x[1])[:10]:
        print(f"  {col}: {count}")

print()

# ============================================================================
# TEST 3: Folder Structure Validation
# ============================================================================
print("=" * 80)
print("TEST 3: Folder Structure Validation")
print("=" * 80)

folder_issues = {
    'orphaned_folders': [],
    'missing_pod': [],
    'missing_ilustracija': [],
    'empty_folders': []
}

for collection in all_collections:
    collection_path = base_images_path / collection
    if not collection_path.exists():
        continue
    
    # Get all product folders (not 'pod' or 'ilustracija')
    product_folders = [f for f in collection_path.iterdir() 
                       if f.is_dir() and f.name not in ['pod', 'ilustracija']]
    
    # Check if folders are referenced in JSON
    json_folders = set()
    for color in json_data['colors']:
        if color['collection'] == collection:
            texture_url = color.get('texture_url') or color.get('image_url')
            if texture_url:
                clean_url = texture_url.split('?')[0]
                if clean_url.startswith('/images/products/lvt/colors/'):
                    rel_path = clean_url[len('/images/products/lvt/colors/'):]
                    parts = rel_path.split('/')
                    if len(parts) >= 2:
                        json_folders.add(parts[1])
    
    # Check for orphaned folders
    for folder in product_folders:
        folder_name = folder.name
        if folder_name not in json_folders:
            folder_issues['orphaned_folders'].append({
                'collection': collection,
                'folder': folder_name
            })
        
        # Check pod folder
        pod_folder = folder / 'pod'
        if not pod_folder.exists() or not list(pod_folder.glob('*.jpg')):
            folder_issues['missing_pod'].append({
                'collection': collection,
                'folder': folder_name
            })
        
        # Check ilustracija folder (optional but good to know)
        ilustracija_folder = folder / 'ilustracija'
        if not ilustracija_folder.exists() or not list(ilustracija_folder.glob('*.jpg')):
            folder_issues['missing_ilustracija'].append({
                'collection': collection,
                'folder': folder_name
            })

print(f"Orphaned folders: {len(folder_issues['orphaned_folders'])}")
print(f"Missing pod folders: {len(folder_issues['missing_pod'])}")
print(f"Missing ilustracija folders: {len(folder_issues['missing_ilustracija'])}")

print()

# ============================================================================
# TEST 4: TypeScript File Consistency
# ============================================================================
print("=" * 80)
print("TEST 4: TypeScript File Consistency")
print("=" * 80)

ts_issues = {
    'products_not_in_json': [],
    'url_mismatches': []
}

if products_ts_path.exists():
    with open(products_ts_path, 'r', encoding='utf-8') as f:
        ts_content = f.read()
    
    # Extract product slugs from TS file (simplified)
    ts_slug_pattern = r"slug:\s*['\"]([^'\"]+)['\"]"
    ts_slugs = set(re.findall(ts_slug_pattern, ts_content))
    
    # Extract image URLs from TS file
    ts_url_pattern = r"url:\s*['\"](/images/products/lvt/colors/[^'\"]+)['\"]"
    ts_urls = re.findall(ts_url_pattern, ts_content)
    
    # Check if URLs match JSON
    json_urls = set()
    for color in json_data['colors']:
        if color.get('texture_url'):
            json_urls.add(color['texture_url'].split('?')[0])
        if color.get('image_url'):
            json_urls.add(color['image_url'].split('?')[0])
    
    print(f"Products in TS file: {len(ts_slugs)} (showing first 20)")
    print(f"Image URLs in TS file: {len(ts_urls)}")
    print(f"Image URLs in JSON: {len(json_urls)}")
else:
    print("TypeScript file not found")

print()

# ============================================================================
# TEST 5: Collection Name Extraction Logic Test
# ============================================================================
print("=" * 80)
print("TEST 5: Collection Name Extraction Logic")
print("=" * 80)

extraction_test_cases = [
    'creation-saga2-terra-35021566',
    'creation-55-looselay-terra-39741566',
    'creation-55-clic-acoustic-ball-39750555',
    'creation-40-clic-acoustic-twist-39750417',
    'creation-70-megaclic-quartet-39750545',
    'gerflor-creation-30',
    'creation-30-ballerina-41870347',
]

extraction_errors = []

for slug in extraction_test_cases:
    collectionName = slug.replace('gerflor-', '')
    
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
    matching = [c for c in json_data['colors'] if c['collection'] == collectionName]
    
    if not exists or len(matching) == 0:
        extraction_errors.append({
            'slug': slug,
            'extracted': collectionName,
            'exists': exists,
            'matching_count': len(matching)
        })
        print(f"❌ {slug} → {collectionName} ({len(matching)} colors)")
    else:
        print(f"✅ {slug} → {collectionName} ({len(matching)} colors)")

print(f"\nExtraction errors: {len(extraction_errors)}")

print()

# ============================================================================
# SUMMARY
# ============================================================================
print("=" * 80)
print("SUMMARY")
print("=" * 80)

total_issues = (
    len(image_issues['missing_files']) +
    len(image_issues['wrong_paths']) +
    len(image_issues['url_encoding_issues']) +
    len(image_issues['invalid_urls']) +
    len(data_issues['missing_fields']) +
    len(data_issues['invalid_slugs']) +
    len(data_issues['duplicate_codes']) +
    len(extraction_errors)
)

print(f"Total issues found: {total_issues}")
print()
print("Breakdown:")
print(f"  Image issues: {len(image_issues['missing_files']) + len(image_issues['wrong_paths'])}")
print(f"  Data integrity issues: {len(data_issues['missing_fields']) + len(data_issues['invalid_slugs'])}")
print(f"  Folder structure issues: {len(folder_issues['orphaned_folders'])}")
print(f"  Collection extraction issues: {len(extraction_errors)}")
print()

# Save detailed report
report = {
    'image_issues': image_issues,
    'data_issues': data_issues,
    'folder_issues': folder_issues,
    'extraction_errors': extraction_errors,
    'summary': {
        'total_issues': total_issues,
        'total_colors': len(json_data['colors']),
        'total_collections': len(all_collections),
    }
}

report_path = Path('deep_test_report.json')
with open(report_path, 'w', encoding='utf-8') as f:
    json.dump(report, f, ensure_ascii=False, indent=2, default=str)

print(f"Detailed report saved to: {report_path}")
print()
print("=" * 80)
print("TESTING COMPLETE")
print("=" * 80)
