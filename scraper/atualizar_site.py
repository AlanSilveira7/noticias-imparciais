#!/usr/bin/env python3
"""
Script para atualizar o arquivo news.ts do site com ACÚMULO de notícias.
Mantém o histórico de notícias antigas e adiciona as novas no topo.
Projeto: Notícias Imparciais
Data: 23/12/2025
"""

import json
import os
import re
from datetime import datetime
from pathlib import Path

# Diretórios
SCRAPER_DATA_DIR = Path(__file__).parent / 'data'
SITE_DATA_DIR = Path(__file__).parent.parent / 'site' / 'client' / 'src' / 'data'

def gerar_id_slug(titulo: str) -> str:
    """Gera um ID slug a partir do título."""
    # Remove acentos e caracteres especiais
    slug = titulo.lower()
    substituicoes = {
        'á': 'a', 'à': 'a', 'ã': 'a', 'â': 'a',
        'é': 'e', 'ê': 'e',
        'í': 'i',
        'ó': 'o', 'ô': 'o', 'õ': 'o',
        'ú': 'u', 'ü': 'u',
        'ç': 'c',
    }
    for orig, subst in substituicoes.items():
        slug = slug.replace(orig, subst)
    
    # Remove caracteres não alfanuméricos
    slug = re.sub(r'[^a-z0-9\s-]', '', slug)
    # Substitui espaços por hífens
    slug = re.sub(r'\s+', '-', slug)
    # Remove hífens duplicados
    slug = re.sub(r'-+', '-', slug)
    # Limita o tamanho
    slug = slug[:50].rstrip('-')
    
    return slug


def carregar_noticias_existentes() -> list:
    """Carrega as notícias existentes do arquivo news.ts."""
    news_ts_path = SITE_DATA_DIR / 'news.ts'
    
    if not news_ts_path.exists():
        return []
    
    # Ler o arquivo
    with open(news_ts_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extrair IDs existentes para evitar duplicatas
    ids_existentes = re.findall(r'id:\s*["\']([^"\']+)["\']', content)
    
    return ids_existentes


def carregar_noticias_imparciais() -> list:
    """Carrega as notícias imparciais geradas."""
    arquivo = SCRAPER_DATA_DIR / 'noticias_imparciais.json'
    
    if not arquivo.exists():
        print(f"Arquivo não encontrado: {arquivo}")
        return []
    
    with open(arquivo, 'r', encoding='utf-8') as f:
        dados = json.load(f)
    
    return dados.get('noticias', [])


def converter_para_formato_site(noticia: dict, data_publicacao: str) -> dict:
    """Converte uma notícia do formato JSON para o formato do site."""
    
    titulo = noticia.get('titulo', 'Sem título')
    id_slug = gerar_id_slug(titulo)
    
    # Montar o conteúdo completo
    corpo = noticia.get('corpo', [])
    if isinstance(corpo, list):
        conteudo = '\n\n'.join(corpo)
    else:
        conteudo = str(corpo)
    
    # Determinar categoria
    secao = noticia.get('secao', 'politica').lower()
    categoria = 'Política' if 'polit' in secao else 'Economia'
    
    # Perspectivas
    esquerda = noticia.get('o_que_diz_esquerda', '')
    direita = noticia.get('o_que_diz_direita', '')
    
    # Pontos de atenção
    pontos = noticia.get('pontos_atencao', [])
    if isinstance(pontos, str):
        pontos = [pontos]
    
    # Fontes
    fontes_esq = noticia.get('fontes_esquerda', ['UOL', 'G1/Globo'])
    fontes_dir = noticia.get('fontes_direita', ['Revista Oeste', 'Brasil Paralelo'])
    
    # Determinar se há viés detectado
    tem_vies = bool(esquerda and direita)
    
    return {
        'id': id_slug,
        'title': titulo,
        'subtitle': noticia.get('subtitulo', ''),
        'summary': noticia.get('lead', ''),
        'content': conteudo,
        'category': categoria,
        'date': data_publicacao,
        'imageUrl': f'/images/noticias/{"planalto" if categoria == "Política" else "b3_touro"}.jpg',
        'hasLeftPerspective': bool(esquerda),
        'leftPerspective': esquerda if esquerda else None,
        'hasRightPerspective': bool(direita),
        'rightPerspective': direita if direita else None,
        'attentionPoints': pontos,
        'sources': list(set(['UOL', 'G1/Globo'] + ['Revista Oeste', 'Brasil Paralelo'])),
        'hasBiasDetected': tem_vies
    }


def gerar_news_ts(noticias: list) -> str:
    """Gera o conteúdo do arquivo news.ts."""
    
    data_atual = datetime.now().strftime('%d/%m/%Y %H:%M')
    
    # Garantir que todas as notícias tenham os campos necessários
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
    
    # Cabeçalho do arquivo
    header = f'''// Dados de notícias do portal Notícias Imparciais
// Atualizado em: {data_atual}
// Total de notícias: {len(noticias)}

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
}}

'''
    
    # Gerar array de notícias
    noticias_ts = []
    for n in noticias:
        # Escapar strings para TypeScript
        def escape_ts(s):
            if s is None:
                return 'null'
            s = str(s).replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')
            return f'"{s}"'
        
        def escape_array(arr):
            if not arr:
                return '[]'
            items = [escape_ts(item) for item in arr]
            return f'[{", ".join(items)}]'
        
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
    hasBiasDetected: {str(n['hasBiasDetected']).lower()}
  }}'''
        noticias_ts.append(noticia_ts)
    
    # Montar arquivo completo
    content = header + 'export const newsArticles: NewsArticle[] = [\n'
    content += ',\n'.join(noticias_ts)
    content += '\n];\n'
    
    return content


def main():
    """Função principal."""
    print("=" * 60)
    print("ATUALIZADOR DE SITE - NOTÍCIAS IMPARCIAIS")
    print(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    print("=" * 60)
    
    # 1. Carregar IDs existentes
    print("\n[1] Verificando notícias existentes no site...")
    ids_existentes = carregar_noticias_existentes()
    print(f"    - {len(ids_existentes)} notícias já publicadas")
    
    # 2. Carregar notícias imparciais novas
    print("\n[2] Carregando notícias imparciais geradas...")
    noticias_novas = carregar_noticias_imparciais()
    print(f"    - {len(noticias_novas)} notícias novas para processar")
    
    # 3. Converter novas notícias
    print("\n[3] Convertendo notícias para formato do site...")
    data_hoje = datetime.now().strftime('%d/%m/%Y')
    noticias_convertidas = []
    
    for noticia in noticias_novas:
        convertida = converter_para_formato_site(noticia, data_hoje)
        
        # Verificar se já existe (evitar duplicatas)
        if convertida['id'] not in ids_existentes:
            noticias_convertidas.append(convertida)
            print(f"    + Nova: {convertida['title'][:50]}...")
        else:
            print(f"    = Já existe: {convertida['title'][:50]}...")
    
    print(f"    - {len(noticias_convertidas)} notícias novas a adicionar")
    
    # 4. Carregar notícias existentes completas do arquivo JSON de backup
    print("\n[4] Carregando histórico de notícias...")
    historico_path = SCRAPER_DATA_DIR / 'historico_noticias_site.json'
    
    if historico_path.exists():
        with open(historico_path, 'r', encoding='utf-8') as f:
            historico = json.load(f)
    else:
        historico = []
    
    print(f"    - {len(historico)} notícias no histórico")
    
    # 5. Mesclar: novas no topo + histórico
    print("\n[5] Mesclando notícias (novas no topo)...")
    
    # Adicionar novas ao início
    todas_noticias = noticias_convertidas + historico
    
    # Remover duplicatas mantendo a mais recente (primeira ocorrência)
    ids_vistos = set()
    noticias_unicas = []
    for n in todas_noticias:
        if n['id'] not in ids_vistos:
            noticias_unicas.append(n)
            ids_vistos.add(n['id'])
    
    print(f"    - Total após mesclagem: {len(noticias_unicas)} notícias")
    
    # 6. Salvar histórico atualizado
    print("\n[6] Salvando histórico atualizado...")
    with open(historico_path, 'w', encoding='utf-8') as f:
        json.dump(noticias_unicas, f, ensure_ascii=False, indent=2)
    print(f"    ✓ Histórico salvo: {historico_path}")
    
    # 7. Gerar arquivo news.ts
    print("\n[7] Gerando arquivo news.ts...")
    news_ts_content = gerar_news_ts(noticias_unicas)
    
    news_ts_path = SITE_DATA_DIR / 'news.ts'
    with open(news_ts_path, 'w', encoding='utf-8') as f:
        f.write(news_ts_content)
    
    print(f"    ✓ Arquivo gerado: {news_ts_path}")
    
    print("\n" + "=" * 60)
    print("ATUALIZAÇÃO CONCLUÍDA!")
    print(f"  - {len(noticias_convertidas)} notícias novas adicionadas")
    print(f"  - {len(noticias_unicas)} notícias totais no site")
    print("=" * 60)
    
    return {
        'novas': len(noticias_convertidas),
        'total': len(noticias_unicas)
    }


if __name__ == '__main__':
    main()
