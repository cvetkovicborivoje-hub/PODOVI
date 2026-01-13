#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BATCH UPDATE: Zameni SVE image_url sa texture_url
"""

import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

print("="*80)
print("BATCH UPDATE - Zamena image_url → texture_url")
print("="*80)
print()

# Load JSON
json_path = r"D:\PODOVI\SAJT\public\data\lvt_colors_complete.json"
with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Učitano: {len(data['colors'])} boja")
print()

# Update all image_url to point to texture_url
updated = 0
for color in data['colors']:
    if 'texture_url' in color and color['texture_url']:
        # Replace image_url with texture_url
        old_url = color.get('image_url', 'N/A')
        color['image_url'] = color['texture_url']
        updated += 1
        
        if updated <= 5:
            print(f"✅ {color['full_name']}: {old_url} → {color['texture_url']}")

print()
print(f"Update-ovano: {updated} boja")
print()

# Save
with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"💾 Sačuvano: {json_path}")
print()
print("="*80)
print("GOTOVO! SVE image_url sada pokazuju na TEKSTURE!")
print("="*80)
