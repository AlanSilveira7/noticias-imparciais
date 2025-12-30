import { useState, useEffect } from "react";
import { Link } from "wouter";
import { Clock, CheckCircle, ArrowRight, AlertTriangle, ChevronDown, Loader2, User } from "lucide-react";
import Header from "@/components/Header";
import Footer from "@/components/Footer";
import { fetchArticlesPaginated, type NewsArticleFrontend } from "@/lib/supabase";

// Alias para manter compatibilidade com os componentes existentes
type NewsArticle = NewsArticleFrontend;

// Configuração de paginação
const FEATURED_COUNT = 4; // 1 destaque principal + 3 ao lado
const ITEMS_PER_PAGE = 6; // Notícias carregadas por vez na seção "Mais Notícias"
const INITIAL_LOAD = FEATURED_COUNT + ITEMS_PER_PAGE; // Carga inicial: 4 destaques + 6 notícias

function CategoryBadge({ category }: { category: string }) {
  const colors: Record<string, string> = {
    "Política": "bg-blue-600",
    "Economia": "bg-green-600",
  };
  
  return (
    <span className={`${colors[category] || "bg-gray-600"} text-white text-[10px] font-bold px-2 py-0.5 rounded`}>
      {category.toUpperCase()}
    </span>
  );
}

function VerifiedBadge({ hasBias }: { hasBias: boolean }) {
  if (hasBias) {
    return (
      <span className="inline-flex items-center gap-1 text-amber-600 text-xs font-medium">
        <AlertTriangle size={12} />
        Viés Detectado
      </span>
    );
  }
  return (
    <span className="inline-flex items-center gap-1 text-green-600 text-xs font-medium">
      <CheckCircle size={12} />
      Verificada
    </span>
  );
}

// Função para formatar data e hora
function formatDateTime(dateString: string): { date: string; time: string } {
  try {
    const date = new Date(dateString);
    const formattedDate = date.toLocaleDateString('pt-BR', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric'
    });
    const formattedTime = date.toLocaleTimeString('pt-BR', {
      hour: '2-digit',
      minute: '2-digit'
    });
    return { date: formattedDate, time: formattedTime };
  } catch {
    return { date: dateString, time: '' };
  }
}

// Notícia em destaque principal - texto ABAIXO da imagem (responsivo)
function MainFeaturedNews({ article }: { article: NewsArticle }) {
  const { date, time } = formatDateTime(article.createdAt);
  
  return (
    <Link href={`/noticia/${article.id}`} className="group block h-full">
      <article className="h-full flex flex-col bg-white rounded-lg overflow-hidden shadow-sm hover:shadow-md transition-shadow">
        {/* Imagem - altura responsiva: 200px mobile, 260px desktop */}
        <div className="h-[200px] lg:h-[260px] overflow-hidden bg-gray-100">
          <img
            src={article.imageUrl}
            alt={article.title}
            className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
          />
        </div>
        {/* Texto - padding responsivo: p-4 mobile, p-3 desktop */}
        <div className="flex-1 p-4 lg:p-3 flex flex-col">
          <div className="flex items-center gap-2 mb-2 lg:mb-1">
            <CategoryBadge category={article.category} />
            <VerifiedBadge hasBias={article.hasBiasDetected} />
          </div>
          <h2 className="text-lg lg:text-base font-bold text-gray-900 group-hover:text-blue-600 transition-colors leading-tight line-clamp-2 mb-2 lg:mb-1">
            {article.title}
          </h2>
          <p className="text-gray-600 text-sm leading-relaxed lg:leading-snug line-clamp-2 flex-1">
            {article.subtitle}
          </p>
          <div className="mt-2 lg:mt-1 flex items-center gap-3 text-xs text-gray-500">
            <span className="flex items-center gap-1">
              <Clock size={12} />
              {date} às {time}
            </span>
          </div>
        </div>
      </article>
    </Link>
  );
}

// Notícias secundárias - layout horizontal (responsivo)
function SideFeaturedNews({ article }: { article: NewsArticle }) {
  const { date, time } = formatDateTime(article.createdAt);
  
  return (
    <Link href={`/noticia/${article.id}`} className="group block h-full">
      <article className="h-full flex bg-white rounded-lg overflow-hidden shadow-sm hover:shadow-md transition-shadow">
        {/* Imagem - largura responsiva: w-24 mobile, w-40 desktop */}
        <div className="w-24 lg:w-40 h-full flex-shrink-0 overflow-hidden bg-gray-100">
          <img
            src={article.imageUrl}
            alt={article.title}
            className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
          />
        </div>
        {/* Texto - padding responsivo: p-3 mobile, p-2 desktop */}
        <div className="flex-1 p-3 lg:p-2 flex flex-col justify-center">
          <div className="flex items-center gap-2 lg:gap-1 mb-1">
            <CategoryBadge category={article.category} />
            <VerifiedBadge hasBias={article.hasBiasDetected} />
          </div>
          <h3 className="text-sm font-bold text-gray-900 group-hover:text-blue-600 transition-colors leading-tight line-clamp-2">
            {article.title}
          </h3>
          <div className="mt-1 flex items-center gap-2 lg:gap-1 text-xs text-gray-500">
            <Clock size={10} />
            <span>{date} às {time}</span>
          </div>
        </div>
      </article>
    </Link>
  );
}

// Card padrão com imagem
function NewsCard({ article }: { article: NewsArticle }) {
  const { date, time } = formatDateTime(article.createdAt);
  
  return (
    <Link href={`/noticia/${article.id}`} className="group block">
      <article className="bg-white rounded-lg overflow-hidden border border-gray-100 hover:border-gray-200 hover:shadow-sm transition-all">
        <div className="aspect-[16/10] overflow-hidden bg-gray-100">
          <img
            src={article.imageUrl}
            alt={article.title}
            className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
          />
        </div>
        <div className="p-4">
          <div className="flex items-center gap-2 mb-2">
            <CategoryBadge category={article.category} />
            <VerifiedBadge hasBias={article.hasBiasDetected} />
          </div>
          <h3 className="font-bold text-gray-900 group-hover:text-blue-600 transition-colors line-clamp-3 leading-snug">
            {article.title}
          </h3>
          <p className="mt-2 text-sm text-gray-600 line-clamp-2">
            {article.subtitle}
          </p>
          <div className="mt-3 flex items-center justify-between">
            <div className="flex items-center gap-3 text-xs text-gray-500">
              <span className="flex items-center gap-1">
                <User size={12} />
                Redação NI
              </span>
              <span className="flex items-center gap-1">
                <Clock size={12} />
                {date} às {time}
              </span>
            </div>
          </div>
        </div>
      </article>
    </Link>
  );
}

// NOVO: Card compacto sem imagem (para diversificar a visualização)
function CompactNewsCard({ article }: { article: NewsArticle }) {
  const { date, time } = formatDateTime(article.createdAt);
  
  return (
    <Link href={`/noticia/${article.id}`} className="group block">
      <article className="bg-white rounded-lg p-4 border border-gray-100 hover:border-blue-200 hover:shadow-sm transition-all h-full flex flex-col">
        <div className="flex items-center gap-2 mb-2">
          <CategoryBadge category={article.category} />
          <VerifiedBadge hasBias={article.hasBiasDetected} />
        </div>
        <h3 className="font-bold text-gray-900 group-hover:text-blue-600 transition-colors line-clamp-2 leading-snug mb-2">
          {article.title}
        </h3>
        <p className="text-sm text-gray-600 line-clamp-3 flex-1">
          {article.subtitle}
        </p>
        <div className="mt-3 pt-3 border-t border-gray-100 flex items-center justify-between">
          <div className="flex items-center gap-1 text-xs text-gray-500">
            <User size={12} />
            <span>Redação NI</span>
          </div>
          <div className="flex items-center gap-1 text-xs text-gray-500">
            <Clock size={12} />
            <span>{date} às {time}</span>
          </div>
        </div>
        <div className="mt-2">
          <span className="text-blue-600 text-xs font-medium group-hover:underline flex items-center gap-1">
            Ler mais <ArrowRight size={12} />
          </span>
        </div>
      </article>
    </Link>
  );
}

function LoadingState() {
  return (
    <div className="flex flex-col items-center justify-center py-20">
      <Loader2 className="w-8 h-8 animate-spin text-blue-600 mb-4" />
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
        className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
      >
        Tentar novamente
      </button>
    </div>
  );
}

export default function Home() {
  const [newsArticles, setNewsArticles] = useState<NewsArticle[]>([]);
  const [loading, setLoading] = useState(true);
  const [loadingMore, setLoadingMore] = useState(false);
  const [error, setError] = useState(false);
  const [totalArticles, setTotalArticles] = useState(0);
  const [currentPage, setCurrentPage] = useState(1);

  // Carrega a primeira página (destaques + primeiras notícias)
  const loadInitialArticles = async () => {
    setLoading(true);
    setError(false);
    try {
      const { articles, total } = await fetchArticlesPaginated(1, INITIAL_LOAD);
      setNewsArticles(articles);
      setTotalArticles(total);
      setCurrentPage(1);
    } catch (err) {
      console.error('Erro ao carregar artigos:', err);
      setError(true);
    } finally {
      setLoading(false);
    }
  };

  // Carrega mais notícias (paginação)
  const loadMoreArticles = async () => {
    setLoadingMore(true);
    try {
      // Calcula quantos itens já foram carregados além dos destaques
      const loadedBeyondFeatured = newsArticles.length - FEATURED_COUNT;
      // Calcula a próxima "página" de itens
      const nextPage = Math.floor(loadedBeyondFeatured / ITEMS_PER_PAGE) + 2;
      
      const { articles: newArticles } = await fetchArticlesPaginated(
        nextPage,
        ITEMS_PER_PAGE
      );
      
      // Filtra artigos que já existem para evitar duplicatas
      const existingIds = new Set(newsArticles.map(a => a.id));
      const uniqueNewArticles = newArticles.filter(a => !existingIds.has(a.id));
      
      setNewsArticles(prev => [...prev, ...uniqueNewArticles]);
      setCurrentPage(nextPage);
    } catch (err) {
      console.error('Erro ao carregar mais artigos:', err);
    } finally {
      setLoadingMore(false);
    }
  };

  useEffect(() => {
    loadInitialArticles();
  }, []);

  // 1 destaque principal + 3 notícias ao lado = 4 notícias em destaque
  const mainFeatured = newsArticles[0];
  const sideFeatured = newsArticles.slice(1, FEATURED_COUNT);
  
  // Notícias restantes (excluindo as 4 em destaque)
  const remainingArticles = newsArticles.slice(FEATURED_COUNT);
  
  // Calcula se há mais notícias para carregar
  const totalRemaining = totalArticles - FEATURED_COUNT;
  const hasMore = remainingArticles.length < totalRemaining;

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50">
        <Header />
        <LoadingState />
        <Footer />
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50">
        <Header />
        <ErrorState onRetry={loadInitialArticles} />
        <Footer />
      </div>
    );
  }

  if (newsArticles.length === 0) {
    return (
      <div className="min-h-screen bg-gray-50">
        <Header />
        <div className="flex flex-col items-center justify-center py-20">
          <p className="text-gray-600">Nenhuma notícia disponível no momento.</p>
        </div>
        <Footer />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      
      <main>
        {/* Featured Section - Mosaico: destaque maior à esquerda, 3 menores à direita */}
        <section className="container py-4">
          <div className="grid lg:grid-cols-5 gap-3 lg:h-[380px]">
            {/* Main featured article - 3 colunas de 5 (60% largura) */}
            <div className="lg:col-span-3 h-full">
              {mainFeatured && <MainFeaturedNews article={mainFeatured} />}
            </div>
            
            {/* 3 notícias ao lado - 2 colunas de 5 (40% largura), dividem a altura igualmente */}
            <div className="lg:col-span-2 flex flex-col gap-2 h-full">
              {sideFeatured.map((article: NewsArticle) => (
                <div key={article.id} className="flex-1 min-h-0">
                  <SideFeaturedNews article={article} />
                </div>
              ))}
            </div>
          </div>
        </section>
        
        {/* Divider */}
        <div className="border-t border-gray-200" />
        
        {/* Remaining News Grid - Layout misto com cards com imagem e cards compactos */}
        {remainingArticles.length > 0 && (
          <section id="mais-noticias" className="container py-8">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-xl font-bold text-gray-900">
                Mais Notícias
              </h2>
              <div className="flex items-center gap-2 text-xs text-gray-500">
                <CheckCircle size={14} className="text-green-600" />
                <span>Todas verificadas e balanceadas</span>
              </div>
            </div>
            
            {/* Layout misto: primeira linha com cards com imagem, segunda linha com cards compactos */}
            <div className="space-y-6">
              {/* Primeira linha: cards com imagem (3 colunas) */}
              <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
                {remainingArticles.slice(0, 3).map((article: NewsArticle) => (
                  <NewsCard key={article.id} article={article} />
                ))}
              </div>
              
              {/* Segunda linha: cards compactos sem imagem (4 colunas para mais densidade) */}
              {remainingArticles.length > 3 && (
                <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-4">
                  {remainingArticles.slice(3, 7).map((article: NewsArticle) => (
                    <CompactNewsCard key={article.id} article={article} />
                  ))}
                </div>
              )}
              
              {/* Terceira linha em diante: alternando entre os dois estilos */}
              {remainingArticles.length > 7 && (
                <>
                  {/* Cards com imagem */}
                  <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
                    {remainingArticles.slice(7, 10).map((article: NewsArticle) => (
                      <NewsCard key={article.id} article={article} />
                    ))}
                  </div>
                  
                  {/* Cards compactos */}
                  {remainingArticles.length > 10 && (
                    <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-4">
                      {remainingArticles.slice(10, 14).map((article: NewsArticle) => (
                        <CompactNewsCard key={article.id} article={article} />
                      ))}
                    </div>
                  )}
                  
                  {/* Restante com cards com imagem */}
                  {remainingArticles.length > 14 && (
                    <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
                      {remainingArticles.slice(14).map((article: NewsArticle) => (
                        <NewsCard key={article.id} article={article} />
                      ))}
                    </div>
                  )}
                </>
              )}
            </div>
            
            {/* Load More Button */}
            {hasMore && (
              <div className="mt-8 text-center">
                <button
                  onClick={loadMoreArticles}
                  disabled={loadingMore}
                  className="inline-flex items-center gap-2 px-6 py-3 bg-gray-100 hover:bg-gray-200 text-gray-700 font-medium rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
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
          </section>
        )}
        
        {/* About Section - Minimal */}
        <section className="bg-white border-t border-gray-200">
          <div className="container py-12">
            <div className="max-w-2xl mx-auto text-center">
              <h2 className="text-lg font-bold text-gray-900 mb-3">
                Por que Notícias Imparciais?
              </h2>
              <p className="text-gray-600 text-sm leading-relaxed mb-4">
                Analisamos diferentes fontes de notícias, identificamos vieses editoriais 
                e apresentamos os fatos de forma neutra. Você decide, nós informamos.
              </p>
              <Link 
                href="/sobre" 
                className="inline-flex items-center gap-1 text-blue-600 text-sm font-medium hover:underline"
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
