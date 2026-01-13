#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Otvara SVAKI proizvod na Gerflor sajtu i čita PRAVO IME
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

sys.stdout.reconfigure(encoding='utf-8')

print("="*80)
print("ČITANJE PRAVIH IMENA - OTVARANJEM SVAKE BOJE NA SAJTU")
print("="*80)
print()

# Load products with URLs
with open("scripts/products_ultra_clean.json", 'r', encoding='utf-8') as f:
    data = json.load(f)

products = data['products']

# For testing, limit to first 10
TEST_MODE = True
if TEST_MODE:
    products = products[:10]
    print("TEST MODE: Samo prvih 10 proizvoda\n")

print(f"Ukupno proizvoda: {len(products)}\n")

# Chrome setup
chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument("--headless")  # Disabled - Gerflor blocks headless
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("--start-maximized")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)

print("Pokrećem Chrome...")
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=chrome_options
)
wait = WebDriverWait(driver, 10)

# Accept cookies once
try:
    # Build URL for first product
    first_url = f"https://www.gerflor-cee.com/products/{products[0]['collection_slug']}-new-collection-{products[0]['code']}-{products[0]['color_slug'].split('-')[0]}-{products[0]['sku']}"
    
    driver.get(first_url)
    time.sleep(2)
    
    accept_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Accept')]")
    driver.execute_script("arguments[0].click();", accept_btn)
    print("✓ Cookies accepted\n")
    time.sleep(1)
except:
    print("- No cookies\n")

results = []

try:
    for idx, product in enumerate(products, 1):
        collection_slug = product['collection_slug']
        code = product['code']
        sku = product['sku']
        color_slug_part = product['color_slug'].split('-')[0]
        
        # Build URL
        if collection_slug == "creation-saga2":
            url_part = "creation-saga2"
        elif "new-collection" in product.get('url', ''):
            url_part = f"{collection_slug}-new-collection"
        else:
            url_part = collection_slug
        
        url = f"https://www.gerflor-cee.com/products/{url_part}-{code}-{color_slug_part}-{sku}"
        
        print(f"[{idx}/{len(products)}] {collection_slug} {code}... ", end='', flush=True)
        
        try:
            driver.get(url)
            time.sleep(0.5)  # Short wait
            
            # Find heading with product name
            # Format: "0347 BALLERINA" or similar
            try:
                heading = driver.find_element(By.XPATH, "//h1 | //h2[contains(@class, 'product') or contains(@class, 'title')]")
                full_text = heading.text.strip()
                
                # Extract just the code + name part (not the collection)
                # Usually it's "CREATION 40 - NEW COLLECTION" (link) then "0347 BALLERINA" (heading)
                # So we look for h1 or h2 that contains the code
                
                if code in full_text:
                    # Found it
                    real_name = full_text.split(code, 1)[-1].strip()
                else:
                    real_name = full_text
                
                results.append({
                    **product,
                    'real_name': real_name.upper(),
                    'url_used': url
                })
                
                print(f"✓ {real_name}")
                
            except Exception as e:
                print(f"✗ Ne mogu da pročitam heading: {e}")
                results.append({
                    **product,
                    'real_name': product['name'],  # Keep old name
                    'url_used': url
                })
        
        except Exception as e:
            print(f"✗ Greška: {e}")
            results.append({
                **product,
                'real_name': product['name'],  # Keep old name
                'url_used': None
            })
        
        # Progress
        if idx % 50 == 0:
            print(f"\n--- Pročitano {idx}/{len(products)} ---\n")

except KeyboardInterrupt:
    print("\n\n⏹️  Prekinuto")

finally:
    # Save
    output_path = "scripts/products_with_real_scraped_names.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump({
            "total": len(results),
            "products": results
        }, f, indent=2, ensure_ascii=False)
    
    print("\n" + "="*80)
    print("GOTOVO!")
    print("="*80)
    print(f"Pročitano: {len(results)}/{len(products)}")
    print(f"Sačuvano u: {output_path}")
    
    driver.quit()
    print("✓ Završeno!")
