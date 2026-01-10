import Link from 'next/link';
import { productRepository } from '@/lib/repositories/product-repository';
import { categoryRepository } from '@/lib/repositories/category-repository';
import ProductCard from '@/components/ProductCard';
import CategoryCard from '@/components/CategoryCard';

export const metadata = {
  title: 'Podovi - Katalog podnih obloga | Početna',
  description: 'Pronađite savršen pod za vaš prostor. Laminat, vinil, parket - najkvalitetnije podne obloge od vodećih svetskih brendova.',
};

export default async function HomePage() {
  const featuredProducts = await productRepository.findFeatured();
  const categories = await categoryRepository.findAll();

  return (
    <div>
      {/* Hero Section */}
      <section className="bg-gradient-to-r from-gray-900 to-gray-800 text-white">
        <div className="container py-20">
          <div className="max-w-3xl">
            <h1 className="text-4xl md:text-5xl font-bold mb-6">
              Pronađite savršen pod za vaš prostor
            </h1>
            <p className="text-xl mb-8 text-gray-300">
              Širok izbor laminata, vinila, parketa i drugih podnih obloga od vodećih evropskih brendova. 
              Kvalitet, izdržljivost i stil za svaki budžet.
            </p>
            <div className="flex flex-col sm:flex-row gap-4">
              <Link href="/kategorije" className="btn bg-primary-600 text-white hover:bg-primary-700 text-center">
                Pregledaj proizvode
              </Link>
              <Link href="/kontakt" className="btn border-2 border-white text-white hover:bg-white hover:text-gray-900 text-center">
                Kontaktirajte nas
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Categories Section */}
      <section className="py-16 bg-white">
        <div className="container">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">
              Kategorije proizvoda
            </h2>
            <p className="text-lg text-gray-600">
              Izaberite kategoriju koja najbolje odgovara vašim potrebama
            </p>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-6">
            {categories.map((category) => (
              <CategoryCard key={category.id} category={category} />
            ))}
          </div>
        </div>
      </section>

      {/* Featured Products */}
      <section className="py-16 bg-gray-50">
        <div className="container">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">
              Izdvojeni proizvodi
            </h2>
            <p className="text-lg text-gray-600">
              Najpopularniji izbor naših kupaca
            </p>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8">
            {featuredProducts.map((product) => (
              <ProductCard key={product.id} product={product} />
            ))}
          </div>
          <div className="text-center mt-12">
            <Link href="/kategorije" className="btn-primary text-lg px-8 py-3">
              Pogledaj sve proizvode
            </Link>
          </div>
        </div>
      </section>

      {/* Why Choose Us */}
      <section className="py-16 bg-white">
        <div className="container">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">
              Zašto izabrati nas?
            </h2>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="text-center">
              <div className="inline-flex items-center justify-center w-16 h-16 bg-primary-100 text-primary-600 rounded-full mb-4">
                <svg className="w-8 h-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold mb-3">Proveren kvalitet</h3>
              <p className="text-gray-600">
                Radimo samo sa renomiranim evropskim proizvođačima sa dugogodišnjom tradicijom
              </p>
            </div>
            <div className="text-center">
              <div className="inline-flex items-center justify-center w-16 h-16 bg-primary-100 text-primary-600 rounded-full mb-4">
                <svg className="w-8 h-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold mb-3">Konkurentne cene</h3>
              <p className="text-gray-600">
                Najbolji odnos cene i kvaliteta zahvaljujući direktnoj saradnji sa proizvođačima
              </p>
            </div>
            <div className="text-center">
              <div className="inline-flex items-center justify-center w-16 h-16 bg-primary-100 text-primary-600 rounded-full mb-4">
                <svg className="w-8 h-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M18.364 5.636l-3.536 3.536m0 5.656l3.536 3.536M9.172 9.172L5.636 5.636m3.536 9.192l-3.536 3.536M21 12a9 9 0 11-18 0 9 9 0 0118 0zm-5 0a4 4 0 11-8 0 4 4 0 018 0z" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold mb-3">Stručna podrška</h3>
              <p className="text-gray-600">
                Naš tim stručnjaka će vam pomoći da izaberete idealno rešenje za vaš prostor
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-16 bg-gray-900 text-white">
        <div className="container text-center">
          <h2 className="text-3xl font-bold mb-4">
            Spremni da transformišete vaš prostor?
          </h2>
          <p className="text-xl mb-8 text-gray-300">
            Pošaljite nam upit i naš tim će vam se javiti u najkraćem roku
          </p>
          <Link href="/upiti" className="btn bg-primary-600 text-white hover:bg-primary-700 text-lg px-8 py-3">
            Pošalji upit
          </Link>
        </div>
      </section>
    </div>
  );
}
