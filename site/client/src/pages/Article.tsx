import { Link, useParams } from "wouter";
import { ArrowLeft, Clock, Share2, CheckCircle, AlertTriangle, BookOpen } from "lucide-react";
import Header from "@/components/Header";
import Footer from "@/components/Footer";
import { newsArticles, type NewsArticle } from "@/data/news";
import { toast } from "sonner";

function CategoryBadge({ category }: { category: string }) {
  const colors: Record<string, string> = {
    "Política": "bg-red-600",
    "Economia": "bg-blue-600",
  };
  
  return (
    <span className={`${colors[category] || "bg-gray-600"} text-white text-xs font-bold px-2 py-1 rounded`}>
      {category.toUpperCase()}
    </span>
  );
}

function getArticleById(id: string): NewsArticle | undefined {
  return newsArticles.find(article => article.id === id);
}

export default function Article() {
  const params = useParams<{ id: string }>();
  const article = getArticleById(params.id || "");

  const handleShare = async () => {
    try {
      await navigator.share({
        title: article?.title,
        text: article?.subtitle,
        url: window.location.href,
      });
    } catch {
      navigator.clipboard.writeText(window.location.href);
      toast.success("Link copiado para a área de transferência!");
    }
  };

  if (!article) {
    return (
      <div className="min-h-screen bg-white">
        <Header />
        <main className="container py-16 text-center">
          <h1 className="text-2xl font-bold text-gray-900 mb-4">Notícia não encontrada</h1>
          <p className="text-gray-600 mb-6">A notícia que você procura não existe ou foi removida.</p>
          <Link href="/" className="text-blue-600 hover:underline">
            Voltar para a página inicial
          </Link>
        </main>
        <Footer />
      </div>
    );
  }

  // Split content into paragraphs
  const paragraphs = article.content.split('\n\n').filter(p => p.trim());

  return (
    <div className="min-h-screen bg-white">
      <Header />
      
      <main>
        {/* Breadcrumb */}
        <div className="border-b border-gray-100">
          <div className="container py-3">
            <nav className="flex items-center gap-2 text-sm text-gray-500">
              <Link href="/" className="hover:text-blue-600">Início</Link>
              <span>/</span>
              <span>{article.category}</span>
            </nav>
          </div>
        </div>

        {/* Article */}
        <article className="container py-8">
          <div className="max-w-3xl mx-auto">
            {/* Category and verification */}
            <div className="flex items-center gap-3 mb-4">
              <CategoryBadge category={article.category} />
              {article.hasBiasDetected ? (
                <span className="inline-flex items-center gap-1 text-amber-600 text-sm font-medium">
                  <AlertTriangle size={14} />
                  Viés detectado nas fontes
                </span>
              ) : (
                <span className="inline-flex items-center gap-1 text-green-600 text-sm font-medium">
                  <CheckCircle size={14} />
                  Notícia verificada
                </span>
              )}
            </div>

            {/* Title */}
            <h1 className="text-3xl lg:text-4xl font-bold text-gray-900 leading-tight mb-4">
              {article.title}
            </h1>

            {/* Subtitle */}
            <p className="text-xl text-gray-600 leading-relaxed mb-6">
              {article.subtitle}
            </p>

            {/* Meta */}
            <div className="flex items-center justify-between py-4 border-y border-gray-200 mb-8">
              <div className="flex items-center gap-4 text-sm text-gray-500">
                <span className="flex items-center gap-1">
                  <Clock size={14} />
                  {article.date}
                </span>
                <span className="flex items-center gap-1">
                  <BookOpen size={14} />
                  {Math.ceil(article.content.split(" ").length / 200)} min de leitura
                </span>
              </div>
              <button 
                onClick={handleShare}
                className="flex items-center gap-2 text-sm text-gray-500 hover:text-blue-600 transition-colors"
              >
                <Share2 size={16} />
                Compartilhar
              </button>
            </div>

            {/* Featured Image */}
            <div className="aspect-[16/9] overflow-hidden rounded-lg bg-gray-100 mb-8">
              <img
                src={article.imageUrl}
                alt={article.title}
                className="w-full h-full object-cover"
              />
            </div>

            {/* Summary */}
            <p className="text-lg text-gray-800 leading-relaxed mb-6 font-medium">
              {article.summary}
            </p>

            {/* Body */}
            <div className="mb-10">
              {paragraphs.map((paragraph, index) => (
                <p key={index} className="text-gray-700 leading-relaxed mb-4">
                  {paragraph}
                </p>
              ))}
            </div>

            {/* Perspectives Section - Only show if both perspectives exist */}
            {(article.hasLeftPerspective || article.hasRightPerspective) && (
              <section className="mb-10">
                <h2 className="text-xl font-bold text-gray-900 mb-6 pb-2 border-b border-gray-200">
                  O Que Diz Cada Lado
                </h2>
                
                <div className="grid md:grid-cols-2 gap-6">
                  {/* Left Perspective */}
                  {article.hasLeftPerspective && article.leftPerspective && (
                    <div className="bg-red-50 rounded-lg p-5 border-l-4 border-red-500">
                      <div className="flex items-center gap-2 mb-3">
                        <span className="w-3 h-3 rounded-full bg-red-500"></span>
                        <h3 className="font-bold text-gray-900">Fontes de esquerda</h3>
                      </div>
                      <p className="text-gray-700 text-sm leading-relaxed">
                        {article.leftPerspective}
                      </p>
                    </div>
                  )}

                  {/* Right Perspective */}
                  {article.hasRightPerspective && article.rightPerspective && (
                    <div className="bg-blue-50 rounded-lg p-5 border-l-4 border-blue-500">
                      <div className="flex items-center gap-2 mb-3">
                        <span className="w-3 h-3 rounded-full bg-blue-500"></span>
                        <h3 className="font-bold text-gray-900">Fontes de direita</h3>
                      </div>
                      <p className="text-gray-700 text-sm leading-relaxed">
                        {article.rightPerspective}
                      </p>
                    </div>
                  )}
                </div>
              </section>
            )}

            {/* Attention Points */}
            {article.attentionPoints.length > 0 && (
              <section className="bg-amber-50 rounded-lg p-6 mb-10 border border-amber-200">
                <div className="flex items-center gap-2 mb-4">
                  <AlertTriangle className="text-amber-600" size={20} />
                  <h2 className="font-bold text-gray-900">Pontos de Atenção</h2>
                </div>
                <ul className="space-y-2">
                  {article.attentionPoints.map((point: string, index: number) => (
                    <li key={index} className="flex items-start gap-2 text-sm text-gray-700">
                      <span className="w-1.5 h-1.5 rounded-full bg-amber-500 mt-2 flex-shrink-0"></span>
                      {point}
                    </li>
                  ))}
                </ul>
              </section>
            )}

            {/* Sources */}
            {article.sources.length > 0 && (
              <section className="mb-10">
                <h3 className="text-sm font-bold text-gray-500 uppercase tracking-wider mb-3">
                  Fontes Consultadas
                </h3>
                <div className="flex flex-wrap gap-2">
                  {article.sources.map((source: string, index: number) => (
                    <span 
                      key={index} 
                      className="px-3 py-1 bg-gray-100 text-gray-700 text-sm rounded-full"
                    >
                      {source}
                    </span>
                  ))}
                </div>
              </section>
            )}

            {/* Back link */}
            <Link 
              href="/" 
              className="inline-flex items-center gap-2 text-blue-600 hover:underline font-medium"
            >
              <ArrowLeft size={16} />
              Voltar para todas as notícias
            </Link>
          </div>
        </article>
      </main>
      
      <Footer />
    </div>
  );
}
