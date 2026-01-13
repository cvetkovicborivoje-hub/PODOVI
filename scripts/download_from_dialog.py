#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DOWNLOAD FROM DIALOG - Koristi dialog sa svim bojama!
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
import glob
import shutil
from pathlib import Path

print("="*80)
print("GERFLOR SCRAPER - DIALOG VERSION")
print("="*80)

def wait_for_new_zip(download_dir, timeout=30):
    """Ceka da se pojavi novi ZIP fajl u download folderu"""
    print(f"         Cekam ZIP... ", end='', flush=True)
    
    start_time = time.time()
    initial_zips = set(glob.glob(os.path.join(download_dir, "*.zip")))
    
    while time.time() - start_time < timeout:
        current_zips = set(glob.glob(os.path.join(download_dir, "*.zip")))
        new_zips = current_zips - initial_zips
        
        if new_zips:
            # Check if download is complete (file size not changing)
            zip_file = list(new_zips)[0]
            size1 = os.path.getsize(zip_file)
            time.sleep(1)
            size2 = os.path.getsize(zip_file)
            
            if size1 == size2:
                print(f"GOTOV!")
                return zip_file
        
        time.sleep(0.5)
    
    print(f"TIMEOUT!")
    return None

def organize_zip(zip_path, collection_slug, color_name, organized_dir):
    """Premesta i preimenuje ZIP u odgovarajuci folder"""
    if not zip_path or not os.path.exists(zip_path):
        return None
    
    # Kreiraj folder za kolekciju
    collection_dir = os.path.join(organized_dir, collection_slug)
    os.makedirs(collection_dir, exist_ok=True)
    
    # Novo ime: {color_name}.zip
    new_name = f"{color_name}.zip"
    new_path = os.path.join(collection_dir, new_name)
    
    # Premesti
    shutil.move(zip_path, new_path)
    print(f"         Organizovano: {collection_slug}/{new_name}")
    
    return new_path

# Config
TEST_MODE = False  # False = SVE boje iz svih kolekcija!
DOWNLOAD_DIR = os.path.abspath("downloads/gerflor_dialog")
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

COLLECTIONS = [
    {"name": "Creation 30", "slug": "creation-30", "url": "https://www.gerflor-cee.com/products/creation-30-new-collection"},
    {"name": "Creation 40", "slug": "creation-40", "url": "https://www.gerflor-cee.com/products/creation-40-new-collection"},
    {"name": "Creation 40 Clic", "slug": "creation-40-clic", "url": "https://www.gerflor-cee.com/products/creation-40-clic-new-collection"},
    {"name": "Creation 40 Clic Acoustic", "slug": "creation-40-clic-acoustic", "url": "https://www.gerflor-cee.com/products/creation-40-clic-acoustic-new-collection"},
    {"name": "Creation 40 Zen", "slug": "creation-40-zen", "url": "https://www.gerflor-cee.com/products/creation-40-zen"},
    {"name": "Creation 55", "slug": "creation-55", "url": "https://www.gerflor-cee.com/products/creation-55-new-collection"},
    {"name": "Creation 55 Clic", "slug": "creation-55-clic", "url": "https://www.gerflor-cee.com/products/creation-55-clic-new-collection"},
    {"name": "Creation 55 Clic Acoustic", "slug": "creation-55-clic-acoustic", "url": "https://www.gerflor-cee.com/products/creation-55-clic-acoustic-new-collection"},
    {"name": "Creation 55 Looselay", "slug": "creation-55-looselay", "url": "https://www.gerflor-cee.com/products/creation-55-looselay"},
    {"name": "Creation 55 Looselay Acoustic", "slug": "creation-55-looselay-acoustic", "url": "https://www.gerflor-cee.com/products/creation-55-looselay-acoustic"},
    {"name": "Creation 55 Zen", "slug": "creation-55-zen", "url": "https://www.gerflor-cee.com/products/creation-55-zen"},
    {"name": "Creation 70", "slug": "creation-70", "url": "https://www.gerflor-cee.com/products/creation-70-new-collection"},
    {"name": "Creation 70 Clic", "slug": "creation-70-clic", "url": "https://www.gerflor-cee.com/products/creation-70-clic-5mm-new-collection"},
    {"name": "Creation 70 Connect", "slug": "creation-70-connect", "url": "https://www.gerflor-cee.com/products/creation-70-connect"},
    {"name": "Creation 70 Megaclic", "slug": "creation-70-megaclic", "url": "https://www.gerflor-cee.com/products/creation-70-megaclic"},
    {"name": "Creation 70 Zen", "slug": "creation-70-zen", "url": "https://www.gerflor-cee.com/products/creation-70-zen"},
    {"name": "Creation 70 Saga²", "slug": "creation-saga2", "url": "https://www.gerflor-cee.com/products/creation-saga2"},
    {"name": "Creation 70 Looselay", "slug": "creation-70-looselay", "url": "https://www.gerflor-cee.com/products/new-2025-creation-70-looselay"}
]

# Chrome options
chrome_options = webdriver.ChromeOptions()
prefs = {
    "download.default_directory": DOWNLOAD_DIR,
    "download.prompt_for_download": False,
}
chrome_options.add_experimental_option("prefs", prefs)
chrome_options.add_argument("--start-maximized")

print(f"\nDownload folder: {DOWNLOAD_DIR}")
if TEST_MODE:
    print("TEST MODE: Samo prve 3 boje!")
print()

# Start Chrome
print("Pokrecem Chrome...")
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=chrome_options
)

wait = WebDriverWait(driver, 20)

results = {
    "collections": [],
    "total_downloads": 0,
    "errors": []
}

try:
    for collection in COLLECTIONS:
        # Check if already downloaded (skip only if we have a lot of colors)
        collection_dir = os.path.join(DOWNLOAD_DIR, collection['slug'])
        if os.path.exists(collection_dir):
            existing_zips = [f for f in os.listdir(collection_dir) if f.endswith('.zip')]
            # Skip only if we have 40+ colors (likely complete)
            if len(existing_zips) >= 40:
                print("="*80)
                print(f"⏭️  PRESKACUJEM: {collection['name']} ({len(existing_zips)} vec download-ovano - verovatno kompletno)")
                print("="*80)
                continue
            elif len(existing_zips) > 0:
                print("="*80)
                print(f"📥 NASTAVLJAM: {collection['name']} ({len(existing_zips)} vec ima, download-ujem ostatak)")
                print("="*80)
        
        print("="*80)
        print(f"KOLEKCIJA: {collection['name']}")
        print(f"URL: {collection['url']}")
        print("="*80)
        
        col_result = {
            "name": collection['name'],
            "slug": collection['slug'],
            "colors_downloaded": 0,
            "colors": []
        }
        
        # Step 1: Open collection page
        print("\n1. Otvaram kolekciju...")
        driver.get(collection['url'])
        time.sleep(3)
        
        # Close cookies
        try:
            accept_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Accept All')]")))
            driver.execute_script("arguments[0].click();", accept_btn)
            print("   Cookies zatvoren!")
            time.sleep(1)
        except:
            print("   Nema cookies pop-up")
        
        # Step 2: Click "View all" button
        print("\n2. Klikam 'View all'...")
        try:
            view_all_btn = wait.until(EC.element_to_be_clickable((
                By.CSS_SELECTOR, 
                "button.color-list-dialog-trigger, button[aria-controls='color-list-dialog']"
            )))
            driver.execute_script("arguments[0].click();", view_all_btn)
            print("   Kliknuto!")
            time.sleep(2)
        except Exception as e:
            print(f"   ERROR: Ne mogu da nadjem 'View all'! {e}")
            continue
        
        # Step 3: Wait for dialog to open
        print("\n3. Cekam da se otvori dialog...")
        try:
            dialog = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "dialog#color-list-dialog[open]")))
            print("   Dialog otvoren!")
            time.sleep(2)
        except Exception as e:
            print(f"   ERROR: Dialog se nije otvorio! {e}")
            continue
        
        # Step 4: Get all color links FROM DIALOG
        print("\n4. Skupljam linkove iz dialoga...")
        color_links = driver.find_elements(By.CSS_SELECTOR, "#color-list-dialog a[href*='/products/']")
        print(f"   Pronadjeno {len(color_links)} boja!")
        
        if len(color_links) == 0:
            print("   ERROR: 0 linkova! Nesto nije u redu!")
            continue
        
        # Get hrefs (store them now, before we navigate away)
        # Extract collection identifier from URL (e.g., "creation-30-new-collection")
        collection_identifier = collection['url'].split('/')[-1]  # e.g., "creation-30-new-collection"
        
        color_hrefs = []
        for link in color_links:
            href = link.get_attribute('href')
            # Check if link contains the collection identifier
            if href and collection_identifier in href and href != collection['url']:
                color_hrefs.append(href)
        
        print(f"   Filtrirano: {len(color_hrefs)} color linkova")
        
        if TEST_MODE:
            color_hrefs = color_hrefs[:3]
            print(f"   TEST MODE: Samo {len(color_hrefs)} boje")
        
        # Step 5: Download each color
        print(f"\n5. Download-ujem {len(color_hrefs)} boja...")
        
        for i, color_url in enumerate(color_hrefs):
            print(f"\n   [{i+1}/{len(color_hrefs)}] {color_url}")
            
            # Extract color name FIRST (before navigating)
            url_parts = color_url.split('/')[-1]  # "creation-30-new-collection-0347-ballerina-41870347"
            color_name = '-'.join(url_parts.split('-')[-2:])  # "ballerina-41870347"
            
            # Check if already downloaded
            expected_zip = os.path.join(DOWNLOAD_DIR, collection['slug'], f"{color_name}.zip")
            if os.path.exists(expected_zip):
                print(f"      ⏭️  Vec postoji: {color_name}.zip - PRESKACUJEM")
                col_result['colors'].append({
                    "name": color_name,
                    "url": color_url,
                    "status": "already_exists",
                    "file": expected_zip
                })
                continue
            
            try:
                # Navigate to color page
                driver.get(color_url)
                time.sleep(3)  # "ballerina-41870347"
                
                # Step 1: Click download trigger button (opens options)
                print(f"      Trazim download dugme...")
                try:
                    download_trigger = wait.until(EC.element_to_be_clickable((
                        By.CSS_SELECTOR, 
                        "button.download-button--trigger"
                    )))
                    driver.execute_script("arguments[0].click();", download_trigger)
                    print(f"      Download trigger kliknuto!")
                    time.sleep(1)
                    
                    # Step 2: Wait for options to become visible and click .JPG
                    print(f"      Trazim .JPG dugme...")
                    jpg_btn = wait.until(EC.element_to_be_clickable((
                        By.CSS_SELECTOR, 
                        "button.download-button--images"
                    )))
                    driver.execute_script("arguments[0].click();", jpg_btn)
                    print(f"      .JPG kliknuto!")
                    
                    # Step 3: Wait for ZIP to download
                    zip_path = wait_for_new_zip(DOWNLOAD_DIR, timeout=30)
                    
                    if zip_path:
                        # Step 4: Organize ZIP file
                        organized_path = organize_zip(zip_path, collection['slug'], color_name, DOWNLOAD_DIR)
                        
                        col_result['colors_downloaded'] += 1
                        col_result['colors'].append({
                            "name": color_name,
                            "url": color_url,
                            "status": "success",
                            "file": organized_path
                        })
                    else:
                        print(f"      ERROR: ZIP nije download-ovan!")
                        col_result['colors'].append({
                            "name": color_name,
                            "url": color_url,
                            "status": "error",
                            "error": "ZIP timeout"
                        })
                    
                except Exception as e:
                    print(f"      ERROR: Ne mogu da nadjem .JPG dugme! {e}")
                    col_result['colors'].append({
                        "name": color_name,
                        "url": color_url,
                        "status": "error",
                        "error": str(e)
                    })
            
            except Exception as e:
                print(f"      ERROR: {e}")
                results['errors'].append({
                    "collection": collection['name'],
                    "url": color_url,
                    "error": str(e)
                })
        
        # Close dialog before next collection
        try:
            print("\n6. Zatvaram dialog...")
            close_btn = driver.find_element(By.CSS_SELECTOR, "button.dlg__close, button.color-list-dialog-close")
            driver.execute_script("arguments[0].click();", close_btn)
            print("   Dialog zatvoren!")
            time.sleep(2)
        except:
            print("   Dialog vec zatvoren ili ne postoji")
        
        results['collections'].append(col_result)
        results['total_downloads'] += col_result['colors_downloaded']
        
        print(f"\n{collection['name']}: {col_result['colors_downloaded']} / {len(color_hrefs)} downloaded")
        print(f"Prelazim na sledecu kolekciju...")
        print()

except Exception as e:
    print(f"\nFATAL ERROR: {e}")
    import traceback
    traceback.print_exc()

finally:
    # Save results
    results_path = os.path.join(DOWNLOAD_DIR, "download_results.json")
    with open(results_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print("\n" + "="*80)
    print("GOTOVO!")
    print("="*80)
    print(f"Total downloads: {results['total_downloads']}")
    print(f"Results: {results_path}")
    
    print("\nOstaviću Chrome otvoren jos 5 sekundi...")
    time.sleep(5)
    print("Zatvaram Chrome...")
    driver.quit()
    print("DONE!")
