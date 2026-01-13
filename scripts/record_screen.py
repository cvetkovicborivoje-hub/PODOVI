#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Snima ekran 10 puta u sekundi
"""

import time
from datetime import datetime
from pathlib import Path
from PIL import ImageGrab
import sys

sys.stdout.reconfigure(encoding='utf-8')

print("="*80)
print("SNIMANJE EKRANA - 10 FPS")
print("="*80)
print()

# Create screenshots directory
screenshots_dir = Path("screenshots_tutorial")
screenshots_dir.mkdir(exist_ok=True)

print(f"Snimanje će biti sačuvano u: {screenshots_dir.absolute()}")
print()
print("Počinjem snimanje za 3 sekunde...")
print("Pritisni Ctrl+C da zaustaviš\n")

time.sleep(3)

frame_count = 0
start_time = time.time()

try:
    while True:
        # Take screenshot
        screenshot = ImageGrab.grab()
        
        # Save with timestamp
        timestamp = datetime.now().strftime("%H-%M-%S-%f")[:-3]  # milliseconds
        filename = f"frame_{frame_count:05d}_{timestamp}.png"
        filepath = screenshots_dir / filename
        
        screenshot.save(filepath)
        
        frame_count += 1
        
        if frame_count % 10 == 0:
            elapsed = time.time() - start_time
            fps = frame_count / elapsed
            print(f"Snimljeno: {frame_count} frame-ova ({fps:.1f} FPS)")
        
        # Wait to achieve ~10 FPS
        time.sleep(0.1)

except KeyboardInterrupt:
    print("\n\n" + "="*80)
    print("SNIMANJE ZAUSTAVLJENO!")
    print("="*80)
    elapsed = time.time() - start_time
    print(f"Ukupno frame-ova: {frame_count}")
    print(f"Vreme: {elapsed:.1f} sekundi")
    print(f"Prosečan FPS: {frame_count/elapsed:.1f}")
    print(f"Lokacija: {screenshots_dir.absolute()}")
    print()
