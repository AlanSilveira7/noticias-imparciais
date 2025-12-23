import { useState, useEffect } from "react";
import { TrendingUp, TrendingDown, Minus, RefreshCw } from "lucide-react";

interface Quote {
  name: string;
  value: string;
  change: string;
  changePercent: string;
  trend: "up" | "down" | "neutral";
}

export default function QuotesWidget() {
  const [quotes, setQuotes] = useState<Quote[]>([
    { name: "Dólar", value: "R$ 6,07", change: "+0,03", changePercent: "+0,50%", trend: "up" },
    { name: "Euro", value: "R$ 6,31", change: "-0,02", changePercent: "-0,32%", trend: "down" },
    { name: "Ibovespa", value: "120.766", change: "+1.234", changePercent: "+1,03%", trend: "up" },
  ]);
  const [loading, setLoading] = useState(false);
  const [lastUpdate, setLastUpdate] = useState(new Date());

  // Simula atualização de cotações
  const refreshQuotes = async () => {
    setLoading(true);
    // Simulação de delay de API
    await new Promise(resolve => setTimeout(resolve, 500));
    
    // Simula pequenas variações nos valores
    setQuotes(prev => prev.map(quote => {
      const variation = (Math.random() - 0.5) * 0.1;
      const currentValue = parseFloat(quote.value.replace(/[^\d,.-]/g, '').replace(',', '.'));
      const newValue = currentValue + variation;
      const changeValue = variation;
      const changePercent = (variation / currentValue) * 100;
      
      return {
        ...quote,
        value: quote.name === "Ibovespa" 
          ? newValue.toFixed(0).replace(/\B(?=(\d{3})+(?!\d))/g, ".")
          : `R$ ${newValue.toFixed(2).replace('.', ',')}`,
        change: changeValue >= 0 ? `+${changeValue.toFixed(2).replace('.', ',')}` : changeValue.toFixed(2).replace('.', ','),
        changePercent: changePercent >= 0 ? `+${changePercent.toFixed(2)}%` : `${changePercent.toFixed(2)}%`,
        trend: changeValue > 0.01 ? "up" : changeValue < -0.01 ? "down" : "neutral"
      };
    }));
    
    setLastUpdate(new Date());
    setLoading(false);
  };

  useEffect(() => {
    // Atualiza a cada 5 minutos
    const interval = setInterval(refreshQuotes, 300000);
    return () => clearInterval(interval);
  }, []);

  const getTrendIcon = (trend: Quote["trend"]) => {
    switch (trend) {
      case "up":
        return <TrendingUp size={14} className="text-green-600" />;
      case "down":
        return <TrendingDown size={14} className="text-red-600" />;
      default:
        return <Minus size={14} className="text-gray-400" />;
    }
  };

  const getTrendColor = (trend: Quote["trend"]) => {
    switch (trend) {
      case "up":
        return "text-green-600";
      case "down":
        return "text-red-600";
      default:
        return "text-gray-500";
    }
  };

  return (
    <div className="bg-white rounded-lg border border-gray-200 p-4">
      <div className="flex items-center justify-between mb-3">
        <h3 className="font-semibold text-gray-900 text-sm">Cotações</h3>
        <button 
          onClick={refreshQuotes}
          disabled={loading}
          className="p-1 text-gray-400 hover:text-gray-600 transition-colors"
          title="Atualizar cotações"
        >
          <RefreshCw size={14} className={loading ? "animate-spin" : ""} />
        </button>
      </div>
      
      <div className="space-y-3">
        {quotes.map((quote) => (
          <div key={quote.name} className="flex items-center justify-between">
            <div>
              <span className="text-xs text-gray-500">{quote.name}</span>
              <div className="font-semibold text-gray-900">{quote.value}</div>
            </div>
            <div className="text-right flex items-center gap-1">
              {getTrendIcon(quote.trend)}
              <span className={`text-xs font-medium ${getTrendColor(quote.trend)}`}>
                {quote.changePercent}
              </span>
            </div>
          </div>
        ))}
      </div>
      
      <div className="mt-3 pt-3 border-t border-gray-100">
        <span className="text-xs text-gray-400">
          Atualizado às {lastUpdate.toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' })}
        </span>
      </div>
    </div>
  );
}
