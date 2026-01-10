import { brandRepository } from '@/lib/repositories/brand-repository';
import Link from 'next/link';

export const metadata = {
  title: 'Brendovi - Podovi',
  description: 'Radimo sa vodećim evropskim proizvođačima podnih obloga. Egger, Quick-Step, Tarkett, Balterio, Kronotex i mnogi drugi.',
};

export default async function BrandsPage() {
  const brands = await brandRepository.findAll();

  return (
    <div className="bg-gray-50 min-h-screen">
      {/* Header */}
      <div className="bg-white border-b">
        <div className="container py-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            Naši brendovi
          </h1>
          <p className="text-lg text-gray-600">
            Radimo sa vodećim evropskim proizvođačima koji garantuju vrhunski kvalitet
          </p>
        </div>
      </div>

      <div className="container py-12">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {brands.map((brand) => (
            <div key={brand.id} className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-xl transition-shadow">
              <div className="h-48 bg-gradient-to-br from-gray-50 to-gray-100 flex items-center justify-center p-8">
                <div className="text-center">
                  <div className="w-24 h-24 bg-white rounded-full mx-auto mb-4 flex items-center justify-center shadow-md">
                    <span className="text-3xl font-bold text-gray-400">
                      {brand.name.charAt(0)}
                    </span>
                  </div>
                  <h2 className="text-2xl font-bold text-gray-900">
                    {brand.name}
                  </h2>
                </div>
              </div>
              <div className="p-6">
                <p className="text-gray-600 mb-4">
                  {brand.description}
                </p>
                {brand.countryOfOrigin && (
                  <p className="text-sm text-gray-500 mb-4">
                    <span className="font-medium">Zemlja porekla:</span> {brand.countryOfOrigin}
                  </p>
                )}
                <div className="flex gap-3">
                  {brand.website && (
                    <a
                      href={brand.website}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-sm text-primary-600 hover:text-primary-700 font-medium"
                    >
                      Zvanični sajt →
                    </a>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
