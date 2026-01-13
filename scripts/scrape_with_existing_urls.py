#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Koristi POSTOJEĆE URL-ove iz download_results.json
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
print("ČITANJE PRAVIH IMENA SA POSTOJEĆIH URL-OVA")
print("="*80)
print()

# Load existing URLs
with open("downloads/gerflor_dialog/download_results.json", 'r', encoding='utf-8') as f:
    download_data = json.load(f)

# Extract all URLs
all_urls = []
for collection in download_data['collections']:
    for color in collection['colors']:
        if 'url' in color:
            all_urls.append({
                'url': color['url'],
                'collection': collection['name'],
                'collection_slug': collection['slug'],
                'color_name': color['name'],
            })

print(f"Ukupno URL-ova: {len(all_urls)}\n")

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
    driver.get(all_urls[0]['url'])
    time.sleep(2)
    accept_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Accept')]")
    driver.execute_script("arguments[0].click();", accept_btn)
    print("✓ Cookies accepted\n")
    time.sleep(1)
except:
    print("- No cookies\n")

results = []

try:
    for idx, url_data in enumerate(all_urls, 1):
        url = url_data['url']
        
        print(f"[{idx}/{len(all_urls)}] {url_data['color_name']}... ", end='', flush=True)
        
        try:
            driver.get(url)
            time.sleep(1)
            
            # Find H1 heading (this contains the code + name)
            try:
                heading = wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1")))
                full_text = heading.text.strip()
                
                # Extract code + name
                # Format: usually just "0347 BALLERINA" or similar
                # Remove any "CREATION XX - NEW COLLECTION" prefix if present
                text = re.sub(r'^CREATION\s+\d+\s+-\s+NEW\s+COLLECTION\s+', '', full_text, flags=re.IGNORECASE)
                
                # Split by first 4-digit code
                match = re.search(r'(\d{4})\s+(.+)', text)
                if match:
                    code = match.group(1)
                    name = match.group(2).strip()
                else:
                    code = "Unknown"
                    name = text
                
                results.append({
                    **url_data,
                    'code': code,
                    'real_name': name.upper(),
                })
                
                print(f"✓ {code} {name}")
                
            except Exception as e:
                print(f"✗ {e}")
                results.append({
                    **url_data,
                    'code': "Unknown",
                    'real_name': url_data['color_name'].upper(),
                })
        
        except Exception as e:
            print(f"✗ Greška: {e}")
        
        if idx % 50 == 0:
            print(f"\n--- {idx}/{len(all_urls)} ---\n")

except KeyboardInterrupt:
    print("\n\n⏹️  Prekinuto")

finally:
    output_path = "scripts/products_real_scraped_final.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump({
            "total": len(results),
            "products": results
        }, f, indent=2, ensure_ascii=False)
    
    print("\n" + "="*80)
    print("GOTOVO!")
    print("="*80)
    print(f"Pročitano: {len(results)}/{len(all_urls)}")
    print(f"Sačuvano u: {output_path}")
    
    driver.quit()
    print("✓ Završeno!")
