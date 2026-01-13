#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Čita imena i šifre direktno sa URL-ova koje već imamo
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
import os

sys.stdout.reconfigure(encoding='utf-8')

print("="*80)
print("GERFLOR - ČITANJE IMENA SA POSTOJEĆIH URL-OVA")
print("="*80)
print()

# Load existing URL data
download_results_path = "downloads/gerflor_dialog/download_results.json"
with open(download_results_path, 'r', encoding='utf-8') as f:
    download_data = json.load(f)

# Extract all color URLs
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

print(f"Pronađeno {len(all_urls)} URL-ova\n")

# Chrome setup
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")  # Run without GUI for speed
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("--start-maximized")

print("Pokrećem Chrome...")
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=chrome_options
)
wait = WebDriverWait(driver, 10)

all_colors = []
errors = []

try:
    # Accept cookies once
    driver.get(all_urls[0]['url'])
    time.sleep(2)
    try:
        accept_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Accept All')]")
        driver.execute_script("arguments[0].click();", accept_btn)
        print("✓ Cookies accepted\n")
        time.sleep(1)
    except:
        print("- No cookies popup\n")
    
    for idx, url_data in enumerate(all_urls, 1):
        url = url_data['url']
        
        print(f"[{idx}/{len(all_urls)}] {url_data['color_name']}... ", end='', flush=True)
        
        try:
            driver.get(url)
            time.sleep(1.5)
            
            # Try to find product title (e.g., "CREATION 30 - NEW COLLECTION 0347 BALLERINA")
            try:
                # Try h1 first
                title_elem = driver.find_element(By.TAG_NAME, "h1")
                full_title = title_elem.text.strip()
                
                # Extract code and name from title
                # Example: "CREATION 30 - NEW COLLECTION 0347 BALLERINA"
                parts = full_title.split()
                
                # Find 4-digit code
                code = None
                name_parts = []
                found_code = False
                
                for part in parts:
                    if part.isdigit() and len(part) == 4:
                        code = part
                        found_code = True
                    elif found_code:
                        # Everything after code is the name
                        name_parts.append(part)
                
                name = ' '.join(name_parts) if name_parts else None
                
                # Try to find SKU (usually in spec table or data attributes)
                sku = None
                try:
                    # Look for SKU in page
                    sku_candidates = driver.find_elements(By.XPATH, "//*[contains(text(), 'SKU') or contains(text(), 'Reference')]")
                    for candidate in sku_candidates:
                        parent = candidate.find_element(By.XPATH, "..")
                        text = parent.text
                        # Extract 8-digit number
                        import re
                        match = re.search(r'\b\d{8}\b', text)
                        if match:
                            sku = match.group()
                            break
                except:
                    pass
                
                # If SKU not found, try to extract from URL
                if not sku:
                    url_parts = url.split('/')[-1].split('-')
                    for part in url_parts:
                        if part.isdigit() and len(part) >= 8:
                            sku = part
                            break
                
                color_data = {
                    "collection": url_data['collection'],
                    "collection_slug": url_data['collection_slug'],
                    "code": code or "Unknown",
                    "name": name or url_data['color_name'],
                    "sku": sku,
                    "url": url,
                    "url_slug": url_data['color_name'],
                }
                
                all_colors.append(color_data)
                print(f"✓ {code} {name}")
                
            except Exception as e:
                print(f"✗ Ne mogu da pročitam naslov: {e}")
                errors.append({'url': url, 'error': str(e)})
        
        except Exception as e:
            print(f"✗ Greška: {e}")
            errors.append({'url': url, 'error': str(e)})
        
        # Progress update every 50 items
        if idx % 50 == 0:
            print(f"\n--- Pročitano {idx}/{len(all_urls)} ---\n")

except Exception as e:
    print(f"\n✗ KRITIČNA GREŠKA: {e}")
    import traceback
    traceback.print_exc()

finally:
    # Save results
    output_path = "scripts/all_colors_scraped.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump({
            "total": len(all_colors),
            "errors": len(errors),
            "colors": all_colors,
            "error_list": errors
        }, f, indent=2, ensure_ascii=False)
    
    print("\n" + "="*80)
    print("GOTOVO!")
    print("="*80)
    print(f"Uspešno pročitano: {len(all_colors)}")
    print(f"Greške: {len(errors)}")
    print(f"Sačuvano u: {output_path}")
    print()
    
    driver.quit()
    print("✓ Završeno!")
