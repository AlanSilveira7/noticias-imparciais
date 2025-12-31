/*
 * HOROSCOPE WIDGET COMPONENT - Clone Globo.com
 * Design: Fidelidade Editorial Clássica
 * 
 * Widget de horóscopo:
 * - Seletor de signos
 * - Previsão do dia
 */

import { useState } from 'react';

const signs = [
  { name: 'Áries', emoji: '♈', dates: '21/03 a 19/04' },
  { name: 'Touro', emoji: '♉', dates: '20/04 a 20/05' },
  { name: 'Gêmeos', emoji: '♊', dates: '21/05 a 20/06' },
  { name: 'Câncer', emoji: '♋', dates: '21/06 a 22/07' },
  { name: 'Leão', emoji: '♌', dates: '23/07 a 22/08' },
  { name: 'Virgem', emoji: '♍', dates: '23/08 a 22/09' },
  { name: 'Libra', emoji: '♎', dates: '23/09 a 22/10' },
  { name: 'Escorpião', emoji: '♏', dates: '23/10 a 21/11' },
  { name: 'Sagitário', emoji: '♐', dates: '22/11 a 21/12' },
  { name: 'Capricórnio', emoji: '♑', dates: '22/12 a 19/01' },
  { name: 'Aquário', emoji: '♒', dates: '20/01 a 18/02' },
  { name: 'Peixes', emoji: '♓', dates: '19/02 a 20/03' },
];

const predictions: Record<string, string> = {
  'Áries': 'O céu indica que sua habilidade de administrar a vida prática pode se destacar hoje, com Lua, Sol, Vênus e Marte alinhados. É um bom momento para sair do óbvio e confiar mais na sua ousadia.',
  'Touro': 'Momento favorável para questões financeiras e investimentos. A estabilidade que você tanto busca pode estar mais próxima do que imagina.',
  'Gêmeos': 'Sua comunicação está em alta. Aproveite para resolver pendências e fazer novos contatos profissionais.',
  'Câncer': 'Dia propício para cuidar da família e do lar. Emoções intensas podem surgir, mas trazem crescimento.',
  'Leão': 'Sua criatividade está em destaque. Projetos artísticos e expressão pessoal são favorecidos.',
  'Virgem': 'Organize suas prioridades e foque no que realmente importa. Detalhes fazem a diferença.',
  'Libra': 'Relacionamentos pedem atenção especial. Busque equilíbrio entre dar e receber.',
  'Escorpião': 'Transformações profundas estão em curso. Confie no processo de renovação.',
  'Sagitário': 'Novos horizontes se abrem. Momento ideal para planejar viagens e estudos.',
  'Capricórnio': 'Foco na carreira traz resultados. Sua disciplina será recompensada.',
  'Aquário': 'Inovação e originalidade são suas aliadas. Não tenha medo de ser diferente.',
  'Peixes': 'Intuição aguçada. Confie nos seus sonhos e na sua sensibilidade.',
};

export default function HoroscopeWidget() {
  const [selectedSign, setSelectedSign] = useState(signs[0]);

  return (
    <div>
      <a 
        href="#" 
        className="globo-section-title text-blue-600 hover:underline inline-block mb-3"
      >
        Horóscopo
      </a>
      
      {/* Sign selector */}
      <div className="flex flex-wrap gap-1 mb-4">
        {signs.map((sign) => (
          <button
            key={sign.name}
            onClick={() => setSelectedSign(sign)}
            className={`w-8 h-8 rounded-full text-lg flex items-center justify-center transition-all ${
              selectedSign.name === sign.name
                ? 'bg-orange-500 text-white scale-110'
                : 'bg-gray-100 hover:bg-gray-200'
            }`}
            title={sign.name}
          >
            {sign.emoji}
          </button>
        ))}
      </div>

      {/* Selected sign prediction */}
      <div className="bg-gradient-to-br from-orange-50 to-pink-50 rounded-lg p-4">
        <div className="flex items-center gap-3 mb-3">
          <span className="text-3xl">{selectedSign.emoji}</span>
          <div>
            <h4 className="font-bold text-gray-900">{selectedSign.name}</h4>
            <p className="text-xs text-gray-500">{selectedSign.dates}</p>
          </div>
        </div>
        <p className="text-sm text-gray-700 leading-relaxed">
          {predictions[selectedSign.name]}
        </p>
      </div>

      <a 
        href="#"
        className="block mt-3 text-sm text-orange-600 font-semibold hover:underline"
      >
        Previsão completa →
      </a>
    </div>
  );
}
