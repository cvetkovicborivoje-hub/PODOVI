import { brandRepository } from '@/lib/repositories/brand-repository';
import BrandCard from '@/components/BrandCard';

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
            <BrandCard key={brand.id} brand={brand} />
          ))}
        </div>
      </div>
    </div>
  );
}
