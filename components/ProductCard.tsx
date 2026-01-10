import Link from 'next/link';
import Image from 'next/image';
import { Product } from '@/types';
import { brandRepository } from '@/lib/repositories/brand-repository';

interface ProductCardProps {
  product: Product;
}

export default async function ProductCard({ product }: ProductCardProps) {
  const brand = await brandRepository.findById(product.brandId);
  const primaryImage = product.images.find(img => img.isPrimary) || product.images[0];

  const href = product.externalLink || `/proizvodi/${product.slug}`;
  const isExternal = !!product.externalLink;

  const cardContent = (
    <>
      <div className="relative h-64 bg-gray-100">
        {primaryImage ? (
          <div className="w-full h-full flex items-center justify-center p-4">
            <div className="text-center text-gray-400">
              <svg className="w-20 h-20 mx-auto mb-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
              <p className="text-sm">{primaryImage.alt}</p>
            </div>
          </div>
        ) : (
          <div className="w-full h-full flex items-center justify-center text-gray-400">
            <span>Bez slike</span>
          </div>
        )}
        {!product.inStock && (
          <div className="absolute top-2 right-2 badge-warning">
            Nema na stanju
          </div>
        )}
        {product.featured && (
          <div className="absolute top-2 left-2 bg-primary-600 text-white px-2 py-1 rounded text-xs font-semibold">
            Izdvojeno
          </div>
        )}
      </div>
      <div className="p-4">
        {brand && (
          <p className="text-xs text-gray-500 mb-1 uppercase tracking-wide">
            {brand.name}
          </p>
        )}
        <h3 className="font-semibold text-lg mb-2 line-clamp-2">
          {product.name}
        </h3>
        <p className="text-sm text-gray-600 mb-3 line-clamp-2">
          {product.shortDescription}
        </p>
        {product.price && product.price > 0 && (
          <div className="flex items-baseline justify-between">
            <div>
              <span className="text-2xl font-bold text-primary-600">
                {product.price.toLocaleString('sr-RS')}
              </span>
              <span className="text-sm text-gray-600 ml-1">
                RSD/{product.priceUnit}
              </span>
            </div>
          </div>
        )}
        <div className="mt-4">
          <span className="text-primary-600 font-medium text-sm">
            {isExternal ? 'Pogledaj kolekciju →' : 'Detaljnije →'}
          </span>
        </div>
      </div>
    </>
  );

  return isExternal ? (
    <a 
      href={href} 
      target="_blank" 
      rel="noopener noreferrer"
      className="card hover:shadow-xl transition-shadow duration-300"
    >
      {cardContent}
    </a>
  ) : (
    <Link href={href} className="card hover:shadow-xl transition-shadow duration-300">
      {cardContent}
    </Link>
  );
}
