import { Metadata } from 'next';
import Link from 'next/link';
import { notFound } from 'next/navigation';
import { productRepository } from '@/lib/repositories/product-repository';
import { categoryRepository } from '@/lib/repositories/category-repository';
import { brandRepository } from '@/lib/repositories/brand-repository';

interface Props {
  params: { slug: string };
}

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const product = await productRepository.findBySlug(params.slug);
  
  if (!product) {
    return {
      title: 'Proizvod nije pronađen',
    };
  }

  return {
    title: `${product.name} | Podovi.online`,
    description: product.shortDescription,
  };
}

export default async function ProductPage({ params }: Props) {
  const product = await productRepository.findBySlug(params.slug);
  
  if (!product) {
    notFound();
  }

  const category = await categoryRepository.findById(product.categoryId);
  const brand = await brandRepository.findById(product.brandId);
  const primaryImage = product.images.find(img => img.isPrimary) || product.images[0];

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Breadcrumbs */}
      <div className="bg-white border-b">
        <div className="container py-4">
          <nav className="flex items-center space-x-2 text-sm">
            <Link href="/" className="text-gray-500 hover:text-primary-600">
              Početna
            </Link>
            <span className="text-gray-400">/</span>
            {category && (
              <>
                <Link
                  href={`/kategorije/${category.slug}`}
                  className="text-gray-500 hover:text-primary-600"
                >
                  {category.name}
                </Link>
                <span className="text-gray-400">/</span>
              </>
            )}
            <span className="text-gray-900 font-medium">{product.name}</span>
          </nav>
        </div>
      </div>

      {/* Product Content */}
      <div className="container py-12">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
          {/* Image Section */}
          <div className="bg-white rounded-2xl shadow-lg p-8">
            <div className="aspect-square relative overflow-hidden rounded-xl bg-gray-100">
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
            </div>
          </div>

          {/* Info Section */}
          <div className="space-y-8">
            {/* Brand */}
            {brand && (
              <div className="flex items-center space-x-3">
                <span className="text-sm text-gray-500">Brend:</span>
                <Link
                  href={`/brendovi/${brand.slug}`}
                  className="text-primary-600 hover:text-primary-700 font-semibold"
                >
                  {brand.name}
                </Link>
              </div>
            )}

            {/* Title */}
            <div>
              <h1 className="text-4xl font-bold text-gray-900 mb-3">
                {product.name}
              </h1>
              <p className="text-xl text-gray-600">
                {product.shortDescription}
              </p>
            </div>

            {/* Price (if available) */}
            {product.price && product.price > 0 && (
              <div className="bg-primary-50 border border-primary-200 rounded-xl p-6">
                <div className="flex items-baseline space-x-2">
                  <span className="text-4xl font-bold text-primary-600">
                    {product.price.toLocaleString('sr-RS')}
                  </span>
                  <span className="text-lg text-gray-600">RSD</span>
                  {product.priceUnit && (
                    <span className="text-lg text-gray-500">/ {product.priceUnit}</span>
                  )}
                </div>
              </div>
            )}

            {/* Availability */}
            <div className="flex items-center space-x-2">
              <div
                className={`w-3 h-3 rounded-full ${
                  product.inStock ? 'bg-green-500' : 'bg-red-500'
                }`}
              ></div>
              <span className="text-gray-700">
                {product.inStock ? 'Na stanju' : 'Nije dostupno'}
              </span>
            </div>

            {/* CTA Buttons */}
            <div className="flex flex-col sm:flex-row gap-4">
              <Link
                href={`/kontakt?product=${product.slug}`}
                className="btn bg-primary-600 text-white hover:bg-primary-700 text-center text-lg px-8 py-4 flex-1"
              >
                Pošaljite upit
              </Link>
              {product.externalLink && (
                <a
                  href={product.externalLink}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="btn border-2 border-gray-300 text-gray-700 hover:border-primary-600 hover:text-primary-600 text-center text-lg px-8 py-4 flex-1"
                >
                  Pogledaj na sajtu proizvođača
                </a>
              )}
            </div>
          </div>
        </div>

        {/* Description & Specs */}
        <div className="mt-16 grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Description */}
          <div className="lg:col-span-2 bg-white rounded-2xl shadow-lg p-8">
            <h2 className="text-2xl font-bold text-gray-900 mb-6">Opis proizvoda</h2>
            <div className="prose prose-lg max-w-none text-gray-700">
              <p>{product.description}</p>
            </div>
          </div>

          {/* Specifications */}
          {product.specs && product.specs.length > 0 && (
            <div className="bg-white rounded-2xl shadow-lg p-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-6">Specifikacije</h2>
              <dl className="space-y-4">
                {product.specs.map((spec) => (
                  <div key={spec.key} className="border-b border-gray-200 pb-4 last:border-0">
                    <dt className="text-sm font-medium text-gray-500 mb-1">
                      {spec.label}
                    </dt>
                    <dd className="text-base font-semibold text-gray-900">
                      {spec.value}
                    </dd>
                  </div>
                ))}
              </dl>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
