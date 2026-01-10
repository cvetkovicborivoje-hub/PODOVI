import { Category } from '@/types';
import { categories as mockCategories } from '@/lib/data/mock-data';

export interface ICategoryRepository {
  findAll(): Promise<Category[]>;
  findBySlug(slug: string): Promise<Category | null>;
  findById(id: string): Promise<Category | null>;
}

export class MockCategoryRepository implements ICategoryRepository {
  private categories: Category[] = mockCategories;

  async findAll(): Promise<Category[]> {
    return [...this.categories].sort((a, b) => a.order - b.order);
  }

  async findBySlug(slug: string): Promise<Category | null> {
    return this.categories.find(c => c.slug === slug) || null;
  }

  async findById(id: string): Promise<Category | null> {
    return this.categories.find(c => c.id === id) || null;
  }
}

export const categoryRepository = new MockCategoryRepository();
