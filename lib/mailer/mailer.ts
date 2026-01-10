import { Inquiry, ContactFormData } from '@/types';

export interface IMailer {
  sendInquiryEmail(inquiry: Inquiry): Promise<void>;
  sendContactEmail(contact: ContactFormData): Promise<void>;
  sendInquiryConfirmation(inquiry: Inquiry): Promise<void>;
}

export class MockMailer implements IMailer {
  async sendInquiryEmail(inquiry: Inquiry): Promise<void> {
    console.log('📧 Email poslat adminu:');
    console.log('---');
    console.log(`Od: ${inquiry.fullName} (${inquiry.email})`);
    console.log(`Telefon: ${inquiry.phone}`);
    console.log(`Grad: ${inquiry.city}`);
    console.log(`Proizvod: ${inquiry.productName} (${inquiry.productSku})`);
    console.log(`Link: ${inquiry.productUrl}`);
    if (inquiry.quantityM2) {
      console.log(`Količina: ${inquiry.quantityM2} m²`);
    }
    console.log(`Poruka: ${inquiry.message}`);
    console.log(`Preferirani kontakt: ${inquiry.preferredContact.join(', ')}`);
    console.log('---');
  }

  async sendInquiryConfirmation(inquiry: Inquiry): Promise<void> {
    console.log('📧 Potvrda poslata klijentu:');
    console.log(`Prima: ${inquiry.email}`);
    console.log('Sadržaj: Hvala na Vašem upitu. Kontaktiraćemo Vas uskoro.');
    console.log('---');
  }

  async sendContactEmail(contact: ContactFormData): Promise<void> {
    console.log('📧 Kontakt forma poslata:');
    console.log('---');
    console.log(`Od: ${contact.fullName} (${contact.email})`);
    console.log(`Telefon: ${contact.phone}`);
    console.log(`Tema: ${contact.subject}`);
    console.log(`Poruka: ${contact.message}`);
    console.log('---');
  }
}

export const mailer = new MockMailer();
