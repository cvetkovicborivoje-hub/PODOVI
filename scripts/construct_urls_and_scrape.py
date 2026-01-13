#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Konstruiše URL-ove iz extracted_colors.json i scrape-uje imena
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
print("KONSTRUISANJE URL-OVA I SCRAPING IMENA")
print("="*80)
print()

# Load extracted colors
with open("downloads/gerflor_dialog/extracted_colors.json", 'r', encoding='utf-8') as f:
    data = json.load(f)

colors = data['colors']
print(f"Ukupno boja: {len(colors)}\n")

# Load existing URLs for pattern matching
with open("downloads/gerflor_dialog/download_results.json", 'r', encoding='utf-8') as f:
    download_data = json.load(f)

# Extract URL pattern
# Example: https://www.gerflor-cee.com/products/creation-40-new-collection-0347-ballerina-41840347

existing_urls = []
for collection in download_data['collections']:
    for color in collection['colors']:
        if 'url' in color:
            existing_urls.append(color['url'])

print(f"Postojeći URL-ovi: {len(existing_urls)}\n")

# Construct URLs for ALL colors
def construct_url(color):
    """Konstruiše URL baziran na color_slug i collection"""
    collection = color['collection']
    color_slug = color['color_slug']
    
    # Extract code (last 4 digits)
    match = re.search(r'(\d{4})$', color_slug)
    if not match:
        return None
    
    code = match.group(1)
    
    # Extract name part (everything before the last number sequence)
    name_part = re.sub(r'-\d+$', '', color_slug)
    
    # Build URL
    # Format: /products/{collection}-new-collection-{code}-{name}-{full_slug}
    url = f"https://www.gerflor-cee.com/products/{collection}-new-collection-{code}-{color_slug}"
    
    return url

# Test with first few
print("Testiram URL konstrukciju sa prvih 3 boje:\n")
for i in range(3):
    color = colors[i]
    url = construct_url(color)
    print(f"  {color['color_slug']} -> {url}")

print("\n" + "="*80)
print("POKRE��EM SELENIUM...")
print("="*80 + "\n")

# Chrome setup
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=chrome_options
)
wait = WebDriverWait(driver, 10)

# Accept cookies
try:
    first_url = construct_url(colors[0])
    driver.get(first_url)
    time.sleep(2)
    accept_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Accept')]")
    driver.execute_script("arguments[0].click();", accept_btn)
    print("✓ Cookies accepted\n")
    time.sleep(1)
except:
    print("- No cookies\n")

results = []

# Limit for testing
TEST_LIMIT = 100  # Process first 100 for speed
colors_to_process = colors[:TEST_LIMIT]

print(f"Obrađujem prvih {TEST_LIMIT} boja...\n")

try:
    for idx, color in enumerate(colors_to_process, 1):
        url = construct_url(color)
        
        if not url:
            print(f"[{idx}/{len(colors_to_process)}] ✗ Ne mogu da konstruišem URL za {color['color_slug']}")
            continue
        
        print(f"[{idx}/{len(colors_to_process)}] {color['color_slug']}... ", end='', flush=True)
        
        try:
            driver.get(url)
            time.sleep(0.5)
            
            # Read H1
            try:
                heading = wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1")))
                full_text = heading.text.strip()
                
                # Clean up
                text = re.sub(r'^CREATION\s+\d+\s+-\s+NEW\s+COLLECTION\s+', '', full_text, flags=re.IGNORECASE)
                
                # Extract code + name
                match = re.search(r'(\d{4})\s+(.+)', text)
                if match:
                    code = match.group(1)
                    name = match.group(2).strip()
                else:
                    code = "Unknown"
                    name = text
                
                results.append({
                    **color,
                    'code': code,
                    'real_name': name.upper(),
                    'url': url
                })
                
                print(f"✓ {code} {name}")
                
            except Exception as e:
                print(f"✗ {e}")
                results.append({
                    **color,
                    'code': "Unknown",
                    'real_name': "Unknown",
                    'url': url
                })
        
        except Exception as e:
            print(f"✗ {e}")
        
        if idx % 50 == 0:
            print(f"\n--- {idx}/{len(colors_to_process)} ---\n")

except KeyboardInterrupt:
    print("\n\n⏹️  Prekinuto")

finally:
    output_path = "scripts/scraped_names_batch1.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump({
            "total": len(results),
            "products": results
        }, f, indent=2, ensure_ascii=False)
    
    print("\n" + "="*80)
    print("GOTOVO!")
    print("="*80)
    print(f"Pročitano: {len(results)}/{len(colors_to_process)}")
    print(f"Sačuvano u: {output_path}")
    
    driver.quit()
    print("✓ Završeno!")
