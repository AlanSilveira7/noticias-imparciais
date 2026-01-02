import { useState, useEffect } from "react";
import { Link, useParams } from "wouter";
import { ArrowLeft, Clock, Share2, CheckCircle, AlertTriangle, BookOpen, RefreshCw, LinkIcon, Loader2, User } from "lucide-react";
import Header from "@/components/Header";
import Footer from "@/components/Footer";
import { fetchArticleById, fetchArticlesByCategory, type NewsArticleFrontend } from "@/lib/supabase";
import { toast } from "sonner";

// Alias para manter compatibilidade
type NewsArticle = NewsArticleFrontend;

// Cores das editorias Axia News
const CATEGORY_COLORS: Record<string, { bg: string; text: string }> = {
  "Política": { bg: "#FF0000", text: "white" },
  "Economia": { bg: "#FF6B00", text: "white" },
  "Tecnologia": { bg: "#00A859", text: "white" },
};

function CategoryBadge({ category }: { category: string }) {
  const colors = CATEGORY_COLORS[category] || { bg: "#666666", text: "white" };
  
  return (
    <span 
      className="text-xs font-bold px-2 py-1 rounded"
      style={{ backgroundColor: colors.bg, color: colors.text }}
    >
      {category.toUpperCase()}
    </span>
  );
}

function LoadingState() {
  return (
    <div className="min-h-screen bg-white">
      <Header />
      <div className="flex flex-col items-center justify-center py-20">
        <Loader2 className="w-8 h-8 animate-spin text-red-600 mb-4" />
        <p className="text-gray-600">Carregando notícia...</p>
      </div>
      <Footer />
    </div>
  );
}

// Função para formatar data e hora a partir do createdAt
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

export default function Article() {
  const params = useParams<{ id: string }>();
  const [article, setArticle] = useState<NewsArticle | null>(null);
  const [relatedArticles, setRelatedArticles] = useState<NewsArticle[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadArticle() {
      setLoading(true);
      const fetchedArticle = await fetchArticleById(params.id || "");
      setArticle(fetchedArticle);
      
      // Carregar artigos relacionados por categoria
      if (fetchedArticle) {
        const categoryArticles = await fetchArticlesByCategory(fetchedArticle.category);
        const related = categoryArticles
          .filter(a => a.id !== fetchedArticle.id)
          .slice(0, 3);
        setRelatedArticles(related);
      }
      
      setLoading(false);
    }
    
    loadArticle();
  }, [params.id]);

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

  if (loading) {
    return <LoadingState />;
  }

  if (!article) {
    return (
      <div className="min-h-screen bg-white">
        <Header />
        <main className="container py-16 text-center">
          <h1 className="text-2xl font-bold text-gray-900 mb-4">Notícia não encontrada</h1>
          <p className="text-gray-600 mb-6">A notícia que você procura não existe ou foi removida.</p>
          <Link href="/" className="text-red-600 hover:underline">
            Voltar para a página inicial
          </Link>
        </main>
        <Footer />
      </div>
    );
  }

  // Split content into paragraphs
  const paragraphs = article.content.split('\n\n').filter(p => p.trim());
  
  // Check if article was updated
  const wasUpdated = article.updatedAt && article.updatedAt !== article.createdAt;
  const version = article.version || 1;
  
  // Formatar data e hora
  const { date: publishDate, time: publishTime } = formatDateTime(article.createdAt);
  const updateDateTime = wasUpdated ? formatDateTime(article.updatedAt!) : null;

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
            <div className="flex items-center gap-3 mb-4 flex-wrap">
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
              {/* Update indicator */}
              {wasUpdated && updateDateTime && (
                <span className="inline-flex items-center gap-1 text-blue-600 text-sm font-medium">
                  <RefreshCw size={14} />
                  Atualizada em {updateDateTime.date} às {updateDateTime.time}
                </span>
              )}
              {version > 1 && (
                <span className="text-xs text-gray-400">
                  v{version}
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

            {/* Meta - Melhorado com autor e hora */}
            <div className="flex flex-col sm:flex-row sm:items-center justify-between py-4 border-y border-gray-200 mb-8 gap-3">
              <div className="flex flex-wrap items-center gap-4 text-sm text-gray-500">
                {/* Autor */}
                <span className="flex items-center gap-1.5">
                  <User size={14} />
                  <span className="font-medium text-gray-700">Redação Axia News</span>
                </span>
                {/* Data e Hora */}
                <span className="flex items-center gap-1">
                  <Clock size={14} />
                  {publishDate} às {publishTime}
                </span>
                {/* Tempo de leitura */}
                <span className="flex items-center gap-1">
                  <BookOpen size={14} />
                  {Math.ceil(article.content.split(" ").length / 200)} min de leitura
                </span>
              </div>
              <button 
                onClick={handleShare}
                className="flex items-center gap-2 text-sm text-gray-500 hover:text-red-600 transition-colors"
              >
                <Share2 size={16} />
                Compartilhar
              </button>
            </div>

            {/* Featured Image with Caption */}
            <figure className="mb-8">
              <div className="aspect-[16/9] overflow-hidden rounded-lg bg-gray-100">
                <img
                  src={article.imageUrl}
                  alt={article.title}
                  loading="eager"
                  decoding="async"
                  fetchPriority="high"
                  className="w-full h-full object-cover"
                />
              </div>
              {/* Legenda e crédito da imagem */}
              <figcaption className="mt-2 text-sm text-gray-500 italic">
                {article.title} — Imagem ilustrativa / Reprodução
              </figcaption>
            </figure>

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

            {/* Related News Section */}
            {relatedArticles.length > 0 && (
              <section className="mb-10">
                <div className="flex items-center gap-2 mb-4">
                  <LinkIcon className="text-gray-600" size={18} />
                  <h2 className="text-lg font-bold text-gray-900">Notícias Relacionadas</h2>
                </div>
                <div className="grid gap-4">
                  {relatedArticles.map((related) => (
                    <Link 
                      key={related.id} 
                      href={`/noticia/${related.id}`}
                      className="flex gap-4 p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors group"
                    >
                      <div className="w-24 h-16 flex-shrink-0 overflow-hidden rounded bg-gray-200">
                        <img 
                          src={related.imageUrl} 
                          alt={related.title}
                          className="w-full h-full object-cover"
                        />
                      </div>
                      <div className="flex-1 min-w-0">
                        <h3 className="font-medium text-gray-900 group-hover:text-red-600 line-clamp-2 text-sm">
                          {related.title}
                        </h3>
                        <p className="text-xs text-gray-500 mt-1">
                          {related.date} • {related.category}
                        </p>
                      </div>
                    </Link>
                  ))}
                </div>
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
              className="inline-flex items-center gap-2 text-red-600 hover:underline font-medium"
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
