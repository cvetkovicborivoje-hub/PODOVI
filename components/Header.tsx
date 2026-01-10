"use client";

import Link from 'next/link';
import { useState } from 'react';

export default function Header() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  return (
    <header className="bg-white shadow-sm sticky top-0 z-50">
      <nav className="container py-4">
        <div className="flex items-center justify-between">
          {/* Logo */}
          <Link href="/" className="flex items-center">
            <div className="text-2xl font-bold lowercase">
              <span className="text-gray-900">podovi</span>
              <div className="h-1 bg-primary-600 w-full mt-0.5"></div>
            </div>
          </Link>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-8">
            <Link href="/" className="text-gray-700 hover:text-primary-600 transition">
              Početna
            </Link>
            <Link href="/kategorije" className="text-gray-700 hover:text-primary-600 transition">
              Kategorije
            </Link>
            <Link href="/brendovi" className="text-gray-700 hover:text-primary-600 transition">
              Brendovi
            </Link>
            <Link href="/kontakt" className="text-gray-700 hover:text-primary-600 transition">
              Kontakt
            </Link>
            <Link href="/upiti" className="btn-primary">
              Pošalji upit
            </Link>
          </div>

          {/* Mobile menu button */}
          <button
            type="button"
            className="md:hidden p-2 text-gray-700"
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
          >
            <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              {mobileMenuOpen ? (
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              ) : (
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              )}
            </svg>
          </button>
        </div>

        {/* Mobile Navigation */}
        {mobileMenuOpen && (
          <div className="md:hidden mt-4 pb-4 space-y-3">
            <Link href="/" className="block text-gray-700 hover:text-primary-600 transition">
              Početna
            </Link>
            <Link href="/kategorije" className="block text-gray-700 hover:text-primary-600 transition">
              Kategorije
            </Link>
            <Link href="/brendovi" className="block text-gray-700 hover:text-primary-600 transition">
              Brendovi
            </Link>
            <Link href="/kontakt" className="block text-gray-700 hover:text-primary-600 transition">
              Kontakt
            </Link>
            <Link href="/upiti" className="block btn-primary text-center">
              Pošalji upit
            </Link>
          </div>
        )}
      </nav>
    </header>
  );
}
