interface PerspectiveBoxProps {
  side: 'left' | 'right';
  content: string;
}

export default function PerspectiveBox({ side, content }: PerspectiveBoxProps) {
  const isLeft = side === 'left';

  return (
    <div className={`p-5 rounded-lg ${isLeft ? 'perspective-left' : 'perspective-right'}`}>
      <div className="flex items-center gap-2 mb-3">
        <span className={`text-lg ${isLeft ? 'text-[#DC2626]' : 'text-[#2563EB]'}`}>
          {isLeft ? '🔴' : '🔵'}
        </span>
        <h4 className={`font-semibold text-sm uppercase tracking-wide ${
          isLeft ? 'text-[#DC2626]' : 'text-[#2563EB]'
        }`}>
          {isLeft ? 'O que dizem fontes de esquerda' : 'O que dizem fontes de direita'}
        </h4>
      </div>
      <p className="text-gray-700 text-sm leading-relaxed font-serif">
        {content || 'Não há cobertura disponível nesta perspectiva.'}
      </p>
    </div>
  );
}
