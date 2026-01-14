const fs = require('fs');
const path = require('path');

function normalize(p) {
  if (!p) return null;
  let s = String(p).trim();
  try { s = decodeURI(s); } catch (e) {}
  s = s.replace(/\\/g, '/').replace(/\/\/+/g, '/');
  // remove query string for filesystem checks
  const withoutQuery = s.split('?')[0];
  if (!withoutQuery.startsWith('/')) return '/' + withoutQuery;
  return withoutQuery;
}

function relToFs(p) {
  // p expected to start with '/'
  return path.join(process.cwd(), 'public', p.replace(/^\//, ''));
}

function listFolders(base) {
  if (!fs.existsSync(base)) return [];
  return fs.readdirSync(base, { withFileTypes: true })
    .filter(d => d.isDirectory())
    .map(d => d.name);
}

(async () => {
  const jsonPath = path.join(process.cwd(), 'public', 'data', 'lvt_colors_complete.json');
  if (!fs.existsSync(jsonPath)) {
    console.error('JSON not found at', jsonPath);
    process.exit(2);
  }
  const data = JSON.parse(fs.readFileSync(jsonPath, 'utf8'));
  const missing = [];
  const referencedFolders = new Set();

  data.colors.forEach((c, idx) => {
    const candidates = [];
    ['texture_url', 'image_url', 'lifestyle_url'].forEach(k => {
      if (c[k]) candidates.push(c[k]);
    });
    if (c.image_url && typeof c.image_url === 'string') {
      const folderMatch = normalize(c.image_url).split('/').slice(0, -1).join('/');
      if (folderMatch) referencedFolders.add(folderMatch.replace(/^\//, ''));
    }

    candidates.forEach(src => {
      const np = normalize(src);
      if (!np) return;
      const fsPath = relToFs(np);
      if (!fs.existsSync(fsPath)) {
        missing.push({ index: idx, collection: c.collection, code: c.code, name: c.name, src: src, checkedPath: fsPath });
      }
    });
  });

  const imagesBase = path.join(process.cwd(), 'public', 'images', 'products', 'lvt', 'colors');
  const allFolders = listFolders(imagesBase);
  const orphaned = allFolders.filter(f => ![...referencedFolders].some(r => r.endsWith(f) || r === f));

  const outDir = path.join(process.cwd(), 'tmp');
  if (!fs.existsSync(outDir)) fs.mkdirSync(outDir, { recursive: true });
  fs.writeFileSync(path.join(outDir, 'missing-images.json'), JSON.stringify({ missing, count: missing.length }, null, 2));
  fs.writeFileSync(path.join(outDir, 'orphaned-folders.json'), JSON.stringify({ orphaned, count: orphaned.length }, null, 2));

  console.log('Checked', data.colors.length, 'colors');
  console.log('Missing images:', missing.length, '-> tmp/missing-images.json');
  console.log('Orphaned folders:', orphaned.length, '-> tmp/orphaned-folders.json');

  process.exit(0);
})();
