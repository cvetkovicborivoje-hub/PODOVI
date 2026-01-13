import Link from 'next/link';
import Image from 'next/image';
import { Product } from '@/types';
import { brandRepository } from '@/lib/repositories/brand-repository';

interface ProductCardProps {
  product: Product;
}

// Color counts for LVT products (extracted from documents)
const colorCounts: Record<string, number> = {
  'gerflor-creation-30': 30,
  'gerflor-creation-40': 30,
  'gerflor-creation-40-clic': 40,
  'gerflor-creation-40-clic-acoustic': 30,
  'gerflor-creation-40-zen': 22,
  'gerflor-creation-55': 30,
  'gerflor-creation-55-clic': 30,
  'gerflor-creation-55-clic-acoustic': 30,
  'gerflor-creation-55-looselay': 52,
  'gerflor-creation-55-looselay-acoustic': 52,
  'gerflor-creation-55-zen': 22,
  'gerflor-creation-70': 70,
  'gerflor-creation-70-clic': 85,
  'gerflor-creation-70-connect': 9,
  'gerflor-creation-70-megaclic': 3,
  'gerflor-creation-70-zen': 22,
  'gerflor-creation-saga': 52,
  'gerflor-creation-70-looselay': 52,
};

export default async function ProductCard({ product }: ProductCardProps) {
  const brand = await brandRepository.findById(product.brandId);
  const primaryImage = product.images.find(img => img.isPrimary) || product.images[0];
  const colorCount = colorCounts[product.slug];
  const isLVT = product.slug.includes('creation');

  return (
    <Link 
      href={`/proizvodi/${product.slug}`}
      className="group card hover:shadow-2xl hover:-translate-y-1 transition-all duration-300 border border-transparent hover:border-primary-100"
    >
      <div className="relative h-64 bg-gray-100 overflow-hidden group-hover:scale-105 transition-transform duration-500">
        {primaryImage ? (
          <img
            src={primaryImage.url}
            alt={primaryImage.alt}
            className="w-full h-full object-cover"
          />
        ) : (
          <div className="w-full h-full flex items-center justify-center text-gray-400">
            <span>Bez slike</span>
          </div>
        )}
        {!product.inStock && (
          <div className="absolute top-3 right-3 badge-warning shadow-lg">
            Nema na stanju
          </div>
        )}
        {product.featured && (
          <div className="absolute top-3 left-3 bg-gradient-to-r from-primary-600 to-primary-700 text-white px-3 py-1.5 rounded-lg text-xs font-semibold shadow-lg">
            Izdvojeno
          </div>
        )}
        {/* Color count badge for LVT */}
        {colorCount && (
          <div className="absolute bottom-3 left-3 bg-white/95 backdrop-blur-sm px-3 py-1.5 rounded-lg text-xs font-semibold shadow-lg flex items-center gap-1.5">
            <span className="w-3 h-3 rounded-full bg-gradient-to-r from-red-400 via-yellow-400 to-blue-400"></span>
            <span className="text-gray-800">{colorCount} boja</span>
          </div>
        )}
        {/* Eco badge for LVT */}
        {isLVT && (
          <div className="absolute bottom-3 right-3 bg-green-500/90 backdrop-blur-sm px-2.5 py-1.5 rounded-lg shadow-lg flex items-center gap-1" title="Ekološki proizvod">
            <svg className="w-4 h-4 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
            </svg>
            <span className="text-white text-xs font-semibold">ECO</span>
          </div>
        )}
        {/* Overlay on hover */}
        <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
      </div>
      <div className="p-5">
        {brand && (
          <p className="text-xs text-primary-600 mb-2 uppercase tracking-wider font-semibold">
            {brand.name}
          </p>
        )}
        <h3 className="font-bold text-lg mb-2 line-clamp-2 text-gray-900 group-hover:text-primary-600 transition-colors duration-300">
          {product.name}
        </h3>
        <p className="text-sm text-gray-600 mb-3 line-clamp-2 leading-relaxed">
          {product.shortDescription}
        </p>
        
        {/* Feature icons for LVT */}
        {isLVT && (
          <div className="flex items-center gap-3 mb-4">
            <div className="flex items-center gap-1 text-xs text-gray-500" title="Podno grejanje">
              <svg className="w-4 h-4 text-orange-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 18.657A8 8 0 016.343 7.343S7 9 9 10c0-2 .5-5 2.986-7C14 5 16.09 5.777 17.656 7.343A7.975 7.975 0 0120 13a7.975 7.975 0 01-2.343 5.657z" />
              </svg>
              <span>Podno grejanje</span>
            </div>
            <div className="flex items-center gap-1 text-xs text-gray-500" title="Lako održavanje">
              <svg className="w-4 h-4 text-blue-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
              </svg>
              <span>Lako čišćenje</span>
            </div>
          </div>
        )}
        
        {product.price && product.price > 0 && (
          <div className="flex items-baseline justify-between mb-4">
            <div>
              <span className="text-2xl font-bold text-gray-900">
                {product.price.toLocaleString('sr-RS')}
              </span>
              <span className="text-sm text-gray-500 ml-1">
                RSD/{product.priceUnit}
              </span>
            </div>
          </div>
        )}
        <div className="flex items-center text-primary-600 font-semibold text-sm group-hover:gap-2 transition-all duration-300">
          <span>Detaljnije</span>
          <svg className="w-4 h-4 transform group-hover:translate-x-1 transition-transform duration-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
          </svg>
        </div>
      </div>
    </Link>
  );
}
