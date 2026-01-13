#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Check progress - koliko je download-ovano"""

import os
import json
import sys

# Fix encoding for Windows
sys.stdout.reconfigure(encoding='utf-8')

DOWNLOAD_DIR = r"D:\PODOVI\SAJT\downloads\gerflor_dialog"

# Expected counts per collection
EXPECTED = {
    "creation-30": 43,
    "creation-40": 53,
    "creation-40-clic": 53,
    "creation-40-clic-acoustic": 53,
    "creation-40-zen": 18,
    "creation-55": 80,
    "creation-55-clic": 80,
    "creation-55-clic-acoustic": 80,
    "creation-55-looselay": 26,
    "creation-55-looselay-acoustic": 26,
    "creation-55-zen": 18,
    "creation-70": 56,
    "creation-70-clic": 56,
    "creation-70-connect": 17,
    "creation-70-megaclic": 17,
    "creation-70-zen": 18,
    "creation-saga2": 18,
    "creation-70-looselay": 26
}

print("="*80)
print("PROGRESS CHECK")
print("="*80)
print()

total_expected = sum(EXPECTED.values())
total_downloaded = 0

for collection_slug, expected_count in EXPECTED.items():
    collection_dir = os.path.join(DOWNLOAD_DIR, collection_slug)
    
    if os.path.exists(collection_dir):
        zips = [f for f in os.listdir(collection_dir) if f.endswith('.zip')]
        count = len(zips)
        total_downloaded += count
        
        status = "✅" if count == expected_count else f"⏳ ({count}/{expected_count})"
        print(f"{status} {collection_slug}: {count}/{expected_count}")
    else:
        print(f"❌ {collection_slug}: 0/{expected_count} (folder ne postoji)")

print()
print("="*80)
print(f"UKUPNO: {total_downloaded}/{total_expected} ({100*total_downloaded//total_expected}%)")
print("="*80)

# Check results.json
results_path = os.path.join(DOWNLOAD_DIR, "download_results.json")
if os.path.exists(results_path):
    print()
    print("Results JSON postoji!")
    with open(results_path, 'r', encoding='utf-8') as f:
        results = json.load(f)
    print(f"Total downloads (from JSON): {results.get('total_downloads', 0)}")
    print(f"Errors: {len(results.get('errors', []))}")
