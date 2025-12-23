import { Link } from "wouter";
import { Clock, AlertTriangle, CheckCircle } from "lucide-react";
import Header from "@/components/Header";
import Footer from "@/components/Footer";
import { newsArticles, NewsArticle } from "@/data/news";

export default function EconomiaPage() {
  const economiaNews = newsArticles.filter(
    (news: NewsArticle) => news.category.toLowerCase() === "economia"
  );

  return (
    <div className="min-h-screen flex flex-col bg-gray-50">
      <Header />
      
      <main className="flex-1">
        <div className="container py-8">
          {/* Page header */}
          <div className="mb-8">
            <h1 className="text-3xl font-bold text-gray-900 mb-2">Economia</h1>
            <p className="text-gray-600">
              {economiaNews.length} notícia{economiaNews.length !== 1 ? "s" : ""} sobre economia
            </p>
          </div>
          
          {/* News grid */}
          {economiaNews.length === 0 ? (
            <div className="text-center py-12">
              <p className="text-gray-500">Nenhuma notícia de economia disponível no momento</p>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {economiaNews.map((news: NewsArticle) => (
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
                      <span className="px-2 py-0.5 text-xs font-semibold rounded bg-green-600 text-white">
                        ECONOMIA
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
          )}
        </div>
      </main>
      
      <Footer />
    </div>
  );
}
