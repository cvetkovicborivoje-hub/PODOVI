#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DEBUG - Screenshot svake faze da vidimo sta se desava
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
print("DEBUG: Screenshot svake faze")
print("="*80)

DOWNLOAD_DIR = os.path.abspath("downloads/debug_screenshots")
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--start-maximized")

print("Pokrecem Chrome...")
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=chrome_options
)
wait = WebDriverWait(driver, 20)

def save_screenshot(name):
    """Snima screenshot i HTML"""
    driver.save_screenshot(f"{DOWNLOAD_DIR}/{name}.png")
    with open(f"{DOWNLOAD_DIR}/{name}.html", "w", encoding="utf-8") as f:
        f.write(driver.page_source)
    print(f"   📸 Screenshot: {name}.png")

try:
    # Step 1: Go to collection
    print("\n1. Otvaram kolekciju...")
    driver.get("https://www.gerflor-cee.com/products/creation-30-new-collection")
    time.sleep(3)
    save_screenshot("01_collection_page")
    
    # Step 2: Accept cookies
    print("\n2. Zatvaram cookies...")
    try:
        cookie_btns = driver.find_elements(By.XPATH, "//button[contains(text(), 'Accept') or contains(text(), 'OK')]")
        if cookie_btns:
            cookie_btns[0].click()
            print("   ✓ Cookies zatvoreni")
            time.sleep(2)
            save_screenshot("02_after_cookies")
    except:
        print("   - No cookies")
    
    # Step 3: Find View all
    print("\n3. Tražim 'View all'...")
    view_all_elements = driver.find_elements(By.XPATH, "//a[contains(text(), 'View all')]")
    print(f"   Pronađeno {len(view_all_elements)} 'View all' linkova")
    
    for idx, elem in enumerate(view_all_elements, 1):
        print(f"     {idx}. Text: '{elem.text}', href: '{elem.get_attribute('href')}'")
    
    if view_all_elements:
        # Scroll to it
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", view_all_elements[0])
        time.sleep(1)
        save_screenshot("03_before_view_all_click")
        
        # Click it
        driver.execute_script("arguments[0].click();", view_all_elements[0])
        print("   ✓ Kliknuo 'View all'")
        time.sleep(4)
        save_screenshot("04_after_view_all_click")
    
    # Step 4: Find colors
    print("\n4. Tražim boje...")
    all_links = driver.find_elements(By.XPATH, "//a[contains(@href, '/products/')]")
    
    color_links = []
    for link in all_links[:20]:  # First 20
        href = link.get_attribute('href')
        if href and 'creation-30' in href:
            text = link.text.strip()
            if len(href.split('/')[-1]) > 30:
                color_links.append({'href': href, 'text': text})
    
    print(f"   Pronađeno {len(color_links)} boja")
    for idx, color in enumerate(color_links[:5], 1):
        print(f"     {idx}. {color['text'][:40]}... -> {color['href'][:60]}...")
    
    if color_links:
        # Step 5: Go to first color
        print(f"\n5. Otvaram prvu boju: {color_links[0]['href']}")
        driver.get(color_links[0]['href'])
        time.sleep(3)
        save_screenshot("05_color_page")
        
        # Step 6: Find JPG buttons
        print("\n6. Tražim JPG dugmad...")
        jpg_elements = driver.find_elements(By.XPATH, "//a[contains(text(), 'JPG') or contains(text(), '.jpg') or contains(@href, '.jpg')]")
        print(f"   Pronađeno {len(jpg_elements)} JPG elemenata")
        
        for idx, elem in enumerate(jpg_elements, 1):
            print(f"     {idx}. Text: '{elem.text}', href: '{elem.get_attribute('href')}'")
        
        # Step 7: Find download buttons
        print("\n7. Tražim download dugmad...")
        download_elements = driver.find_elements(By.XPATH, "//button[contains(@aria-label, 'Download')] | //a[contains(@aria-label, 'Download')] | //*[contains(text(), 'Download')]")
        print(f"   Pronađeno {len(download_elements)} download elemenata")
        
        for idx, elem in enumerate(download_elements[:10], 1):
            try:
                print(f"     {idx}. Tag: {elem.tag_name}, Text: '{elem.text}', aria-label: '{elem.get_attribute('aria-label')}'")
            except:
                pass
    
    print(f"\n{'='*80}")
    print("DEBUG ZAVRŠEN!")
    print(f"{'='*80}")
    print(f"\nProveri screenshot-ove u: {DOWNLOAD_DIR}")
    print("\nČekam 10 sekundi da pogledaš Chrome...")
    time.sleep(10)

except Exception as e:
    print(f"\nERROR: {e}")
    import traceback
    traceback.print_exc()
    save_screenshot("99_error")

finally:
    print("\nZatvaram Chrome...")
    driver.quit()
    print("DONE!")
    input("\nPritisni ENTER...")
