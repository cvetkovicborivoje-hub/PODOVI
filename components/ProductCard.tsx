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
      <div className="relative h-64 bg-gray-100 overflow-hidden">
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
