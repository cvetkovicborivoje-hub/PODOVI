import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import Header from "@/components/Header";
import Footer from "@/components/Footer";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Podovi - Katalog podnih obloga",
  description: "Pronađite savršen pod za vaš prostor. Širok izbor laminata, vinila, parketa i drugih podnih obloga od vodećih brendova.",
  keywords: "podovi, laminat, vinil, parket, podne obloge, Srbija",
  authors: [{ name: "Podovi" }],
  openGraph: {
    title: "Podovi - Katalog podnih obloga",
    description: "Pronađite savršen pod za vaš prostor. Širok izbor laminata, vinila, parketa i drugih podnih obloga od vodećih brendova.",
    type: "website",
    locale: "sr_RS",
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
        </div>
      </body>
    </html>
  );
}
