import { NextRequest, NextResponse } from 'next/server';
import { mailer } from '@/lib/mailer/mailer';
import { ContactFormData } from '@/types';

export async function POST(request: NextRequest) {
  try {
    const data: ContactFormData = await request.json();

    // Validate required fields
    if (!data.fullName || !data.email || !data.phone || !data.subject || !data.message) {
      return NextResponse.json(
        { error: 'Sva polja moraju biti popunjena' },
        { status: 400 }
      );
    }

    // Send email
    await mailer.sendContactEmail(data);

    return NextResponse.json(
      { 
        success: true,
        message: 'Poruka je uspešno poslata' 
      },
      { status: 200 }
    );
  } catch (error) {
    console.error('Error sending contact form:', error);
    return NextResponse.json(
      { error: 'Greška pri slanju poruke. Molimo pokušajte ponovo.' },
      { status: 500 }
    );
  }
}
