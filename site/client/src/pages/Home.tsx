/*
 * HOME PAGE - Axia News
 * Design: Fidelidade Editorial Clássica
 * 
 * Estrutura:
 * 1. Header com navegação
 * 2. Hero Section (destaque principal + destaques secundários)
 * 3. Três colunas temáticas (Política, Economia, Mais Notícias)
 * 4. Seção "Mais Notícias" com paginação
 * 5. Footer
 */

import { useState, useEffect } from "react";
import { Link } from "wouter";
import { Clock, CheckCircle, ArrowRight, AlertTriangle, ChevronDown, Loader2, User } from "lucide-react";
import Header from "@/components/Header";
import Footer from "@/components/Footer";
import NewsCard from "@/components/NewsCard";
import SectionColumn from "@/components/SectionColumn";
import { fetchArticlesPaginated, fetchArticlesByCategory, type NewsArticleFrontend } from "@/lib/supabase";

// Alias para manter compatibilidade
type NewsArticle = NewsArticleFrontend;

// Configuração de paginação
const HERO_COUNT = 4; // 1 destaque principal + 3 ao lado
const ITEMS_PER_PAGE = 6;
const INITIAL_LOAD = HERO_COUNT + ITEMS_PER_PAGE;

// Cores das editorias
const CATEGORY_COLORS = {
  'Política': '#FF0000',
  'Economia': '#FF6B00',
  'Tecnologia': '#00A859',
};

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

export default function Home() {
  const [newsArticles, setNewsArticles] = useState<NewsArticle[]>([]);
  const [politicaArticles, setPoliticaArticles] = useState<NewsArticle[]>([]);
  const [economiaArticles, setEconomiaArticles] = useState<NewsArticle[]>([]);
  const [loading, setLoading] = useState(true);
  const [loadingMore, setLoadingMore] = useState(false);
  const [error, setError] = useState(false);
  const [totalArticles, setTotalArticles] = useState(0);

  // Carrega artigos iniciais e por categoria
  const loadInitialArticles = async () => {
    setLoading(true);
    setError(false);
    try {
      const [allResult, politicaResult, economiaResult] = await Promise.all([
        fetchArticlesPaginated(1, INITIAL_LOAD),
        fetchArticlesByCategory('Política'),
        fetchArticlesByCategory('Economia'),
      ]);
      
      setNewsArticles(allResult.articles);
      setTotalArticles(allResult.total);
      setPoliticaArticles(politicaResult);
      setEconomiaArticles(economiaResult);
    } catch (err) {
      console.error('Erro ao carregar artigos:', err);
      setError(true);
    } finally {
      setLoading(false);
    }
  };

  // Carrega mais notícias
  const loadMoreArticles = async () => {
    setLoadingMore(true);
    try {
      const loadedBeyondHero = newsArticles.length - HERO_COUNT;
      const nextPage = Math.floor(loadedBeyondHero / ITEMS_PER_PAGE) + 2;
      
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

  // Separação de artigos
  const heroArticle = newsArticles[0];
  const featuredArticles = newsArticles.slice(1, HERO_COUNT);
  const remainingArticles = newsArticles.slice(HERO_COUNT);
  
  const totalRemaining = totalArticles - HERO_COUNT;
  const hasMore = remainingArticles.length < totalRemaining;

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-100">
        <Header />
        <LoadingState />
        <Footer />
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-100">
        <Header />
        <ErrorState onRetry={loadInitialArticles} />
        <Footer />
      </div>
    );
  }

  if (newsArticles.length === 0) {
    return (
      <div className="min-h-screen bg-gray-100">
        <Header />
        <div className="flex flex-col items-center justify-center py-20">
          <p className="text-gray-600">Nenhuma notícia disponível no momento.</p>
        </div>
        <Footer />
      </div>
    );
  }

  return (
    <div className="min-h-screen flex flex-col bg-gray-100">
      <Header />
      
      <main className="flex-1">
        {/* Hero Section */}
        <section className="bg-white">
          <div className="container py-4">
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-4">
              {/* Main Hero - 6 colunas */}
              <div className="lg:col-span-6">
                {heroArticle && (
                  <NewsCard article={heroArticle} variant="hero" />
                )}
              </div>

              {/* Featured News - 3 colunas */}
              <div className="lg:col-span-3 space-y-4">
                {featuredArticles.slice(0, 2).map((article) => (
                  <NewsCard key={article.id} article={article} variant="featured" />
                ))}
              </div>

              {/* Side News - 3 colunas */}
              <div className="lg:col-span-3 space-y-3">
                {featuredArticles.slice(2).map((article) => (
                  <NewsCard key={article.id} article={article} variant="small" />
                ))}
                {/* Preencher com mais artigos se necessário */}
                {remainingArticles.slice(0, 3 - featuredArticles.slice(2).length).map((article) => (
                  <NewsCard key={article.id} article={article} variant="small" />
                ))}
              </div>
            </div>
          </div>
        </section>

        {/* Three Columns Section - Editorias */}
        <section className="py-6">
          <div className="container">
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              {/* Política Column */}
              {politicaArticles.length > 0 && (
                <SectionColumn
                  title="Política"
                  color={CATEGORY_COLORS['Política']}
                  articles={politicaArticles}
                  moreLink="/politica"
                  maxItems={4}
                />
              )}

              {/* Economia Column */}
              {economiaArticles.length > 0 && (
                <SectionColumn
                  title="Economia"
                  color={CATEGORY_COLORS['Economia']}
                  articles={economiaArticles}
                  moreLink="/economia"
                  maxItems={4}
                />
              )}

              {/* Mais Notícias Column */}
              <section 
                className="bg-white rounded-lg overflow-hidden shadow-sm"
                style={{ borderTop: '4px solid #0A1F44' }}
              >
                <div className="p-4 pb-2">
                  <span className="axia-section-title" style={{ color: '#0A1F44' }}>
                    ÚLTIMAS NOTÍCIAS
                  </span>
                </div>
                <div className="divide-y divide-gray-100">
                  {remainingArticles.slice(0, 4).map((article) => (
                    <NewsCard key={article.id} article={article} variant="column" />
                  ))}
                </div>
                <div className="p-4 pt-2">
                  <a 
                    href="#mais-noticias"
                    className="block w-full py-2.5 text-center text-white font-semibold rounded transition-opacity hover:opacity-90"
                    style={{ backgroundColor: '#0A1F44' }}
                  >
                    Ver Todas
                  </a>
                </div>
              </section>
            </div>
          </div>
        </section>

        {/* Remaining News Grid */}
        {remainingArticles.length > 4 && (
          <section id="mais-noticias" className="bg-white py-8">
            <div className="container">
              <div className="flex items-center justify-between mb-6">
                <h2 
                  className="axia-section-title"
                  style={{ color: '#0A1F44' }}
                >
                  MAIS NOTÍCIAS
                </h2>
                <div className="flex items-center gap-2 text-xs text-gray-500">
                  <CheckCircle size={14} className="text-green-600" />
                  <span>Todas verificadas e balanceadas</span>
                </div>
              </div>
              
              {/* Grid de notícias */}
              <div className="space-y-6">
                {/* Primeira linha: cards featured */}
                <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
                  {remainingArticles.slice(4, 7).map((article) => (
                    <NewsCard key={article.id} article={article} variant="featured" />
                  ))}
                </div>
                
                {/* Segunda linha: cards compactos */}
                {remainingArticles.length > 7 && (
                  <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-4">
                    {remainingArticles.slice(7, 11).map((article) => (
                      <NewsCard key={article.id} article={article} variant="compact" />
                    ))}
                  </div>
                )}
                
                {/* Terceira linha em diante */}
                {remainingArticles.length > 11 && (
                  <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
                    {remainingArticles.slice(11).map((article) => (
                      <NewsCard key={article.id} article={article} variant="featured" />
                    ))}
                  </div>
                )}
              </div>
              
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
                    Mostrando {remainingArticles.length} de {totalRemaining} notícias adicionais
                  </p>
                </div>
              )}
            </div>
          </section>
        )}
        
        {/* About Section */}
        <section className="bg-gray-100 border-t border-gray-200">
          <div className="container py-12">
            <div className="max-w-2xl mx-auto text-center">
              <h2 
                className="text-lg font-bold mb-3"
                style={{ 
                  fontFamily: "'Encode Sans Semi Condensed', sans-serif",
                  background: 'linear-gradient(135deg, #FF0000 0%, #FF6B00 100%)',
                  WebkitBackgroundClip: 'text',
                  WebkitTextFillColor: 'transparent',
                  backgroundClip: 'text'
                }}
              >
                Por que Axia News?
              </h2>
              <p className="text-gray-600 text-sm leading-relaxed mb-4">
                Analisamos diferentes fontes de notícias, identificamos vieses editoriais 
                e apresentamos os fatos de forma neutra. Você decide, nós informamos.
              </p>
              <Link 
                href="/sobre" 
                className="inline-flex items-center gap-1 text-red-600 text-sm font-medium hover:underline"
              >
                Saiba mais sobre nossa metodologia <ArrowRight size={14} />
              </Link>
            </div>
          </div>
        </section>
      </main>
      
      <Footer />
    </div>
  );
}
