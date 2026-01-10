"use client";

import Link from 'next/link';
import { useState } from 'react';

export default function Header() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  return (
    <header className="bg-white shadow-sm sticky top-0 z-50">
      <nav className="container py-4">
        <div className="flex items-center justify-between">
          {/* Logo - ENHANCED VERSION */}
          <Link href="/" className="flex items-center gap-3 group">
            {/* Icon/Square */}
            <div className="w-10 h-10 bg-gradient-to-br from-primary-600 to-primary-700 rounded-lg flex items-center justify-center 
                            shadow-md group-hover:shadow-lg transition-shadow duration-300">
              <svg className="w-6 h-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} 
                      d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
              </svg>
            </div>
            
            {/* Text */}
            <div className="relative">
              <div className="text-2xl md:text-3xl font-bold lowercase tracking-tight">
                <span className="text-gray-900 relative inline-block">
                  podovi
                  <div className="absolute -bottom-1 left-0 w-full h-1 bg-gradient-to-r from-primary-600 via-primary-500 to-primary-600 
                                  transform origin-left transition-transform duration-300 group-hover:scale-x-105 rounded-full"></div>
                </span>
              </div>
              {/* Subtle shadow/glow effect */}
              <div className="absolute -bottom-0.5 left-0 w-full h-1 bg-primary-600/20 blur-sm rounded-full"></div>
            </div>
          </Link>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-8">
            <Link href="/" className="text-gray-700 hover:text-primary-600 transition font-medium">
              Početna
            </Link>
            <Link href="/kategorije" className="text-gray-700 hover:text-primary-600 transition font-medium">
              Kategorije
            </Link>
            <Link href="/brendovi" className="text-gray-700 hover:text-primary-600 transition font-medium">
              Brendovi
            </Link>
            <Link href="/kontakt" className="text-gray-700 hover:text-primary-600 transition font-medium">
              Kontakt
            </Link>
            <Link href="/upiti" className="btn-primary shadow-md hover:shadow-lg transition-shadow">
              Pošalji upit
            </Link>
          </div>

          {/* Mobile menu button */}
          <button
            type="button"
            className="md:hidden p-2 text-gray-700 hover:bg-gray-100 rounded-lg transition"
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
          <div className="md:hidden mt-4 pb-4 space-y-3 animate-fadeIn">
            <Link href="/" className="block text-gray-700 hover:text-primary-600 transition font-medium py-2 px-3 hover:bg-gray-50 rounded-lg">
              Početna
            </Link>
            <Link href="/kategorije" className="block text-gray-700 hover:text-primary-600 transition font-medium py-2 px-3 hover:bg-gray-50 rounded-lg">
              Kategorije
            </Link>
            <Link href="/brendovi" className="block text-gray-700 hover:text-primary-600 transition font-medium py-2 px-3 hover:bg-gray-50 rounded-lg">
              Brendovi
            </Link>
            <Link href="/kontakt" className="block text-gray-700 hover:text-primary-600 transition font-medium py-2 px-3 hover:bg-gray-50 rounded-lg">
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
