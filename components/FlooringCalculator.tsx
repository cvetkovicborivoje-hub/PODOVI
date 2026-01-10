"use client";

import { useState } from 'react';

interface FlooringCalculatorProps {
  productName: string;
  coveragePerPackage?: number; // m² po pakovanju
  onSendInquiry?: (area: number, packagesNeeded: number) => void;
}

export default function FlooringCalculator({ 
  productName, 
  coveragePerPackage = 2.25,
  onSendInquiry 
}: FlooringCalculatorProps) {
  const [area, setArea] = useState<string>('');
  const [calculated, setCalculated] = useState(false);

  const WASTE_PERCENTAGE = 5; // 5% otpada

  const handleCalculate = () => {
    if (area && parseFloat(area) > 0) {
      setCalculated(true);
    }
  };

  const areaNumber = parseFloat(area) || 0;
  const wasteAmount = areaNumber * (WASTE_PERCENTAGE / 100);
  const totalAreaWithWaste = areaNumber + wasteAmount;
  const packagesNeeded = Math.ceil(totalAreaWithWaste / coveragePerPackage);
  const totalCoverage = packagesNeeded * coveragePerPackage;

  return (
    <div className="bg-gradient-to-br from-primary-50 to-white border-2 border-primary-100 rounded-lg p-6 shadow-md">
      <div className="flex items-start mb-4">
        <div className="flex-shrink-0 w-10 h-10 bg-primary-600 text-white rounded-full flex items-center justify-center mr-3">
          <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
          </svg>
        </div>
        <div>
          <h3 className="text-xl font-bold text-gray-900">
            Kalkulator potrebne količine
          </h3>
          <p className="text-sm text-gray-600 mt-1">
            Izračunajte koliko paketa vam je potrebno za vaš prostor
          </p>
        </div>
      </div>

      <div className="bg-white rounded-lg p-4 mb-4">
        <label htmlFor="area-input" className="label">
          Površina prostora (m²) <span className="text-red-500">*</span>
        </label>
        <div className="flex gap-3">
          <input
            id="area-input"
            type="number"
            min="0"
            step="0.01"
            value={area}
            onChange={(e) => {
              setArea(e.target.value);
              setCalculated(false);
            }}
            onKeyPress={(e) => e.key === 'Enter' && handleCalculate()}
            placeholder="Unesite površinu u m²..."
            className="input flex-1"
          />
          <button
            onClick={handleCalculate}
            disabled={!area || parseFloat(area) <= 0}
            className="btn-primary px-6"
          >
            Izračunaj
          </button>
        </div>
        <p className="text-xs text-gray-500 mt-2">
          💡 Jedno pakovanje pokriva <strong>{coveragePerPackage} m²</strong>
        </p>
      </div>

      {calculated && areaNumber > 0 && (
        <div className="space-y-4 animate-fadeIn">
          {/* Rezultati */}
          <div className="bg-white rounded-lg p-4 border-l-4 border-primary-600">
            <h4 className="font-semibold text-gray-900 mb-3 flex items-center">
              <svg className="w-5 h-5 text-primary-600 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
              </svg>
              Rezultat proračuna:
            </h4>
            
            <div className="space-y-2.5">
              <div className="flex justify-between items-center pb-2 border-b border-gray-100">
                <span className="text-sm text-gray-600">Vaša površina:</span>
                <span className="font-semibold text-gray-900">{areaNumber.toFixed(2)} m²</span>
              </div>
              
              <div className="flex justify-between items-center pb-2 border-b border-gray-100">
                <span className="text-sm text-gray-600">
                  Otpad ({WASTE_PERCENTAGE}%):
                  <span className="ml-1 text-xs text-primary-600 font-medium">
                    ⚡ Manje od standardnih 10%
                  </span>
                </span>
                <span className="font-semibold text-primary-600">+{wasteAmount.toFixed(2)} m²</span>
              </div>
              
              <div className="flex justify-between items-center pb-2 border-b-2 border-primary-200">
                <span className="text-sm font-medium text-gray-700">Ukupno potrebno:</span>
                <span className="font-bold text-lg text-gray-900">{totalAreaWithWaste.toFixed(2)} m²</span>
              </div>
              
              <div className="bg-primary-50 rounded-lg p-3 mt-3">
                <div className="flex justify-between items-center">
                  <span className="text-base font-semibold text-gray-900">
                    Broj paketa:
                  </span>
                  <div className="text-right">
                    <span className="text-3xl font-bold text-primary-600">
                      {packagesNeeded}
                    </span>
                    <span className="text-sm text-gray-600 ml-1">kom</span>
                  </div>
                </div>
                <p className="text-xs text-gray-600 mt-2">
                  Ukupna pokrivenost: {totalCoverage.toFixed(2)} m²
                </p>
              </div>
            </div>
          </div>

          {/* Info box */}
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-3">
            <div className="flex items-start">
              <svg className="w-5 h-5 text-blue-600 mr-2 flex-shrink-0 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <p className="text-xs text-blue-800">
                <strong>Preporuka:</strong> Uračunali smo samo <strong>5% otpada</strong> (umesto standardnih 10%), što znači 
                <strong> uštedu za vas</strong>. Za prostorije sa dosta uglova ili dijagonalno postavljanje, razmotrite dodavanje još 1-2 paketa.
              </p>
            </div>
          </div>

          {/* CTA dugme */}
          {onSendInquiry && (
            <button
              onClick={() => onSendInquiry(areaNumber, packagesNeeded)}
              className="btn-primary w-full text-base py-3 shadow-lg hover:shadow-xl transition-shadow"
            >
              <svg className="w-5 h-5 mr-2 inline-block" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
              </svg>
              Pošalji upit za {packagesNeeded} paketa
            </button>
          )}
        </div>
      )}
    </div>
  );
}
