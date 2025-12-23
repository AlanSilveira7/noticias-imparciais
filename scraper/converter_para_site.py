#!/usr/bin/env python3
"""
Script para converter notícias JSON para o formato TypeScript do site
"""

import json
import os
from datetime import datetime

# Caminhos
NOTICIAS_JSON = "/home/ubuntu/noticias_imparciais/scraper/data/noticias_22dez2025/noticias_imparciais.json"
SITE_DATA_FILE = "/home/ubuntu/noticias-imparciais/client/src/data/news.ts"

def gerar_id(titulo):
    """Gera um ID único baseado no título"""
    import re
    slug = titulo.lower()
    slug = re.sub(r'[áàâã]', 'a', slug)
    slug = re.sub(r'[éèê]', 'e', slug)
    slug = re.sub(r'[íìî]', 'i', slug)
    slug = re.sub(r'[óòôõ]', 'o', slug)
    slug = re.sub(r'[úùû]', 'u', slug)
    slug = re.sub(r'[ç]', 'c', slug)
    slug = re.sub(r'[^a-z0-9\s]', '', slug)
    slug = re.sub(r'\s+', '-', slug)
    return slug[:50]

def converter_noticias():
    """Converte notícias do JSON para formato TypeScript"""
    
    # Carregar notícias geradas
    with open(NOTICIAS_JSON, 'r', encoding='utf-8') as f:
        dados = json.load(f)
    
    noticias = dados.get('noticias', [])
    
    # Gerar código TypeScript
    ts_code = '''// Dados de notícias do portal Notícias Imparciais
// Atualizado em: ''' + datetime.now().strftime('%d/%m/%Y %H:%M') + '''

export interface NewsArticle {
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
}

// Imagens disponíveis para as notícias
const newsImages = [
  "/images/hero_balance.png",
  "/images/about_methodology.png",
  "/images/pattern_editorial.png",
  "https://images.unsplash.com/photo-1529107386315-e1a2ed48a620?w=800",
  "https://images.unsplash.com/photo-1504711434969-e33886168f5c?w=800",
  "https://images.unsplash.com/photo-1495020689067-958852a7765e?w=800",
  "https://images.unsplash.com/photo-1585829365295-ab7cd400c167?w=800",
  "https://images.unsplash.com/photo-1526304640581-d334cdbbf45e?w=800",
  "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=800",
  "https://images.unsplash.com/photo-1554224155-6726b3ff858f?w=800",
  "https://images.unsplash.com/photo-1590283603385-17ffb3a7f29f?w=800",
  "https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=800"
];

export const newsArticles: NewsArticle[] = [
'''
    
    for i, noticia in enumerate(noticias):
        id_noticia = gerar_id(noticia.get('titulo', f'noticia-{i}'))
        
        # Escapar strings para JavaScript
        def escape_js(s):
            if s is None:
                return 'null'
            return json.dumps(s, ensure_ascii=False)
        
        # Determinar categoria
        tema = noticia.get('tema', '')
        if 'economia' in tema.lower() or 'dólar' in tema.lower() or 'orçamento' in tema.lower():
            categoria = 'Economia'
        else:
            categoria = 'Política'
        
        # Selecionar imagem
        img_index = i % len(noticias)
        
        ts_code += f'''  {{
    id: "{id_noticia}",
    title: {escape_js(noticia.get('titulo', ''))},
    subtitle: {escape_js(noticia.get('subtitulo', ''))},
    summary: {escape_js(noticia.get('resumo', ''))},
    content: {escape_js(noticia.get('texto', ''))},
    category: "{categoria}",
    date: "{datetime.now().strftime('%d/%m/%Y')}",
    imageUrl: newsImages[{img_index}],
    hasLeftPerspective: {str(noticia.get('perspectiva_esquerda') is not None).lower()},
    leftPerspective: {escape_js(noticia.get('perspectiva_esquerda'))},
    hasRightPerspective: {str(noticia.get('perspectiva_direita') is not None).lower()},
    rightPerspective: {escape_js(noticia.get('perspectiva_direita'))},
    attentionPoints: {json.dumps(noticia.get('pontos_atencao', []), ensure_ascii=False)},
    sources: {json.dumps(noticia.get('fontes', []), ensure_ascii=False)},
    hasBiasDetected: {str(noticia.get('tem_vies_detectado', False)).lower()}
  }},
'''
    
    ts_code += '''];

export default newsArticles;
'''
    
    # Salvar arquivo TypeScript
    with open(SITE_DATA_FILE, 'w', encoding='utf-8') as f:
        f.write(ts_code)
    
    print(f"✅ Convertidas {len(noticias)} notícias para o site")
    print(f"📁 Arquivo salvo em: {SITE_DATA_FILE}")
    
    return len(noticias)

if __name__ == "__main__":
    converter_noticias()
