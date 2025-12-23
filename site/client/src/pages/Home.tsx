import { useState } from "react";
import { Link } from "wouter";
import { Clock, CheckCircle, ArrowRight, AlertTriangle, ChevronDown } from "lucide-react";
import Header from "@/components/Header";
import Footer from "@/components/Footer";
import QuotesWidget from "@/components/QuotesWidget";
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

// Função para encontrar notícias relacionadas (mesmo tema/categoria)
function getRelatedNews(article: NewsArticle, allNews: NewsArticle[], limit: number = 3): NewsArticle[] {
  const keywords = article.title.toLowerCase().split(' ').filter(w => w.length > 4);
  
  return allNews
    .filter(news => news.id !== article.id)
    .map(news => {
      let score = 0;
      // Mesma categoria = +2
      if (news.category === article.category) score += 2;
      // Palavras em comum no título = +1 cada
      keywords.forEach(keyword => {
        if (news.title.toLowerCase().includes(keyword)) score += 1;
      });
      return { news, score };
    })
    .filter(item => item.score > 0)
    .sort((a, b) => b.score - a.score)
    .slice(0, limit)
    .map(item => item.news);
}

function FeaturedNews({ article, relatedNews }: { article: NewsArticle; relatedNews: NewsArticle[] }) {
  return (
    <div>
      <Link href={`/noticia/${article.id}`} className="group block">
        <article className="relative">
          <div className="aspect-[16/10] overflow-hidden rounded-lg bg-gray-100">
            <img
              src={article.imageUrl}
              alt={article.title}
              className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
            />
          </div>
          <div className="mt-4">
            <div className="flex items-center gap-2 mb-2">
              <CategoryBadge category={article.category} />
              <VerifiedBadge hasBias={article.hasBiasDetected} />
            </div>
            <h2 className="text-2xl lg:text-3xl font-bold text-gray-900 group-hover:text-blue-600 transition-colors leading-tight">
              {article.title}
            </h2>
            <p className="mt-2 text-gray-600 text-base leading-relaxed line-clamp-3">
              {article.subtitle}
            </p>
            <div className="mt-3 flex items-center gap-2 text-xs text-gray-500">
              <Clock size={12} />
              <span>{article.date}</span>
            </div>
          </div>
        </article>
      </Link>
      
      {/* Notícias Relacionadas */}
      {relatedNews.length > 0 && (
        <div className="mt-4 pt-4 border-t border-gray-200">
          <h3 className="text-xs font-bold text-gray-500 uppercase tracking-wider mb-2">
            Veja também sobre este tema
          </h3>
          <ul className="space-y-1">
            {relatedNews.map((news) => (
              <li key={news.id}>
                <Link 
                  href={`/noticia/${news.id}`}
                  className="text-sm text-gray-700 hover:text-blue-600 transition-colors flex items-start gap-2"
                >
                  <span className="text-blue-600 mt-1">•</span>
                  <span className="line-clamp-1">{news.title}</span>
                </Link>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

function SecondaryNews({ article }: { article: NewsArticle }) {
  return (
    <Link href={`/noticia/${article.id}`} className="group block">
      <article className="flex gap-4 py-4 border-b border-gray-100 last:border-0">
        <div className="w-32 h-20 flex-shrink-0 overflow-hidden rounded bg-gray-100">
          <img
            src={article.imageUrl}
            alt={article.title}
            className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
          />
        </div>
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 mb-1">
            <CategoryBadge category={article.category} />
            {article.hasBiasDetected && (
              <AlertTriangle size={12} className="text-amber-500" />
            )}
          </div>
          <h3 className="font-semibold text-gray-900 group-hover:text-blue-600 transition-colors line-clamp-2 text-sm leading-snug">
            {article.title}
          </h3>
          <div className="mt-1 flex items-center gap-2 text-xs text-gray-500">
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
  
  const featuredArticle = newsArticles[0];
  const secondaryArticles = newsArticles.slice(1, 4);
  const allArticles = newsArticles;
  const visibleArticles = allArticles.slice(0, visibleCount);
  const hasMore = visibleCount < allArticles.length;
  
  // Notícias relacionadas à manchete principal
  const relatedToFeatured = getRelatedNews(featuredArticle, newsArticles, 3);

  const loadMore = () => {
    setVisibleCount(prev => Math.min(prev + ITEMS_PER_PAGE, allArticles.length));
  };

  return (
    <div className="min-h-screen bg-white">
      <Header />
      
      <main>
        {/* Featured Section */}
        <section className="container py-6">
          <div className="grid lg:grid-cols-3 gap-6">
            {/* Main featured article */}
            <div className="lg:col-span-2">
              <FeaturedNews article={featuredArticle} relatedNews={relatedToFeatured} />
            </div>
            
            {/* Sidebar */}
            <div className="space-y-6">
              {/* Widget de Cotações */}
              <QuotesWidget />
              
              {/* Secondary articles */}
              <div className="lg:border-t lg:border-gray-200 lg:pt-6">
                <h2 className="text-xs font-bold text-gray-500 uppercase tracking-wider mb-4">
                  Mais notícias
                </h2>
                <div>
                  {secondaryArticles.map((article: NewsArticle) => (
                    <SecondaryNews key={article.id} article={article} />
                  ))}
                </div>
              </div>
            </div>
          </div>
        </section>
        
        {/* Divider */}
        <div className="border-t border-gray-200" />
        
        {/* All News Grid */}
        <section className="container py-8">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-xl font-bold text-gray-900">
              Últimas Notícias
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
                Mostrando {visibleCount} de {allArticles.length} notícias
              </p>
            </div>
          )}
        </section>
        
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
