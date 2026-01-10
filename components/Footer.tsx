import Link from 'next/link';

export default function Footer() {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="bg-black text-gray-300 mt-auto">
      <div className="container py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* About */}
          <div>
            <h3 className="text-white text-lg font-semibold mb-4">O nama</h3>
            <p className="text-sm">
              Vodeci uvoznik i distributer kvalitetnih podnih obloga u Srbiji. 
              Nudimo širok asortiman proizvoda od renomiranih evropskih brendova.
            </p>
          </div>

          {/* Quick Links */}
          <div>
            <h3 className="text-white text-lg font-semibold mb-4">Brzi linkovi</h3>
            <ul className="space-y-2 text-sm">
              <li>
                <Link href="/" className="hover:text-white transition">
                  Početna
                </Link>
              </li>
              <li>
                <Link href="/kategorije" className="hover:text-white transition">
                  Kategorije
                </Link>
              </li>
              <li>
                <Link href="/brendovi" className="hover:text-white transition">
                  Brendovi
                </Link>
              </li>
              <li>
                <Link href="/kontakt" className="hover:text-white transition">
                  Kontakt
                </Link>
              </li>
            </ul>
          </div>

          {/* Categories */}
          <div>
            <h3 className="text-white text-lg font-semibold mb-4">Kategorije</h3>
            <ul className="space-y-2 text-sm">
              <li>
                <Link href="/kategorije/laminat" className="hover:text-white transition">
                  Laminat
                </Link>
              </li>
              <li>
                <Link href="/kategorije/vinil" className="hover:text-white transition">
                  Vinil
                </Link>
              </li>
              <li>
                <Link href="/kategorije/parket" className="hover:text-white transition">
                  Parket
                </Link>
              </li>
              <li>
                <Link href="/kategorije/podne-obloge" className="hover:text-white transition">
                  Podne obloge
                </Link>
              </li>
            </ul>
          </div>

          {/* Contact */}
          <div>
            <h3 className="text-white text-lg font-semibold mb-4">Kontakt</h3>
            <ul className="space-y-2 text-sm">
              <li className="flex items-start">
                <svg className="h-5 w-5 mr-2 mt-0.5 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
                </svg>
                <span>+381 11 123 4567</span>
              </li>
              <li className="flex items-start">
                <svg className="h-5 w-5 mr-2 mt-0.5 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                </svg>
                <span>info@podovi.rs</span>
              </li>
              <li className="flex items-start">
                <svg className="h-5 w-5 mr-2 mt-0.5 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
                <span>Beograd, Srbija</span>
              </li>
            </ul>
          </div>
        </div>

        <div className="border-t border-gray-800 mt-8 pt-8 text-sm text-center">
          <p>&copy; {currentYear} Podovi.rs. Sva prava zadržana.</p>
        </div>
      </div>
    </footer>
  );
}
