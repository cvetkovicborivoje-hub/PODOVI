#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Čita PRAVA imena direktno sa Gerflor sajta za svaki proizvod
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
print("ČITANJE PRAVIH IMENA SA GERFLOR SAJTA")
print("="*80)
print()

# Load existing products to get URLs
with open("scripts/all_gerflor_products.json", 'r', encoding='utf-8') as f:
    data = json.load(f)

products = data['products']

print(f"Ukupno proizvoda za proveru: {len(products)}\n")

# Chrome setup - headless mode
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")

print("Pokrećem Chrome (headless)...")
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=chrome_options
)
wait = WebDriverWait(driver, 10)

# Accept cookies once
try:
    driver.get(products[0]['url'])
    time.sleep(2)
    accept_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Accept')]")
    driver.execute_script("arguments[0].click();", accept_btn)
    print("✓ Cookies accepted\n")
    time.sleep(1)
except:
    pass

results = []

try:
    for idx, product in enumerate(products, 1):
        url = product['url']
        
        print(f"[{idx}/{len(products)}] {product['code']} {product['color_name']}... ", end='', flush=True)
        
        try:
            driver.get(url)
            time.sleep(1)
            
            # Try to find the H1 title
            try:
                h1 = driver.find_element(By.TAG_NAME, "h1")
                full_title = h1.text.strip()
                
                # Title format: "CREATION 40 - NEW COLLECTION" then separate "0347 BALLERINA"
                # OR just "0347 BALLERINA"
                
                # Extract code and name
                # Look for pattern: 4-digit code followed by name
                match = re.search(r'(\d{4})\s+(.+)', full_title)
                
                if match:
                    code = match.group(1)
                    name = match.group(2).strip()
                    
                    results.append({
                        'id': product['id'],
                        'url': url,
                        'code': code,
                        'name': name,
                        'sku': product['sku'],
                        'collection': product['collection'],
                        'collection_slug': product['collection_slug'],
                        'image_url': product['images'][0]['url'],
                        'color_slug': product.get('color_slug', '')
                    })
                    
                    print(f"✓ {code} {name}")
                else:
                    # Fallback - use existing data
                    results.append({
                        'id': product['id'],
                        'url': url,
                        'code': product['code'],
                        'name': product['color_name'],
                        'sku': product['sku'],
                        'collection': product['collection'],
                        'collection_slug': product['collection_slug'],
                        'image_url': product['images'][0]['url'],
                        'color_slug': product.get('color_slug', '')
                    })
                    print(f"⚠️  Nema match, koristim postojeće: {product['color_name']}")
                
            except Exception as e:
                print(f"✗ Ne mogu da pročitam h1: {e}")
                # Use existing data
                results.append({
                    'id': product['id'],
                    'url': url,
                    'code': product['code'],
                    'name': product['color_name'],
                    'sku': product['sku'],
                    'collection': product['collection'],
                    'collection_slug': product['collection_slug'],
                    'image_url': product['images'][0]['url'],
                    'color_slug': product.get('color_slug', '')
                })
        
        except Exception as e:
            print(f"✗ Greška: {e}")
        
        # Progress indicator every 50
        if idx % 50 == 0:
            print(f"\n--- Pročitano {idx}/{len(products)} ---\n")

except KeyboardInterrupt:
    print("\n\n⏹️  Prekinuto od korisnika")

finally:
    # Save results
    output_path = "scripts/real_names_from_site.json"
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
