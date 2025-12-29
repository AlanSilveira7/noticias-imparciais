#!/usr/bin/env python3
"""
Script para fazer upload das imagens existentes para o Cloudflare R2
e atualizar as URLs no Supabase.
"""

import os
import boto3
from dotenv import load_dotenv
from supabase import create_client
import mimetypes

# Carregar variáveis de ambiente
load_dotenv()

# Configurações do R2
R2_ACCOUNT_ID = os.getenv('R2_ACCOUNT_ID')
R2_ACCESS_KEY_ID = os.getenv('R2_ACCESS_KEY_ID')
R2_SECRET_ACCESS_KEY = os.getenv('R2_SECRET_ACCESS_KEY')
R2_BUCKET_NAME = os.getenv('R2_BUCKET_NAME')
R2_PUBLIC_URL = os.getenv('R2_PUBLIC_URL')

# Configurações do Supabase
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_ANON_KEY')

# Diretório das imagens de notícias
IMAGES_DIR = '/home/ubuntu/noticias-imparciais/site/client/public/images/noticias'

def create_r2_client():
    """Cria cliente S3 compatível com R2"""
    return boto3.client(
        's3',
        endpoint_url=f'https://{R2_ACCOUNT_ID}.r2.cloudflarestorage.com',
        aws_access_key_id=R2_ACCESS_KEY_ID,
        aws_secret_access_key=R2_SECRET_ACCESS_KEY,
        region_name='auto'
    )

def upload_image_to_r2(client, local_path, r2_key):
    """Faz upload de uma imagem para o R2"""
    content_type, _ = mimetypes.guess_type(local_path)
    if content_type is None:
        content_type = 'application/octet-stream'
    
    with open(local_path, 'rb') as f:
        client.put_object(
            Bucket=R2_BUCKET_NAME,
            Key=r2_key,
            Body=f,
            ContentType=content_type
        )
    
    return f"{R2_PUBLIC_URL}/{r2_key}"

def main():
    print("=" * 60)
    print("UPLOAD DE IMAGENS PARA CLOUDFLARE R2")
    print("=" * 60)
    
    # Verificar configurações
    if not all([R2_ACCOUNT_ID, R2_ACCESS_KEY_ID, R2_SECRET_ACCESS_KEY, R2_BUCKET_NAME]):
        print("✗ Erro: Credenciais do R2 não configuradas!")
        return
    
    print(f"✓ Bucket: {R2_BUCKET_NAME}")
    print(f"✓ URL Pública: {R2_PUBLIC_URL}")
    
    # Criar cliente R2
    print("\n[1/3] Conectando ao Cloudflare R2...")
    try:
        r2_client = create_r2_client()
        print("✓ Conexão estabelecida!")
    except Exception as e:
        print(f"✗ Erro ao conectar: {e}")
        return
    
    # Criar cliente Supabase
    print("\n[2/3] Conectando ao Supabase...")
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        print("✓ Conexão estabelecida!")
    except Exception as e:
        print(f"✗ Erro ao conectar: {e}")
        return
    
    # Listar imagens de notícias
    print("\n[3/3] Fazendo upload das imagens...")
    
    if not os.path.exists(IMAGES_DIR):
        print(f"✗ Diretório não encontrado: {IMAGES_DIR}")
        return
    
    images = [f for f in os.listdir(IMAGES_DIR) if f.endswith(('.jpg', '.jpeg', '.png', '.webp', '.gif'))]
    print(f"✓ {len(images)} imagens encontradas")
    
    success_count = 0
    error_count = 0
    url_mapping = {}
    
    for i, image_name in enumerate(images, 1):
        local_path = os.path.join(IMAGES_DIR, image_name)
        r2_key = f"noticias/{image_name}"
        old_url = f"/images/noticias/{image_name}"
        
        print(f"  [{i}/{len(images)}] Uploading: {image_name}...", end=" ")
        
        try:
            new_url = upload_image_to_r2(r2_client, local_path, r2_key)
            url_mapping[old_url] = new_url
            print(f"✓")
            success_count += 1
        except Exception as e:
            print(f"✗ Erro: {e}")
            error_count += 1
    
    print(f"\n✓ Upload concluído: {success_count} sucesso, {error_count} erros")
    
    # Atualizar URLs no Supabase
    if url_mapping:
        print("\n[4/4] Atualizando URLs no Supabase...")
        
        # Buscar todos os artigos
        response = supabase.table('articles').select('id', 'image_url').execute()
        articles = response.data
        
        updated_count = 0
        for article in articles:
            old_url = article['image_url']
            if old_url in url_mapping:
                new_url = url_mapping[old_url]
                try:
                    supabase.table('articles').update({'image_url': new_url}).eq('id', article['id']).execute()
                    print(f"  ✓ Atualizado: {article['id'][:40]}...")
                    updated_count += 1
                except Exception as e:
                    print(f"  ✗ Erro ao atualizar {article['id']}: {e}")
        
        print(f"\n✓ {updated_count} artigos atualizados no Supabase")
    
    print("\n" + "=" * 60)
    print("UPLOAD CONCLUÍDO!")
    print("=" * 60)
    print(f"\nAs imagens agora estão disponíveis em:")
    print(f"{R2_PUBLIC_URL}/noticias/[nome_da_imagem]")

if __name__ == '__main__':
    main()
