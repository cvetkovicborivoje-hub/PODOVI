#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Izvuci SIFRU + IME za svaku boju iz URL-a/fajla
"""

import os
import sys
import json
import re

sys.stdout.reconfigure(encoding='utf-8')

print("="*80)
print("IZVLAČENJE ŠIFRI + IMENA")
print("="*80)
print()

# Load extracted colors
json_path = r"D:\PODOVI\SAJT\downloads\gerflor_dialog\extracted_colors.json"
with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Učitano: {len(data['colors'])} boja")
print()

# Extract code + name from zip_name
# Examples:
# "ballerina-41870347.zip" → Šifra je u kodu (41870347 → 0347), Ime je "ballerina"
# "honey-oak-41870441.zip" → Šifra je u kodu (41870441 → 0441), Ime je "honey oak"

final_colors = []

for color in data['colors']:
    zip_name = color['zip_name']
    color_slug = color['color_slug']
    
    # Remove .zip
    name_part = zip_name.replace('.zip', '')
    
    # Split by last dash to get code
    # "ballerina-41870347" → ["ballerina", "41870347"]
    # "honey-oak-41870441" → ["honey-oak", "41870441"]
    parts = name_part.rsplit('-', 1)
    
    if len(parts) == 2:
        name_raw = parts[0]  # "ballerina" or "honey-oak"
        code_full = parts[1]  # "41870347"
        
        # Extract 4-digit code from end
        # "41870347" → "0347"
        code_short = code_full[-4:] if len(code_full) >= 4 else code_full
        
        # Clean up name: replace dashes with spaces, capitalize
        name_clean = name_raw.replace('-', ' ').upper()
        
        # Full name: "0347 BALLERINA"
        full_name = f"{code_short} {name_clean}"
    else:
        # Fallback
        code_short = "????"
        name_clean = name_part.upper()
        full_name = name_clean
    
    final_colors.append({
        "collection": color['collection'],
        "collection_name": color['collection'].replace('-', ' ').title(),
        "code": code_short,
        "name": name_clean,
        "full_name": full_name,
        "slug": color_slug,
        "image_url": color['image_url'],
        "image_count": color['image_count']
    })

print(f"✅ Procesovano: {len(final_colors)} boja")
print()

# Show first 10 as examples
print("Primeri:")
for i, color in enumerate(final_colors[:10]):
    print(f"   {i+1}. {color['full_name']} ({color['collection_name']})")

print()

# Save final JSON
output_path = r"D:\PODOVI\SAJT\public\data\lvt_colors_complete.json"
os.makedirs(os.path.dirname(output_path), exist_ok=True)

with open(output_path, 'w', encoding='utf-8') as f:
    json.dump({
        "total": len(final_colors),
        "collections": len(set(c['collection'] for c in final_colors)),
        "colors": final_colors
    }, f, indent=2, ensure_ascii=False)

print(f"💾 Sačuvano: {output_path}")
print()

# Group by collection
by_collection = {}
for color in final_colors:
    coll = color['collection']
    if coll not in by_collection:
        by_collection[coll] = []
    by_collection[coll].append(color)

print("Po kolekcijama:")
for coll, colors in sorted(by_collection.items()):
    print(f"   {coll}: {len(colors)} boja")

print()
print("="*80)
print("GOTOVO!")
print("="*80)
