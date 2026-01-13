#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FINALNI SCRAPER - Sa explicit wait za AJAX loading
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
print("FINAL SCRAPER - SA AJAX WAIT")
print("="*80)

# Config
COLLECTIONS = [
    {"name": "Creation 30", "url": "https://www.gerflor-cee.com/products/creation-30-new-collection", "slug": "creation-30"},
]

TEST_MODE = True
TEST_LIMIT = 3

DOWNLOAD_DIR = os.path.abspath("downloads/gerflor_final")
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

print(f"Download: {DOWNLOAD_DIR}")
print(f"Test: {TEST_LIMIT} boja\n")

# Chrome
chrome_options = webdriver.ChromeOptions()
prefs = {"download.default_directory": DOWNLOAD_DIR, "download.prompt_for_download": False}
chrome_options.add_experimental_option("prefs", prefs)
chrome_options.add_argument("--start-maximized")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
wait = WebDriverWait(driver, 30)  # 30 sekundi

results = []

try:
    for coll in COLLECTIONS:
        print(f"\n{'='*80}")
        print(f"{coll['name']}")
        print(f"{'='*80}\n")
        
        print(f"1. Otvaram {coll['url']}", flush=True)
        driver.get(coll['url'])
        time.sleep(5)
        
        # Cookies
        try:
            cookie_btns = driver.find_elements(By.XPATH, "//button[contains(text(), 'Accept')]")
            if cookie_btns:
                driver.execute_script("arguments[0].click();", cookie_btns[0])
                print("   ✓ Cookies\n", flush=True)
                time.sleep(3)
        except:
            pass
        
        # View all - SA SCROLL I WAIT
        print("2. Trazim 'View all'...", flush=True)
        view_all = wait.until(EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'View all')]")))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", view_all)
        time.sleep(2)
        driver.execute_script("arguments[0].click();", view_all)
        print("   ✓ Kliknuo!\n", flush=True)
        
        # WAIT FOR AJAX - Cekaj da se pojave NOVI linkovi
        print("3. Cekam da se ucitaju boje (AJAX)...", flush=True)
        time.sleep(8)  # Eksplicitno čekaj 8 sekundi
        
        # Scroll down da trigger-ujem lazy loading
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(2)
        
        # Sad trazi linkove
        print("4. Skupljam linkove...", flush=True)
        all_links = driver.find_elements(By.XPATH, "//a[contains(@href, '/products/')]")
        
        color_urls = []
        for link in all_links:
            href = link.get_attribute('href')
            if href and coll['slug'] in href and href != coll['url']:
                if len(href.split('/')[-1]) > 30:
                    if href not in color_urls:
                        color_urls.append(href)
        
        print(f"   ✓ Pronadjeno {len(color_urls)} boja\n", flush=True)
        
        if len(color_urls) == 0:
            print("   ✗ GRESKA: 0 boja! AJAX nije ucitao sadrzaj!\n", flush=True)
            continue
        
        if TEST_MODE:
            color_urls = color_urls[:TEST_LIMIT]
            print(f"   TEST: {len(color_urls)} boja\n", flush=True)
        
        # Download colors
        for idx, color_url in enumerate(color_urls, 1):
            print(f"  [{idx}/{len(color_urls)}] {color_url.split('/')[-1][:30]}...", flush=True)
            driver.get(color_url)
            time.sleep(4)
            
            # Try download button
            try:
                download_btns = driver.find_elements(By.XPATH, "//button[contains(@aria-label, 'Download')]")
                if download_btns:
                    driver.execute_script("arguments[0].scrollIntoView();", download_btns[0])
                    driver.execute_script("arguments[0].click();", download_btns[0])
                    print("  ✓ Download button", flush=True)
                    time.sleep(2)
            except:
                pass
            
            # JPG button
            try:
                jpg_btns = driver.find_elements(By.XPATH, "//a[contains(text(), '.JPG') or contains(text(), 'JPG')]")
                
                if jpg_btns:
                    files_before = set(os.listdir(DOWNLOAD_DIR))
                    
                    driver.execute_script("arguments[0].scrollIntoView();", jpg_btns[0])
                    driver.execute_script("arguments[0].click();", jpg_btns[0])
                    print("  ✓ JPG click", flush=True)
                    time.sleep(5)
                    
                    files_after = set(os.listdir(DOWNLOAD_DIR))
                    new_files = files_after - files_before
                    
                    if new_files:
                        print(f"  ✅ Downloaded: {list(new_files)[0]}\n", flush=True)
                        results.append({'collection': coll['name'], 'color_url': color_url, 'file': list(new_files)[0]})
                    else:
                        print("  ✗ No file\n", flush=True)
                else:
                    print("  ✗ No JPG button\n", flush=True)
            except Exception as e:
                print(f"  ✗ Error: {e}\n", flush=True)
    
    print(f"\n{'='*80}")
    print(f"GOTOVO! Downloaded: {len(results)}")
    print(f"{'='*80}\n")
    
    with open("downloads/final_results.json", 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

except Exception as e:
    print(f"\nERROR: {e}", flush=True)
    import traceback
    traceback.print_exc()

finally:
    print("\nZatvaram Chrome...", flush=True)
    driver.quit()
    input("\nPritisni ENTER...")
