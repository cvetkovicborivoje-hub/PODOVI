import { notFound } from 'next/navigation';
import Link from 'next/link';
import { promises as fs } from 'fs';
import path from 'path';

interface Props {
  params: { collection: string };
}

export default async function DocumentsPage({ params }: Props) {
  const collectionName = params.collection;
  const documentsPath = path.join(process.cwd(), 'public', 'documents', 'lvt', collectionName);
  
  let files: string[] = [];
  
  try {
    files = await fs.readdir(documentsPath);
    // Filter only PDF files
    files = files.filter(file => file.toLowerCase().endsWith('.pdf'));
  } catch (error) {
    notFound();
  }

  if (files.length === 0) {
    notFound();
  }

  // Format collection name for display
  const displayName = collectionName
    .split('-')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ');

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b">
        <div className="container py-6">
          <div className="flex items-center space-x-2 text-sm mb-4">
            <Link href="/" className="text-gray-500 hover:text-primary-600">
              Početna
            </Link>
            <span className="text-gray-400">/</span>
            <Link href="/kategorije/lvt" className="text-gray-500 hover:text-primary-600">
              LVT
            </Link>
            <span className="text-gray-400">/</span>
            <span className="text-gray-900 font-medium">Dokumentacija</span>
          </div>
          <h1 className="text-4xl font-bold text-gray-900">
            Dokumentacija - {displayName}
          </h1>
          <p className="text-lg text-gray-600 mt-2">
            Kompletna tehnička dokumentacija, uputstva i sertifikati
          </p>
        </div>
      </div>

      {/* Documents Grid */}
      <div className="container py-12">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {files.map((file) => {
            const fileName = file.replace(/^\d+\s*-\s*/, '').replace('.pdf', '');
            const filePath = `/documents/lvt/${collectionName}/${file}`;
            
            return (
              <a
                key={file}
                href={filePath}
                target="_blank"
                rel="noopener noreferrer"
                className="group bg-white rounded-xl shadow-md hover:shadow-xl transition-all duration-300 p-6 border-2 border-transparent hover:border-primary-600"
              >
                <div className="flex items-start gap-4">
                  {/* PDF Icon */}
                  <div className="flex-shrink-0 w-14 h-14 bg-red-100 rounded-lg flex items-center justify-center group-hover:bg-primary-600 transition-colors">
                    <svg className="w-8 h-8 text-red-600 group-hover:text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
                    </svg>
                  </div>
                  
                  {/* File Info */}
                  <div className="flex-1 min-w-0">
                    <h3 className="font-semibold text-gray-900 group-hover:text-primary-600 mb-1 line-clamp-2">
                      {fileName}
                    </h3>
                    <p className="text-sm text-gray-500">PDF dokument</p>
                  </div>
                  
                  {/* Download Icon */}
                  <div className="flex-shrink-0">
                    <svg className="w-6 h-6 text-gray-400 group-hover:text-primary-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                    </svg>
                  </div>
                </div>
              </a>
            );
          })}
        </div>

        {/* Back Button */}
        <div className="mt-12 text-center">
          <Link
            href={`/proizvodi/gerflor-${collectionName}`}
            className="inline-flex items-center gap-2 text-primary-600 hover:text-primary-700 font-semibold"
          >
            <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
            </svg>
            Nazad na proizvod
          </Link>
        </div>
      </div>
    </div>
  );
}
