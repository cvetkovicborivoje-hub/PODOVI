import { categoryRepository } from '@/lib/repositories/category-repository';
import CategoryCard from '@/components/CategoryCard';

export const metadata = {
  title: 'Kategorije - Podovi',
  description: 'Pregledajte sve kategorije podnih obloga. Laminat, vinil, parket, terasni podovi i ostale podne obloge.',
};

export default async function CategoriesPage() {
  const categories = await categoryRepository.findAll();

  return (
    <div className="container py-12">
      <div className="mb-12">
        <h1 className="text-4xl font-bold text-gray-900 mb-4">
          Vrste podova
        </h1>
        <p className="text-lg text-gray-600">
          Izaberite kategoriju koja najbolje odgovara vašim potrebama i pregledajte našu ponudu
        </p>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
        {categories.map((category) => (
          <CategoryCard key={category.id} category={category} />
        ))}
      </div>
    </div>
  );
}
