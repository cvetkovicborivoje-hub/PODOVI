# Podovi.online

Moderna web aplikacija za katalog podnih obloga.Buildan za srpsko tržište.

## 🚀 Sajt

**Live:** https://podovi.online

---

## 📋 Šta ima na sajtu?

### **Kategorije podova:**
- 🪵 Parket
- 🟫 Laminat  
- 💎 LVT (Luxury Vinyl Tile)
- 📐 Tekstilne ploče
- 🌲 Deking
- 🎨 Vinil
- 🌿 Linoleum

### **Brendovi:**
- Egger
- Quick-Step
- Tarkett
- Balterio
- Gerflor (36 kolekcija sa slikama)

### **Funkcionalnosti:**
- ✅ Moderan dizajn sa gradientima i hover efektima
- ✅ WhatsApp dugme (+38163299444)
- ✅ Responsive dizajn (radi na mobilnom)
- ✅ Eksterni linkovi ka Gerflor sajtu za detaljne kataloge
- ✅ SSL sertifikat (HTTPS)

---

## 🛠️ Tehnologije

- **Next.js 14** - React framework
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **Vercel** - Hosting & deployment

---

## 💻 Development

```bash
# Instaliraj dependencies
npm install

# Pokreni dev server
npm run dev

# Build za produkciju
npm run build
```

Sajt će biti na: http://localhost:3000

---

## 📁 Struktura

```
├── app/              # Stranice (Next.js App Router)
├── components/       # React komponente
├── lib/data/         # Mock data (proizvodi, kategorije)
├── public/images/    # Slike proizvoda
└── types/            # TypeScript tipovi
```

---

## 📸 Slike proizvoda

Sve slike su lokalno u `public/images/products/`:
- `lvt/` - 18 Gerflor LVT kolekcija
- `linoleum/` - 15 DLW Linoleum kolekcija
- `tekstilne-ploce/` - 3 Gerflor Armonia kolekcije

---

## 🚢 Deployment

Sajt je povezan sa GitHub repo-m i automatski se deployuje na Vercel pri svakom push-u na `main` branch.

**Domen:** podovi.online (Hostinger + Vercel nameservers)

---

## 📝 Napomene

- Nema online plaćanja - sajt je katalog/landing page
- Proizvodi vode ka eksternim sajtovima (Gerflor) ili WhatsApp kontaktu
- Mock data - spremno za integraciju sa pravom bazom

---

Sva prava zadržana © 2026
