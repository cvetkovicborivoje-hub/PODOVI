#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Preuzima PRAVE SWATCH SLIKE sa Gerflor sajta
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import requests
import json
import sys
from pathlib import Path
import re

sys.stdout.reconfigure(encoding='utf-8')

print("="*80)
print("PREUZIMANJE PRAVIH SWATCH SLIKA SA GERFLOR SAJTA")
print("="*80)
print()

# Gerflor collections
collections = [
    {"name": "Creation 30", "slug": "creation-30", "url": "https://www.gerflor-cee.com/products/creation-30-new-collection"},
]

print(f"Kolekcije: {len(collections)}\n")

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

all_swatches = []

try:
    for coll_idx, collection in enumerate(collections, 1):
        print(f"[{coll_idx}/{len(collections)}] {collection['name']}...\n")
        
        driver.get(collection['url'])
        time.sleep(2)
        
        # Click "View all"
        try:
            view_all_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'View all')]")))
            driver.execute_script("arguments[0].click();", view_all_btn)
            print("✓ Otvoren 'View all' dialog\n")
            time.sleep(2)
            
            # Find all swatch images in the dialog
            # They are usually <img> elements with specific class or inside specific divs
            swatch_containers = driver.find_elements(By.XPATH, "//img[contains(@src, 'cloudinary') or contains(@src, 'gerflor')][@alt]")
            
            print(f"Pronađeno {len(swatch_containers)} slika\n")
            
            for idx, swatch_img in enumerate(swatch_containers, 1):
                try:
                    # Get image URL
                    img_url = swatch_img.get_attribute('src')
                    
                    # Skip if not a swatch (too large or wrong URL)
                    if not img_url or 'cloudinary' not in img_url:
                        continue
                    
                    # Get alt text (contains code + name)
                    alt_text = swatch_img.get_attribute('alt')
                    
                    # Extract code from alt or nearby text
                    # Usually format: "0347 BALLERINA" or similar
                    parent = swatch_img.find_element(By.XPATH, "./ancestor::*[contains(@class, 'color') or contains(@class, 'swatch') or contains(@class, 'product')]")
                    text_content = parent.text
                    
                    # Extract code (4 digits)
                    code_match = re.search(r'\b(\d{4})\b', text_content)
                    if not code_match:
                        continue
                    
                    code = code_match.group(1)
                    
                    all_swatches.append({
                        'collection': collection['slug'],
                        'code': code,
                        'image_url': img_url,
                        'alt_text': alt_text or text_content,
                    })
                    
                    print(f"  [{idx}] {code}: {img_url[:80]}...")
                    
                except Exception as e:
                    continue
        
        except Exception as e:
            print(f"✗ Greška: {e}\n")

except KeyboardInterrupt:
    print("\n\n⏹️  Prekinuto")

finally:
    driver.quit()
    
    # Save results
    output_path = "scripts/gerflor_swatch_urls.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump({
            "total": len(all_swatches),
            "swatches": all_swatches
        }, f, indent=2, ensure_ascii=False)
    
    print("\n" + "="*80)
    print("GOTOVO!")
    print("="*80)
    print(f"Pronađeno: {len(all_swatches)} swatch slika")
    print(f"Sačuvano u: {output_path}")
    print("✓ Završeno!")
