#!/usr/bin/env python3
"""
Processador de Imagens para Notícias
Portal Notícias Imparciais

Este módulo integra:
1. Busca de imagem relevante no Unsplash
2. Upload para Cloudflare R2
3. Atualização da URL no Supabase

Data: 26/12/2025
"""

import os
import re
import boto3
import requests
import hashlib
from pathlib import Path
from typing import Optional, Dict
from dotenv import load_dotenv
from supabase import create_client

# Importar módulo Unsplash
from unsplash_service import obter_imagem_para_noticia, baixar_imagem

# Carregar variáveis de ambiente
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(env_path)

# Configurações R2
R2_ACCOUNT_ID = os.getenv('R2_ACCOUNT_ID')
R2_ACCESS_KEY_ID = os.getenv('R2_ACCESS_KEY_ID')
R2_SECRET_ACCESS_KEY = os.getenv('R2_SECRET_ACCESS_KEY')
R2_BUCKET_NAME = os.getenv('R2_BUCKET_NAME')
R2_PUBLIC_URL = os.getenv('R2_PUBLIC_URL')

# Configurações Supabase
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_ANON_KEY')

# Diretório temporário para downloads
TEMP_DIR = Path(__file__).parent / 'temp_images'
TEMP_DIR.mkdir(exist_ok=True)


def criar_cliente_r2():
    """Cria cliente S3 compatível com R2."""
    return boto3.client(
        's3',
        endpoint_url=f'https://{R2_ACCOUNT_ID}.r2.cloudflarestorage.com',
        aws_access_key_id=R2_ACCESS_KEY_ID,
        aws_secret_access_key=R2_SECRET_ACCESS_KEY,
        region_name='auto'
    )


def gerar_nome_arquivo(titulo: str, unsplash_id: str) -> str:
    """
    Gera um nome de arquivo único baseado no título e ID do Unsplash.
    
    Args:
        titulo: Título da notícia
        unsplash_id: ID da imagem no Unsplash
    
    Returns:
        Nome do arquivo (sem extensão)
    """
    # Criar slug do título
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
    slug = slug[:40].rstrip('-')
    
    # Adicionar parte do ID do Unsplash para garantir unicidade
    return f"{slug}_{unsplash_id[:8]}"


def upload_para_r2(arquivo_local: str, nome_r2: str) -> Optional[str]:
    """
    Faz upload de um arquivo para o Cloudflare R2.
    
    Args:
        arquivo_local: Caminho do arquivo local
        nome_r2: Nome do arquivo no R2 (com extensão)
    
    Returns:
        URL pública do arquivo ou None se falhar
    """
    try:
        r2_client = criar_cliente_r2()
        
        # Determinar content type
        if nome_r2.endswith('.jpg') or nome_r2.endswith('.jpeg'):
            content_type = 'image/jpeg'
        elif nome_r2.endswith('.png'):
            content_type = 'image/png'
        elif nome_r2.endswith('.webp'):
            content_type = 'image/webp'
        else:
            content_type = 'application/octet-stream'
        
        # Upload
        with open(arquivo_local, 'rb') as f:
            r2_client.put_object(
                Bucket=R2_BUCKET_NAME,
                Key=f"noticias/{nome_r2}",
                Body=f,
                ContentType=content_type
            )
        
        return f"{R2_PUBLIC_URL}/noticias/{nome_r2}"
    
    except Exception as e:
        print(f"  ⚠ Erro no upload para R2: {e}")
        return None


def processar_imagem_para_noticia(
    titulo: str,
    categoria: str,
    article_id: str = None
) -> Optional[Dict]:
    """
    Processa uma imagem completa para uma notícia:
    1. Busca imagem relevante no Unsplash
    2. Baixa a imagem
    3. Faz upload para R2
    4. Opcionalmente atualiza no Supabase
    
    Args:
        titulo: Título da notícia
        categoria: Categoria (Política, Economia)
        article_id: ID do artigo no Supabase (opcional)
    
    Returns:
        Dicionário com informações da imagem processada
    """
    print(f"\n📷 Processando imagem para: {titulo[:50]}...")
    
    # 1. Buscar imagem no Unsplash
    imagem = obter_imagem_para_noticia(titulo, categoria)
    
    if not imagem:
        print("  ❌ Não foi possível encontrar imagem")
        return None
    
    # 2. Gerar nome do arquivo
    nome_base = gerar_nome_arquivo(titulo, imagem['id'])
    nome_arquivo = f"{nome_base}.jpg"
    arquivo_temp = TEMP_DIR / nome_arquivo
    
    # 3. Baixar imagem (usar URL regular - 1080px)
    print(f"  ⬇ Baixando imagem...")
    if not baixar_imagem(imagem['url_regular'], str(arquivo_temp)):
        print("  ❌ Falha ao baixar imagem")
        return None
    
    # 4. Upload para R2
    print(f"  ⬆ Enviando para Cloudflare R2...")
    url_r2 = upload_para_r2(str(arquivo_temp), nome_arquivo)
    
    if not url_r2:
        print("  ❌ Falha no upload para R2")
        return None
    
    print(f"  ✓ Upload concluído: {url_r2}")
    
    # 5. Limpar arquivo temporário
    try:
        arquivo_temp.unlink()
    except:
        pass
    
    # 6. Atualizar no Supabase se article_id fornecido
    if article_id and SUPABASE_URL and SUPABASE_KEY:
        try:
            supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
            supabase.table('articles').update({
                'image_url': url_r2
            }).eq('id', article_id).execute()
            print(f"  ✓ Supabase atualizado")
        except Exception as e:
            print(f"  ⚠ Erro ao atualizar Supabase: {e}")
    
    return {
        'url': url_r2,
        'unsplash_id': imagem['id'],
        'photographer': imagem['photographer'],
        'photographer_url': imagem['photographer_url'],
        'unsplash_url': imagem['unsplash_url'],
        'alt_description': imagem.get('alt_description', '')
    }


def atualizar_todas_imagens_supabase():
    """
    Atualiza as imagens de todos os artigos no Supabase que ainda
    usam imagens locais ou repetidas.
    """
    print("=" * 60)
    print("ATUALIZAÇÃO DE IMAGENS - NOTÍCIAS IMPARCIAIS")
    print("=" * 60)
    
    if not SUPABASE_URL or not SUPABASE_KEY:
        print("❌ Credenciais do Supabase não configuradas!")
        return
    
    # Conectar ao Supabase
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    # Buscar todos os artigos
    response = supabase.table('articles').select('id', 'title', 'category', 'image_url').execute()
    artigos = response.data
    
    print(f"\n📊 {len(artigos)} artigos encontrados")
    
    # Filtrar artigos que precisam de nova imagem
    # (imagens locais ou do R2 com nomes genéricos)
    artigos_para_atualizar = []
    for artigo in artigos:
        url = artigo.get('image_url', '')
        # Atualizar se for imagem local ou genérica
        if '/images/noticias/' in url or 'planalto.jpg' in url or 'b3_touro.jpg' in url:
            artigos_para_atualizar.append(artigo)
    
    print(f"📝 {len(artigos_para_atualizar)} artigos precisam de novas imagens")
    
    if not artigos_para_atualizar:
        print("\n✅ Todos os artigos já possuem imagens únicas!")
        return
    
    # Processar cada artigo
    sucesso = 0
    falha = 0
    
    for i, artigo in enumerate(artigos_para_atualizar, 1):
        print(f"\n[{i}/{len(artigos_para_atualizar)}] {artigo['title'][:50]}...")
        
        resultado = processar_imagem_para_noticia(
            titulo=artigo['title'],
            categoria=artigo['category'],
            article_id=artigo['id']
        )
        
        if resultado:
            sucesso += 1
        else:
            falha += 1
    
    print("\n" + "=" * 60)
    print("RESULTADO FINAL")
    print("=" * 60)
    print(f"✅ Sucesso: {sucesso}")
    print(f"❌ Falha: {falha}")
    print(f"📊 Total processado: {sucesso + falha}")


# Teste do módulo
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--atualizar-todas":
        # Modo: atualizar todas as imagens
        atualizar_todas_imagens_supabase()
    else:
        # Modo: teste com uma notícia
        print("=" * 60)
        print("TESTE DO PROCESSADOR DE IMAGENS")
        print("=" * 60)
        
        resultado = processar_imagem_para_noticia(
            titulo="Congresso Nacional aprova Orçamento da União para o próximo exercício",
            categoria="Economia"
        )
        
        if resultado:
            print("\n✅ Teste concluído com sucesso!")
            print(f"   URL: {resultado['url']}")
            print(f"   Fotógrafo: {resultado['photographer']}")
        else:
            print("\n❌ Teste falhou")
