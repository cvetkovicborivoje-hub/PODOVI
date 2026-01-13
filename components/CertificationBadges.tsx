interface CertificationBadgesProps {
  certifications: string[];
}

const certIcons: Record<string, string> = {
  "FloorScore": "🌿",
  "Indoor Air Comfort Gold": "🏅",
  "M1": "✓",
  "A+": "A+",
  "CE": "CE",
  "REACH": "🇪🇺",
  "EPD": "♻️",
  "ISO 9001": "ISO",
  "ISO 14001": "🌍"
};

const certColors: Record<string, string> = {
  "FloorScore": "bg-green-100 text-green-700 border-green-300",
  "Indoor Air Comfort Gold": "bg-yellow-100 text-yellow-700 border-yellow-300",
  "M1": "bg-blue-100 text-blue-700 border-blue-300",
  "A+": "bg-emerald-100 text-emerald-700 border-emerald-300",
  "CE": "bg-indigo-100 text-indigo-700 border-indigo-300",
  "REACH": "bg-blue-100 text-blue-700 border-blue-300",
  "EPD": "bg-green-100 text-green-700 border-green-300",
  "ISO 9001": "bg-gray-100 text-gray-700 border-gray-300",
  "ISO 14001": "bg-teal-100 text-teal-700 border-teal-300"
};

export default function CertificationBadges({ certifications }: CertificationBadgesProps) {
  if (!certifications || certifications.length === 0) return null;

  return (
    <div className="flex flex-wrap gap-2">
      {certifications.map((cert) => (
        <span
          key={cert}
          className={`inline-flex items-center gap-1 px-3 py-1.5 rounded-full text-xs font-semibold border ${
            certColors[cert] || "bg-gray-100 text-gray-700 border-gray-300"
          }`}
          title={cert}
        >
          <span className="text-sm">{certIcons[cert] || "✓"}</span>
          {cert}
        </span>
      ))}
    </div>
  );
}
