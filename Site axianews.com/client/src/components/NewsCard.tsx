/*
 * NEWS CARD COMPONENT - Clone Globo.com
 * Design: Fidelidade Editorial Clássica
 * 
 * Variantes:
 * - hero: Card grande para manchete principal
 * - featured: Card médio para destaques
 * - small: Card pequeno para listagens
 * - column: Card para colunas temáticas (com borda colorida)
 */

interface NewsCardProps {
  title: string;
  image: string;
  category?: string;
  source?: string;
  sourceColor?: string;
  variant?: 'hero' | 'featured' | 'small' | 'column';
  borderColor?: string;
  subtitle?: string;
  bullets?: string[];
}

export default function NewsCard({
  title,
  image,
  category,
  source,
  sourceColor = '#666',
  variant = 'featured',
  borderColor,
  subtitle,
  bullets,
}: NewsCardProps) {
  if (variant === 'hero') {
    return (
      <article className="globo-card relative group cursor-pointer">
        <div className="relative overflow-hidden aspect-[16/9]">
          <img
            src={image}
            alt={title}
            className="w-full h-full object-cover transition-transform duration-300"
          />
          <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-black/40 to-transparent" />
          <div className="absolute bottom-0 left-0 right-0 p-4 sm:p-6">
            {category && (
              <span 
                className="inline-block px-2 py-1 text-xs font-bold text-white mb-2 rounded"
                style={{ backgroundColor: '#FF0000' }}
              >
                {category}
              </span>
            )}
            <h2 
              className="globo-news-title text-white text-xl sm:text-2xl md:text-3xl mb-2"
              style={{ textShadow: '0 2px 4px rgba(0,0,0,0.3)' }}
            >
              {title}
            </h2>
            {subtitle && (
              <p className="text-white/90 text-sm sm:text-base">{subtitle}</p>
            )}
            {bullets && bullets.length > 0 && (
              <ul className="mt-3 space-y-1">
                {bullets.map((bullet, i) => (
                  <li key={i} className="text-white/80 text-sm flex items-start gap-2">
                    <span className="text-yellow-400">•</span>
                    {bullet}
                  </li>
                ))}
              </ul>
            )}
          </div>
        </div>
      </article>
    );
  }

  if (variant === 'column') {
    return (
      <article 
        className="globo-card flex gap-3 p-3 cursor-pointer border-l-4"
        style={{ borderLeftColor: borderColor || '#00A859' }}
      >
        <div className="w-24 h-20 flex-shrink-0 overflow-hidden rounded">
          <img
            src={image}
            alt={title}
            className="w-full h-full object-cover transition-transform duration-300"
          />
        </div>
        <div className="flex-1 min-w-0">
          <h3 className="globo-news-title text-sm leading-tight line-clamp-3 text-gray-900">
            {title}
          </h3>
          {source && (
            <div className="mt-2 flex items-center gap-2">
              <span 
                className="globo-source-tag"
                style={{ color: sourceColor }}
              >
                {category && <span className="text-gray-500">{category} · </span>}
                {source}
              </span>
            </div>
          )}
        </div>
      </article>
    );
  }

  if (variant === 'small') {
    return (
      <article className="globo-card cursor-pointer group">
        <div className="relative overflow-hidden aspect-[4/3] rounded">
          <img
            src={image}
            alt={title}
            className="w-full h-full object-cover transition-transform duration-300"
          />
        </div>
        <div className="pt-2">
          <h3 className="globo-news-title text-sm leading-tight line-clamp-3 text-gray-900 group-hover:text-red-600 transition-colors">
            {title}
          </h3>
          {source && (
            <span 
              className="globo-source-tag mt-1 block"
              style={{ color: sourceColor }}
            >
              {source}
            </span>
          )}
        </div>
      </article>
    );
  }

  // Default: featured variant
  return (
    <article className="globo-card cursor-pointer group">
      <div className="relative overflow-hidden aspect-[16/10] rounded">
        <img
          src={image}
          alt={title}
          className="w-full h-full object-cover transition-transform duration-300"
        />
        {category && (
          <span 
            className="absolute top-2 left-2 px-2 py-0.5 text-xs font-bold text-white rounded"
            style={{ backgroundColor: borderColor || '#FF0000' }}
          >
            {category}
          </span>
        )}
      </div>
      <div className="pt-3">
        <h3 className="globo-news-title text-base sm:text-lg leading-tight line-clamp-3 text-gray-900 group-hover:text-red-600 transition-colors">
          {title}
        </h3>
        {bullets && bullets.length > 0 && (
          <ul className="mt-2 space-y-1">
            {bullets.map((bullet, i) => (
              <li key={i} className="text-gray-600 text-sm flex items-start gap-2">
                <span className="text-red-500">•</span>
                {bullet}
              </li>
            ))}
          </ul>
        )}
        {source && (
          <span 
            className="globo-source-tag mt-2 block"
            style={{ color: sourceColor }}
          >
            {source}
          </span>
        )}
      </div>
    </article>
  );
}
