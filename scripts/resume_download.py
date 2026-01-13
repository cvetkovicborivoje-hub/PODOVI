#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RESUME DOWNLOAD - Nastavlja odakle je script stao
"""

import os
import sys

# Read main script
script_path = r"D:\PODOVI\SAJT\scripts\download_from_dialog.py"
with open(script_path, 'r', encoding='utf-8') as f:
    script_content = f.read()

# Modify to skip completed collections
DOWNLOAD_DIR = r"D:\PODOVI\SAJT\downloads\gerflor_dialog"

print("Proveravam koje kolekcije su vec download-ovane...")
print()

completed_collections = []
for item in os.listdir(DOWNLOAD_DIR):
    item_path = os.path.join(DOWNLOAD_DIR, item)
    if os.path.isdir(item_path):
        zips = [f for f in os.listdir(item_path) if f.endswith('.zip')]
        if len(zips) > 0:
            completed_collections.append(item)
            print(f"✅ {item}: {len(zips)} boja vec download-ovano - PRESKOCI")

print()
print(f"Preskacujem {len(completed_collections)} kolekcija")
print()

# Execute script
exec(script_content)
