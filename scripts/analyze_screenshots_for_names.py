#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Analizira screenshot-ove i izvlači PRAVA imena proizvoda
"""

import sys
from pathlib import Path
from PIL import Image
import pytesseract
import re

sys.stdout.reconfigure(encoding='utf-8')

print("="*80)
print("ANALIZA SCREENSHOT-OVA - IZVLAČENJE IMENA")
print("="*80)
print()

# Screenshot folder
screenshots_dir = Path("screenshots_tutorial")

if not screenshots_dir.exists():
    print("❌ Folder sa screenshot-ovima ne postoji!")
    sys.exit(1)

screenshots = sorted(screenshots_dir.glob("*.png"))
print(f"Pronađeno screenshot-ova: {len(screenshots)}\n")

# Analiziraj svaki 10-ti screenshot (jer su slični)
products_data = []

for idx in range(0, len(screenshots), 10):
    screenshot = screenshots[idx]
    
    try:
        # Open image
        img = Image.open(screenshot)
        
        # Extract text using OCR
        text = pytesseract.image_to_string(img)
        
        # Look for product codes and names
        # Format: "XXXX NAME" or "CREATION XX - NEW COLLECTION XXXX NAME"
        
        # Find 4-digit codes
        codes = re.findall(r'\b(\d{4})\s+([A-Z\s]+)', text)
        
        if codes:
            for code, name in codes:
                # Clean up name
                name = ' '.join(name.split())
                if len(name) > 3:  # Valid name
                    products_data.append({
                        'code': code,
                        'name': name,
                        'screenshot': screenshot.name
                    })
                    print(f"[{idx}/{len(screenshots)}] {code} {name}")
    
    except Exception as e:
        print(f"[{idx}] Greška: {e}")
        continue

print("\n" + "="*80)
print(f"Pronađeno proizvoda: {len(products_data)}")
print("="*80)

# Save results
import json
with open("scripts/scraped_names_from_screenshots.json", 'w', encoding='utf-8') as f:
    json.dump(products_data, f, indent=2, ensure_ascii=False)

print(f"Sačuvano u: scripts/scraped_names_from_screenshots.json")
