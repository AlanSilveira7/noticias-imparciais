import { AlertTriangle } from 'lucide-react';

interface AttentionBoxProps {
  points: string[];
}

export default function AttentionBox({ points }: AttentionBoxProps) {
  if (!points || points.length === 0) return null;

  return (
    <div className="attention-box rounded-lg p-5">
      <div className="flex items-center gap-2 mb-3">
        <AlertTriangle className="w-5 h-5 text-amber-600" />
        <h4 className="font-semibold text-amber-800">Pontos de Atenção</h4>
      </div>
      <ul className="space-y-2">
        {points.map((point, index) => (
          <li key={index} className="text-sm text-amber-900/80 flex items-start gap-2">
            <span className="text-amber-600 mt-1">•</span>
            <span>{point}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}
