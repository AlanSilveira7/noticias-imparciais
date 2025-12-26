import { useState, useEffect } from "react";
import { Link } from "wouter";
import { Clock, AlertTriangle, CheckCircle, Loader2, ChevronDown } from "lucide-react";
import Header from "@/components/Header";
import Footer from "@/components/Footer";
import { fetchArticlesByCategoryPaginated, type NewsArticleFrontend } from "@/lib/supabase";

type NewsArticle = NewsArticleFrontend;

const ITEMS_PER_PAGE = 12;

export default function PoliticaPage() {
  const [articles, setArticles] = useState<NewsArticle[]>([]);
  const [loading, setLoading] = useState(true);
  const [loadingMore, setLoadingMore] = useState(false);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);

  const loadInitialArticles = async () => {
    setLoading(true);
    const result = await fetchArticlesByCategoryPaginated("Política", 1, ITEMS_PER_PAGE);
    setArticles(result.articles);
    setTotal(result.total);
    setPage(1);
    setLoading(false);
  };

  const loadMoreArticles = async () => {
    setLoadingMore(true);
    const nextPage = page + 1;
    const result = await fetchArticlesByCategoryPaginated("Política", nextPage, ITEMS_PER_PAGE);
    setArticles(prev => [...prev, ...result.articles]);
    setPage(nextPage);
    setLoadingMore(false);
  };

  useEffect(() => {
    loadInitialArticles();
  }, []);

  const hasMore = articles.length < total;

  if (loading) {
    return (
      <div className="min-h-screen flex flex-col bg-gray-50">
        <Header />
        <div className="flex-1 flex items-center justify-center">
          <Loader2 className="w-8 h-8 animate-spin text-blue-600" />
        </div>
        <Footer />
      </div>
    );
  }

  return (
    <div className="min-h-screen flex flex-col bg-gray-50">
      <Header />
      
      <main className="flex-1">
        <div className="container py-8">
          {/* Page header */}
          <div className="mb-8">
            <h1 className="text-3xl font-bold text-gray-900 mb-2">Política</h1>
            <p className="text-gray-600">
              {total} notícia{total !== 1 ? "s" : ""} sobre política
            </p>
          </div>
          
          {/* News grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {articles.map((news: NewsArticle) => (
              <Link
                key={news.id}
                href={`/noticia/${news.id}`}
                className="bg-white rounded-lg border border-gray-200 overflow-hidden hover:shadow-md transition-shadow group"
              >
                <div className="aspect-video overflow-hidden">
                  <img
                    src={news.imageUrl}
                    alt={news.title}
                    className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                  />
                </div>
                <div className="p-4">
                  <div className="flex items-center gap-2 mb-2">
                    <span className="px-2 py-0.5 text-xs font-semibold rounded bg-blue-600 text-white">
                      POLÍTICA
                    </span>
                    {news.hasBiasDetected ? (
                      <span className="flex items-center gap-1 text-xs text-amber-600">
                        <AlertTriangle size={12} />
                        Viés Detectado
                      </span>
                    ) : (
                      <span className="flex items-center gap-1 text-xs text-green-600">
                        <CheckCircle size={12} />
                        Verificada
                      </span>
                    )}
                  </div>
                  <h2 className="text-lg font-bold text-gray-900 mb-2 line-clamp-2 group-hover:text-blue-600 transition-colors">
                    {news.title}
                  </h2>
                  <p className="text-gray-600 text-sm mb-3 line-clamp-2">
                    {news.subtitle}
                  </p>
                  <div className="flex items-center gap-1 text-xs text-gray-500">
                    <Clock size={12} />
                    <span>{news.date}</span>
                  </div>
                </div>
              </Link>
            ))}
          </div>

          {/* Load More Button */}
          {hasMore && (
            <div className="mt-8 text-center">
              <button
                onClick={loadMoreArticles}
                disabled={loadingMore}
                className="inline-flex items-center gap-2 px-6 py-3 bg-gray-100 hover:bg-gray-200 text-gray-700 font-medium rounded-lg transition-colors disabled:opacity-50"
              >
                {loadingMore ? (
                  <>
                    <Loader2 className="w-4 h-4 animate-spin" />
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
                Mostrando {articles.length} de {total} notícias
              </p>
            </div>
          )}
        </div>
      </main>
      
      <Footer />
    </div>
  );
}
