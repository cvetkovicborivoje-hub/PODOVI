'use client';

import { useState, useEffect } from 'react';
import Image from 'next/image';

interface Color {
  collection: string;
  collection_name: string;
  code: string;
  name: string;
  full_name: string;
  slug: string;
  image_url: string;
  image_count: number;
}

interface ColorGridProps {
  collectionSlug: string;
}

export default function ColorGrid({ collectionSlug }: ColorGridProps) {
  const [colors, setColors] = useState<Color[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    fetch('/data/lvt_colors_complete.json')
      .then(res => res.json())
      .then(data => {
        // Extract collection name from slug
        // e.g., "gerflor-creation-30" → "creation-30"
        const collectionName = collectionSlug.replace('gerflor-', '');
        
        const filtered = data.colors.filter(
          (c: Color) => c.collection === collectionName || c.collection === collectionSlug
        );
        setColors(filtered);
        setLoading(false);
      })
      .catch(err => {
        console.error('Error loading colors:', err);
        setLoading(false);
      });
  }, [collectionSlug]);

  const filteredColors = colors.filter(color =>
    color.full_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    color.code.includes(searchTerm)
  );

  if (loading) {
    return (
      <div className="text-center py-12">
        <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
        <p className="mt-4 text-gray-600">Učitavam boje...</p>
      </div>
    );
  }

  if (colors.length === 0) {
    return null;
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h2 className="text-2xl font-bold text-gray-900">
            Dostupne boje
          </h2>
          <p className="text-gray-600 mt-1">
            {colors.length} {colors.length === 1 ? 'boja' : colors.length < 5 ? 'boje' : 'boja'}
          </p>
        </div>

        {/* Search */}
        <div className="relative">
          <input
            type="text"
            placeholder="Pretraži po šifri ili nazivu..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full sm:w-64 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
          />
          {searchTerm && (
            <button
              onClick={() => setSearchTerm('')}
              className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600"
            >
              ✕
            </button>
          )}
        </div>
      </div>

      {/* Grid */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4">
        {filteredColors.map((color) => (
          <div
            key={color.slug}
            className="group bg-white rounded-lg shadow-sm hover:shadow-md transition-shadow overflow-hidden border border-gray-200"
          >
            {/* Image */}
            <div className="aspect-square relative overflow-hidden bg-gray-100">
              {color.image_url ? (
                <img
                  src={color.image_url}
                  alt={color.full_name}
                  className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-300"
                />
              ) : (
                <div className="w-full h-full flex items-center justify-center text-gray-400 text-sm">
                  Bez slike
                </div>
              )}
            </div>

            {/* Info */}
            <div className="p-3">
              <p className="font-semibold text-gray-900 text-sm truncate">
                {color.code}
              </p>
              <p className="text-xs text-gray-600 truncate mt-1">
                {color.name}
              </p>
            </div>
          </div>
        ))}
      </div>

      {/* No results */}
      {filteredColors.length === 0 && (
        <div className="text-center py-12">
          <p className="text-gray-600">
            Nije pronađena nijed na boja sa "{searchTerm}"
          </p>
          <button
            onClick={() => setSearchTerm('')}
            className="mt-4 text-primary-600 hover:text-primary-700 font-medium"
          >
            Očisti pretragu
          </button>
        </div>
      )}
    </div>
  );
}
