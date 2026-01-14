const fs = require('fs');
const path = require('path');

function normalizeStr(p) {
  if (!p) return p;
  let s = String(p).trim();
  try { s = decodeURI(s); } catch (e) {}
  s = s.replace(/\\/g, '/').replace(/\/\/+/g, '/');
  if (!s.startsWith('/')) s = '/' + s;
  return s;
}

(function main() {
  const jsonPath = path.join(process.cwd(), 'public', 'data', 'lvt_colors_complete.json');
  if (!fs.existsSync(jsonPath)) {
    console.error('JSON not found at', jsonPath);
    process.exit(2);
  }
  const data = JSON.parse(fs.readFileSync(jsonPath, 'utf8'));
  const changed = [];

  data.colors = data.colors.map(c => {
    const image_url = normalizeStr(c.image_url);
    const texture_url = normalizeStr(c.texture_url);
    const lifestyle_url = normalizeStr(c.lifestyle_url);
    if (image_url !== c.image_url || texture_url !== c.texture_url || lifestyle_url !== c.lifestyle_url) {
      changed.push(c.slug || c.name || c.code);
    }
    return { ...c, image_url, texture_url, lifestyle_url };
  });

  const backupPath = jsonPath + '.bak.' + Date.now();
  fs.copyFileSync(jsonPath, backupPath);
  fs.writeFileSync(jsonPath, JSON.stringify(data, null, 2));
  console.log('Normalized', changed.length, 'entries. Backup written to', backupPath);
})();
