const fs = require('fs');
const path = require('path');

function normalize(p) {
  if (!p) return null;
  try { p = decodeURI(String(p)); } catch (e) {}
  p = p.replace(/\\/g, '/').replace(/\/\/+/g, '/');
  return p.split('?')[0];
}

function listFiles(dir) {
  if (!fs.existsSync(dir)) return [];
  return fs.readdirSync(dir);
}

(function main() {
  const jsonPath = path.join(process.cwd(), 'public', 'data', 'lvt_colors_complete.json');
  const imagesBase = path.join(process.cwd(), 'public', 'images', 'products', 'lvt', 'colors');
  if (!fs.existsSync(jsonPath)) { console.error('JSON missing'); process.exit(2); }
  const data = JSON.parse(fs.readFileSync(jsonPath, 'utf8'));
  const unknowns = data.colors.filter(c => String(c.code).toLowerCase() === 'unknown');
  const suggestions = [];
  unknowns.forEach(u => {
    const candidates = [];
    const imgPath = normalize(u.image_url) || normalize(u.texture_url) || '';
    if (imgPath) {
      const parts = imgPath.split('/').filter(Boolean);
      const folder = parts.slice(0, parts.length - 1).join('/');
      const absFolder = path.join(process.cwd(), 'public', folder.replace(/^\//, ''));
      if (fs.existsSync(absFolder)) {
        const files = listFiles(absFolder);
        candidates.push(...files);
      }
      suggestions.push({ slug: u.slug, name: u.name, imgPath, folder: folder, foundFiles: candidates });
    } else {
      suggestions.push({ slug: u.slug, name: u.name, imgPath: null, folder: null, foundFiles: [] });
    }
  });

  const outDir = path.join(process.cwd(), 'tmp');
  if (!fs.existsSync(outDir)) fs.mkdirSync(outDir, { recursive: true });
  fs.writeFileSync(path.join(outDir, 'unknown-suggestions.json'), JSON.stringify(suggestions, null, 2));
  console.log('Unknown suggestions written to tmp/unknown-suggestions.json');
})();
