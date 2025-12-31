/*
 * SECTION COLUMN COMPONENT - Axia News
 * Design: Fidelidade Editorial Clássica
 * 
 * Layout:
 * - Título da seção com cor da editoria
 * - Lista de notícias com imagem à esquerda
 * - Botão "Mais [Categoria]" no final
 */

import { Link } from 'wouter';
import NewsCard from './NewsCard';
import type { NewsArticleFrontend } from '@/lib/supabase';

interface SectionColumnProps {
  title: string;
  color: string;
  articles: NewsArticleFrontend[];
  moreLink: string;
  maxItems?: number;
}

export default function SectionColumn({
  title,
  color,
  articles,
  moreLink,
  maxItems = 5,
}: SectionColumnProps) {
  const displayArticles = articles.slice(0, maxItems);

  return (
    <section 
      className="bg-white rounded-lg overflow-hidden shadow-sm"
      style={{ borderTop: `4px solid ${color}` }}
    >
      {/* Section Header */}
      <div className="p-4 pb-2">
        <Link 
          href={moreLink}
          className="axia-section-title inline-block hover:underline"
          style={{ color }}
        >
          {title.toUpperCase()}
        </Link>
      </div>

      {/* News Cards */}
      <div className="divide-y divide-gray-100">
        {displayArticles.map((article) => (
          <NewsCard 
            key={article.id} 
            article={article} 
            variant="column" 
          />
        ))}
      </div>

      {/* More Link */}
      <div className="p-4 pt-2">
        <Link 
          href={moreLink}
          className="block w-full py-2.5 text-center text-white font-semibold rounded transition-opacity hover:opacity-90"
          style={{ backgroundColor: color }}
        >
          Mais {title}
        </Link>
      </div>
    </section>
  );
}
