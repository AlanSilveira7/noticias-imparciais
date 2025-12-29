#!/usr/bin/env python3
"""
Script para fazer upload de novas imagens HD para o R2 e atualizar as notícias no Supabase.
"""

import os
import boto3
from botocore.config import Config
from supabase import create_client
from dotenv import load_dotenv
import hashlib
import re

# Carregar variáveis de ambiente
load_dotenv('../.env')

# Configuração do Supabase
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_SERVICE_KEY = os.getenv('SUPABASE_SERVICE_KEY')

# Configuração do R2
R2_ACCOUNT_ID = os.getenv('R2_ACCOUNT_ID')
R2_ACCESS_KEY_ID = os.getenv('R2_ACCESS_KEY_ID')
R2_SECRET_ACCESS_KEY = os.getenv('R2_SECRET_ACCESS_KEY')
R2_BUCKET_NAME = os.getenv('R2_BUCKET_NAME')
R2_PUBLIC_URL = os.getenv('R2_PUBLIC_URL')
R2_ENDPOINT = os.getenv('R2_ENDPOINT')

# Inicializar clientes
supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

s3_client = boto3.client(
    's3',
    endpoint_url=R2_ENDPOINT,
    aws_access_key_id=R2_ACCESS_KEY_ID,
    aws_secret_access_key=R2_SECRET_ACCESS_KEY,
    config=Config(signature_version='s3v4'),
    region_name='auto'
)

def slugify(text):
    """Converte texto para slug."""
    text = text.lower()
    text = re.sub(r'[àáâãäå]', 'a', text)
    text = re.sub(r'[èéêë]', 'e', text)
    text = re.sub(r'[ìíîï]', 'i', text)
    text = re.sub(r'[òóôõö]', 'o', text)
    text = re.sub(r'[ùúûü]', 'u', text)
    text = re.sub(r'[ç]', 'c', text)
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = re.sub(r'[\s_]+', '-', text)
    text = re.sub(r'-+', '-', text)
    return text[:40].strip('-')

def upload_to_r2(local_path, remote_key):
    """Faz upload de arquivo para o R2."""
    content_type = 'image/jpeg' if local_path.endswith('.jpg') or local_path.endswith('.jpeg') else 'image/webp'
    
    with open(local_path, 'rb') as f:
        s3_client.put_object(
            Bucket=R2_BUCKET_NAME,
            Key=remote_key,
            Body=f,
            ContentType=content_type
        )
    
    return f"{R2_PUBLIC_URL}/{remote_key}"

def get_file_hash(filepath):
    """Gera hash curto do arquivo."""
    with open(filepath, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()[:8]

def main():
    # Mapeamento de notícias para novas imagens
    # Baseado na análise das notícias de hoje
    noticias_imagens = {
        # Bolsonaro - já tem imagem de boa qualidade no acervo
        '8166d5f2-d97e-45c8-acd6-64edc6149901': {
            'titulo': 'Bolsonaro passa por novo procedimento médico',
            'imagem_local': '../acervo_temas/pessoas/bolsonaro_01.jpg',
            'pessoa': 'bolsonaro'
        },
        # Alexandre de Moraes - nova imagem HD
        '60583e60-f0a7-41cf-98d0-1fb6ce1c78fa': {
            'titulo': 'Acareação e Investigações Envolvendo Ministro Alexandre de Moraes',
            'imagem_local': '../acervo_temas/pessoas/alexandre_moraes_03.jpeg',
            'pessoa': 'alexandre-moraes'
        },
        # General Heleno - nova imagem HD
        '7c60d20f-3532-4362-b5dd-792297364355': {
            'titulo': 'General Heleno e Prisão Domiciliar',
            'imagem_local': '../acervo_temas/pessoas/augusto_heleno_03.jpeg',
            'pessoa': 'augusto-heleno'
        },
        # Indulto de Natal (Lula) - nova imagem HD
        'ec33cbec-e5e3-4deb-9372-7761bfae02b9': {
            'titulo': 'Presidência concede indulto de Natal',
            'imagem_local': '../acervo_temas/pessoas/lula_oficial_03.jpeg',
            'pessoa': 'lula'
        },
        # Inflação - usar imagem do Banco Central
        'c6f78fc2-fca2-49e0-978a-2c8d3cc97a50': {
            'titulo': 'Mercado financeiro revisa projeções de inflação',
            'imagem_local': '../acervo_temas/economia/banco_central_sede_01.jpg',
            'pessoa': 'banco-central'
        },
        # FGTS - usar imagem da B3/economia
        'fd80fbd1-6cf3-470b-937d-c2e27aeefab2': {
            'titulo': 'Mudanças no FGTS e prazos para saque',
            'imagem_local': '../acervo_temas/economia/b3_pregao_02.jpg',
            'pessoa': 'economia-fgts'
        }
    }
    
    print("=" * 60)
    print("ATUALIZANDO IMAGENS DAS NOTÍCIAS")
    print("=" * 60)
    
    for article_id, info in noticias_imagens.items():
        print(f"\n📰 {info['titulo'][:50]}...")
        
        # Verificar se arquivo existe
        if not os.path.exists(info['imagem_local']):
            print(f"   ❌ Arquivo não encontrado: {info['imagem_local']}")
            continue
        
        # Gerar nome do arquivo para o R2
        slug = slugify(info['titulo'])
        file_hash = get_file_hash(info['imagem_local'])
        ext = info['imagem_local'].split('.')[-1]
        remote_key = f"noticias/imagens/{slug}_{file_hash}.{ext}"
        
        print(f"   📤 Fazendo upload para R2...")
        try:
            new_url = upload_to_r2(info['imagem_local'], remote_key)
            print(f"   ✅ Upload concluído: {new_url}")
            
            # Atualizar no Supabase
            print(f"   📝 Atualizando Supabase...")
            supabase.table('articles').update({'image_url': new_url}).eq('id', article_id).execute()
            print(f"   ✅ Supabase atualizado!")
            
        except Exception as e:
            print(f"   ❌ Erro: {e}")
    
    print("\n" + "=" * 60)
    print("PROCESSO CONCLUÍDO!")
    print("=" * 60)

if __name__ == "__main__":
    main()
