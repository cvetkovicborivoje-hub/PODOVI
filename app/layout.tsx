import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import Header from "@/components/Header";
import Footer from "@/components/Footer";
import WhatsAppButton from "@/components/WhatsAppButton";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Podovi - Katalog podnih obloga",
  description: "Pronađite savršen pod za vaš prostor. Širok izbor laminata, vinila, parketa i drugih podnih obloga od vodećih brendova.",
  keywords: "podovi, laminat, vinil, parket, podne obloge, Srbija",
  authors: [{ name: "Podovi" }],
  openGraph: {
    title: "Najveći izbor podova u Srbiji",
    description: "📞 063 299 444 | 💬 WhatsApp | 🌐 podovi.online",
    type: "website",
    locale: "sr_RS",
    url: "https://podovi.online",
    siteName: "Podovi.online",
    images: [
      {
        url: "/og-image.jpg",
        width: 1200,
        height: 630,
        alt: "Podovi - Katalog podnih obloga",
      },
    ],
  },
  twitter: {
    card: "summary_large_image",
    title: "Najveći izbor podova u Srbiji",
    description: "📞 063 299 444 | 💬 WhatsApp | 🌐 podovi.online",
    images: ["/og-image.jpg"],
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="sr">
      <body className={inter.className}>
        <div className="flex flex-col min-h-screen">
          <Header />
          <main className="flex-grow">
            {children}
          </main>
          <Footer />
          <WhatsAppButton />
        </div>
      </body>
    </html>
  );
}
