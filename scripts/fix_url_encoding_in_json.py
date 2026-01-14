# -*- coding: utf-8 -*-
"""
Fix URL encoding issues in JSON
URL-ovi u JSON-u trebaju da budu plain stringovi, ne URL-encoded
Next.js Image komponenta će automatski encodovati URL-ove kada ih koristi
"""
import json
import sys
from pathlib import Path
from urllib.parse import unquote, quote

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

json_path = Path('public/data/lvt_colors_complete.json')
base_images_path = Path('public/images/products/lvt/colors')

# Load JSON
with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Total colors: {len(data['colors'])}\n")

fixed_count = 0
checked_count = 0

for color in data['colors']:
    # Check texture_url/image_url
    texture_url = color.get('texture_url') or color.get('image_url')
    if texture_url:
        checked_count += 1
        # Extract filename from URL
        clean_url = texture_url.split('?')[0]
        
        # Check if URL contains encoded characters
        if '%' in clean_url:
            # Decode the URL
            decoded_url = unquote(clean_url)
            
            # Check if decoded URL matches actual file
            if clean_url.startswith('/images/products/lvt/colors/'):
                rel_path = clean_url[len('/images/products/lvt/colors/'):]
                file_path = base_images_path / rel_path
                
                # Try with decoded path
                decoded_rel_path = decoded_url[len('/images/products/lvt/colors/'):]
                decoded_file_path = base_images_path / decoded_rel_path
                
                # Use decoded path if file exists
                if decoded_file_path.exists():
                    # Update URL to use decoded path
                    new_url = decoded_url + ('?v=9' if '?v=' in texture_url else '')
                    if texture_url != new_url:
                        if color.get('texture_url'):
                            color['texture_url'] = new_url
                        if color.get('image_url'):
                            color['image_url'] = new_url
                        fixed_count += 1
    
    # Check lifestyle_url
    lifestyle_url = color.get('lifestyle_url')
    if lifestyle_url:
        clean_url = lifestyle_url.split('?')[0]
        
        if '%' in clean_url:
            decoded_url = unquote(clean_url)
            
            if clean_url.startswith('/images/products/lvt/colors/'):
                decoded_rel_path = decoded_url[len('/images/products/lvt/colors/'):]
                decoded_file_path = base_images_path / decoded_rel_path
                
                if decoded_file_path.exists():
                    new_url = decoded_url + ('?v=9' if '?v=' in lifestyle_url else '')
                    if lifestyle_url != new_url:
                        color['lifestyle_url'] = new_url
                        fixed_count += 1

print(f"Checked {checked_count} URLs")
print(f"Fixed {fixed_count} URLs")

# Save updated JSON
if fixed_count > 0:
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"\n✅ Updated JSON saved")
else:
    print("\n✅ No changes needed")
