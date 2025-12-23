import { useState, useEffect } from "react";
import { useSearch } from "wouter";
import { Link } from "wouter";
import { Clock, AlertTriangle, CheckCircle, Search as SearchIcon, Loader2 } from "lucide-react";
import Header from "@/components/Header";
import Footer from "@/components/Footer";
import { searchArticles, type NewsArticleFrontend } from "@/lib/supabase";

type NewsArticle = NewsArticleFrontend;

export default function SearchPage() {
  const searchString = useSearch();
  const params = new URLSearchParams(searchString);
  const query = params.get("q") || "";
  
  const [searchResults, setSearchResults] = useState<NewsArticle[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    async function performSearch() {
      if (!query) {
        setSearchResults([]);
        return;
      }
      
      setLoading(true);
      const results = await searchArticles(query);
      setSearchResults(results);
      setLoading(false);
    }
    
    performSearch();
  }, [query]);

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
                {searchResults.length} resultado{searchResults.length !== 1 ? "s" : ""} para "{query}"
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
          )}
        </div>
      </main>
      
      <Footer />
    </div>
  );
}
