#!/usr/bin/env python3
"""
Script para atualizar o arquivo news.ts do site com ACÚMULO de notícias.
Inclui sistema de DEDUPLICAÇÃO INTELIGENTE para evitar duplicatas e
linkar notícias relacionadas.

Projeto: Notícias Imparciais
Data: 23/12/2025
Versão: 2.0 - Com deduplicação
"""

import json
import os
import re
import requests
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Tuple, Optional

# Importar módulos de deduplicação
import sys
sys.path.insert(0, str(Path(__file__).parent))
from similaridade import calcular_similaridade, classificar_similaridade
from deduplicacao import GerenciadorDeduplicacao, processar_com_deduplicacao

# Deploy Hook do Vercel para disparar deploy automático
VERCEL_DEPLOY_HOOK = "https://api.vercel.com/v1/integrations/deploy/prj_voMU8PT7Aj80coLKjayjtnDB5yNi/9GsbAASQml"

# Diretórios
SCRAPER_DATA_DIR = Path(__file__).parent / 'data'
SITE_DATA_DIR = Path(__file__).parent.parent / 'site' / 'client' / 'src' / 'data'


def disparar_deploy_vercel():
    """Dispara o deploy no Vercel via Deploy Hook."""
    try:
        print("\n[9] Disparando deploy no Vercel...")
        response = requests.post(VERCEL_DEPLOY_HOOK)
        if response.status_code == 200 or response.status_code == 201:
            print("    ✓ Deploy disparado com sucesso!")
            return True
        else:
            print(f"    ✗ Erro ao disparar deploy: {response.status_code}")
            print(f"      Resposta: {response.text}")
            return False
    except Exception as e:
        print(f"    ✗ Erro ao disparar deploy: {e}")
        return False


def gerar_id_slug(titulo: str) -> str:
    """Gera um ID slug a partir do título."""
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
    
    slug = re.sub(r'[^a-z0-9\s-]', '', slug)
    slug = re.sub(r'\s+', '-', slug)
    slug = re.sub(r'-+', '-', slug)
    slug = slug[:50].rstrip('-')
    
    return slug


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
        'sources': ['UOL', 'G1/Globo', 'Revista Oeste', 'Brasil Paralelo'],
        'hasBiasDetected': tem_vies,
        # Novos campos para deduplicação
        'version': 1,
        'createdAt': data_publicacao,
        'updatedAt': None,
        'relatedNews': [],
        'originalId': None
    }


def gerar_news_ts(noticias: list) -> str:
    """Gera o conteúdo do arquivo news.ts com suporte aos novos campos."""
    
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
        # Novos campos
        n.setdefault('version', 1)
        n.setdefault('createdAt', n.get('date', ''))
        n.setdefault('updatedAt', None)
        n.setdefault('relatedNews', [])
        n.setdefault('originalId', None)
    
    # Cabeçalho do arquivo
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
  // Campos de versionamento e relacionamento
  version: number;
  createdAt: string;
  updatedAt: string | null;
  relatedNews: string[];
  originalId: string | null;
}}

'''
    
    # Gerar array de notícias
    noticias_ts = []
    for n in noticias:
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
    
    return content


def main():
    """Função principal com deduplicação inteligente."""
    print("=" * 60)
    print("ATUALIZADOR DE SITE - NOTÍCIAS IMPARCIAIS")
    print("Versão 2.0 - Com Deduplicação Inteligente")
    print(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    print("=" * 60)
    
    # 1. Carregar notícias imparciais novas
    print("\n[1] Carregando notícias imparciais geradas...")
    noticias_novas_raw = carregar_noticias_imparciais()
    print(f"    - {len(noticias_novas_raw)} notícias novas para processar")
    
    if not noticias_novas_raw:
        print("\n⚠ Nenhuma notícia nova encontrada. Encerrando.")
        return {'novas': 0, 'total': 0}
    
    # 2. Converter novas notícias para formato do site
    print("\n[2] Convertendo notícias para formato do site...")
    data_hoje = datetime.now().strftime('%d/%m/%Y')
    noticias_convertidas = []
    
    for noticia in noticias_novas_raw:
        convertida = converter_para_formato_site(noticia, data_hoje)
        noticias_convertidas.append(convertida)
        print(f"    + {convertida['title'][:50]}...")
    
    # 3. Carregar histórico
    print("\n[3] Carregando histórico de notícias...")
    historico_path = SCRAPER_DATA_DIR / 'historico_noticias_site.json'
    
    if historico_path.exists():
        with open(historico_path, 'r', encoding='utf-8') as f:
            historico = json.load(f)
    else:
        historico = []
    
    print(f"    - {len(historico)} notícias no histórico")
    
    # 4. DEDUPLICAÇÃO INTELIGENTE
    print("\n[4] Executando deduplicação inteligente...")
    
    gerenciador = GerenciadorDeduplicacao(
        dias_comparacao=2,
        limiar_duplicata=0.85,
        limiar_relacionada=0.50
    )
    
    noticias_processadas, historico_atualizado = gerenciador.processar_noticias(
        noticias_convertidas,
        historico
    )
    
    # 5. Mesclar: processadas + histórico (sem duplicatas)
    print("\n[5] Mesclando notícias (novas no topo)...")
    
    ids_processados = {n['id'] for n in noticias_processadas}
    historico_sem_atualizadas = [n for n in historico_atualizado if n['id'] not in ids_processados]
    
    todas_noticias = noticias_processadas + historico_sem_atualizadas
    
    # Remover duplicatas mantendo a mais recente
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
    
    # 8. Estatísticas finais
    print("\n[8] Estatísticas de deduplicação:")
    print(f"    - Notícias novas: {gerenciador.stats['novas']}")
    print(f"    - Notícias atualizadas: {gerenciador.stats['atualizadas']}")
    print(f"    - Com relacionadas: {gerenciador.stats['relacionadas']}")
    
    print("\n" + "=" * 60)
    print("ATUALIZAÇÃO CONCLUÍDA!")
    print(f"  - {len(noticias_processadas)} notícias processadas")
    print(f"  - {len(noticias_unicas)} notícias totais no site")
    print("=" * 60)
    
    # 9. Disparar deploy no Vercel
    disparar_deploy_vercel()
    
    return {
        'novas': gerenciador.stats['novas'],
        'atualizadas': gerenciador.stats['atualizadas'],
        'relacionadas': gerenciador.stats['relacionadas'],
        'total': len(noticias_unicas)
    }


if __name__ == '__main__':
    main()
