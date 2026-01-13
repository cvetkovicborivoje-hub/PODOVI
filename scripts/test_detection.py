import sys
from pathlib import Path
from PIL import Image
import numpy as np
sys.stdout.reconfigure(encoding='utf-8')

def detect_furniture_simple(image_path):
    """Jednostavna detekcija"""
    try:
        img = Image.open(image_path).convert('RGB')
        img_array = np.array(img)
        
        # Edge detection
        gray = img.convert('L')
        gray_array = np.array(gray)
        edges_h = np.abs(np.diff(gray_array, axis=0))
        edges_v = np.abs(np.diff(gray_array, axis=1))
        edge_ratio = (np.sum(edges_h > 30) + np.sum(edges_v > 30)) / gray_array.size
        
        # Brightness variance
        brightness_var = np.var(gray_array)
        
        # Color complexity
        unique_colors = len(np.unique(img_array.reshape(-1, 3), axis=0))
        color_ratio = unique_colors / (img.size[0] * img.size[1])
        
        score = 0
        if edge_ratio > 0.15: score += 3
        if brightness_var > 2000: score += 2
        if color_ratio > 0.15: score += 2
        
        return {
            'furniture': score >= 5,
            'score': score,
            'edge_ratio': edge_ratio,
            'brightness_var': brightness_var,
            'color_ratio': color_ratio
        }
    except Exception as e:
        return {'error': str(e)}

# Testiraj nekoliko primera
examples = [
    "public/images/products/lvt/colors/creation-30/ballerina-41870347/ballerina-41870347.jpg",
    "public/images/products/lvt/colors/creation-30/beige-41870853/beige-41870853.jpg",
    "public/images/products/lvt/colors/creation-30/beige-41751278/beige-41751278.jpg",
]

print("=" * 80)
print("TEST DETEKCIJE NAMEŠTAJA")
print("=" * 80)
print()

for img_path in examples:
    path = Path(img_path)
    if path.exists():
        result = detect_furniture_simple(path)
        print(f"📸 {path.name}")
        print(f"   Furniture: {result.get('furniture', 'ERROR')}")
        print(f"   Score: {result.get('score', 0)}")
        print(f"   Edges: {result.get('edge_ratio', 0):.3f}")
        print(f"   Variance: {result.get('brightness_var', 0):.0f}")
        print(f"   Colors: {result.get('color_ratio', 0):.3f}")
        print()
    else:
        print(f"❌ Nije pronađen: {img_path}\n")

print("=" * 80)
print("Ako su sve FALSE - onda je logika OK za swatches!")
print("=" * 80)
