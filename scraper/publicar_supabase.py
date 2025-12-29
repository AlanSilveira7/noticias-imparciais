#!/usr/bin/env python3
"""
PUBLICADOR SUPABASE - NOTÍCIAS IMPARCIAIS
==========================================
Este script é um ADAPTADOR que substitui a publicação no arquivo news.ts
pela publicação no Supabase.

Ele lê o arquivo noticias_imparciais.json gerado pelo processar_noticias.py
e publica as notícias no banco de dados Supabase.

IMPORTANTE: Este script NÃO altera o fluxo original de coleta e processamento.
Ele apenas adapta a etapa de publicação.

Fluxo Original:
1. scraper_browser.py → Coleta notícias reais dos sites
2. processar_noticias.py → Analisa viés e gera notícias imparciais
3. publicar_supabase.py → Publica no Supabase (este script)

ATUALIZAÇÃO v2.0 (29/12/2025):
- Integração com análise semântica para seleção de imagens contextuais
- Prioriza tema/conceito sobre pessoas na seleção de imagens
- Usa mapeamento inteligente: FGTS→carteira de trabalho, indulto→presídio, etc.

Versão: 2.0
Data: 29/12/2025
"""

import json
import os
import re
import uuid
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional

# Carregar variáveis de ambiente
from dotenv import load_dotenv
load_dotenv(Path(__file__).parent.parent / '.env')

# Importar Supabase
from supabase import create_client

# Importar módulos de seleção de imagens
import sys
sys.path.insert(0, str(Path(__file__).parent))
from analisador_contexto import analisar_titulo, PESSOAS_CONHECIDAS

# Configurações
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_SERVICE_KEY = os.getenv('SUPABASE_SERVICE_KEY')
R2_ACCESS_KEY = os.getenv('R2_ACCESS_KEY_ID')
R2_SECRET_KEY = os.getenv('R2_SECRET_ACCESS_KEY')
R2_BUCKET = os.getenv('R2_BUCKET_NAME')
R2_ACCOUNT_ID = os.getenv('R2_ACCOUNT_ID')
R2_ENDPOINT = f"https://{R2_ACCOUNT_ID}.r2.cloudflarestorage.com" if R2_ACCOUNT_ID else None
R2_PUBLIC_URL = os.getenv('R2_PUBLIC_URL')

# Diretórios
DATA_DIR = Path(__file__).parent / 'data'
ACERVO_DIR = Path(__file__).parent.parent / 'acervo_temas'

# Mapeamento de análise semântica para imagens específicas do acervo
MAPEAMENTO_IMAGENS_ACERVO = {
    # Temas específicos (conceitos)
    'fgts': 'economia/carteira_trabalho_01.jpeg',
    'abono salarial': 'economia/carteira_trabalho_01.jpeg',
    'indulto': 'seguranca/presidio_alcacuz_01.jpeg',
    'prisão': 'seguranca/presidio_alcacuz_01.jpeg',
    'acareação': 'judiciario/stf_plenario_05.jpeg',
    'julgamento': 'judiciario/stf_plenario_05.jpeg',
    'inflação': 'economia/banco_central_sede_01.jpg',
    'selic': 'economia/banco_central_sede_01.jpg',
    'bolsa': 'economia/b3_pregao_02.jpg',
    'dólar': 'economia/banco_central_sede_01.jpg',
    'eleição': 'eleicoes/urna_eletronica_votacao_01.jpg',
    'votação': 'legislativo/camara_plenario_votacao_01.jpg',
    
    # Instituições
    'stf': 'judiciario/stf_plenario_05.jpeg',
    'congresso': 'executivo/congresso_panorama_01.jpg',
    'câmara': 'legislativo/camara_plenario_votacao_01.jpg',
    'senado': 'legislativo/camara_plenario_votacao_01.jpg',
    'planalto': 'executivo/planalto_fachada_02.jpg',
    'banco central': 'economia/banco_central_sede_01.jpg',
    
    # Pessoas
    'bolsonaro': 'pessoas/bolsonaro_01.jpg',
    'augusto heleno': 'pessoas/augusto_heleno_03.jpeg',
    'general heleno': 'pessoas/augusto_heleno_03.jpeg',
    'heleno': 'pessoas/augusto_heleno_03.jpeg',
    'alexandre de moraes': 'pessoas/alexandre_moraes_03.jpeg',
    'moraes': 'pessoas/alexandre_moraes_03.jpeg',
    'lula': 'pessoas/lula_oficial_03.jpeg',
    
    # Categorias fallback
    'economia': 'economia/banco_central_sede_01.jpg',
    'judiciario': 'judiciario/stf_plenario_05.jpeg',
    'seguranca': 'seguranca/presidio_alcacuz_01.jpeg',
    'executivo': 'executivo/planalto_fachada_02.jpg',
    'legislativo': 'legislativo/camara_plenario_votacao_01.jpg',
    'eleicoes': 'eleicoes/urna_eletronica_votacao_01.jpg',
    'pessoas': 'executivo/planalto_fachada_02.jpg',
}


def log(msg: str, level: str = "INFO"):
    """Log formatado com timestamp."""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] [{level}] {msg}")


def gerar_slug(titulo: str) -> str:
    """Gera um slug a partir do título."""
    slug = titulo.lower()
    substituicoes = {
        'á': 'a', 'à': 'a', 'ã': 'a', 'â': 'a',
        'é': 'e', 'ê': 'e', 'í': 'i',
        'ó': 'o', 'ô': 'o', 'õ': 'o',
        'ú': 'u', 'ü': 'u', 'ç': 'c',
    }
    for orig, subst in substituicoes.items():
        slug = slug.replace(orig, subst)
    
    slug = re.sub(r'[^a-z0-9\s-]', '', slug)
    slug = re.sub(r'\s+', '-', slug)
    slug = re.sub(r'-+', '-', slug)
    slug = slug[:50].rstrip('-')
    
    return slug


def carregar_noticias_imparciais() -> List[dict]:
    """Carrega as notícias imparciais geradas pelo processar_noticias.py."""
    arquivo = DATA_DIR / 'noticias_imparciais.json'
    
    if not arquivo.exists():
        log(f"Arquivo não encontrado: {arquivo}", "ERROR")
        return []
    
    with open(arquivo, 'r', encoding='utf-8') as f:
        dados = json.load(f)
    
    return dados.get('noticias', [])


def fazer_upload_imagem(imagem_path: str, titulo: str) -> str:
    """Faz upload da imagem para o Cloudflare R2."""
    try:
        import boto3
        
        if not os.path.exists(imagem_path):
            log(f"Imagem não encontrada: {imagem_path}", "WARN")
            return f"{R2_PUBLIC_URL}/noticias/acervo_v4/planalto_fachada_01.jpg"
        
        s3 = boto3.client(
            's3',
            endpoint_url=R2_ENDPOINT,
            aws_access_key_id=R2_ACCESS_KEY,
            aws_secret_access_key=R2_SECRET_KEY
        )
        
        # Gerar nome único para a imagem
        slug = gerar_slug(titulo)[:30]
        ext = os.path.splitext(imagem_path)[1]
        nome_arquivo = f"{slug}_{uuid.uuid4().hex[:8]}{ext}"
        chave_r2 = f"noticias/imagens/{nome_arquivo}"
        
        # Upload
        content_type = 'image/jpeg' if ext.lower() in ['.jpg', '.jpeg'] else 'image/png'
        if ext.lower() == '.webp':
            content_type = 'image/webp'
        
        s3.upload_file(
            imagem_path,
            R2_BUCKET,
            chave_r2,
            ExtraArgs={'ContentType': content_type}
        )
        
        url_publica = f"{R2_PUBLIC_URL}/{chave_r2}"
        log(f"  ✓ Upload: {nome_arquivo}")
        
        return url_publica
        
    except Exception as e:
        log(f"  ✗ Erro no upload: {e}", "ERROR")
        return f"{R2_PUBLIC_URL}/noticias/acervo_v4/planalto_fachada_01.jpg"


def selecionar_imagem_semantica(titulo: str) -> str:
    """
    Seleciona a melhor imagem do acervo usando análise semântica.
    
    Prioridade:
    1. Tema específico (FGTS, indulto, acareação, etc.)
    2. Pessoa (quando é o foco principal)
    3. Categoria genérica (fallback)
    """
    analise = analisar_titulo(titulo)
    
    log(f"  📊 Análise: tema={analise['tema_principal']}, tipo={analise['tipo_contexto']}")
    
    # 1. Se deve usar foto de pessoa específica
    if analise['usar_foto_pessoa'] and analise['pessoa_identificada']:
        pessoa_lower = analise['pessoa_identificada'].lower()
        for key, imagem in MAPEAMENTO_IMAGENS_ACERVO.items():
            if key in pessoa_lower or pessoa_lower in key:
                imagem_path = str(ACERVO_DIR / imagem)
                if os.path.exists(imagem_path):
                    log(f"  🖼️ Selecionado (pessoa): {imagem}")
                    return imagem_path
    
    # 2. Buscar pelo tema específico
    if analise['tema_principal']:
        tema = analise['tema_principal'].lower()
        if tema in MAPEAMENTO_IMAGENS_ACERVO:
            imagem = MAPEAMENTO_IMAGENS_ACERVO[tema]
            imagem_path = str(ACERVO_DIR / imagem)
            if os.path.exists(imagem_path):
                log(f"  🖼️ Selecionado (tema): {imagem}")
                return imagem_path
    
    # 3. Buscar por palavras no título que correspondam ao mapeamento
    titulo_lower = titulo.lower()
    for key, imagem in MAPEAMENTO_IMAGENS_ACERVO.items():
        if key in titulo_lower:
            imagem_path = str(ACERVO_DIR / imagem)
            if os.path.exists(imagem_path):
                log(f"  🖼️ Selecionado (palavra-chave): {imagem}")
                return imagem_path
    
    # 4. Fallback para categoria
    categoria = analise['categoria_acervo']
    if categoria in MAPEAMENTO_IMAGENS_ACERVO:
        imagem = MAPEAMENTO_IMAGENS_ACERVO[categoria]
        imagem_path = str(ACERVO_DIR / imagem)
        if os.path.exists(imagem_path):
            log(f"  🖼️ Fallback (categoria {categoria}): {imagem}")
            return imagem_path
    
    # 5. Fallback final
    fallback = str(ACERVO_DIR / "executivo" / "planalto_fachada_02.jpg")
    log(f"  ⚠️ Usando fallback genérico")
    return fallback


def selecionar_e_fazer_upload_imagem(titulo: str) -> str:
    """Seleciona imagem do acervo usando análise semântica e faz upload para R2."""
    
    # Usar análise semântica para selecionar a melhor imagem
    imagem_path = selecionar_imagem_semantica(titulo)
    
    if not imagem_path or not os.path.exists(imagem_path):
        log(f"  ⚠️ Imagem não encontrada para: {titulo[:40]}...", "WARN")
        imagem_path = str(ACERVO_DIR / "executivo" / "planalto_fachada_02.jpg")
    
    return fazer_upload_imagem(imagem_path, titulo)


def verificar_duplicata(supabase, titulo: str) -> bool:
    """Verifica se já existe uma notícia com título similar."""
    try:
        # Buscar notícias com título similar
        response = supabase.table('articles').select('title').execute()
        
        titulo_normalizado = titulo.lower().strip()
        
        for art in response.data:
            titulo_existente = art['title'].lower().strip()
            # Verificar se os títulos são muito similares
            if titulo_normalizado == titulo_existente:
                return True
            # Verificar se um contém o outro (para títulos parcialmente iguais)
            if len(titulo_normalizado) > 30 and len(titulo_existente) > 30:
                if titulo_normalizado[:30] == titulo_existente[:30]:
                    return True
        
        return False
        
    except Exception as e:
        log(f"Erro ao verificar duplicata: {e}", "WARN")
        return False


def publicar_noticia(supabase, noticia: dict, imagem_url: str) -> bool:
    """Publica uma notícia no Supabase."""
    
    try:
        # Preparar corpo
        corpo = noticia.get('corpo', [])
        if isinstance(corpo, list):
            conteudo = '\n\n'.join(corpo)
        else:
            conteudo = str(corpo)
        
        # Extrair perspectivas
        esquerda = noticia.get('o_que_diz_esquerda', '')
        direita = noticia.get('o_que_diz_direita', '')
        
        # Determinar categoria
        secao = noticia.get('secao', 'politica').lower()
        categoria = 'Política' if 'polit' in secao else 'Economia'
        
        # Determinar se há viés detectado
        # IMPORTANTE: Só marca como viés detectado se AMBAS as perspectivas existirem
        # e forem diferentes (não apenas "não há informações")
        tem_perspectiva_esquerda = bool(esquerda and 
            'não há' not in esquerda.lower() and 
            'não foram' not in esquerda.lower() and
            'nenhuma' not in esquerda.lower())
        tem_perspectiva_direita = bool(direita and 
            'não há' not in direita.lower() and 
            'não foram' not in direita.lower() and
            'nenhuma' not in direita.lower())
        
        tem_vies = tem_perspectiva_esquerda and tem_perspectiva_direita
        
        # Pontos de atenção
        pontos = noticia.get('pontos_atencao', [])
        if isinstance(pontos, str):
            pontos = [pontos]
        
        # Fontes consultadas
        fontes = ['UOL', 'G1/Globo', 'Revista Oeste', 'Brasil Paralelo']
        
        dados = {
            'id': str(uuid.uuid4()),
            'title': noticia.get('titulo', ''),
            'subtitle': noticia.get('subtitulo', ''),
            'summary': noticia.get('lead', ''),
            'content': conteudo,
            'category': categoria,
            'date': datetime.now().strftime('%d/%m/%Y'),
            'image_url': imagem_url,
            'has_left_perspective': tem_perspectiva_esquerda,
            'left_perspective': esquerda if tem_perspectiva_esquerda else '',
            'has_right_perspective': tem_perspectiva_direita,
            'right_perspective': direita if tem_perspectiva_direita else '',
            'attention_points': pontos,
            'sources': fontes,
            'has_bias_detected': tem_vies,
            'version': 1,
            'created_at': datetime.now().isoformat(),
            'updated_at': None,
            'related_news': [],
            'original_id': None
        }
        
        # Inserir no Supabase
        resultado = supabase.table('articles').insert(dados).execute()
        
        if resultado.data:
            log(f"  ✓ Publicado: {noticia.get('titulo', '')[:50]}...")
            return True
        else:
            log(f"  ✗ Erro ao publicar", "ERROR")
            return False
            
    except Exception as e:
        log(f"  ✗ Erro no Supabase: {e}", "ERROR")
        return False


def main():
    """Função principal - Publica notícias imparciais no Supabase."""
    
    print("\n" + "=" * 70)
    print("📤 PUBLICADOR SUPABASE - NOTÍCIAS IMPARCIAIS v2.0")
    print("   (com análise semântica para seleção de imagens)")
    print(f"📅 Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    print("=" * 70)
    
    # Verificar configurações
    if not SUPABASE_URL or not SUPABASE_SERVICE_KEY:
        log("Credenciais do Supabase não configuradas!", "ERROR")
        return {'publicadas': 0, 'duplicadas': 0, 'erros': 0}
    
    # Conectar ao Supabase
    log("Conectando ao Supabase...")
    supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
    
    # Carregar notícias imparciais
    log("Carregando notícias imparciais...")
    noticias = carregar_noticias_imparciais()
    
    if not noticias:
        log("Nenhuma notícia encontrada para publicar.", "WARN")
        return {'publicadas': 0, 'duplicadas': 0, 'erros': 0}
    
    log(f"  → {len(noticias)} notícias para processar")
    
    # Estatísticas
    stats = {
        'publicadas': 0,
        'duplicadas': 0,
        'erros': 0
    }
    
    # Processar cada notícia
    for i, noticia in enumerate(noticias, 1):
        titulo = noticia.get('titulo', 'Sem título')
        log(f"\n[{i}/{len(noticias)}] {titulo[:50]}...")
        
        # Verificar duplicata
        if verificar_duplicata(supabase, titulo):
            log(f"  ⏭️ Duplicata - pulando")
            stats['duplicadas'] += 1
            continue
        
        # Selecionar e fazer upload de imagem (com análise semântica)
        imagem_url = selecionar_e_fazer_upload_imagem(titulo)
        
        # Publicar
        if publicar_noticia(supabase, noticia, imagem_url):
            stats['publicadas'] += 1
        else:
            stats['erros'] += 1
    
    # Relatório final
    print("\n" + "=" * 70)
    print("📊 RELATÓRIO FINAL")
    print("=" * 70)
    print(f"  ✅ Notícias publicadas: {stats['publicadas']}")
    print(f"  ⏭️ Duplicatas ignoradas: {stats['duplicadas']}")
    print(f"  ❌ Erros: {stats['erros']}")
    print("=" * 70)
    
    return stats


if __name__ == '__main__':
    main()
