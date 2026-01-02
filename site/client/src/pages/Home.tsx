/*
 * HOME PAGE - Axia News
 * Design: Fiel ao modelo original do outro agente
 * 
 * Estrutura por bloco de editoria:
 * 1. Manchete principal em TEXTO (sem imagem)
 * 2. 2 notícias complementares em texto com bullets
 * 3. Card com imagem (título sobre fundo colorido)
 * 4. 1 notícia complementar em texto com bullet
 * 5. Repetir padrão para próxima editoria
 * 
 * Ordem das editorias: Política → Economia → Tecnologia
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
function HeadlineText({ article }: { article: NewsArticle }) {
  const color = CATEGORY_COLORS[article.category] || '#333';
  
  return (
    <Link href={`/noticia/${article.id}`} className="block group mb-2">
      <h1 
        className="text-[24px] md:text-[30px] font-bold leading-tight group-hover:opacity-80 transition-opacity"
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

// Componente: Separador pequeno (após 3ª notícia - entre bullets e imagem)
function SmallSeparator() {
  return (
    <div className="my-1.5 h-1 bg-gray-100 -mx-5" />
  );
}

// Componente: Separador normal (após 5ª notícia - fim do bloco)
function BlockSeparator() {
  return (
    <div className="my-2 py-1 bg-gray-100 -mx-5" />
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

  // Renderizar bloco de uma editoria com separadores
  // Estrutura: Manchete + 2 bullets + SEPARADOR + Imagem + 1 bullet + SEPARADOR
  const renderCategoryBlock = (category: string, articles: NewsArticle[], isLastCategory: boolean) => {
    if (articles.length === 0) return null;
    
    const elements: JSX.Element[] = [];
    
    // 1. Manchete principal (primeira notícia) - SEM linha separadora
    if (articles[0]) {
      elements.push(
        <HeadlineText key={`headline-${articles[0].id}`} article={articles[0]} />
      );
    }

    // 2. Duas notícias em bullet com linha separadora em cada uma
    if (articles[1]) {
      elements.push(
        <BulletNews key={`bullet-${articles[1].id}`} article={articles[1]} showDivider={true} />
      );
    }
    if (articles[2]) {
      elements.push(
        <BulletNews key={`bullet-${articles[2].id}`} article={articles[2]} showDivider={false} />
      );
    }

    // SEPARADOR PEQUENO após a 3ª notícia (entre bullets e imagem)
    if (articles.length >= 3) {
      elements.push(
        <SmallSeparator key={`sep-1-${category}`} />
      );
    }

    // 3. Card com imagem
    if (articles[3]) {
      elements.push(
        <ImageCard key={`image-${articles[3].id}`} article={articles[3]} />
      );
    }

    // 4. Uma notícia em bullet (sem linha separadora)
    if (articles[4]) {
      elements.push(
        <BulletNews key={`bullet-4-${articles[4].id}`} article={articles[4]} showDivider={false} />
      );
    }

    // SEPARADOR após a 5ª notícia (fim do bloco)
    if (articles.length >= 5) {
      elements.push(
        <BlockSeparator key={`sep-2-${category}`} />
      );
    }

    // Se houver mais notícias, continuar o padrão
    let index = 5;
    while (index < articles.length) {
      // Card com imagem
      if (articles[index]) {
        elements.push(
          <ImageCard key={`image-loop-${articles[index].id}`} article={articles[index]} />
        );
        index++;
      }

      // Duas notícias em bullet com linha separadora
      for (let i = 0; i < 2 && articles[index]; i++) {
        elements.push(
          <BulletNews 
            key={`bullet-loop-${articles[index].id}`} 
            article={articles[index]} 
            showDivider={true}
          />
        );
        index++;
      }

      // Separador após cada grupo de 3 notícias
      if (index < articles.length) {
        elements.push(
          <BlockSeparator key={`sep-loop-${index}`} />
        );
      }
    }

    return elements;
  };

  return (
    <div className="min-h-screen flex flex-col bg-gray-100">
      <Header />
      
      <main className="flex-1">
        <div className="px-5 py-4 bg-white">
          {/* Renderizar blocos por editoria na ordem: Política → Economia → Tecnologia */}
          {CATEGORY_ORDER.map((category, idx) => (
            <div key={category}>
              {renderCategoryBlock(category, byCategory[category], idx === CATEGORY_ORDER.length - 1)}
            </div>
          ))}
          
          {/* Load More Button */}
          {hasMore && (
            <div className="mt-6 text-center">
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
        </div>
      </main>
      
      <Footer />
    </div>
  );
}
