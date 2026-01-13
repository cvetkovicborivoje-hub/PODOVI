#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Scrape-uje JEDNU kolekciju
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

# URL kolekcije
COLLECTION_URL = "https://www.gerflor-cee.com/products/new-2025-creation-70-looselay"

print("="*80)
print(f"SCRAPING: {COLLECTION_URL}")
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

all_products = []

try:
    driver.get(COLLECTION_URL)
    time.sleep(3)
    
    # Accept cookies
    try:
        accept_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Accept')]")
        driver.execute_script("arguments[0].click();", accept_btn)
        print("✓ Cookies accepted\n")
        time.sleep(1)
    except:
        print("- No cookies\n")
    
    # Get collection name
    try:
        collection_heading = driver.find_element(By.TAG_NAME, "h1")
        collection_name = collection_heading.text.strip()
        print(f"Kolekcija: {collection_name}\n")
    except:
        collection_name = COLLECTION_URL.split('/')[-1]
    
    # Click "View all"
    try:
        view_all_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'View all')]")))
        driver.execute_script("arguments[0].click();", view_all_btn)
        print("✓ Otvoren 'View all' dialog\n")
        time.sleep(2)
    except Exception as e:
        print(f"✗ Ne mogu da otvorim 'View all': {e}\n")
        driver.quit()
        sys.exit(1)
    
    # Find all color links
    color_links = driver.find_elements(By.XPATH, "//a[contains(@href, '/products/')]")
    
    color_urls = []
    for link in color_links:
        url = link.get_attribute('href')
        if url and url != COLLECTION_URL and url not in color_urls:
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
                heading = wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1")))
                full_text = heading.text.strip()
                
                # Extract code and name
                match = re.search(r'(\d{4})\s+(.+?)(?:\s*$)', full_text)
                if match:
                    code = match.group(1)
                    name = match.group(2).strip()
                else:
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
                    'collection_url': COLLECTION_URL,
                    'code': code,
                    'name': name.upper(),
                    'url': color_url
                })
                
                print(f"{code} {name}")
            
            except Exception as e:
                print(f"✗ Greška: {e}")
        
        except Exception as e:
            print(f"✗ Ne mogu da otvorim: {e}")
            continue

except KeyboardInterrupt:
    print("\n\n⏹️  Prekinuto")

except Exception as e:
    print(f"\n\n❌ Greška: {e}")

finally:
    output_path = "scripts/new_2025_creation_70_looselay.json"
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
