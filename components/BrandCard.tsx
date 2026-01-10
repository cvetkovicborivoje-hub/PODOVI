'use client';

import Link from 'next/link';
import { Brand } from '@/types';

interface BrandCardProps {
  brand: Brand;
}

export default function BrandCard({ brand }: BrandCardProps) {
  return (
    <Link href={`/brendovi/${brand.slug}`}>
      <div className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-xl transition-all duration-300 hover:scale-105 cursor-pointer h-full">
        <div className="h-48 bg-gradient-to-br from-gray-50 to-gray-100 flex items-center justify-center p-8">
          <div className="text-center">
            <div className="w-24 h-24 bg-white rounded-full mx-auto mb-4 flex items-center justify-center shadow-md">
              <span className="text-3xl font-bold text-gray-400">
                {brand.name.charAt(0)}
              </span>
            </div>
            <h2 className="text-2xl font-bold text-gray-900">
              {brand.name}
            </h2>
          </div>
        </div>
        <div className="p-6">
          <p className="text-gray-600 mb-4">
            {brand.description}
          </p>
          {brand.countryOfOrigin && (
            <p className="text-sm text-gray-500 mb-4">
              <span className="font-medium">Zemlja porekla:</span> {brand.countryOfOrigin}
            </p>
          )}
          <div className="flex gap-3 items-center">
            <span className="text-sm text-primary-600 font-medium">
              Pogledaj proizvode →
            </span>
            {brand.website && (
              <a
                href={brand.website}
                target="_blank"
                rel="noopener noreferrer"
                className="text-sm text-gray-500 hover:text-gray-700 font-medium ml-auto"
                onClick={(e) => e.stopPropagation()}
              >
                Sajt ↗
              </a>
            )}
          </div>
        </div>
      </div>
    </Link>
  );
}
