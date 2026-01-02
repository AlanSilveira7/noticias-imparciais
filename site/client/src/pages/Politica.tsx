/*
 * PÁGINA POLÍTICA - Axia News
 * Design: Fidelidade Editorial Clássica
 * Cor da editoria: Vermelho (#FF0000)
 */

import { useState, useEffect } from "react";
import Header from "@/components/Header";
import Footer from "@/components/Footer";
import NewsCard from "@/components/NewsCard";
import { fetchArticlesByCategoryPaginated, type NewsArticleFrontend } from "@/lib/supabase";
import { Loader2, ChevronDown } from "lucide-react";

type NewsArticle = NewsArticleFrontend;

const CATEGORY_COLOR = "#FF0000";
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
      <div className="min-h-screen flex flex-col bg-gray-100">
        <Header />
        <div className="flex-1 flex items-center justify-center">
          <Loader2 className="w-8 h-8 animate-spin" style={{ color: CATEGORY_COLOR }} />
        </div>
        <Footer />
      </div>
    );
  }

  return (
    <div className="min-h-screen flex flex-col bg-gray-100">
      <Header />
      
      <main className="flex-1">
        {/* Page header */}
        <div 
          className="py-8"
          style={{ 
            background: `linear-gradient(135deg, ${CATEGORY_COLOR}15 0%, transparent 100%)`,
            borderBottom: `4px solid ${CATEGORY_COLOR}`
          }}
        >
          <div className="container">
            <h1 
              className="text-3xl font-bold mb-2"
              style={{ 
                fontFamily: "'Encode Sans Semi Condensed', sans-serif",
                color: CATEGORY_COLOR 
              }}
            >
              POLÍTICA
            </h1>
            <p className="text-gray-600">
              {total} notícia{total !== 1 ? "s" : ""} sobre política
            </p>
          </div>
        </div>
        
        <div className="container py-8">
          {/* News grid - todas as notícias com o mesmo formato */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {articles.map((article) => (
              <NewsCard key={article.id} article={article} variant="featured" />
            ))}
          </div>

          {/* Load More Button */}
          {hasMore && (
            <div className="mt-8 text-center">
              <button
                onClick={loadMoreArticles}
                disabled={loadingMore}
                className="inline-flex items-center gap-2 px-6 py-3 text-white font-semibold rounded-lg transition-opacity hover:opacity-90 disabled:opacity-50"
                style={{ backgroundColor: CATEGORY_COLOR }}
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
