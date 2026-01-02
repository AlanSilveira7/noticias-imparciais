/*
 * PÁGINA DE BUSCA - Axia News
 * Design: Fidelidade Editorial Clássica
 */

import { useState, useEffect } from "react";
import { useSearch } from "wouter";
import { Search as SearchIcon, Loader2, ChevronDown } from "lucide-react";
import Header from "@/components/Header";
import Footer from "@/components/Footer";
import NewsCard from "@/components/NewsCard";
import { searchArticlesPaginated, type NewsArticleFrontend } from "@/lib/supabase";

type NewsArticle = NewsArticleFrontend;

const ITEMS_PER_PAGE = 12;

export default function SearchPage() {
  const searchString = useSearch();
  const params = new URLSearchParams(searchString);
  const query = params.get("q") || "";
  
  const [searchResults, setSearchResults] = useState<NewsArticle[]>([]);
  const [loading, setLoading] = useState(false);
  const [loadingMore, setLoadingMore] = useState(false);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);

  const performSearch = async (searchQuery: string, pageNum: number = 1, append: boolean = false) => {
    if (!searchQuery) {
      setSearchResults([]);
      setTotal(0);
      return;
    }
    
    if (append) {
      setLoadingMore(true);
    } else {
      setLoading(true);
    }
    
    const result = await searchArticlesPaginated(searchQuery, pageNum, ITEMS_PER_PAGE);
    
    if (append) {
      setSearchResults(prev => [...prev, ...result.articles]);
    } else {
      setSearchResults(result.articles);
    }
    setTotal(result.total);
    setPage(pageNum);
    
    setLoading(false);
    setLoadingMore(false);
  };

  useEffect(() => {
    performSearch(query, 1, false);
  }, [query]);

  const loadMore = () => {
    performSearch(query, page + 1, true);
  };

  const hasMore = searchResults.length < total;

  return (
    <div className="min-h-screen flex flex-col bg-gray-100">
      <Header />
      
      <main className="flex-1">
        {/* Search header */}
        <div 
          className="py-8 bg-white border-b"
          style={{ borderBottomColor: '#0A1F44', borderBottomWidth: '4px' }}
        >
          <div className="container">
            <div className="flex items-center gap-3 mb-2">
              <SearchIcon className="w-6 h-6 text-gray-400" />
              <h1 
                className="text-2xl font-bold"
                style={{ 
                  fontFamily: "'Encode Sans Semi Condensed', sans-serif",
                  color: '#0A1F44'
                }}
              >
                RESULTADOS DA BUSCA
              </h1>
            </div>
            {query && !loading && (
              <p className="text-gray-600">
                {total} resultado{total !== 1 ? "s" : ""} para "<strong>{query}</strong>"
              </p>
            )}
          </div>
        </div>
        
        <div className="container py-8">
          {/* Results */}
          {loading ? (
            <div className="flex items-center justify-center py-12">
              <Loader2 className="w-8 h-8 animate-spin text-red-600" />
            </div>
          ) : !query ? (
            <div className="text-center py-12 bg-white rounded-lg shadow-sm">
              <SearchIcon className="w-16 h-16 text-gray-300 mx-auto mb-4" />
              <p className="text-gray-500">Digite algo para buscar notícias</p>
            </div>
          ) : searchResults.length === 0 ? (
            <div className="text-center py-12 bg-white rounded-lg shadow-sm">
              <SearchIcon className="w-16 h-16 text-gray-300 mx-auto mb-4" />
              <p className="text-gray-500">Nenhuma notícia encontrada para "{query}"</p>
              <p className="text-gray-400 text-sm mt-2">Tente buscar por outros termos</p>
            </div>
          ) : (
            <>
              {/* Results grid */}
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {searchResults.map((article) => (
                  <NewsCard key={article.id} article={article} variant="featured" />
                ))}
              </div>

              {/* Load More Button */}
              {hasMore && (
                <div className="mt-8 text-center">
                  <button
                    onClick={loadMore}
                    disabled={loadingMore}
                    className="inline-flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-red-600 to-orange-500 text-white font-semibold rounded-lg transition-opacity hover:opacity-90 disabled:opacity-50"
                  >
                    {loadingMore ? (
                      <>
                        <Loader2 className="w-4 h-4 animate-spin" />
                        <span>Carregando...</span>
                      </>
                    ) : (
                      <>
                        <span>Carregar mais resultados</span>
                        <ChevronDown size={18} />
                      </>
                    )}
                  </button>
                  <p className="mt-2 text-xs text-gray-500">
                    Mostrando {searchResults.length} de {total} resultados
                  </p>
                </div>
              )}
            </>
          )}
        </div>
      </main>
      
      <Footer />
    </div>
  );
}
