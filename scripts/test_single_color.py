#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TEST SCRIPT - Download samo JEDNE boje da vidim gde pada
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

print("="*80)
print("TEST: Download JEDNE boje")
print("="*80)

DOWNLOAD_DIR = os.path.abspath("downloads/test_single")
os.makedirs(DOWNLOAD_DIR, exist_ok=True)
print(f"Download folder: {DOWNLOAD_DIR}\n")

# Chrome setup
chrome_options = webdriver.ChromeOptions()
prefs = {
    "download.default_directory": DOWNLOAD_DIR,
    "download.prompt_for_download": False,
}
chrome_options.add_experimental_option("prefs", prefs)
chrome_options.add_argument("--start-maximized")

print("Pokrecem Chrome...")
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=chrome_options
)
wait = WebDriverWait(driver, 20)

try:
    # Go to collection page
    url = "https://www.gerflor-cee.com/products/creation-30-new-collection"
    print(f"\n1. Otvaram: {url}")
    driver.get(url)
    time.sleep(3)
    
    # Accept cookies
    try:
        cookie_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Accept')]")))
        cookie_btn.click()
        print("   ✓ Cookies accepted")
        time.sleep(2)
    except:
        print("   - No cookies")
    
    # Click "View all"
    print("\n2. Tražim 'View all' dugme...")
    try:
        view_all = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'View all')]")))
        print(f"   ✓ Našao! href: {view_all.get_attribute('href')}")
        view_all.click()
        time.sleep(3)
        print("   ✓ Kliknuo 'View all'")
    except Exception as e:
        print(f"   ✗ ERROR: {e}")
        raise
    
    # Get first color link
    print("\n3. Tražim prvu boju...")
    wait.until(EC.presence_of_all_elements_located((By.XPATH, "//a[contains(@href, '/products/')]")))
    all_links = driver.find_elements(By.XPATH, "//a[contains(@href, '/products/')]")
    
    color_links = []
    for link in all_links:
        href = link.get_attribute('href')
        if href and 'creation-30' in href and href != url:
            if len(href.split('/')[-1]) > 30:
                color_links.append(href)
                if len(color_links) >= 1:  # Samo prva boja
                    break
    
    if not color_links:
        print("   ✗ ERROR: Nisam našao nijednu boju!")
        raise Exception("No colors found")
    
    color_url = color_links[0]
    print(f"   ✓ Našao boju: {color_url}")
    
    # Go to color page
    print(f"\n4. Otvaram stranicu boje...")
    driver.get(color_url)
    time.sleep(3)
    print("   ✓ Stranica otvorena")
    
    # Try to find and click download button (if exists)
    print("\n5. Tražim DOWNLOAD dugme...")
    try:
        download_btn = driver.find_element(By.XPATH, "//button[contains(@aria-label, 'Download')] | //a[contains(@aria-label, 'Download')]")
        print(f"   ✓ Našao! Text: {download_btn.text}")
        download_btn.click()
        print("   ✓ Kliknuo DOWNLOAD dugme")
        time.sleep(2)
    except Exception as e:
        print(f"   - Nije pronađeno (možda nije potrebno): {e}")
    
    # Try to find .JPG button
    print("\n6. Tražim .JPG dugme...")
    try:
        # Try multiple XPath variants
        jpg_buttons = driver.find_elements(By.XPATH, "//a[contains(text(), '.JPG') or contains(text(), 'JPG') or contains(., '.jpg') or contains(@class, 'jpg')]")
        
        if jpg_buttons:
            print(f"   ✓ Našao {len(jpg_buttons)} JPG dugmeta!")
            for idx, btn in enumerate(jpg_buttons, 1):
                print(f"     {idx}. Text: '{btn.text}', href: '{btn.get_attribute('href')}'")
            
            # Click first one
            print("\n7. Klikćem PRVO JPG dugme...")
            files_before = set(os.listdir(DOWNLOAD_DIR))
            
            jpg_buttons[0].click()
            print("   ✓ Kliknuo!")
            time.sleep(5)
            
            files_after = set(os.listdir(DOWNLOAD_DIR))
            new_files = files_after - files_before
            
            if new_files:
                print(f"\n✅ USPEH! Downloaded: {list(new_files)[0]}")
            else:
                print("\n✗ Download nije uspeo - nema novog fajla")
        else:
            print("   ✗ Nisam našao nijedano JPG dugme!")
            
            # Let's see ALL links on the page
            print("\n   DEBUG: Sve linkove sa 'download' ili 'jpg':")
            all_links_on_page = driver.find_elements(By.XPATH, "//a")
            for link in all_links_on_page[:20]:  # First 20
                text = link.text.strip()
                href = link.get_attribute('href')
                if text and ('download' in text.lower() or 'jpg' in text.lower() or 'image' in text.lower()):
                    print(f"     - Text: '{text}', href: '{href}'")
    
    except Exception as e:
        print(f"   ✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "="*80)
    print("TEST ZAVRŠEN - Čekam 10 sekundi pre zatvaranja...")
    print("Možeš gledati Chrome dok još radi!")
    print("="*80)
    time.sleep(10)

except Exception as e:
    print(f"\nCRITICAL ERROR: {e}")
    import traceback
    traceback.print_exc()

finally:
    print("\nZatvaram Chrome...")
    driver.quit()
    print("DONE!")
    input("\nPritisni ENTER za zatvaranje...")
