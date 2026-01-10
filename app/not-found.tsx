import Link from 'next/link';

export default function NotFound() {
  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center px-4">
      <div className="text-center">
        <h1 className="text-9xl font-bold text-primary-600">404</h1>
        <h2 className="text-3xl font-bold text-gray-900 mt-4 mb-2">
          Stranica nije pronađena
        </h2>
        <p className="text-lg text-gray-600 mb-8">
          Stranica koju tražite ne postoji ili je premeštena.
        </p>
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <Link href="/" className="btn-primary">
            Nazad na početnu
          </Link>
          <Link href="/kategorije" className="btn-outline">
            Pregledaj proizvode
          </Link>
        </div>
      </div>
    </div>
  );
}
