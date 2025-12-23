import { useState } from "react";
import { Link } from "wouter";
import { Clock, CheckCircle, ArrowRight, AlertTriangle, ChevronDown } from "lucide-react";
import Header from "@/components/Header";
import Footer from "@/components/Footer";
import { newsArticles, type NewsArticle } from "@/data/news";

const ITEMS_PER_PAGE = 6;

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

// Notícia em destaque principal (proporção 3x3)
function MainFeaturedNews({ article }: { article: NewsArticle }) {
  return (
    <Link href={`/noticia/${article.id}`} className="group block h-full">
      <article className="relative h-full rounded-lg overflow-hidden bg-gray-900">
        <div className="absolute inset-0">
          <img
            src={article.imageUrl}
            alt={article.title}
            className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500 opacity-80"
          />
          <div className="absolute inset-0 bg-gradient-to-t from-black/90 via-black/40 to-transparent" />
        </div>
        <div className="relative h-full flex flex-col justify-end p-6">
          <div className="flex items-center gap-2 mb-3">
            <CategoryBadge category={article.category} />
            <VerifiedBadge hasBias={article.hasBiasDetected} />
          </div>
          <h2 className="text-2xl lg:text-3xl font-bold text-white group-hover:text-blue-300 transition-colors leading-tight mb-3">
            {article.title}
          </h2>
          <p className="text-gray-300 text-sm leading-relaxed line-clamp-2 mb-4">
            {article.subtitle}
          </p>
          <div className="flex items-center gap-2 text-xs text-gray-400">
            <Clock size={12} />
            <span>{article.date}</span>
          </div>
        </div>
      </article>
    </Link>
  );
}

// Notícias secundárias ao lado do destaque (flex-1 para ocupar altura igual)
function SideFeaturedNews({ article }: { article: NewsArticle }) {
  return (
    <Link href={`/noticia/${article.id}`} className="group block h-full">
      <article className="relative rounded-lg overflow-hidden bg-gray-900 h-full">
        <div className="absolute inset-0">
          <img
            src={article.imageUrl}
            alt={article.title}
            className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500 opacity-80"
          />
          <div className="absolute inset-0 bg-gradient-to-t from-black/90 via-black/40 to-transparent" />
        </div>
        <div className="relative h-full flex flex-col justify-end p-4">
          <div className="flex items-center gap-2 mb-2">
            <CategoryBadge category={article.category} />
            {article.hasBiasDetected && (
              <AlertTriangle size={10} className="text-amber-400" />
            )}
          </div>
          <h3 className="text-sm lg:text-base font-bold text-white group-hover:text-blue-300 transition-colors leading-tight line-clamp-2">
            {article.title}
          </h3>
          <div className="mt-2 flex items-center gap-2 text-xs text-gray-400">
            <Clock size={10} />
            <span>{article.date}</span>
          </div>
        </div>
      </article>
    </Link>
  );
}

function NewsCard({ article }: { article: NewsArticle }) {
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
            <div className="flex items-center gap-2 text-xs text-gray-500">
              <Clock size={12} />
              <span>{article.date}</span>
            </div>
            <span className="text-blue-600 text-xs font-medium group-hover:underline flex items-center gap-1">
              Ler mais <ArrowRight size={12} />
            </span>
          </div>
        </div>
      </article>
    </Link>
  );
}

export default function Home() {
  const [visibleCount, setVisibleCount] = useState(ITEMS_PER_PAGE);
  
  // 1 destaque principal + 3 notícias ao lado = 4 notícias em destaque
  const mainFeatured = newsArticles[0];
  const sideFeatured = newsArticles.slice(1, 4);
  
  // Notícias restantes (excluindo as 4 em destaque)
  const remainingArticles = newsArticles.slice(4);
  const visibleArticles = remainingArticles.slice(0, visibleCount);
  const hasMore = visibleCount < remainingArticles.length;

  const loadMore = () => {
    setVisibleCount(prev => Math.min(prev + ITEMS_PER_PAGE, remainingArticles.length));
  };

  return (
    <div className="min-h-screen bg-white">
      <Header />
      
      <main>
        {/* Featured Section - Destaque principal (65%) + 3 ao lado (35%) com mesma altura */}
        <section className="container py-6">
          <div className="grid lg:grid-cols-5 gap-4" style={{ minHeight: '500px' }}>
            {/* Main featured article - 3 colunas de 5 (60%) */}
            <div className="lg:col-span-3 h-full">
              <MainFeaturedNews article={mainFeatured} />
            </div>
            
            {/* 3 notícias ao lado - 2 colunas de 5 (40%), mesma altura total */}
            <div className="lg:col-span-2 flex flex-col gap-3 h-full">
              {sideFeatured.map((article: NewsArticle) => (
                <div key={article.id} className="flex-1">
                  <SideFeaturedNews article={article} />
                </div>
              ))}
            </div>
          </div>
        </section>
        
        {/* Divider */}
        <div className="border-t border-gray-200" />
        
        {/* Remaining News Grid - Notícias que não estão em destaque */}
        {remainingArticles.length > 0 && (
          <section className="container py-8">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-xl font-bold text-gray-900">
                Mais Notícias
              </h2>
              <div className="flex items-center gap-2 text-xs text-gray-500">
                <CheckCircle size={14} className="text-green-600" />
                <span>Todas verificadas e balanceadas</span>
              </div>
            </div>
            
            <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
              {visibleArticles.map((article: NewsArticle) => (
                <NewsCard key={article.id} article={article} />
              ))}
            </div>
            
            {/* Load More Button */}
            {hasMore && (
              <div className="mt-8 text-center">
                <button
                  onClick={loadMore}
                  className="inline-flex items-center gap-2 px-6 py-3 bg-gray-100 hover:bg-gray-200 text-gray-700 font-medium rounded-lg transition-colors"
                >
                  <span>Carregar mais notícias</span>
                  <ChevronDown size={18} />
                </button>
                <p className="mt-2 text-xs text-gray-500">
                  Mostrando {Math.min(visibleCount, remainingArticles.length)} de {remainingArticles.length} notícias adicionais
                </p>
              </div>
            )}
          </section>
        )}
        
        {/* About Section - Minimal */}
        <section className="bg-gray-50 border-t border-gray-200">
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
