#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pametno ekstraktuje imena iz fajlova - bira najbolji fajl za ime
"""

import json
import sys
import re
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

print("="*80)
print("PAMETNA EKSTRAKCIJA IMENA")
print("="*80)
print()

# Load colors
with open("downloads/gerflor_dialog/extracted_colors.json", 'r', encoding='utf-8') as f:
    colors_data = json.load(f)

all_colors = colors_data['colors']
print(f"Ukupno boja: {len(all_colors)}\n")

# Load real scraped names
with open("scripts/products_real_scraped_final.json", 'r', encoding='utf-8') as f:
    real_names_data = json.load(f)

real_names = {}
for product in real_names_data['products']:
    code = product['code']
    real_names[code] = product['real_name']

print(f"Pravih imena: {len(real_names)}\n")

# Funkcije za filtriranje fajlova
def has_furniture(filename):
    """Proverava da li fajl sadrži roomscene/skyview"""
    lower = filename.lower()
    furniture_words = ['sky-view', 'skyview', 'room scene', 'roomscene', 
                       'bedroom', 'kitchen', 'bathroom', 'office', 'restaurant']
    return any(word in lower for word in furniture_words)

def is_simple_swatch(filename):
    """Proverava da li je jednostavan swatch (5 cifara - kod - ime)"""
    # "49041 - 0347 Ballerina .jpg"
    return re.match(r'^\d{5}\s*-\s*\d{4}', filename) is not None

def extract_name_from_filename(filename):
    """Ekstraktuje ime iz naziva fajla"""
    # Remove extension
    name = filename.rsplit('.', 1)[0]
    
    # Step 1: Remove prefixes
    name = re.sub(r'^\d+\s*-\s*', '', name)  # Remove leading numbers "62346 - "
    name = re.sub(r'^\d{4}\s*-?\s*', '', name)  # Remove code "0347-"
    name = re.sub(r'^JPG\s+72\s+dpi-?', '', name, flags=re.IGNORECASE)  # Remove "JPG 72 dpi-"
    name = re.sub(r'^RS\d+_?', '', name, flags=re.IGNORECASE)  # Remove "RS12345_"
    name = re.sub(r'^ENHANCED\s+', '', name, flags=re.IGNORECASE)  # Remove "ENHANCED "
    
    # Step 2: Remove "Creation XX" patterns
    name = re.sub(r'Creation\s+\d+\s+', '', name, flags=re.IGNORECASE)  # "Creation 1272 "
    name = re.sub(r'\s+\d{4}\s+Creation2?', '', name, flags=re.IGNORECASE)  # " 1704 CREATION2"
    name = re.sub(r'\s+Creation2?(\s+HP)?$', '', name, flags=re.IGNORECASE)  # " CREATION" or " CREATION HP" at end
    name = re.sub(r'_Creation(\s+HP)?$', '', name, flags=re.IGNORECASE)  # "_Creation" or "_Creation HP"
    
    # Step 3: Remove room/view suffixes
    name = re.sub(r'-?sky[-\s]?view', '', name, flags=re.IGNORECASE)  # "sky-view" or "Sky View"
    name = re.sub(r'-?room[-\s]?scene', '', name, flags=re.IGNORECASE)  # "room-scene" or "Room Scene"
    
    # Step 4: Remove other suffixes
    name = re.sub(r'-?\d+x\d+[^a-zA-Z]*', '', name)  # "610x610_TERRA-NOVA"
    name = re.sub(r'\s+HB\s+VDC$', '', name, flags=re.IGNORECASE)  # " HB VDC"
    name = re.sub(r'\s+(HP|VDC|HB)$', '', name, flags=re.IGNORECASE)  # " HP", " VDC", " HB"
    name = re.sub(r'\s+COPIE\s*\(\d+\)', '', name, flags=re.IGNORECASE)  # " COPIE (1)"
    name = re.sub(r'\s+COPIE$', '', name, flags=re.IGNORECASE)  # " COPIE"
    name = re.sub(r'\(\d+\)\s*$', '', name)  # "(1)" at end
    
    # Clean up
    name = name.replace('-', ' ').replace('_', ' ')
    name = ' '.join(name.split())
    name = name.strip(' .')
    
    # Step 5: Split by problem keywords and take first part
    problem_keywords = ['TERRA NOVA', 'COPIE', 'CREATION2', 'CREATION']
    for keyword in problem_keywords:
        if keyword in name.upper():
            parts = re.split(r'\s*' + keyword + r'\s*', name, flags=re.IGNORECASE)
            if parts and parts[0]:
                name = parts[0].strip()
    
    # Final cleanup - remove trailing numbers and "ENHANCED"
    name = re.sub(r'\s+\d{4}\s*$', '', name)  # Remove trailing "1704"
    name = re.sub(r'^ENHANCED\s+', '', name, flags=re.IGNORECASE)
    
    return name.upper()

# Process all colors
results = []

for color in all_colors:
    # Extract code
    match = re.search(r'(\d{4})$', color['color_slug'])
    code = match.group(1) if match else None
    
    # Use real name if available
    if code and code in real_names:
        name = real_names[code]
        source = "scraped"
    else:
        # Find best file to extract name from
        image_url = color['image_url']
        # Get folder with same name as image (without extension)
        image_path = Path(f"public{image_url}")
        folder_name = image_path.stem  # Get filename without extension
        path = image_path.parent / folder_name
        
        if path.exists():
            # Get all images
            images = list(path.glob("*.jpg")) + list(path.glob("*.png"))
            
            # Filter out the main image (color_slug.jpg)
            images = [img for img in images if img.stem != color['color_slug']]
            
            if images:
                # Prioritize simple swatch files
                simple_swatches = [img for img in images if is_simple_swatch(img.name)]
                
                if simple_swatches:
                    best_file = simple_swatches[0]
                else:
                    # Filter out furniture images
                    no_furniture = [img for img in images if not has_furniture(img.name)]
                    
                    if no_furniture:
                        # Choose shortest filename (usually simplest)
                        best_file = min(no_furniture, key=lambda x: len(x.name))
                    else:
                        # Use any image
                        best_file = images[0]
                
                name = extract_name_from_filename(best_file.name)
                source = "extracted"
            else:
                # Fallback to color_slug
                name = color['color_slug'].rsplit('-', 1)[0].replace('-', ' ').upper()
                source = "fallback"
        else:
            name = color['color_slug'].rsplit('-', 1)[0].replace('-', ' ').upper()
            source = "fallback"
    
    results.append({
        "collection": color['collection'],
        "color_slug": color['color_slug'],
        "code": code or "Unknown",
        "name": name,
        "image_url": color['image_url'],
        "source": source
    })

# Stats
scraped = len([r for r in results if r['source'] == 'scraped'])
extracted = len([r for r in results if r['source'] == 'extracted'])
fallback = len([r for r in results if r['source'] == 'fallback'])

print(f"✅ Scraped: {scraped}")
print(f"📦 Extracted: {extracted}")
print(f"⚠️  Fallback: {fallback}")
print(f"📊 Ukupno: {len(results)}\n")

# Save
output_path = "scripts/all_products_smart_names.json"
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump({
        "total": len(results),
        "products": results
    }, f, indent=2, ensure_ascii=False)

print(f"✅ Sačuvano u: {output_path}\n")

# Show examples
print("Primeri (prvih 30):\n")
for i in range(min(30, len(results))):
    p = results[i]
    print(f"  {p['code']} {p['name']} ({p['source']})")
