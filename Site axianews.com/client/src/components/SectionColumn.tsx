/*
 * SECTION COLUMN COMPONENT - Clone Globo.com
 * Design: Fidelidade Editorial Clássica
 * 
 * Layout mobile do Globo.com:
 * - 5 cards iguais
 * - Foto à esquerda (maior)
 * - Título à direita (cor da seção)
 * - Notícia secundária em texto abaixo
 */

interface NewsItem {
  title: string;
  image: string;
  category?: string;
  source: string;
  bullet?: string;
}

interface SectionColumnProps {
  title: string;
  color: string;
  news: NewsItem[];
  moreLink?: string;
  widget?: React.ReactNode;
}

export default function SectionColumn({
  title,
  color,
  news,
  moreLink = '#',
  widget,
}: SectionColumnProps) {
  return (
    <section 
      className="bg-white rounded overflow-hidden"
      style={{ borderTop: `4px solid ${color}` }}
    >
      {/* Section Header */}
      <div className="p-4 pb-2">
        <a 
          href={moreLink}
          className="globo-section-title inline-block hover:underline"
          style={{ color }}
        >
          {title.toUpperCase()}
        </a>
      </div>

      {/* News Cards - All equal layout */}
      <div className="divide-y divide-gray-100">
        {news.map((item, index) => (
          <article key={index} className="p-4">
            {/* Card with image left, text right */}
            <a href="#" className="flex gap-4 group">
              {/* Image - Left side, larger */}
              <div className="flex-shrink-0 w-32 sm:w-40">
                <div className="relative overflow-hidden rounded aspect-[4/3]">
                  <img
                    src={item.image}
                    alt={item.title}
                    className="w-full h-full object-cover transition-transform duration-300 group-hover:scale-105"
                  />
                </div>
              </div>

              {/* Text - Right side */}
              <div className="flex-1 min-w-0">
                <h3 
                  className="text-base sm:text-lg font-bold leading-tight group-hover:opacity-80 transition-opacity"
                  style={{ 
                    fontFamily: "'Encode Sans Semi Condensed', sans-serif",
                    color: color 
                  }}
                >
                  {item.title}
                </h3>
              </div>
            </a>

            {/* Secondary news bullet below */}
            {item.bullet && (
              <div className="mt-3 pt-3 border-t border-gray-50">
                <a 
                  href="#"
                  className="flex items-start gap-2 group/bullet"
                >
                  <span 
                    className="w-2 h-2 rounded-full mt-1.5 flex-shrink-0"
                    style={{ backgroundColor: color }}
                  />
                  <span className="text-sm text-gray-800 group-hover/bullet:text-gray-600 transition-colors leading-snug">
                    {item.bullet}
                  </span>
                </a>
              </div>
            )}
          </article>
        ))}
      </div>

      {/* Widget (Economy, Agenda, Horoscope) */}
      {widget && (
        <div className="p-4 border-t border-gray-100">
          {widget}
        </div>
      )}

      {/* More Link */}
      <div className="p-4 pt-2">
        <a 
          href={moreLink}
          className="block w-full py-2.5 text-center text-white font-semibold rounded transition-opacity hover:opacity-90"
          style={{ backgroundColor: color }}
        >
          Mais {title}
        </a>
      </div>
    </section>
  );
}
