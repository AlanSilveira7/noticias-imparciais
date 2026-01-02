/*
 * HOME PAGE - Axia News
 * Design: Fiel ao modelo original do outro agente
 * 
 * MOBILE: Layout vertical (uma coluna)
 * DESKTOP: Layout em 3 colunas (Política 50%, Economia 25%, Tecnologia 25%)
 * 
 * Estrutura Mobile:
 * PARTE 1 - Blocos principais (5 notícias por editoria):
 * 1. Manchete principal em TEXTO (sem imagem)
 * 2. 2 notícias complementares em texto com bullets
 * 3. Card com imagem (título sobre fundo colorido)
 * 4. 1 notícia complementar em texto com bullet
 * 
 * PARTE 2 - Seções de duplas (10 notícias restantes por editoria):
 * - Card de título com barra colorida
 * - 5 duplas: imagem à esquerda + manchete à direita + bullet abaixo
 * - Botão "Mais [Tema]"
 * 
 * Estrutura Desktop:
 * - Coluna Política (50%): Manchete + 2 bullets + imagem + 1 bullet
 * - Coluna Economia (25%): 3 cards verticais (foto + manchete)
 * - Coluna Tecnologia (25%): 3 cards verticais (foto + manchete)
 */

import { useState, useEffect } from "react";
import { Link } from "wouter";
import { AlertTriangle, ChevronDown, Loader2 } from "lucide-react";
import Header from "@/components/Header";
import Footer from "@/components/Footer";
import { fetchArticlesPaginated, type NewsArticleFrontend } from "@/lib/supabase";

type NewsArticle = NewsArticleFrontend;

// Cores das editorias
const CATEGORY_COLORS: Record<string, string> = {
  'Política': '#FF0000',
  'Economia': '#FF6B00',
  'Tecnologia': '#00A859',
};

// Ordem de prioridade das editorias
const CATEGORY_ORDER = ['Política', 'Economia', 'Tecnologia'];

// URLs das páginas de cada editoria
const CATEGORY_URLS: Record<string, string> = {
  'Política': '/politica',
  'Economia': '/economia',
  'Tecnologia': '/tecnologia',
};

// Configuração de paginação
const ITEMS_PER_PAGE = 15;

function LoadingState() {
  return (
    <div className="flex flex-col items-center justify-center py-20">
      <Loader2 className="w-8 h-8 animate-spin text-red-600 mb-4" />
      <p className="text-gray-600">Carregando notícias...</p>
    </div>
  );
}

function ErrorState({ onRetry }: { onRetry: () => void }) {
  return (
    <div className="flex flex-col items-center justify-center py-20">
      <AlertTriangle className="w-12 h-12 text-amber-500 mb-4" />
      <p className="text-gray-600 mb-4">Erro ao carregar notícias</p>
      <button
        onClick={onRetry}
        className="px-4 py-2 bg-gradient-to-r from-red-600 to-orange-500 text-white rounded-lg hover:opacity-90 transition-opacity"
      >
        Tentar novamente
      </button>
    </div>
  );
}

// Componente: Manchete Principal (apenas texto) - SEM linha separadora
function HeadlineText({ article, size = 'normal' }: { article: NewsArticle; size?: 'normal' | 'large' }) {
  const color = CATEGORY_COLORS[article.category] || '#333';
  
  return (
    <Link href={`/noticia/${article.id}`} className="block group mb-2">
      <h1 
        className={`font-bold leading-tight group-hover:opacity-80 transition-opacity ${
          size === 'large' ? 'text-[28px] lg:text-[36px]' : 'text-[24px] md:text-[30px]'
        }`}
        style={{ color }}
      >
        {article.title}
      </h1>
    </Link>
  );
}

// Componente: Notícia em texto com bullet - espaçamento reduzido
function BulletNews({ article, showDivider = false }: { article: NewsArticle; showDivider?: boolean }) {
  const color = CATEGORY_COLORS[article.category] || '#333';
  
  return (
    <div className={showDivider ? "border-b border-gray-200" : ""}>
      <Link 
        href={`/noticia/${article.id}`} 
        className="flex items-start gap-3 py-2.5 group"
      >
        <span 
          className="w-2 h-2 rounded-full mt-2 flex-shrink-0"
          style={{ backgroundColor: color }}
        />
        <span className="text-gray-800 text-base group-hover:opacity-70 transition-opacity leading-snug">
          {article.title}
        </span>
      </Link>
    </div>
  );
}

// Componente: Card com imagem (título sobre fundo colorido)
function ImageCard({ article }: { article: NewsArticle }) {
  const color = CATEGORY_COLORS[article.category] || '#333';
  
  return (
    <Link href={`/noticia/${article.id}`} className="block group my-3">
      <div className="relative rounded-2xl overflow-hidden shadow-sm">
        <img
          src={article.imageUrl}
          alt={article.title}
          className="w-full aspect-[16/10] object-cover group-hover:scale-105 transition-transform duration-300"
        />
        <div 
          className="absolute bottom-0 left-0 right-0 p-4 rounded-b-2xl"
          style={{ backgroundColor: color }}
        >
          <h2 className="text-white font-bold text-base md:text-lg leading-tight">
            {article.title}
          </h2>
        </div>
      </div>
    </Link>
  );
}

// Componente: Card vertical para colunas laterais (Desktop)
function VerticalCard({ article }: { article: NewsArticle }) {
  const color = CATEGORY_COLORS[article.category] || '#333';
  
  return (
    <Link href={`/noticia/${article.id}`} className="block group mb-4">
      <div className="overflow-hidden rounded-lg">
        <img
          src={article.imageUrl}
          alt={article.title}
          className="w-full aspect-[4/3] object-cover group-hover:scale-105 transition-transform duration-300"
        />
      </div>
      <h3 
        className="mt-2 text-base font-bold leading-tight group-hover:opacity-80 transition-opacity"
        style={{ color }}
      >
        {article.title}
      </h3>
    </Link>
  );
}

// Componente: Separador pequeno (após 3ª notícia - entre bullets e imagem)
function SmallSeparator() {
  return (
    <div className="my-1.5 h-1 bg-gray-100 -mx-5 lg:mx-0" />
  );
}

// Componente: Separador normal (após 5ª notícia - fim do bloco)
function BlockSeparator() {
  return (
    <div className="my-2 py-1 bg-gray-100 -mx-5 lg:hidden" />
  );
}

// Componente: Dupla de notícias (imagem à esquerda + manchete à direita + bullet abaixo)
function NewsDupla({ 
  imageArticle, 
  bulletArticle, 
  showDivider = true 
}: { 
  imageArticle: NewsArticle; 
  bulletArticle?: NewsArticle;
  showDivider?: boolean;
}) {
  const color = CATEGORY_COLORS[imageArticle.category] || '#333';
  
  return (
    <div className={showDivider ? "border-b border-gray-100" : ""}>
      {/* Card horizontal: imagem à esquerda, título à direita */}
      <Link href={`/noticia/${imageArticle.id}`} className="flex gap-4 py-3 group">
        {/* Imagem à esquerda */}
        <div className="flex-shrink-0 w-32 sm:w-36">
          <div className="relative overflow-hidden rounded-lg aspect-[4/3]">
            <img
              src={imageArticle.imageUrl}
              alt={imageArticle.title}
              className="w-full h-full object-cover transition-transform duration-300 group-hover:scale-105"
            />
          </div>
        </div>

        {/* Título à direita */}
        <div className="flex-1 min-w-0 flex items-center">
          <h3 
            className="text-base sm:text-lg font-bold leading-tight group-hover:opacity-80 transition-opacity"
            style={{ color }}
          >
            {imageArticle.title}
          </h3>
        </div>
      </Link>

      {/* Bullet com notícia secundária abaixo */}
      {bulletArticle && (
        <Link 
          href={`/noticia/${bulletArticle.id}`} 
          className="flex items-start gap-2.5 pb-3 group"
        >
          <span 
            className="w-2 h-2 rounded-full mt-1.5 flex-shrink-0"
            style={{ backgroundColor: color }}
          />
          <span className="text-sm text-gray-800 group-hover:opacity-70 transition-opacity leading-snug">
            {bulletArticle.title}
          </span>
        </Link>
      )}
    </div>
  );
}

// Componente: Seção de editoria com duplas (10 notícias restantes)
function CategorySection({ 
  category, 
  articles 
}: { 
  category: string; 
  articles: NewsArticle[];
}) {
  const color = CATEGORY_COLORS[category] || '#333';
  const categoryUrl = CATEGORY_URLS[category] || '/';
  
  // Pegar as notícias restantes (a partir da 6ª, índice 5)
  const remainingArticles = articles.slice(5);
  
  if (remainingArticles.length === 0) return null;
  
  // Organizar em duplas (cada dupla usa 2 notícias: 1 com imagem + 1 bullet)
  const duplas: { imageArticle: NewsArticle; bulletArticle?: NewsArticle }[] = [];
  for (let i = 0; i < remainingArticles.length; i += 2) {
    duplas.push({
      imageArticle: remainingArticles[i],
      bulletArticle: remainingArticles[i + 1],
    });
  }
  
  return (
    <section className="bg-white mb-3">
      {/* Barra colorida no topo + título da editoria */}
      <div 
        className="px-5 pt-4 pb-2"
        style={{ borderTop: `4px solid ${color}` }}
      >
        <Link 
          href={categoryUrl}
          className="text-xl font-bold uppercase tracking-wide hover:opacity-80 transition-opacity"
          style={{ color }}
        >
          {category}
        </Link>
      </div>

      {/* Duplas de notícias */}
      <div className="px-5">
        {duplas.map((dupla, index) => (
          <NewsDupla 
            key={`dupla-${category}-${index}`}
            imageArticle={dupla.imageArticle}
            bulletArticle={dupla.bulletArticle}
            showDivider={index < duplas.length - 1}
          />
        ))}
      </div>

      {/* Botão "Mais [Tema]" */}
      <div className="px-5 py-4">
        <Link 
          href={categoryUrl}
          className="block w-full py-3 text-center text-white font-semibold rounded-lg transition-opacity hover:opacity-90"
          style={{ backgroundColor: color }}
        >
          Mais {category}
        </Link>
      </div>
    </section>
  );
}

// Componente: Coluna lateral para Desktop (Economia ou Tecnologia)
function DesktopSideColumn({ 
  category, 
  articles 
}: { 
  category: string; 
  articles: NewsArticle[];
}) {
  const color = CATEGORY_COLORS[category] || '#333';
  const categoryUrl = CATEGORY_URLS[category] || '/';
  
  // Pegar apenas 3 notícias para a coluna lateral
  const columnArticles = articles.slice(0, 3);
  
  if (columnArticles.length === 0) return null;
  
  return (
    <div className="h-full">
      {/* Título da editoria */}
      <Link 
        href={categoryUrl}
        className="block text-lg font-bold uppercase tracking-wide hover:opacity-80 transition-opacity mb-4 pb-2"
        style={{ color, borderBottom: `3px solid ${color}` }}
      >
        {category}
      </Link>
      
      {/* Cards verticais */}
      {columnArticles.map((article) => (
        <VerticalCard key={article.id} article={article} />
      ))}
    </div>
  );
}

// Função para organizar notícias por categoria
function organizeByCategory(articles: NewsArticle[]): Record<string, NewsArticle[]> {
  const byCategory: Record<string, NewsArticle[]> = {
    'Política': [],
    'Economia': [],
    'Tecnologia': [],
  };
  
  articles.forEach(article => {
    if (byCategory[article.category]) {
      byCategory[article.category].push(article);
    }
  });
  
  return byCategory;
}

export default function Home() {
  const [newsArticles, setNewsArticles] = useState<NewsArticle[]>([]);
  const [loading, setLoading] = useState(true);
  const [loadingMore, setLoadingMore] = useState(false);
  const [error, setError] = useState(false);
  const [totalArticles, setTotalArticles] = useState(0);

  const loadInitialArticles = async () => {
    setLoading(true);
    setError(false);
    try {
      const result = await fetchArticlesPaginated(1, 45); // Carregar todas as 45 notícias
      setNewsArticles(result.articles);
      setTotalArticles(result.total);
    } catch (err) {
      console.error('Erro ao carregar artigos:', err);
      setError(true);
    } finally {
      setLoading(false);
    }
  };

  const loadMoreArticles = async () => {
    setLoadingMore(true);
    try {
      const nextPage = Math.floor(newsArticles.length / ITEMS_PER_PAGE) + 1;
      const { articles: newArticles } = await fetchArticlesPaginated(nextPage, ITEMS_PER_PAGE);
      
      const existingIds = new Set(newsArticles.map(a => a.id));
      const uniqueNewArticles = newArticles.filter(a => !existingIds.has(a.id));
      
      setNewsArticles(prev => [...prev, ...uniqueNewArticles]);
    } catch (err) {
      console.error('Erro ao carregar mais artigos:', err);
    } finally {
      setLoadingMore(false);
    }
  };

  useEffect(() => {
    loadInitialArticles();
  }, []);

  const hasMore = newsArticles.length < totalArticles;

  if (loading) {
    return (
      <div className="min-h-screen bg-white">
        <Header />
        <LoadingState />
        <Footer />
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-white">
        <Header />
        <ErrorState onRetry={loadInitialArticles} />
        <Footer />
      </div>
    );
  }

  if (newsArticles.length === 0) {
    return (
      <div className="min-h-screen bg-white">
        <Header />
        <div className="flex flex-col items-center justify-center py-20">
          <p className="text-gray-600">Nenhuma notícia disponível no momento.</p>
        </div>
        <Footer />
      </div>
    );
  }

  // Organizar notícias por categoria
  const byCategory = organizeByCategory(newsArticles);

  // Renderizar bloco de uma editoria com separadores (apenas 5 primeiras notícias) - MOBILE
  // Estrutura: Manchete + 2 bullets + SEPARADOR + Imagem + 1 bullet + SEPARADOR
  const renderCategoryBlock = (category: string, articles: NewsArticle[], isLastCategory: boolean) => {
    if (articles.length === 0) return null;
    
    // Limitar a 5 notícias por editoria neste bloco
    const limitedArticles = articles.slice(0, 5);
    const elements: JSX.Element[] = [];
    
    // 1. Manchete principal (primeira notícia) - SEM linha separadora
    if (limitedArticles[0]) {
      elements.push(
        <HeadlineText key={`headline-${limitedArticles[0].id}`} article={limitedArticles[0]} />
      );
    }

    // 2. Duas notícias em bullet com linha separadora em cada uma
    if (limitedArticles[1]) {
      elements.push(
        <BulletNews key={`bullet-${limitedArticles[1].id}`} article={limitedArticles[1]} showDivider={true} />
      );
    }
    if (limitedArticles[2]) {
      elements.push(
        <BulletNews key={`bullet-${limitedArticles[2].id}`} article={limitedArticles[2]} showDivider={false} />
      );
    }

    // SEPARADOR PEQUENO após a 3ª notícia (entre bullets e imagem)
    if (limitedArticles.length >= 3) {
      elements.push(
        <SmallSeparator key={`sep-1-${category}`} />
      );
    }

    // 3. Card com imagem
    if (limitedArticles[3]) {
      elements.push(
        <ImageCard key={`image-${limitedArticles[3].id}`} article={limitedArticles[3]} />
      );
    }

    // 4. Uma notícia em bullet (sem linha separadora)
    if (limitedArticles[4]) {
      elements.push(
        <BulletNews key={`bullet-4-${limitedArticles[4].id}`} article={limitedArticles[4]} showDivider={false} />
      );
    }

    // SEPARADOR após a 5ª notícia (fim do bloco) - apenas se não for a última categoria
    if (limitedArticles.length >= 5 && !isLastCategory) {
      elements.push(
        <BlockSeparator key={`sep-2-${category}`} />
      );
    }

    return elements;
  };

  // Renderizar coluna de Política para Desktop (5 notícias)
  const renderDesktopPoliticaColumn = () => {
    const articles = byCategory['Política'];
    if (articles.length === 0) return null;
    
    const limitedArticles = articles.slice(0, 5);
    
    return (
      <div>
        {/* Manchete principal grande */}
        {limitedArticles[0] && (
          <HeadlineText article={limitedArticles[0]} size="large" />
        )}
        
        {/* Bullets */}
        {limitedArticles[1] && (
          <BulletNews article={limitedArticles[1]} showDivider={true} />
        )}
        {limitedArticles[2] && (
          <BulletNews article={limitedArticles[2]} showDivider={true} />
        )}
        {limitedArticles[3] && (
          <BulletNews article={limitedArticles[3]} showDivider={false} />
        )}
        
        {/* Card com imagem */}
        {limitedArticles[4] && (
          <ImageCard article={limitedArticles[4]} />
        )}
      </div>
    );
  };

  return (
    <div className="min-h-screen flex flex-col bg-gray-100">
      <Header />
      
      <main className="flex-1">
        {/* ========== LAYOUT DESKTOP (3 colunas) ========== */}
        <div className="hidden lg:block bg-white">
          <div className="container mx-auto px-6 py-6">
            <div className="flex gap-8">
              {/* Coluna Política (50%) */}
              <div className="w-1/2 pr-6 border-r border-gray-200">
                {renderDesktopPoliticaColumn()}
              </div>
              
              {/* Coluna Economia (25%) */}
              <div className="w-1/4 px-2">
                <DesktopSideColumn 
                  category="Economia" 
                  articles={byCategory['Economia']} 
                />
              </div>
              
              {/* Coluna Tecnologia (25%) */}
              <div className="w-1/4 pl-2">
                <DesktopSideColumn 
                  category="Tecnologia" 
                  articles={byCategory['Tecnologia']} 
                />
              </div>
            </div>
          </div>
        </div>

        {/* ========== LAYOUT MOBILE (vertical) ========== */}
        {/* PARTE 1: Blocos principais (5 notícias por editoria) - apenas mobile */}
        <div className="lg:hidden px-5 py-4 bg-white">
          {CATEGORY_ORDER.map((category, idx) => (
            <div key={category}>
              {renderCategoryBlock(category, byCategory[category], idx === CATEGORY_ORDER.length - 1)}
            </div>
          ))}
        </div>

        {/* PARTE 2: Seções de duplas (10 notícias restantes por editoria) - apenas mobile */}
        <div className="lg:hidden mt-3">
          {CATEGORY_ORDER.map((category) => (
            <CategorySection 
              key={`section-${category}`}
              category={category}
              articles={byCategory[category]}
            />
          ))}
        </div>

        {/* ========== SEÇÕES DE DUPLAS PARA DESKTOP ========== */}
        <div className="hidden lg:block mt-6">
          <div className="container mx-auto px-6">
            <div className="grid grid-cols-3 gap-6">
              {CATEGORY_ORDER.map((category) => (
                <CategorySection 
                  key={`desktop-section-${category}`}
                  category={category}
                  articles={byCategory[category]}
                />
              ))}
            </div>
          </div>
        </div>
        
        {/* Load More Button */}
        {hasMore && (
          <div className="py-6 text-center bg-white">
            <button
              onClick={loadMoreArticles}
              disabled={loadingMore}
              className="inline-flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-red-600 to-orange-500 text-white font-semibold rounded-lg hover:opacity-90 transition-opacity disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loadingMore ? (
                <>
                  <Loader2 size={18} className="animate-spin" />
                  <span>Carregando...</span>
                </>
              ) : (
                <>
                  <span>Carregar mais notícias</span>
                  <ChevronDown size={18} />
                </>
              )}
            </button>
            <p className="mt-2 text-xs text-gray-500">
              Mostrando {newsArticles.length} de {totalArticles} notícias
            </p>
          </div>
        )}
      </main>
      
      <Footer />
    </div>
  );
}
