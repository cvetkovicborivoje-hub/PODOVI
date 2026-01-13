#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Analyze dialog HTML to find color links"""

from bs4 import BeautifulSoup
import sys

html_path = r"D:\PODOVI\SAJT\downloads\manual_screenshots\02_page.html"

with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

# Find dialog
dialog = soup.find('dialog', id='color-list-dialog')

if not dialog:
    print("ERROR: Dialog not found!")
    sys.exit(1)

print(f"Dialog found! Has 'open' attribute: {dialog.has_attr('open')}")
print()

# Find all links in dialog
links = dialog.find_all('a', href=True)
print(f"Total links in dialog: {len(links)}")
print()

# Filter product links
product_links = [l for l in links if '/products/creation-30-new-collection-' in l.get('href', '')]
print(f"Product color links: {len(product_links)}")
print()

# Show first 10
for i, link in enumerate(product_links[:10]):
    href = link.get('href')
    text = link.get_text(strip=True)
    print(f"{i+1}. {href}")
    if text:
        print(f"   Text: {text}")

print()
print(f"... and {len(product_links) - 10} more")
