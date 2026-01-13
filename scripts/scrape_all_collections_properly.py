#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Prolazi kroz SVE Gerflor kolekcije i čita SVA imena
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import json
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

print("="*80)
print("PROČITAJ SVA IMENA - SVE KOLEKCIJE")
print("="*80)
print()

# Gerflor collections
collections = [
    {"name": "Creation 30", "slug": "creation-30", "url": "https://www.gerflor-cee.com/products/creation-30-new-collection"},
    {"name": "Creation 40", "slug": "creation-40", "url": "https://www.gerflor-cee.com/products/creation-40-new-collection"},
    {"name": "Creation 55", "slug": "creation-55", "url": "https://www.gerflor-cee.com/products/creation-55-new-collection"},
    {"name": "Creation 70", "slug": "creation-70", "url": "https://www.gerflor-cee.com/products/creation-70-new-collection"},
]

print(f"Kolekcije za obradu: {len(collections)}\n")

# Chrome setup
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)

print("Pokrećem Chrome...")
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=chrome_options
)
wait = WebDriverWait(driver, 10)

# Accept cookies
try:
    driver.get(collections[0]['url'])
    time.sleep(2)
    accept_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Accept')]")
    driver.execute_script("arguments[0].click();", accept_btn)
    print("✓ Cookies accepted\n")
    time.sleep(1)
except:
    print("- No cookies\n")

all_results = []

try:
    for coll_idx, collection in enumerate(collections, 1):
        print(f"\n{'='*80}")
        print(f"[{coll_idx}/{len(collections)}] {collection['name']}")
        print(f"{'='*80}\n")
        
        driver.get(collection['url'])
        time.sleep(2)
        
        # Click "View all" button
        try:
            view_all_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'View all')]")))
            driver.execute_script("arguments[0].click();", view_all_btn)
            print("✓ Kliknuo 'View all'\n")
            time.sleep(2)
            
            # Find all color items in the dialog
            # They are usually in a list or grid
            color_items = driver.find_elements(By.XPATH, "//div[contains(@class, 'color') or contains(@class, 'swatch') or contains(@class, 'product-item')]//a")
            
            print(f"Pronađeno {len(color_items)} boja\n")
            
            if len(color_items) == 0:
                print("⚠️  Nisam našao boje u dialogu!\n")
                continue
            
            # Click each color and read its name
            for idx in range(len(color_items)):
                try:
                    # Re-find elements (to avoid stale reference)
                    color_items = driver.find_elements(By.XPATH, "//div[contains(@class, 'color') or contains(@class, 'swatch') or contains(@class, 'product-item')]//a")
                    
                    if idx >= len(color_items):
                        break
                    
                    color_item = color_items[idx]
                    
                    # Get href before clicking
                    href = color_item.get_attribute('href')
                    
                    # Click
                    driver.execute_script("arguments[0].click();", color_item)
                    time.sleep(1)
                    
                    # Read H1
                    try:
                        heading = wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1")))
                        full_text = heading.text.strip()
                        
                        # Extract code + name
                        text = re.sub(r'^CREATION\s+\d+\s+-\s+NEW\s+COLLECTION\s+', '', full_text, flags=re.IGNORECASE)
                        
                        match = re.search(r'(\d{4})\s+(.+)', text)
                        if match:
                            code = match.group(1)
                            name = match.group(2).strip()
                        else:
                            code = "Unknown"
                            name = text
                        
                        all_results.append({
                            "collection": collection['name'],
                            "collection_slug": collection['slug'],
                            "code": code,
                            "real_name": name.upper(),
                            "url": href
                        })
                        
                        print(f"  [{idx+1}/{len(color_items)}] {code} {name}")
                        
                    except Exception as e:
                        print(f"  [{idx+1}/{len(color_items)}] ✗ Ne mogu da pročitam heading: {e}")
                    
                    # Go back
                    driver.back()
                    time.sleep(1)
                    
                    # Re-open "View all" dialog
                    view_all_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'View all')]")))
                    driver.execute_script("arguments[0].click();", view_all_btn)
                    time.sleep(1)
                    
                except Exception as e:
                    print(f"  [{idx+1}] ✗ Greška: {e}")
                    continue
        
        except Exception as e:
            print(f"✗ Ne mogu da otvorim 'View all': {e}\n")

except KeyboardInterrupt:
    print("\n\n⏹️  Prekinuto")

finally:
    output_path = "scripts/all_colors_scraped_complete.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump({
            "total": len(all_results),
            "products": all_results
        }, f, indent=2, ensure_ascii=False)
    
    print("\n" + "="*80)
    print("GOTOVO!")
    print("="*80)
    print(f"Pročitano: {len(all_results)} proizvoda")
    print(f"Sačuvano u: {output_path}")
    
    driver.quit()
    print("✓ Završeno!")
