import { useState, useEffect } from "react";
import { useSearch } from "wouter";
import { Link } from "wouter";
import { Clock, AlertTriangle, CheckCircle, Search as SearchIcon, Loader2, ChevronDown } from "lucide-react";
import Header from "@/components/Header";
import Footer from "@/components/Footer";
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
    <div className="min-h-screen flex flex-col bg-gray-50">
      <Header />
      
      <main className="flex-1">
        <div className="container py-8">
          {/* Search header */}
          <div className="mb-8">
            <div className="flex items-center gap-3 mb-2">
              <SearchIcon className="w-6 h-6 text-gray-400" />
              <h1 className="text-2xl font-bold text-gray-900">
                Resultados da busca
              </h1>
            </div>
            {query && !loading && (
              <p className="text-gray-600">
                {total} resultado{total !== 1 ? "s" : ""} para "{query}"
              </p>
            )}
          </div>
          
          {/* Results */}
          {loading ? (
            <div className="flex items-center justify-center py-12">
              <Loader2 className="w-8 h-8 animate-spin text-blue-600" />
            </div>
          ) : !query ? (
            <div className="text-center py-12">
              <SearchIcon className="w-16 h-16 text-gray-300 mx-auto mb-4" />
              <p className="text-gray-500">Digite algo para buscar notícias</p>
            </div>
          ) : searchResults.length === 0 ? (
            <div className="text-center py-12">
              <SearchIcon className="w-16 h-16 text-gray-300 mx-auto mb-4" />
              <p className="text-gray-500">Nenhuma notícia encontrada para "{query}"</p>
              <p className="text-gray-400 text-sm mt-2">Tente buscar por outros termos</p>
            </div>
          ) : (
            <>
              <div className="space-y-4">
                {searchResults.map((news: NewsArticle) => (
                  <Link
                    key={news.id}
                    href={`/noticia/${news.id}`}
                    className="block bg-white rounded-lg border border-gray-200 overflow-hidden hover:shadow-md transition-shadow"
                  >
                    <div className="flex flex-col md:flex-row">
                      <div className="md:w-64 h-48 md:h-auto flex-shrink-0">
                        <img
                          src={news.imageUrl}
                          alt={news.title}
                          className="w-full h-full object-cover"
                        />
                      </div>
                      <div className="p-4 flex-1">
                        <div className="flex items-center gap-2 mb-2">
                          <span className={`px-2 py-0.5 text-xs font-semibold rounded uppercase ${
                            news.category.toLowerCase() === "política" 
                              ? "bg-blue-600 text-white" 
                              : "bg-green-600 text-white"
                          }`}>
                            {news.category}
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
                        <h2 className="text-lg font-bold text-gray-900 mb-2 line-clamp-2">
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
                    </div>
                  </Link>
                ))}
              </div>

              {/* Load More Button */}
              {hasMore && (
                <div className="mt-8 text-center">
                  <button
                    onClick={loadMore}
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
