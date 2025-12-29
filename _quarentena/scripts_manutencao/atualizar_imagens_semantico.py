#!/usr/bin/env python3
"""
Script para atualizar as notícias de hoje com imagens baseadas na análise semântica.
Usa o novo módulo analisador_contexto.py para selecionar imagens mais contextuais.
"""

import os
import sys
import boto3
from dotenv import load_dotenv
from supabase import create_client
from analisador_contexto import analisar_titulo

# Carregar variáveis de ambiente
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

# Configurações
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_SERVICE_KEY')
R2_ACCOUNT_ID = os.getenv('R2_ACCOUNT_ID')
R2_ACCESS_KEY_ID = os.getenv('R2_ACCESS_KEY_ID')
R2_SECRET_ACCESS_KEY = os.getenv('R2_SECRET_ACCESS_KEY')
R2_BUCKET_NAME = os.getenv('R2_BUCKET_NAME')
R2_PUBLIC_URL = os.getenv('R2_PUBLIC_URL')
R2_ENDPOINT = os.getenv('R2_ENDPOINT')

ACERVO_PATH = os.path.join(os.path.dirname(__file__), '..', 'acervo_temas')

# Mapeamento de análise semântica para imagens específicas
MAPEAMENTO_IMAGENS = {
    # Temas específicos
    'fgts': 'economia/carteira_trabalho_01.jpeg',
    'abono salarial': 'economia/carteira_trabalho_01.jpeg',
    'indulto': 'seguranca/presidio_alcacuz_01.jpeg',
    'acareação': 'judiciario/stf_plenario_05.jpeg',
    'inflação': 'economia/banco_central_sede_01.jpg',
    
    # Pessoas
    'bolsonaro': 'pessoas/bolsonaro_01.jpg',
    'augusto heleno': 'pessoas/augusto_heleno_03.jpeg',
    'alexandre de moraes': 'pessoas/alexandre_moraes_03.jpeg',
    'lula': 'pessoas/lula_oficial_03.jpeg',
    
    # Categorias fallback
    'economia': 'economia/banco_central_sede_01.jpg',
    'judiciario': 'judiciario/stf_plenario_05.jpeg',
    'seguranca': 'seguranca/presidio_alcacuz_01.jpeg',
    'executivo': 'executivo/planalto_fachada_02.jpg',
    'legislativo': 'legislativo/camara_plenario_votacao_01.jpg',
}


def get_supabase_client():
    """Cria cliente Supabase."""
    return create_client(SUPABASE_URL, SUPABASE_KEY)


def get_r2_client():
    """Cria cliente S3 para R2."""
    return boto3.client(
        's3',
        endpoint_url=R2_ENDPOINT,
        aws_access_key_id=R2_ACCESS_KEY_ID,
        aws_secret_access_key=R2_SECRET_ACCESS_KEY,
        region_name='auto'
    )


def upload_to_r2(local_path: str, remote_name: str) -> str:
    """Faz upload de uma imagem para o R2 e retorna a URL pública."""
    s3 = get_r2_client()
    
    # Determinar content type
    if local_path.endswith('.jpeg') or local_path.endswith('.jpg'):
        content_type = 'image/jpeg'
    elif local_path.endswith('.png'):
        content_type = 'image/png'
    elif local_path.endswith('.webp'):
        content_type = 'image/webp'
    else:
        content_type = 'image/jpeg'
    
    # Upload
    with open(local_path, 'rb') as f:
        s3.put_object(
            Bucket=R2_BUCKET_NAME,
            Key=remote_name,
            Body=f,
            ContentType=content_type
        )
    
    return f"{R2_PUBLIC_URL}/{remote_name}"


def selecionar_imagem_por_analise(titulo: str) -> str:
    """Seleciona a melhor imagem baseado na análise semântica do título."""
    analise = analisar_titulo(titulo)
    
    print(f"\n📰 Título: {titulo[:60]}...")
    print(f"   Tema: {analise['tema_principal']}")
    print(f"   Tipo: {analise['tipo_contexto']}")
    print(f"   Usar foto pessoa: {analise['usar_foto_pessoa']}")
    
    # 1. Se deve usar foto de pessoa específica
    if analise['usar_foto_pessoa'] and analise['pessoa_identificada']:
        pessoa = analise['pessoa_identificada'].lower()
        for key, imagem in MAPEAMENTO_IMAGENS.items():
            if key in pessoa or pessoa in key:
                print(f"   ✅ Selecionado (pessoa): {imagem}")
                return imagem
    
    # 2. Buscar pelo tema específico
    if analise['tema_principal']:
        tema = analise['tema_principal'].lower()
        if tema in MAPEAMENTO_IMAGENS:
            print(f"   ✅ Selecionado (tema): {MAPEAMENTO_IMAGENS[tema]}")
            return MAPEAMENTO_IMAGENS[tema]
    
    # 3. Fallback para categoria
    categoria = analise['categoria_acervo']
    if categoria in MAPEAMENTO_IMAGENS:
        print(f"   ⚠️ Fallback (categoria): {MAPEAMENTO_IMAGENS[categoria]}")
        return MAPEAMENTO_IMAGENS[categoria]
    
    # 4. Fallback final
    print(f"   ❌ Usando fallback genérico")
    return 'executivo/planalto_fachada_02.jpg'


def atualizar_noticias_hoje():
    """Atualiza as notícias de hoje com imagens baseadas na análise semântica."""
    supabase = get_supabase_client()
    
    # Buscar notícias de hoje
    response = supabase.table('articles').select('id, title, image_url').execute()
    noticias = response.data
    
    print(f"\n{'='*70}")
    print(f"ATUALIZANDO {len(noticias)} NOTÍCIAS COM ANÁLISE SEMÂNTICA")
    print(f"{'='*70}")
    
    atualizadas = 0
    
    for noticia in noticias:
        titulo = noticia['title']
        noticia_id = noticia['id']
        
        # Selecionar imagem baseado na análise semântica
        imagem_relativa = selecionar_imagem_por_analise(titulo)
        imagem_local = os.path.join(ACERVO_PATH, imagem_relativa)
        
        if not os.path.exists(imagem_local):
            print(f"   ❌ Imagem não encontrada: {imagem_local}")
            continue
        
        # Nome para o R2 (usar título sanitizado)
        titulo_sanitizado = "".join(c if c.isalnum() else "_" for c in titulo[:30]).lower()
        extensao = os.path.splitext(imagem_relativa)[1]
        remote_name = f"noticias/{titulo_sanitizado}{extensao}"
        
        # Upload para R2
        try:
            nova_url = upload_to_r2(imagem_local, remote_name)
            print(f"   📤 Upload: {nova_url}")
            
            # Atualizar no Supabase
            supabase.table('articles').update({'image_url': nova_url}).eq('id', noticia_id).execute()
            print(f"   ✅ Atualizado no Supabase")
            atualizadas += 1
            
        except Exception as e:
            print(f"   ❌ Erro: {e}")
    
    print(f"\n{'='*70}")
    print(f"RESUMO: {atualizadas}/{len(noticias)} notícias atualizadas")
    print(f"{'='*70}")


if __name__ == "__main__":
    atualizar_noticias_hoje()
