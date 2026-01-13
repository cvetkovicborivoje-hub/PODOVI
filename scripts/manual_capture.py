#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MANUAL CAPTURE - Ti klicas, ja snimam screenshot-ove
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

print("="*80)
print("MANUAL CAPTURE - Ja snimam tvoje akcije!")
print("="*80)
print()
print("UPUTSTVO:")
print("1. Chrome ce se otvoriti")
print("2. TI RUCNO klikes kroz sajt kako bi normalno download-ovao sliku")
print("3. Posle SVAKE akcije (klik, scroll) - pritisni ENTER ovde")
print("4. Ja cu snimiti screenshot")
print("5. Na kraju cu pokazati sta si radio korak po korak")
print()
print("="*80)

SCREENSHOT_DIR = os.path.abspath("downloads/manual_screenshots")
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--start-maximized")

print("\nPokrecem Chrome...")
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=chrome_options
)

print("Chrome otvoren!")
print()
print("="*80)
print("POCNI!")
print("="*80)

screenshots = []
step = 0

try:
    # Initial page
    url = input("\nUnesi URL Creation 30 kolekcije (ili Enter za default): ").strip()
    if not url:
        url = "https://www.gerflor-cee.com/products/creation-30-new-collection"
    
    driver.get(url)
    step += 1
    filename = f"{step:02d}_start.png"
    driver.save_screenshot(f"{SCREENSHOT_DIR}/{filename}")
    screenshots.append(f"{step}. START - {url}")
    print(f"   Screenshot: {filename}")
    
    # Manual steps
    while True:
        action = input(f"\nKorak {step+1} - Sto si uradio? (ili 'done' za kraj): ").strip()
        
        if action.lower() == 'done':
            break
        
        if not action:
            action = "akcija"
        
        step += 1
        filename = f"{step:02d}_{action.replace(' ', '_')[:30]}.png"
        driver.save_screenshot(f"{SCREENSHOT_DIR}/{filename}")
        
        # Save HTML too
        with open(f"{SCREENSHOT_DIR}/{step:02d}_page.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        
        screenshots.append(f"{step}. {action}")
        print(f"   Screenshot: {filename}")
        print(f"   HTML: {step:02d}_page.html")
        print(f"   Current URL: {driver.current_url}")
    
    print("\n" + "="*80)
    print("GOTOVO!")
    print("="*80)
    print("\nTvoji koraci:")
    for s in screenshots:
        print(f"  {s}")
    
    print(f"\nScreenshot-ovi: {SCREENSHOT_DIR}")
    
except Exception as e:
    print(f"\nERROR: {e}")
    import traceback
    traceback.print_exc()

finally:
    print("\nOstaviću Chrome otvoren jos 10 sekundi...")
    time.sleep(10)
    print("Zatvaram Chrome...")
    driver.quit()
    print("DONE!")
