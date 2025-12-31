/*
 * ECONOMY WIDGET COMPONENT - Clone Globo.com
 * Design: Fidelidade Editorial Clássica
 * 
 * Widget de cotações:
 * - Ibovespa
 * - Moedas (Dólar, Euro)
 */

import { TrendingUp, TrendingDown } from 'lucide-react';

interface Quote {
  name: string;
  value: string;
  change: string;
  isPositive: boolean;
}

const quotes: Quote[] = [
  { name: 'Ibovespa', value: '161.511pts', change: '+0.64%', isPositive: true },
  { name: 'Dólar Comercial', value: 'R$ 5,489', change: '-0.32%', isPositive: false },
  { name: 'Euro Comercial', value: 'R$ 6,448', change: '-0.18%', isPositive: false },
];

export default function EconomyWidget() {
  return (
    <div>
      <a 
        href="#" 
        className="globo-section-title text-blue-600 hover:underline inline-block mb-3"
      >
        Economia
      </a>
      
      <div className="space-y-3">
        {quotes.map((quote) => (
          <div 
            key={quote.name}
            className="flex items-center justify-between p-3 bg-gray-50 rounded"
          >
            <div>
              <span className="text-xs text-gray-500 block">{quote.name}</span>
              <span className="font-bold text-gray-900">{quote.value}</span>
            </div>
            <div className={`flex items-center gap-1 ${quote.isPositive ? 'text-green-600' : 'text-red-600'}`}>
              {quote.isPositive ? <TrendingUp size={16} /> : <TrendingDown size={16} />}
              <span className="font-semibold text-sm">{quote.change}</span>
            </div>
          </div>
        ))}
      </div>

      <p className="text-xs text-gray-400 mt-2">
        atualizado 30/12/2025 17h59 · fonte: Valor
      </p>
    </div>
  );
}
