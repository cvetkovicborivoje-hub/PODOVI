import { Inquiry } from '@/types';

export interface IInquiryRepository {
  create(inquiry: Omit<Inquiry, 'id' | 'createdAt'>): Promise<Inquiry>;
  findById(id: string): Promise<Inquiry | null>;
  findAll(): Promise<Inquiry[]>;
  updateStatus(id: string, status: Inquiry['status']): Promise<Inquiry>;
}

// Mock implementation for now
export class MockInquiryRepository implements IInquiryRepository {
  private inquiries: Inquiry[] = [];

  async create(data: Omit<Inquiry, 'id' | 'createdAt'>): Promise<Inquiry> {
    const inquiry: Inquiry = {
      ...data,
      id: `INQ-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
      createdAt: new Date(),
    };
    
    this.inquiries.push(inquiry);
    console.log('✅ Nova upit sačuvan:', inquiry);
    return inquiry;
  }

  async findById(id: string): Promise<Inquiry | null> {
    return this.inquiries.find(i => i.id === id) || null;
  }

  async findAll(): Promise<Inquiry[]> {
    return this.inquiries;
  }

  async updateStatus(id: string, status: Inquiry['status']): Promise<Inquiry> {
    const inquiry = await this.findById(id);
    if (!inquiry) {
      throw new Error(`Upit sa ID ${id} nije pronađen`);
    }
    inquiry.status = status;
    return inquiry;
  }
}

// Singleton instance
export const inquiryRepository = new MockInquiryRepository();
