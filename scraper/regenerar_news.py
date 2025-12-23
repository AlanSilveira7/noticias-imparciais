#!/usr/bin/env python3
"""Script para regenerar o news.ts a partir do histórico limpo."""

import json
from pathlib import Path
from datetime import datetime

SCRAPER_DATA_DIR = Path(__file__).parent / 'data'
SITE_DATA_DIR = Path(__file__).parent.parent / 'site' / 'client' / 'src' / 'data'

# Carregar histórico limpo
historico_path = SCRAPER_DATA_DIR / 'historico_noticias_site.json'
with open(historico_path, 'r', encoding='utf-8') as f:
    noticias = json.load(f)

print(f'Gerando news.ts com {len(noticias)} notícias...')

# Garantir campos
for n in noticias:
    n.setdefault('id', 'sem-id')
    n.setdefault('title', 'Sem título')
    n.setdefault('subtitle', '')
    n.setdefault('summary', '')
    n.setdefault('content', '')
    n.setdefault('category', 'Política')
    n.setdefault('date', datetime.now().strftime('%d/%m/%Y'))
    n.setdefault('imageUrl', '/images/noticias/planalto.jpg')
    n.setdefault('hasLeftPerspective', False)
    n.setdefault('leftPerspective', None)
    n.setdefault('hasRightPerspective', False)
    n.setdefault('rightPerspective', None)
    n.setdefault('attentionPoints', [])
    n.setdefault('sources', [])
    n.setdefault('hasBiasDetected', False)
    n.setdefault('version', 1)
    n.setdefault('createdAt', n.get('date', ''))
    n.setdefault('updatedAt', None)
    n.setdefault('relatedNews', [])
    n.setdefault('originalId', None)

data_atual = datetime.now().strftime('%d/%m/%Y %H:%M')

header = f'''// Dados de notícias do portal Notícias Imparciais
// Atualizado em: {data_atual}
// Total de notícias: {len(noticias)}
// Sistema de deduplicação: ATIVO

export interface NewsArticle {{
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
}}

'''

def escape_ts(s):
    if s is None:
        return 'null'
    s = str(s).replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')
    return f'"{s}"'

def escape_array(arr):
    if not arr:
        return '[]'
    items = [escape_ts(item) for item in arr]
    return '[' + ', '.join(items) + ']'

noticias_ts = []
for n in noticias:
    noticia_ts = f'''  {{
    id: {escape_ts(n['id'])},
    title: {escape_ts(n['title'])},
    subtitle: {escape_ts(n['subtitle'])},
    summary: {escape_ts(n['summary'])},
    content: {escape_ts(n['content'])},
    category: {escape_ts(n['category'])},
    date: {escape_ts(n['date'])},
    imageUrl: {escape_ts(n['imageUrl'])},
    hasLeftPerspective: {str(n['hasLeftPerspective']).lower()},
    leftPerspective: {escape_ts(n['leftPerspective']) if n['leftPerspective'] else 'null'},
    hasRightPerspective: {str(n['hasRightPerspective']).lower()},
    rightPerspective: {escape_ts(n['rightPerspective']) if n['rightPerspective'] else 'null'},
    attentionPoints: {escape_array(n['attentionPoints'])},
    sources: {escape_array(n['sources'])},
    hasBiasDetected: {str(n['hasBiasDetected']).lower()},
    version: {n.get('version', 1)},
    createdAt: {escape_ts(n.get('createdAt', n['date']))},
    updatedAt: {escape_ts(n.get('updatedAt')) if n.get('updatedAt') else 'null'},
    relatedNews: {escape_array(n.get('relatedNews', []))},
    originalId: {escape_ts(n.get('originalId')) if n.get('originalId') else 'null'}
  }}'''
    noticias_ts.append(noticia_ts)

content = header + 'export const newsArticles: NewsArticle[] = [\n'
content += ',\n'.join(noticias_ts)
content += '\n];\n'

news_ts_path = SITE_DATA_DIR / 'news.ts'
with open(news_ts_path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f'news.ts gerado com sucesso: {news_ts_path}')
print(f'Total: {len(noticias)} notícias')
