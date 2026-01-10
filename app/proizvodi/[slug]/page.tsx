import { notFound } from 'next/navigation';
import { productRepository } from '@/lib/repositories/product-repository';
import { brandRepository } from '@/lib/repositories/brand-repository';
import { categoryRepository } from '@/lib/repositories/category-repository';
import InquiryButton from '@/components/InquiryButton';
import FlooringCalculator from '@/components/FlooringCalculator';

interface ProductPageProps {
  params: { slug: string };
}

export async function generateMetadata({ params }: ProductPageProps) {
  const product = await productRepository.findBySlug(params.slug);
  
  if (!product) {
    return {
      title: 'Proizvod nije pronađen',
    };
  }

  const brand = await brandRepository.findById(product.brandId);

  return {
    title: `${product.name} - ${brand?.name} - Podovi`,
    description: product.shortDescription,
    openGraph: {
      title: product.name,
      description: product.shortDescription,
      type: 'website',
    },
  };
}

export default async function ProductPage({ params }: ProductPageProps) {
  const product = await productRepository.findBySlug(params.slug);
  
  if (!product) {
    notFound();
  }

  const brand = await brandRepository.findById(product.brandId);
  const category = await categoryRepository.findById(product.categoryId);
  const primaryImage = product.images.find(img => img.isPrimary) || product.images[0];

  // Generate product URL for inquiry form
  const productUrl = `${process.env.NEXT_PUBLIC_BASE_URL || 'http://localhost:3000'}/proizvodi/${product.slug}`;

  return (
    <div className="bg-gray-50 min-h-screen">
      {/* Breadcrumb */}
      <div className="bg-white border-b">
        <div className="container py-4">
          <nav className="text-sm text-gray-600">
            <a href="/" className="hover:text-primary-600">Početna</a>
            <span className="mx-2">/</span>
            <a href="/kategorije" className="hover:text-primary-600">Kategorije</a>
            {category && (
              <>
                <span className="mx-2">/</span>
                <a href={`/kategorije/${category.slug}`} className="hover:text-primary-600">
                  {category.name}
                </a>
              </>
            )}
            <span className="mx-2">/</span>
            <span className="text-gray-900">{product.name}</span>
          </nav>
        </div>
      </div>

      {/* Product Details */}
      <div className="container py-8">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 mb-12">
          {/* Left: Images */}
          <div>
            <div className="bg-white rounded-lg shadow-md overflow-hidden mb-4">
              {primaryImage ? (
                <div className="aspect-square flex items-center justify-center p-8 bg-gray-50">
                  <div className="text-center text-gray-400">
                    <svg className="w-32 h-32 mx-auto mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                    </svg>
                    <p>{primaryImage.alt}</p>
                  </div>
                </div>
              ) : (
                <div className="aspect-square flex items-center justify-center bg-gray-100 text-gray-400">
                  Bez slike
                </div>
              )}
            </div>

            {product.images.length > 1 && (
              <div className="grid grid-cols-4 gap-2">
                {product.images.map((image) => (
                  <div key={image.id} className="bg-white rounded-lg shadow-sm overflow-hidden aspect-square">
                    <div className="w-full h-full flex items-center justify-center bg-gray-50 p-2">
                      <svg className="w-8 h-8 text-gray-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                      </svg>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Right: Product Info */}
          <div>
            <div className="bg-white rounded-lg shadow-md p-8">
              {brand && (
                <p className="text-sm text-gray-500 mb-2 uppercase tracking-wide">
                  {brand.name}
                </p>
              )}
              
              <h1 className="text-3xl font-bold text-gray-900 mb-4">
                {product.name}
              </h1>

              <div className="flex items-center gap-3 mb-6">
                <span className="text-sm text-gray-600">
                  SKU: <span className="font-mono font-medium">{product.sku}</span>
                </span>
                {product.inStock ? (
                  <span className="badge-success">Na stanju</span>
                ) : (
                  <span className="badge-warning">Nema na stanju</span>
                )}
              </div>

              {product.price && (
                <div className="mb-8 pb-8 border-b">
                  <div className="flex items-baseline">
                    <span className="text-4xl font-bold text-primary-600">
                      {product.price.toLocaleString('sr-RS')}
                    </span>
                    <span className="text-xl text-gray-600 ml-2">
                      RSD/{product.priceUnit}
                    </span>
                  </div>
                  <p className="text-sm text-gray-500 mt-2">
                    *Cena je informativna. Za tačnu cenu i dostupnost pošaljite upit.
                  </p>
                </div>
              )}

              <div className="mb-8">
                <p className="text-gray-700 leading-relaxed">
                  {product.shortDescription}
                </p>
              </div>

              {/* Inquiry Button */}
              <InquiryButton 
                product={{
                  id: product.id,
                  name: product.name,
                  sku: product.sku,
                  url: productUrl,
                }}
              />

              <div className="mt-6 grid grid-cols-3 gap-4 text-center text-sm">
                <div className="p-3 bg-gray-50 rounded-lg">
                  <svg className="w-6 h-6 mx-auto mb-1 text-primary-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  <span className="text-gray-600">Kvalitet</span>
                </div>
                <div className="p-3 bg-gray-50 rounded-lg">
                  <svg className="w-6 h-6 mx-auto mb-1 text-primary-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  <span className="text-gray-600">Brza dostava</span>
                </div>
                <div className="p-3 bg-gray-50 rounded-lg">
                  <svg className="w-6 h-6 mx-auto mb-1 text-primary-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M18.364 5.636l-3.536 3.536m0 5.656l3.536 3.536M9.172 9.172L5.636 5.636m3.536 9.192l-3.536 3.536M21 12a9 9 0 11-18 0 9 9 0 0118 0zm-5 0a4 4 0 11-8 0 4 4 0 018 0z" />
                  </svg>
                  <span className="text-gray-600">Podrška</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Calculator and Product Description/Specs */}
        <div className="grid grid-cols-1 gap-8 mb-8">
          {/* Calculator */}
          <FlooringCalculator 
            productName={product.name}
            coveragePerPackage={2.25}
            onSendInquiry={(area, packages) => {
              // This will be handled by the InquiryButton which is already on the page
              // We could enhance this later to pass calculator data to the modal
            }}
          />
        </div>

        {/* Product Description and Specs */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Description */}
          <div className="lg:col-span-2">
            <div className="bg-white rounded-lg shadow-md p-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">Opis proizvoda</h2>
              <div className="prose max-w-none text-gray-700">
                <p>{product.description}</p>
              </div>
            </div>
          </div>

          {/* Specifications */}
          <div>
            <div className="bg-white rounded-lg shadow-md p-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">Specifikacije</h2>
              <dl className="space-y-3">
                {product.specs.map((spec) => (
                  <div key={spec.key} className="border-b border-gray-200 pb-3 last:border-0 last:pb-0">
                    <dt className="text-sm font-medium text-gray-500 mb-1">
                      {spec.label}
                    </dt>
                    <dd className="text-sm text-gray-900 font-medium">
                      {spec.value}
                    </dd>
                  </div>
                ))}
              </dl>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
