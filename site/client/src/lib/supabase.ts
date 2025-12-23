import { createClient } from '@supabase/supabase-js';

// Configurações do Supabase
const supabaseUrl = import.meta.env.VITE_SUPABASE_URL || 'https://rlrnqrgempxjymhiisua.supabase.co';
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY || 'sb_publishable_lQCq61WfKT5M65vUSvYhxA_I4VJOP0p';

export const supabase = createClient(supabaseUrl, supabaseAnonKey);

// Interface do artigo (compatível com o banco de dados)
export interface NewsArticle {
  id: string;
  title: string;
  subtitle: string;
  summary: string;
  content: string;
  category: string;
  date: string;
  image_url: string;
  has_left_perspective: boolean;
  left_perspective: string | null;
  has_right_perspective: boolean;
  right_perspective: string | null;
  attention_points: string[];
  sources: string[];
  has_bias_detected: boolean;
  version: number;
  created_at: string;
  updated_at: string | null;
  related_news: string[];
  original_id: string | null;
}

// Interface do artigo para o frontend (camelCase)
export interface NewsArticleFrontend {
  id: string;
  title: string;
  subtitle: string;
  summary: string;
  content: string;
  category: string;
  date: string;
  imageUrl: string;
  hasLeftPerspective: boolean;
  leftPerspective: string | null;
  hasRightPerspective: boolean;
  rightPerspective: string | null;
  attentionPoints: string[];
  sources: string[];
  hasBiasDetected: boolean;
  version: number;
  createdAt: string;
  updatedAt: string | null;
  relatedNews: string[];
  originalId: string | null;
}

// Função para converter snake_case para camelCase
export function convertToFrontend(article: NewsArticle): NewsArticleFrontend {
  return {
    id: article.id,
    title: article.title,
    subtitle: article.subtitle,
    summary: article.summary,
    content: article.content,
    category: article.category,
    date: article.date,
    imageUrl: article.image_url,
    hasLeftPerspective: article.has_left_perspective,
    leftPerspective: article.left_perspective,
    hasRightPerspective: article.has_right_perspective,
    rightPerspective: article.right_perspective,
    attentionPoints: article.attention_points || [],
    sources: article.sources || [],
    hasBiasDetected: article.has_bias_detected,
    version: article.version,
    createdAt: article.created_at,
    updatedAt: article.updated_at,
    relatedNews: article.related_news || [],
    originalId: article.original_id,
  };
}

// Buscar todas as notícias
export async function fetchAllArticles(): Promise<NewsArticleFrontend[]> {
  const { data, error } = await supabase
    .from('articles')
    .select('*')
    .order('created_at', { ascending: false });

  if (error) {
    console.error('Erro ao buscar artigos:', error);
    return [];
  }

  return (data || []).map(convertToFrontend);
}

// Buscar notícias com paginação
export async function fetchArticlesPaginated(
  page: number = 1,
  pageSize: number = 10
): Promise<{ articles: NewsArticleFrontend[]; total: number }> {
  const from = (page - 1) * pageSize;
  const to = from + pageSize - 1;

  const { data, error, count } = await supabase
    .from('articles')
    .select('*', { count: 'exact' })
    .order('created_at', { ascending: false })
    .range(from, to);

  if (error) {
    console.error('Erro ao buscar artigos paginados:', error);
    return { articles: [], total: 0 };
  }

  return {
    articles: (data || []).map(convertToFrontend),
    total: count || 0,
  };
}

// Buscar notícia por ID
export async function fetchArticleById(id: string): Promise<NewsArticleFrontend | null> {
  const { data, error } = await supabase
    .from('articles')
    .select('*')
    .eq('id', id)
    .single();

  if (error) {
    console.error('Erro ao buscar artigo:', error);
    return null;
  }

  return data ? convertToFrontend(data) : null;
}

// Buscar notícias por categoria
export async function fetchArticlesByCategory(category: string): Promise<NewsArticleFrontend[]> {
  const { data, error } = await supabase
    .from('articles')
    .select('*')
    .eq('category', category)
    .order('created_at', { ascending: false });

  if (error) {
    console.error('Erro ao buscar artigos por categoria:', error);
    return [];
  }

  return (data || []).map(convertToFrontend);
}

// Buscar notícias por termo de pesquisa
export async function searchArticles(searchTerm: string): Promise<NewsArticleFrontend[]> {
  const { data, error } = await supabase
    .from('articles')
    .select('*')
    .or(`title.ilike.%${searchTerm}%,subtitle.ilike.%${searchTerm}%,content.ilike.%${searchTerm}%`)
    .order('created_at', { ascending: false });

  if (error) {
    console.error('Erro ao buscar artigos:', error);
    return [];
  }

  return (data || []).map(convertToFrontend);
}
