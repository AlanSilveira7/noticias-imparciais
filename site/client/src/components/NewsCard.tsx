/*
 * NEWS CARD COMPONENT - Axia News
 * Design: Fidelidade Editorial Clássica
 * 
 * Variantes:
 * - hero: Card grande para manchete principal
 * - featured: Card médio para destaques
 * - small: Card pequeno para listagens
 * - column: Card para colunas temáticas (com borda colorida)
 * - compact: Card compacto sem imagem
 */

import { Link } from 'wouter';
import { AlertTriangle, CheckCircle, Clock, User } from 'lucide-react';
import type { NewsArticleFrontend } from '@/lib/supabase';

// Mapeamento de cores por categoria
const categoryColors: Record<string, string> = {
  'Política': '#FF0000',
  'Economia': '#FF6B00',
  'Tecnologia': '#00A859',
};

interface NewsCardProps {
  article: NewsArticleFrontend;
  variant?: 'hero' | 'featured' | 'small' | 'column' | 'compact';
}

// Função para formatar data
function formatDate(dateString: string): string {
  const date = new Date(dateString);
  return date.toLocaleDateString('pt-BR', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
  });
}

// Função para formatar data e hora
function formatDateTime(dateString: string): string {
  const date = new Date(dateString);
  return `${date.toLocaleDateString('pt-BR', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
  })} às ${date.toLocaleTimeString('pt-BR', {
    hour: '2-digit',
    minute: '2-digit',
  })}`;
}

export default function NewsCard({ article, variant = 'featured' }: NewsCardProps) {
  const categoryColor = categoryColors[article.category] || '#666666';
  
  // Indicador de viés
  const BiasIndicator = () => (
    <span 
      className={`inline-flex items-center gap-1 px-2 py-0.5 rounded text-xs font-semibold ${
        article.hasBiasDetected 
          ? 'bg-amber-100 text-amber-800' 
          : 'bg-green-100 text-green-800'
      }`}
    >
      {article.hasBiasDetected ? (
        <>
          <AlertTriangle size={12} />
          Viés Detectado
        </>
      ) : (
        <>
          <CheckCircle size={12} />
          Verificada
        </>
      )}
    </span>
  );

  // HERO variant - Card grande para manchete principal
  if (variant === 'hero') {
    return (
      <Link href={`/noticia/${article.id}`}>
        <article className="axia-card relative group cursor-pointer">
          <div className="relative overflow-hidden aspect-[16/9] rounded-2xl">
            <img
              src={article.imageUrl}
              alt={article.title}
              className="w-full h-full object-cover transition-transform duration-300"
            />
            <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-black/40 to-transparent" />
            <div className="absolute bottom-0 left-0 right-0 p-4 sm:p-6">
              <div className="flex items-center gap-2 mb-2">
                <span 
                  className="inline-block px-2 py-1 text-xs font-bold text-white rounded"
                  style={{ backgroundColor: categoryColor }}
                >
                  {article.category.toUpperCase()}
                </span>
                <BiasIndicator />
              </div>
              <h2 
                className="axia-news-title text-white text-xl sm:text-2xl md:text-3xl mb-2"
                style={{ textShadow: '0 2px 4px rgba(0,0,0,0.3)' }}
              >
                {article.title}
              </h2>
              <p className="text-white/90 text-sm sm:text-base line-clamp-2">{article.subtitle}</p>
            </div>
          </div>
        </article>
      </Link>
    );
  }

  // COLUMN variant - Card para colunas temáticas
  if (variant === 'column') {
    return (
      <Link href={`/noticia/${article.id}`}>
        <article className="p-4 group">
          <div className="flex gap-4">
            {/* Image - Left side */}
            <div className="flex-shrink-0 w-32 sm:w-40">
              <div className="relative overflow-hidden rounded aspect-[4/3]">
                <img
                  src={article.imageUrl}
                  alt={article.title}
                  className="w-full h-full object-cover transition-transform duration-300 group-hover:scale-105"
                />
              </div>
            </div>

            {/* Text - Right side */}
            <div className="flex-1 min-w-0">
              <div className="flex items-center gap-2 mb-1">
                <BiasIndicator />
              </div>
              <h3 
                className="text-base sm:text-lg font-bold leading-tight group-hover:opacity-80 transition-opacity line-clamp-3"
                style={{ 
                  fontFamily: "'Encode Sans Semi Condensed', sans-serif",
                  color: categoryColor 
                }}
              >
                {article.title}
              </h3>
              <p className="text-gray-600 text-sm mt-1 line-clamp-2">{article.subtitle}</p>
            </div>
          </div>
        </article>
      </Link>
    );
  }

  // SMALL variant - Card pequeno para listagens
  if (variant === 'small') {
    return (
      <Link href={`/noticia/${article.id}`}>
        <article className="axia-card cursor-pointer group">
          <div className="relative overflow-hidden aspect-[4/3] rounded">
            <img
              src={article.imageUrl}
              alt={article.title}
              className="w-full h-full object-cover transition-transform duration-300"
            />
          </div>
          <div className="pt-2">
            <div className="flex items-center gap-2 mb-1">
              <BiasIndicator />
            </div>
            <h3 className="axia-news-title text-sm leading-tight line-clamp-3 text-gray-900 group-hover:text-red-600 transition-colors">
              {article.title}
            </h3>
            <span className="axia-source-tag mt-1 block text-gray-500">
              {formatDate(article.date)}
            </span>
          </div>
        </article>
      </Link>
    );
  }

  // COMPACT variant - Card sem imagem
  if (variant === 'compact') {
    return (
      <Link href={`/noticia/${article.id}`}>
        <article className="axia-card p-4 cursor-pointer group border-l-4 hover:bg-gray-50" style={{ borderLeftColor: categoryColor }}>
          <div className="flex items-center gap-2 mb-2">
            <span 
              className="text-xs font-bold"
              style={{ color: categoryColor }}
            >
              {article.category.toUpperCase()}
            </span>
            <BiasIndicator />
          </div>
          <h3 className="axia-news-title text-base leading-tight text-gray-900 group-hover:opacity-80 transition-opacity line-clamp-2">
            {article.title}
          </h3>
          <p className="text-gray-600 text-sm mt-1 line-clamp-2">{article.subtitle}</p>
          <div className="flex items-center gap-3 mt-2 text-gray-500 text-xs">
            <span className="flex items-center gap-1">
              <User size={12} />
              Redação
            </span>
            <span className="flex items-center gap-1">
              <Clock size={12} />
              {formatDateTime(article.createdAt)}
            </span>
          </div>
        </article>
      </Link>
    );
  }

  // DEFAULT: FEATURED variant - Card médio para destaques
  return (
    <Link href={`/noticia/${article.id}`}>
      <article className="axia-card cursor-pointer group p-3">
        {/* Imagem reduzida em 30% - aspect ratio mais compacto */}
        <div className="relative overflow-hidden aspect-[2/1] rounded-2xl">
          <img
            src={article.imageUrl}
            alt={article.title}
            className="w-full h-full object-cover transition-transform duration-300"
          />
        </div>
        <div className="pt-3 pb-1">
          <div className="flex items-center gap-2 mb-2">
            <BiasIndicator />
          </div>
          {/* Título com cor da editoria */}
          <h3 
            className="axia-news-title text-base sm:text-lg leading-tight line-clamp-3 group-hover:opacity-80 transition-opacity"
            style={{ color: categoryColor }}
          >
            {article.title}
          </h3>
          <p className="text-gray-600 text-sm mt-1 line-clamp-2">{article.subtitle}</p>
        </div>
      </article>
    </Link>
  );
}
