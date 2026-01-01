/*
 * HOME PAGE - Axia News
 * Design: Fiel ao modelo original do outro agente
 * 
 * Estrutura:
 * 1. Manchete principal em TEXTO (sem imagem)
 * 2. Lista de notícias em texto com bullets coloridos
 * 3. Card com imagem (título sobre fundo colorido)
 * 4. Mais notícias em texto com bullets
 * 5. Repetir padrão
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

// Configuração de paginação
const ITEMS_PER_PAGE = 12;

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

// Componente: Manchete Principal (apenas texto)
function HeadlineText({ article }: { article: NewsArticle }) {
  const color = CATEGORY_COLORS[article.category] || '#333';
  
  return (
    <Link href={`/noticia/${article.id}`} className="block group">
      <h1 
        className="text-2xl md:text-3xl lg:text-4xl font-bold leading-tight mb-4 group-hover:opacity-80 transition-opacity"
        style={{ color }}
      >
        {article.title}
      </h1>
      <div className="border-b border-gray-200 pb-4 mb-4" />
    </Link>
  );
}

// Componente: Notícia em texto com bullet
function BulletNews({ article }: { article: NewsArticle }) {
  const color = CATEGORY_COLORS[article.category] || '#333';
  
  return (
    <Link 
      href={`/noticia/${article.id}`} 
      className="flex items-start gap-3 py-2 group"
    >
      <span 
        className="w-2.5 h-2.5 rounded-full mt-2 flex-shrink-0"
        style={{ backgroundColor: color }}
      />
      <span className="text-gray-800 group-hover:opacity-70 transition-opacity leading-relaxed">
        {article.title}
      </span>
    </Link>
  );
}

// Componente: Card com imagem (título sobre fundo colorido)
function ImageCard({ article }: { article: NewsArticle }) {
  const color = CATEGORY_COLORS[article.category] || '#333';
  
  return (
    <Link href={`/noticia/${article.id}`} className="block group my-6">
      <div className="relative rounded-lg overflow-hidden">
        <img
          src={article.imageUrl}
          alt={article.title}
          className="w-full aspect-[16/10] object-cover group-hover:scale-105 transition-transform duration-300"
        />
        <div 
          className="absolute bottom-0 left-0 right-0 p-4"
          style={{ backgroundColor: color }}
        >
          <h2 className="text-white font-bold text-lg md:text-xl leading-tight">
            {article.title}
          </h2>
        </div>
      </div>
    </Link>
  );
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
      const result = await fetchArticlesPaginated(1, ITEMS_PER_PAGE);
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

  // Organizar notícias no padrão: manchete → bullets → imagem → bullets → imagem...
  const renderNewsPattern = () => {
    const elements: JSX.Element[] = [];
    let index = 0;

    // 1. Manchete principal (primeira notícia)
    if (newsArticles[index]) {
      elements.push(
        <HeadlineText key={`headline-${newsArticles[index].id}`} article={newsArticles[index]} />
      );
      index++;
    }

    // 2. Duas notícias em bullet
    const firstBullets: JSX.Element[] = [];
    for (let i = 0; i < 2 && newsArticles[index]; i++) {
      firstBullets.push(
        <BulletNews key={`bullet-${newsArticles[index].id}`} article={newsArticles[index]} />
      );
      index++;
    }
    if (firstBullets.length > 0) {
      elements.push(
        <div key="first-bullets" className="mb-4">
          {firstBullets}
        </div>
      );
    }

    // 3. Card com imagem
    if (newsArticles[index]) {
      elements.push(
        <ImageCard key={`image-${newsArticles[index].id}`} article={newsArticles[index]} />
      );
      index++;
    }

    // 4. Uma notícia em bullet
    if (newsArticles[index]) {
      elements.push(
        <div key="second-bullets" className="mb-4">
          <BulletNews article={newsArticles[index]} />
        </div>
      );
      index++;
    }

    // 5. Continuar o padrão: imagem → 2 bullets → imagem → 2 bullets...
    while (index < newsArticles.length) {
      // Card com imagem
      if (newsArticles[index]) {
        elements.push(
          <ImageCard key={`image-loop-${newsArticles[index].id}`} article={newsArticles[index]} />
        );
        index++;
      }

      // Duas notícias em bullet
      const loopBullets: JSX.Element[] = [];
      for (let i = 0; i < 2 && newsArticles[index]; i++) {
        loopBullets.push(
          <BulletNews key={`bullet-loop-${newsArticles[index].id}`} article={newsArticles[index]} />
        );
        index++;
      }
      if (loopBullets.length > 0) {
        elements.push(
          <div key={`bullets-group-${index}`} className="mb-4">
            {loopBullets}
          </div>
        );
      }
    }

    return elements;
  };

  return (
    <div className="min-h-screen flex flex-col bg-white">
      <Header />
      
      <main className="flex-1">
        <div className="container py-6">
          <div className="max-w-2xl mx-auto">
            {renderNewsPattern()}
            
            {/* Load More Button */}
            {hasMore && (
              <div className="mt-8 text-center">
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
        </div>
      </main>
      
      <Footer />
    </div>
  );
}
