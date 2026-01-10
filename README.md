# Podovi - Katalog podnih obloga

Moderna web aplikacija za katalog podnih obloga sa funkcijom slanja upita. Građena za srpsko tržište bez online plaćanja - fokus na generisanju lead-ova kroz upite.

## 🚀 Tehnologije

- **Next.js 14** - App Router
- **TypeScript** - Type safety
- **Tailwind CSS** - Modern styling
- **Mock Repository Pattern** - Spremno za integraciju sa pravom bazom

## 📋 Karakteristike

### 🏠 Stranice
- **Početna** - Hero sekcija, kategorije, izdvojeni proizvodi
- **Kategorije** - Lista svih kategorija sa prikazom proizvoda
- **Kategorija** - Filtriranje, pretraga, paginacija proizvoda
- **Proizvod** - Detaljni prikaz sa specifikacijama i dugmetom za upit
- **Brendovi** - Lista svih brendova partnera
- **Kontakt** - Kontakt forma i informacije
- **Upiti** - Objašnjenje procesa slanja upita

### 💼 Funkcionalnosti
- ✅ Filtriranje proizvoda (brend, cena, dostupnost)
- ✅ Pretraga proizvoda
- ✅ Inquiry forma sa prefilled podacima
- ✅ Mock email sistem (priprema za pravu integraciju)
- ✅ Responzivni dizajn (mobile-first)
- ✅ SEO optimizovano (meta tagovi, Open Graph, strukturirani podaci)
- ✅ Clean URL slugs
- ✅ Sitemap i robots.txt

### 📊 Data modeli
- **Category** - Kategorije proizvoda
- **Brand** - Brendovi
- **Product** - Proizvodi sa slikama i specifikacijama
- **Inquiry** - Upiti kupaca sa svim potrebnim poljima

## 🛠️ Instalacija

### Preduslovi
- Node.js 18+ 
- npm ili yarn

### Koraci

1. **Kloniraj repozitorijum**
```bash
git clone <repository-url>
cd SAJT
```

2. **Instaliraj dependencies**
```bash
npm install
```

3. **Podesi environment variables**
Kreiraj `.env.local` fajl:
```env
NEXT_PUBLIC_BASE_URL=http://localhost:3000
```

4. **Pokreni development server**
```bash
npm run dev
```

Aplikacija će biti dostupna na `http://localhost:3000`

## 📁 Struktura projekta

```
.
├── app/                      # Next.js App Router
│   ├── api/                  # API routes
│   │   ├── inquiries/        # Inquiry endpoints
│   │   └── contact/          # Contact form endpoint
│   ├── kategorije/           # Category pages
│   ├── proizvodi/            # Product pages
│   ├── brendovi/             # Brands page
│   ├── kontakt/              # Contact page
│   ├── upiti/                # Inquiry info page
│   ├── layout.tsx            # Root layout
│   ├── page.tsx              # Home page
│   ├── robots.ts             # Robots.txt
│   ├── sitemap.ts            # Dynamic sitemap
│   └── not-found.tsx         # 404 page
├── components/               # React components
│   ├── Header.tsx
│   ├── Footer.tsx
│   ├── ProductCard.tsx
│   ├── CategoryCard.tsx
│   ├── ProductFilters.tsx
│   ├── InquiryButton.tsx
│   ├── InquiryModal.tsx
│   └── StructuredData.tsx
├── lib/                      # Business logic
│   ├── data/                 # Mock data
│   │   └── mock-data.ts
│   ├── repositories/         # Data access layer
│   │   ├── product-repository.ts
│   │   ├── category-repository.ts
│   │   ├── brand-repository.ts
│   │   └── inquiry-repository.ts
│   ├── mailer/               # Email service
│   │   └── mailer.ts
│   └── seo/                  # SEO utilities
│       ├── structured-data.ts
│       └── metadata.ts
├── types/                    # TypeScript types
│   └── index.ts
├── public/                   # Static assets
└── tailwind.config.ts        # Tailwind configuration
```

## 🎨 Stilizovanje

Projekat koristi Tailwind CSS sa custom komponentama definisanim u `globals.css`:
- `.btn`, `.btn-primary`, `.btn-secondary`, `.btn-outline` - Dugmad
- `.input`, `.label` - Form elementi
- `.card` - Kartice
- `.badge`, `.badge-success`, `.badge-warning` - Badge-ovi

## 🔌 Integracija sa bazom podataka

Trenutno projekat koristi mock repozitorijume. Za integraciju sa pravom bazom:

1. **Instaliraj ORM** (npr. Prisma)
```bash
npm install @prisma/client
npm install -D prisma
```

2. **Implementiraj repository interface**
Svaki repository ima definisan interface (npr. `IProductRepository`). Kreiraj novu implementaciju koja se povezuje na pravu bazu.

3. **Zameni mock instance**
U `lib/repositories/*.ts` fajlovima zameni mock instancu sa pravom implementacijom.

## 📧 Email integracija

Za slanje pravih email-ova:

1. **Instaliraj email library** (npr. Nodemailer, SendGrid, Resend)
```bash
npm install nodemailer
npm install -D @types/nodemailer
```

2. **Implementiraj `IMailer` interface**
Fajl `lib/mailer/mailer.ts` sadrži interface. Kreiraj implementaciju koja koristi odabranu email biblioteku.

3. **Dodaj credentials u environment**
```env
SMTP_HOST=smtp.example.com
SMTP_PORT=587
SMTP_USER=your-email@example.com
SMTP_PASS=your-password
```

## 🔍 SEO

Projekat uključuje:
- ✅ Meta tagovi (title, description, keywords)
- ✅ Open Graph tagovi
- ✅ Twitter Card tagovi
- ✅ Structured data (JSON-LD) za proizvode i organizaciju
- ✅ Canonical URLs
- ✅ Dynamic sitemap
- ✅ robots.txt
- ✅ Clean URL slugs

## 📱 Responzivnost

Dizajn je mobile-first sa breakpoints:
- `sm`: 640px
- `md`: 768px
- `lg`: 1024px
- `xl`: 1280px

## 🚢 Deploy

### Vercel (preporučeno)

1. Push code na GitHub
2. Uvezi projekat u Vercel
3. Postavi environment variables
4. Deploy!

### Druge platforme

Projekat je standardna Next.js aplikacija i može se deployovati na bilo koju platformu koja podržava Next.js:
- Netlify
- Railway
- AWS
- DigitalOcean

## 📝 Licenca

Sva prava zadržana.

## 🤝 Kontakt

Za pitanja i podršku:
- Email: info@podovi.rs
- Telefon: +381 11 123 4567
