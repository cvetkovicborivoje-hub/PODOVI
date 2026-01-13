interface EcoFeaturesProps {
  features: string[];
  underfloorHeating?: boolean;
}

export default function EcoFeatures({ features, underfloorHeating }: EcoFeaturesProps) {
  if ((!features || features.length === 0) && !underfloorHeating) return null;

  const allFeatures = [...features];
  if (underfloorHeating) {
    allFeatures.push("Kompatibilno sa podnim grejanjem");
  }

  return (
    <div className="bg-gradient-to-br from-green-50 to-emerald-50 border-2 border-green-200 rounded-2xl p-6">
      <div className="flex items-center gap-2 mb-4">
        <div className="w-10 h-10 bg-green-500 rounded-full flex items-center justify-center">
          <svg className="w-6 h-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
          </svg>
        </div>
        <h3 className="text-xl font-bold text-gray-900">Ekološke karakteristike</h3>
      </div>
      
      <ul className="space-y-3">
        {allFeatures.map((feature, index) => (
          <li key={index} className="flex items-start gap-3">
            <svg className="w-5 h-5 text-green-600 mt-0.5 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <span className="text-gray-700 font-medium">{feature}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}
