import sys
import shutil
from pathlib import Path
from PIL import Image
import numpy as np
from concurrent.futures import ProcessPoolExecutor, as_completed
import multiprocessing
sys.stdout.reconfigure(encoding='utf-8')

def detect_furniture(image_path):
    """Detekcija nameštaja na slici"""
    try:
        img = Image.open(image_path).convert('RGB')
        img_array = np.array(img)
        
        # 1. KOMPLEKSNOST BOJA
        unique_colors = len(np.unique(img_array.reshape(-1, img_array.shape[2]), axis=0))
        color_complexity = unique_colors / (img.size[0] * img.size[1])
        
        # 2. EDGE DETECTION
        gray = img.convert('L')
        gray_array = np.array(gray)
        edges_h = np.abs(np.diff(gray_array, axis=0))
        edges_v = np.abs(np.diff(gray_array, axis=1))
        edge_ratio = (np.sum(edges_h > 30) + np.sum(edges_v > 30)) / gray_array.size
        
        # 3. BRIGHTNESS VARIANCE
        brightness_variance = np.var(gray_array)
        
        # 4. HISTOGRAM
        hist, _ = np.histogram(gray_array, bins=50)
        hist_std = np.std(hist)
        
        # SCORING
        score = 0
        if color_complexity > 0.15: score += 2
        if edge_ratio > 0.15: score += 3
        if brightness_variance > 2000: score += 2
        if hist_std > 200: score += 2
        
        return {
            'path': str(image_path),
            'has_furniture': score >= 5,
            'score': score
        }
    except Exception as e:
        return {'path': str(image_path), 'has_furniture': False, 'score': 0, 'error': str(e)}

def analyze_product(product_info):
    """Analizira jedan proizvod"""
    product_dir, slug, collection = product_info
    
    all_images = list(product_dir.glob('*.jpg'))
    main_image = product_dir / f"{slug}.jpg"
    
    if not main_image.exists() or len(all_images) < 2:
        return None
    
    # Testiraj glavnu sliku
    main_result = detect_furniture(main_image)
    
    if main_result['has_furniture']:
        # Pronađi swatch
        original_images = [img for img in all_images if img != main_image]
        best_swatch = None
        min_score = 999
        
        for img in original_images:
            result = detect_furniture(img)
            if not result['has_furniture'] and result['score'] < min_score:
                best_swatch = img
                min_score = result['score']
        
        if best_swatch:
            return {
                'collection': collection,
                'slug': slug,
                'main_image': main_image,
                'replace_with': best_swatch,
                'score': main_result['score']
            }
    
    return None

if __name__ == '__main__':
    # Priprema liste svih proizvoda
    base_path = Path('public/images/products/lvt/colors')
    products = []
    
    print("=" * 80)
    print("PARALELNA AI DETEKCIJA - KORISTI SVE CPU CORE-OVE!")
    print("=" * 80)
    print(f"\n🖥️  CPU Cores: {multiprocessing.cpu_count()}")
    print("📊 Prikupljam proizvode...\n")
    
    for collection_dir in sorted(base_path.iterdir()):
        if not collection_dir.is_dir():
            continue
        collection = collection_dir.name
        for product_dir in sorted(collection_dir.iterdir()):
            if product_dir.is_dir():
                products.append((product_dir, product_dir.name, collection))
    
    print(f"✅ Pronađeno {len(products)} proizvoda")
    print(f"🚀 Pokrećem analizu sa {multiprocessing.cpu_count()} procesa...\n")
    
    # Paralelna obrada
    products_to_fix = []
    processed = 0
    
    with ProcessPoolExecutor(max_workers=multiprocessing.cpu_count()) as executor:
        futures = {executor.submit(analyze_product, prod): prod for prod in products}
        
        for future in as_completed(futures):
            processed += 1
            if processed % 50 == 0:
                print(f"📊 Proverio {processed}/{len(products)} proizvoda...")
            
            result = future.result()
            if result:
                products_to_fix.append(result)
                print(f"❌ {result['collection']}/{result['slug']} (score={result['score']})")
    
    print()
    print("=" * 80)
    print(f"📊 REZULTATI:")
    print(f"   Ukupno: {len(products)}")
    print(f"   ✅ Već OK: {len(products) - len(products_to_fix)}")
    print(f"   ❌ Treba popraviti: {len(products_to_fix)}")
    print("=" * 80)
    print()
    
    if products_to_fix:
        print(f"🔧 ZAMENJUJEM {len(products_to_fix)} SLIKA...\n")
        
        for i, product in enumerate(products_to_fix, 1):
            print(f"[{i}/{len(products_to_fix)}] {product['collection']}/{product['slug']}")
            shutil.copy(product['replace_with'], product['main_image'])
        
        print()
        print("=" * 80)
        print(f"✅ GOTOVO! Zamenjeno {len(products_to_fix)} slika!")
        print("=" * 80)
    else:
        print("✅ Sve slike su već dobre!")
