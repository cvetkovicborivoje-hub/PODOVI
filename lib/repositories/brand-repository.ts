import { Brand } from '@/types';
import { brands as mockBrands } from '@/lib/data/mock-data';

export interface IBrandRepository {
  findAll(): Promise<Brand[]>;
  findBySlug(slug: string): Promise<Brand | null>;
  findById(id: string): Promise<Brand | null>;
}

export class MockBrandRepository implements IBrandRepository {
  private brands: Brand[] = mockBrands;

  async findAll(): Promise<Brand[]> {
    return [...this.brands];
  }

  async findBySlug(slug: string): Promise<Brand | null> {
    return this.brands.find(b => b.slug === slug) || null;
  }

  async findById(id: string): Promise<Brand | null> {
    return this.brands.find(b => b.id === id) || null;
  }
}

export const brandRepository = new MockBrandRepository();

// Helper functions for easier imports
export async function getBrandBySlug(slug: string): Promise<Brand | null> {
  return brandRepository.findBySlug(slug);
}
