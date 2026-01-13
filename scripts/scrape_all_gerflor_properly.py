#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Automatski scrape SVE Gerflor kolekcije i boje
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
import re

sys.stdout.reconfigure(encoding='utf-8')

print("="*80)
print("AUTOMATSKI SCRAPING SVIH GERFLOR PROIZVODA")
print("="*80)
print()

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
wait = WebDriverWait(driver, 15)

# Known collections based on Gerflor website structure
collection_urls = [
    "https://www.gerflor-cee.com/products/creation-30-new-collection",
    "https://www.gerflor-cee.com/products/creation-40-new-collection",
    "https://www.gerflor-cee.com/products/creation-40-clic-new-collection",
    "https://www.gerflor-cee.com/products/creation-40-clic-acoustic-new-collection",
    "https://www.gerflor-cee.com/products/creation-40-zen",
    "https://www.gerflor-cee.com/products/creation-55-new-collection",
    "https://www.gerflor-cee.com/products/creation-55-clic-new-collection",
    "https://www.gerflor-cee.com/products/creation-55-clic-acoustic-new-collection",
    "https://www.gerflor-cee.com/products/creation-55-looselay",
    "https://www.gerflor-cee.com/products/creation-55-looselay-acoustic",
    "https://www.gerflor-cee.com/products/creation-55-zen",
    "https://www.gerflor-cee.com/products/creation-70-new-collection",
    "https://www.gerflor-cee.com/products/creation-70-clic-5mm-new-collection",
    "https://www.gerflor-cee.com/products/creation-70-connect",
    "https://www.gerflor-cee.com/products/creation-70-looselay",
    "https://www.gerflor-cee.com/products/new-2025-creation-70-looselay",
    "https://www.gerflor-cee.com/products/creation-70-megaclic",
    "https://www.gerflor-cee.com/products/creation-70-zen",
    "https://www.gerflor-cee.com/products/creation-saga2",
]

print(f"Kolekcije za obradu: {len(collection_urls)}\n")

try:
    # Accept cookies on first page
    driver.get(collection_urls[0])
    time.sleep(3)
    try:
        accept_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Accept')]")
        driver.execute_script("arguments[0].click();", accept_btn)
        print("✓ Cookies accepted\n")
        time.sleep(1)
    except:
        print("- No cookies dialog\n")
    
    all_products = []
    
    for coll_idx, collection_url in enumerate(collection_urls, 1):
        print(f"\n{'='*80}")
        print(f"[{coll_idx}/{len(collection_urls)}] {collection_url}")
        print(f"{'='*80}\n")
        
        try:
            driver.get(collection_url)
            time.sleep(3)
            
            # Get collection name
            try:
                collection_heading = driver.find_element(By.TAG_NAME, "h1")
                collection_name = collection_heading.text.strip()
                print(f"Kolekcija: {collection_name}\n")
            except:
                collection_name = collection_url.split('/')[-1]
            
            # Click "View all" to see all colors
            try:
                view_all_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'View all')]")))
                driver.execute_script("arguments[0].click();", view_all_btn)
                print("✓ Otvoren 'View all' dialog\n")
                time.sleep(2)
            except Exception as e:
                print(f"✗ Ne mogu da otvorim 'View all': {e}\n")
                continue
            
            # Find all color items in the dialog
            color_links = driver.find_elements(By.XPATH, "//a[contains(@href, '/products/creation-')]")
            
            color_urls = []
            for link in color_links:
                url = link.get_attribute('href')
                if url and url != collection_url and url not in color_urls:
                    color_urls.append(url)
            
            print(f"Pronađeno boja: {len(color_urls)}\n")
            
            # Visit each color
            for color_idx, color_url in enumerate(color_urls, 1):
                print(f"  [{color_idx}/{len(color_urls)}] ", end='', flush=True)
                
                try:
                    driver.get(color_url)
                    time.sleep(1)
                    
                    # Extract product info
                    try:
                        # Get heading with code and name
                        heading = wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1")))
                        full_text = heading.text.strip()
                        
                        # Extract code and name
                        # Format: "CREATION XX - NEW COLLECTION XXXX NAME"
                        match = re.search(r'(\d{4})\s+(.+?)(?:\s*$)', full_text)
                        if match:
                            code = match.group(1)
                            name = match.group(2).strip()
                        else:
                            # Try alternative format
                            parts = full_text.split()
                            code = None
                            for part in parts:
                                if part.isdigit() and len(part) == 4:
                                    code = part
                                    break
                            if code:
                                idx = parts.index(code)
                                name = ' '.join(parts[idx+1:])
                            else:
                                code = "UNKNOWN"
                                name = full_text
                        
                        all_products.append({
                            'collection': collection_name,
                            'collection_url': collection_url,
                            'code': code,
                            'name': name.upper(),
                            'url': color_url
                        })
                        
                        print(f"{code} {name}")
                    
                    except Exception as e:
                        print(f"✗ Greška pri čitanju: {e}")
                
                except Exception as e:
                    print(f"✗ Ne mogu da otvorim: {e}")
                    continue
        
        except Exception as e:
            print(f"✗ Greška pri obradi kolekcije: {e}\n")
            continue

except KeyboardInterrupt:
    print("\n\n⏹️  Prekinuto korisničkim zahtevom")

except Exception as e:
    print(f"\n\n❌ Kritična greška: {e}")

finally:
    # Save results
    output_path = "scripts/gerflor_complete_scrape.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump({
            "total": len(all_products),
            "products": all_products
        }, f, indent=2, ensure_ascii=False)
    
    print("\n" + "="*80)
    print("GOTOVO!")
    print("="*80)
    print(f"Ukupno proizvoda: {len(all_products)}")
    print(f"Sačuvano u: {output_path}")
    
    driver.quit()
    print("\n✓ Chrome zatvoren")
