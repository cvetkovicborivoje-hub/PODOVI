#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FIKSOVANI SCRAPER - Koristi JavaScript click + scroll
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

sys.stdout.reconfigure(line_buffering=True)

print("="*80)
print("GERFLOR LVT SCRAPER - FIKSOVANA VERZIJA")
print("="*80)

# Config
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

# Chrome
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
wait = WebDriverWait(driver, 20)

results = []
downloaded = 0

def js_click(element):
    """JavaScript click - zaobilazi overlay probleme"""
    driver.execute_script("arguments[0].click();", element)

def scroll_to_element(element):
    """Scroll do elementa da bude vidljiv"""
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
    time.sleep(1)

try:
    for coll in COLLECTIONS:
        print(f"\n{'='*80}")
        print(f"Kolekcija: {coll['name']}")
        print(f"{'='*80}")
        
        print(f"1. Otvaram: {coll['url']}", flush=True)
        driver.get(coll['url'])
        time.sleep(4)
        
        # Accept cookies - FORCEFULLY
        print("2. Zatvaram cookies...", flush=True)
        try:
            # Try multiple cookie button variants
            cookie_btns = driver.find_elements(By.XPATH, "//button[contains(text(), 'Accept') or contains(text(), 'OK') or contains(@class, 'accept') or contains(@class, 'cookie')]")
            for btn in cookie_btns:
                try:
                    js_click(btn)
                    print("   ✓ Cookie button clicked", flush=True)
                    time.sleep(2)
                    break
                except:
                    pass
        except:
            print("   - No cookies", flush=True)
        
        # Find "View all" - WITH SCROLL
        print("3. Tražim 'View all'...", flush=True)
        try:
            view_all = wait.until(EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'View all')]")))
            print(f"   ✓ Našao! href: {view_all.get_attribute('href')}", flush=True)
            
            # SCROLL TO IT
            scroll_to_element(view_all)
            print("   ✓ Scroll-ovao do elementa", flush=True)
            
            # JAVASCRIPT CLICK
            js_click(view_all)
            print("   ✓ Kliknuo (JavaScript)", flush=True)
            time.sleep(4)
        except Exception as e:
            print(f"   ✗ ERROR: {e}", flush=True)
            continue
        
        # Get colors
        print("4. Skupljam boje...", flush=True)
        wait.until(EC.presence_of_all_elements_located((By.XPATH, "//a[contains(@href, '/products/')]")))
        all_links = driver.find_elements(By.XPATH, "//a[contains(@href, '/products/')]")
        
        color_urls = []
        for link in all_links:
            href = link.get_attribute('href')
            if href and coll['slug'] in href and href != coll['url']:
                if len(href.split('/')[-1]) > 30 and href not in color_urls:
                    color_urls.append(href)
        
        print(f"   ✓ Pronađeno {len(color_urls)} boja", flush=True)
        
        if TEST_MODE:
            color_urls = color_urls[:TEST_LIMIT]
            print(f"   TEST: Obradjujem {len(color_urls)} boja", flush=True)
        
        # Process colors
        for idx, color_url in enumerate(color_urls, 1):
            print(f"\n  [{idx}/{len(color_urls)}] {color_url.split('/')[-1][:40]}...", flush=True)
            driver.get(color_url)
            time.sleep(3)
            
            # Try download button
            try:
                download_btns = driver.find_elements(By.XPATH, "//button[contains(@aria-label, 'Download')] | //a[contains(@aria-label, 'Download')]")
                if download_btns:
                    scroll_to_element(download_btns[0])
                    js_click(download_btns[0])
                    print("  ✓ Aktivirao download", flush=True)
                    time.sleep(2)
            except:
                print("  - No download button", flush=True)
            
            # Click .JPG
            try:
                jpg_btns = driver.find_elements(By.XPATH, "//a[contains(text(), '.JPG') or contains(text(), 'JPG')]")
                
                if jpg_btns:
                    print(f"  ✓ Našao {len(jpg_btns)} JPG dugmeta", flush=True)
                    
                    files_before = set(os.listdir(DOWNLOAD_DIR))
                    
                    # Scroll and click
                    scroll_to_element(jpg_btns[0])
                    js_click(jpg_btns[0])
                    print("  ✓ Kliknuo .JPG", flush=True)
                    time.sleep(4)
                    
                    files_after = set(os.listdir(DOWNLOAD_DIR))
                    new_files = files_after - files_before
                    
                    if new_files:
                        new_file = list(new_files)[0]
                        print(f"  ✅ Downloaded: {new_file}", flush=True)
                        downloaded += 1
                        results.append({
                            'collection': coll['name'],
                            'color_url': color_url,
                            'file': new_file
                        })
                    else:
                        print("  ✗ Download failed", flush=True)
                else:
                    print("  ✗ JPG dugme nije pronađeno", flush=True)
            except Exception as e:
                print(f"  ✗ Error: {e}", flush=True)
            
            time.sleep(1)
    
    print(f"\n{'='*80}")
    print("GOTOVO!")
    print(f"{'='*80}")
    print(f"Ukupno downloaded: {downloaded} boja")
    
    # Save results
    json_file = os.path.join("downloads", "results_fixed.json")
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
