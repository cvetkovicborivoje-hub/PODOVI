import sys
import re
sys.stdout.reconfigure(encoding='utf-8')

# Čita TS fajl
with open('lib/data/gerflor-products-generated.ts', 'r', encoding='utf-8') as f:
    content = f.read()

# Dodaje ?v=2 na sve image URL-ove
content = re.sub(
    r'image: "(/images/products/lvt/colors/[^"]+\.jpg)"',
    r'image: "\1?v=2"',
    content
)

# Piše nazad
with open('lib/data/gerflor-products-generated.ts', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Cache bust dodat na sve slike!")
