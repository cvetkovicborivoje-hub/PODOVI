#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SCRAPE COLOR NAMES - Čita prava imena i šifre sa Gerflor sajta
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

print("="*80)
print("GERFLOR - SCRAPE COLOR NAMES")
print("="*80)
print()

COLLECTIONS = [
    {"name": "Creation 30", "slug": "creation-30", "url": "https://www.gerflor-cee.com/products/creation-30-new-collection"},
    {"name": "Creation 40", "slug": "creation-40", "url": "https://www.gerflor-cee.com/products/creation-40-new-collection"},
    {"name": "Creation 40 Clic", "slug": "creation-40-clic", "url": "https://www.gerflor-cee.com/products/creation-40-clic-new-collection"},
    {"name": "Creation 40 Clic Acoustic", "slug": "creation-40-clic-acoustic", "url": "https://www.gerflor-cee.com/products/creation-40-clic-acoustic-new-collection"},
    {"name": "Creation 40 Zen", "slug": "creation-40-zen", "url": "https://www.gerflor-cee.com/products/creation-40-zen"},
    {"name": "Creation 55", "slug": "creation-55", "url": "https://www.gerflor-cee.com/products/creation-55-new-collection"},
    {"name": "Creation 55 Clic", "slug": "creation-55-clic", "url": "https://www.gerflor-cee.com/products/creation-55-clic-new-collection"},
    {"name": "Creation 55 Clic Acoustic", "slug": "creation-55-clic-acoustic", "url": "https://www.gerflor-cee.com/products/creation-55-clic-acoustic-new-collection"},
    {"name": "Creation 55 Looselay", "slug": "creation-55-looselay", "url": "https://www.gerflor-cee.com/products/creation-55-looselay"},
    {"name": "Creation 55 Looselay Acoustic", "slug": "creation-55-looselay-acoustic", "url": "https://www.gerflor-cee.com/products/creation-55-looselay-acoustic"},
    {"name": "Creation 55 Zen", "slug": "creation-55-zen", "url": "https://www.gerflor-cee.com/products/creation-55-zen"},
    {"name": "Creation 70", "slug": "creation-70", "url": "https://www.gerflor-cee.com/products/creation-70-new-collection"},
    {"name": "Creation 70 Clic", "slug": "creation-70-clic", "url": "https://www.gerflor-cee.com/products/creation-70-clic-5mm-new-collection"},
    {"name": "Creation 70 Connect", "slug": "creation-70-connect", "url": "https://www.gerflor-cee.com/products/creation-70-connect"},
    {"name": "Creation 70 Looselay", "slug": "creation-70-looselay", "url": "https://www.gerflor-cee.com/products/new-2025-creation-70-looselay"},
    {"name": "Creation 70 Megaclic", "slug": "creation-70-megaclic", "url": "https://www.gerflor-cee.com/products/creation-70-megaclic"},
    {"name": "Creation 70 Zen", "slug": "creation-70-zen", "url": "https://www.gerflor-cee.com/products/creation-70-zen"},
    {"name": "Creation Saga²", "slug": "creation-saga2", "url": "https://www.gerflor-cee.com/products/creation-saga2"},
]

# Chrome setup
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")

print("Pokrećem Chrome...")
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=chrome_options
)
wait = WebDriverWait(driver, 20)

all_colors = []

try:
    for collection in COLLECTIONS:
        print("="*80)
        print(f"KOLEKCIJA: {collection['name']}")
        print(f"URL: {collection['url']}")
        print("="*80)
        
        # Step 1: Open collection page
        print("\n1. Otvaram stranicu...")
        driver.get(collection['url'])
        time.sleep(3)
        
        # Close cookies if present
        try:
            accept_btn = wait.until(EC.element_to_be_clickable((
                By.XPATH, "//button[contains(text(), 'Accept All')]"
            )))
            driver.execute_script("arguments[0].click();", accept_btn)
            print("   ✓ Cookies zatvoren")
            time.sleep(1)
        except:
            print("   - Nema cookies")
        
        # Step 2: Click "View all" to open dialog
        print("\n2. Otvaram listu boja...")
        try:
            view_all_btn = wait.until(EC.element_to_be_clickable((
                By.CSS_SELECTOR, 
                "button.color-list-dialog-trigger, button[aria-controls='color-list-dialog']"
            )))
            driver.execute_script("arguments[0].click();", view_all_btn)
            print("   ✓ Dialog otvoren")
            time.sleep(2)
        except Exception as e:
            print(f"   ✗ Ne mogu da otvorim dialog: {e}")
            continue
        
        # Step 3: Wait for dialog
        try:
            dialog = wait.until(EC.presence_of_element_located((
                By.CSS_SELECTOR, "dialog#color-list-dialog[open]"
            )))
            print("   ✓ Dialog učitan")
        except Exception as e:
            print(f"   ✗ Dialog se nije učitao: {e}")
            continue
        
        # Step 4: Get all color items from dialog
        print("\n3. Čitam boje iz dialoga...")
        color_items = driver.find_elements(By.CSS_SELECTOR, "#color-list-dialog .color-list-dialog-item")
        print(f"   Pronađeno: {len(color_items)} boja")
        
        # Extract data from each color item
        for idx, item in enumerate(color_items, 1):
            try:
                # Get the link
                link = item.find_element(By.TAG_NAME, "a")
                href = link.get_attribute('href')
                
                # Get color code (e.g., "0347")
                try:
                    code_elem = item.find_element(By.CSS_SELECTOR, ".color-item-code, .color-code")
                    code = code_elem.text.strip()
                except:
                    # Try to extract from URL
                    url_parts = href.split('/')[-1].split('-')
                    # Find 4-digit code
                    code = None
                    for part in url_parts:
                        if part.isdigit() and len(part) == 4:
                            code = part
                            break
                    if not code:
                        code = "Unknown"
                
                # Get color name (e.g., "BALLERINA")
                try:
                    name_elem = item.find_element(By.CSS_SELECTOR, ".color-item-name, .color-name")
                    name = name_elem.text.strip()
                except:
                    # Try to extract from URL
                    url_parts = href.split('/')[-1]
                    # Remove collection prefix and code suffix
                    name = url_parts.replace(collection['slug'] + '-', '').replace('-new-collection-', '')
                    # Remove code parts
                    for part in url_parts.split('-'):
                        if part.isdigit():
                            name = name.replace('-' + part, '')
                    name = name.strip('-').replace('-', ' ').title()
                
                # Get SKU from URL (last part with numbers)
                url_parts = href.split('/')[-1]
                # SKU is usually the last numeric part (8 digits)
                sku = None
                for part in url_parts.split('-'):
                    if part.isdigit() and len(part) >= 8:
                        sku = part
                        break
                
                color_data = {
                    "collection": collection['name'],
                    "collection_slug": collection['slug'],
                    "code": code,
                    "name": name,
                    "sku": sku,
                    "url": href,
                }
                
                all_colors.append(color_data)
                
                if idx % 10 == 0:
                    print(f"   Pročitano: {idx}/{len(color_items)}")
                
            except Exception as e:
                print(f"   ✗ Greška kod boje {idx}: {e}")
        
        print(f"\n✓ Završeno: {len(color_items)} boja iz {collection['name']}\n")
        
        # Close dialog
        try:
            close_btn = driver.find_element(By.CSS_SELECTOR, "button.dlg__close, button.color-list-dialog-close")
            driver.execute_script("arguments[0].click();", close_btn)
            time.sleep(1)
        except:
            pass

except Exception as e:
    print(f"\n✗ GREŠKA: {e}")
    import traceback
    traceback.print_exc()

finally:
    # Save results
    output_path = "scripts/all_colors_with_names.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump({
            "total": len(all_colors),
            "colors": all_colors
        }, f, indent=2, ensure_ascii=False)
    
    print("\n" + "="*80)
    print("GOTOVO!")
    print("="*80)
    print(f"Ukupno boja: {len(all_colors)}")
    print(f"Sačuvano u: {output_path}")
    print()
    
    print("Zatvaram Chrome...")
    driver.quit()
    print("✓ Završeno!")
