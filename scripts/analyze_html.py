#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Analizira HTML fajl da nadje color linkove
"""

import re
import sys
sys.stdout.reconfigure(encoding='utf-8')

html_file = "downloads/debug_screenshots/04_after_view_all_click.html"

print("="*80)
print("ANALIZA HTML FAJLA")
print("="*80)

with open(html_file, "r", encoding="utf-8") as f:
    html = f.read()

print(f"\nHTML fajl: {len(html)} karaktera")

# Find all links with "creation-30" and "/products/"
pattern = r'href="([^"]*creation-30[^"]*)"'
matches = re.findall(pattern, html)

print(f"\nPronađeno {len(matches)} linkova sa 'creation-30'")

# Filter only product pages (not collection page)
product_links = []
for match in matches:
    if '/products/' in match and len(match.split('/')[-1]) > 30:
        if match not in product_links:
            product_links.append(match)

print(f"Od toga {len(product_links)} individual product linkova:")
for idx, link in enumerate(product_links[:10], 1):
    print(f"  {idx}. {link}")

# Find all links with .JPG or JPG
jpg_pattern = r'href="([^"]*\.(?:jpg|JPG|zip)[^"]*)"'
jpg_matches = re.findall(jpg_pattern, html)

print(f"\n\nPronađeno {len(jpg_matches)} linkova ka JPG/ZIP fajlovima:")
for idx, link in enumerate(jpg_matches[:10], 1):
    print(f"  {idx}. {link}")

print("\n" + "="*80)
