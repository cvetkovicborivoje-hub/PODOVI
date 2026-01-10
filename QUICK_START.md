# 🚀 Quick Start Guide

## Pokretanje projekta (5 minuta)

### 1. Instaliraj dependencies
```bash
npm install
```

### 2. Pokreni development server
```bash
npm run dev
```

### 3. Otvori u browseru
```
http://localhost:3000
```

## 📍 Gde početi?

### Početna stranica
`http://localhost:3000`
- Hero sekcija
- Kategorije
- Izdvojeni proizvodi

### Pregledaj kategorije
`http://localhost:3000/kategorije`
- Lista svih kategorija

### Filtriraj proizvode
`http://localhost:3000/kategorije/laminat`
- Filteri za brend, cenu, dostupnost
- Pretraga

### Pregledaj proizvod
`http://localhost:3000/proizvodi/egger-pro-laminat-hrast-valley-dymny`
- Detaljne specifikacije
- **Klikni "Pošalji upit"** - testiranje inquiry forme!

### Kontakt
`http://localhost:3000/kontakt`
- Kontakt forma

## 🧪 Testiranje inquiry forme

1. Otvori bilo koji proizvod
2. Klikni **"Pošalji upit"**
3. Popuni formu:
   - Ime i prezime
   - Telefon i email
   - Grad
   - Količina (opciono)
   - Poruka
   - Izaberi način kontakta (poziv/email/viber/whatsapp)
4. Klikni **"Pošalji upit"**
5. Proveri **konzolu u terminalu** - videćeš mock email output

## 📊 Mock podaci

Trenutno projekat ima:
- **5 kategorija** (Laminat, Vinil, Parket, Podne obloge, Terasni podovi)
- **5 brendova** (Egger, Quick-Step, Tarkett, Balterio, Kronotex)
- **6 proizvoda** sa detaljnim specifikacijama

## 🔧 Šta dalje?

### Dodaj proizvode
Edituj `lib/data/mock-data.ts` i dodaj nove proizvode u `products` array.

### Promeni dizajn
- Boje: `tailwind.config.ts` - primary color paleta
- Stilovi: `app/globals.css` - custom komponente

### Integracija sa bazom
1. Instaliraj Prisma: `npm install @prisma/client prisma`
2. Kreiraj schema u `prisma/schema.prisma`
3. Implementiraj pravi repository umesto mock-a
4. Zameni mock instance u repository fajlovima

### Email integracija
1. Instaliraj: `npm install nodemailer` ili koristi SendGrid/Resend
2. Implementiraj pravi mailer u `lib/mailer/mailer.ts`
3. Dodaj SMTP credentials u `.env.local`

## 📱 Test responzivnosti

- Otvori DevTools (F12)
- Toggle device toolbar (Ctrl+Shift+M)
- Testiraj na mobilnim dimenzijama

## 🏗️ Build za produkciju

```bash
npm run build
npm start
```

## ❓ Česta pitanja

**Q: Kako dodati novu kategoriju?**
A: Dodaj novi objekat u `categories` array u `lib/data/mock-data.ts`

**Q: Kako promeniti logo?**
A: Trenutno je tekst "Podovi.rs" u `components/Header.tsx` - možeš zameniti sa Image komponentom

**Q: Gde se čuvaju upiti?**
A: Trenutno in-memory u `MockInquiryRepository`. Za produkciju integriši sa pravom bazom.

**Q: Kako promeniti kontakt informacije?**
A: Edituj `components/Footer.tsx` i `app/kontakt/page.tsx`

## 📞 Pomoć

Ako nešto ne radi:
1. Proveri da li je `npm install` uspešno završen
2. Proveri Node.js verziju (treba 18+)
3. Obriši `.next` folder i pokreni ponovo `npm run dev`
4. Proveri konzolu za greške

---

**Srećno kodiranje! 🎉**
