#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FINALNI SCRAPER - Download svih Gerflor LVT boja
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

# Force unbuffered output
sys.stdout.reconfigure(line_buffering=True)

print("="*80)
print("GERFLOR LVT SCRAPER - FINALNA VERZIJA")
print("="*80)
print(f"Trenutni folder: {os.getcwd()}")
print("")

# Konfiguracija
COLLECTIONS = [
    {"name": "Creation 30", "url": "https://www.gerflor-cee.com/products/creation-30-new-collection", "slug": "creation-30"},
]

TEST_MODE = True
TEST_LIMIT = 5

DOWNLOAD_DIR = os.path.abspath("downloads/gerflor_images")
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

print(f"Download folder: {DOWNLOAD_DIR}")
print(f"Test mode: {TEST_MODE} (prvih {TEST_LIMIT} boja)")
print("")

# Chrome setup
chrome_options = webdriver.ChromeOptions()
prefs = {
    "download.default_directory": DOWNLOAD_DIR,
    "download.prompt_for_download": False,
}
chrome_options.add_experimental_option("prefs", prefs)
chrome_options.add_argument("--start-maximized")

print("Pokrecem Chrome...", flush=True)
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=chrome_options
)
wait = WebDriverWait(driver, 15)

results = []
downloaded = 0

try:
    for coll in COLLECTIONS:
        print(f"\n{'='*80}")
        print(f"Kolekcija: {coll['name']}")
        print(f"{'='*80}")
        
        print(f"Otvaram: {coll['url']}", flush=True)
        driver.get(coll['url'])
        time.sleep(3)
        
        # Accept cookies
        try:
            cookie_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Accept')]")))
            cookie_btn.click()
            print("✓ Cookies accepted", flush=True)
            time.sleep(1)
        except:
            print("- No cookies", flush=True)
        
        # Find colors count
        try:
            colors_text = driver.find_element(By.XPATH, "//h2[contains(text(), 'color')]").text
            print(f"✓ {colors_text}", flush=True)
        except:
            pass
        
        # Click "View all"
        try:
            view_all = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'View all')]")))
            view_all.click()
            print("✓ Kliknuo 'View all'", flush=True)
            time.sleep(3)
        except Exception as e:
            print(f"✗ ERROR: Nisam mogao kliknuti 'View all': {e}", flush=True)
            continue
        
        # Get all color URLs
        wait.until(EC.presence_of_all_elements_located((By.XPATH, "//a[contains(@href, '/products/')]")))
        all_links = driver.find_elements(By.XPATH, "//a[contains(@href, '/products/')]")
        
        color_urls = []
        for link in all_links:
            href = link.get_attribute('href')
            if href and coll['slug'] in href and href != coll['url']:
                if len(href.split('/')[-1]) > 30 and href not in color_urls:
                    color_urls.append(href)
        
        print(f"✓ Pronađeno {len(color_urls)} boja", flush=True)
        
        if TEST_MODE:
            color_urls = color_urls[:TEST_LIMIT]
            print(f"TEST: Obradjujem samo {len(color_urls)} boja", flush=True)
        
        # Process each color
        for idx, color_url in enumerate(color_urls, 1):
            print(f"\n  [{idx}/{len(color_urls)}] {color_url.split('/')[-1][:40]}...", flush=True)
            driver.get(color_url)
            time.sleep(2)
            
            # Try to click download button (if exists)
            try:
                download_btn = driver.find_element(By.XPATH, "//button[contains(@aria-label, 'Download')]")
                download_btn.click()
                print("  ✓ Aktivirao download", flush=True)
                time.sleep(1)
            except:
                print("  - No download button", flush=True)
            
            # Click .JPG button
            try:
                jpg_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), '.JPG')]")))
                files_before = set(os.listdir(DOWNLOAD_DIR))
                
                jpg_btn.click()
                print("  ✓ Kliknuo .JPG", flush=True)
                time.sleep(3)
                
                files_after = set(os.listdir(DOWNLOAD_DIR))
                new_files = files_after - files_before
                
                if new_files:
                    new_file = list(new_files)[0]
                    print(f"  ✓ Downloaded: {new_file}", flush=True)
                    downloaded += 1
                    results.append({
                        'collection': coll['name'],
                        'color_url': color_url,
                        'file': new_file
                    })
                else:
                    print("  ✗ Download failed", flush=True)
            except Exception as e:
                print(f"  ✗ Error: {e}", flush=True)
            
            time.sleep(1)
    
    print(f"\n{'='*80}")
    print("GOTOVO!")
    print(f"{'='*80}")
    print(f"Ukupno downloaded: {downloaded} boja")
    
    # Save JSON
    json_file = os.path.join("downloads", "results.json")
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"Metadata: {json_file}")
    
except Exception as e:
    print(f"\nCRITICAL ERROR: {e}", flush=True)
    import traceback
    traceback.print_exc()

finally:
    print("\nZatvaram Chrome...", flush=True)
    driver.quit()
    print("DONE!", flush=True)
    input("\nPritisni ENTER za zatvaranje...")
