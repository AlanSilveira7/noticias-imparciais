"""
Script para adicionar Cache-Control nas imagens existentes do Cloudflare R2.
Este script copia cada objeto para ele mesmo, adicionando o header Cache-Control.
"""

import boto3
from botocore.config import Config

# Credenciais R2
R2_ACCOUNT_ID = 'ec85f027ae9088cd81296ad023dcb4d1'
R2_ACCESS_KEY_ID = '64b69f7f55a15b49377c07a146a5b981'
R2_SECRET_ACCESS_KEY = '439b838c339384d6972d7aca44133973d52549423d5158f6c09dc31732532760'
R2_BUCKET_NAME = 'noticias-imparciais-imagens'
R2_ENDPOINT = f'https://{R2_ACCOUNT_ID}.r2.cloudflarestorage.com'

# Configuração do cliente S3
s3 = boto3.client(
    's3',
    endpoint_url=R2_ENDPOINT,
    aws_access_key_id=R2_ACCESS_KEY_ID,
    aws_secret_access_key=R2_SECRET_ACCESS_KEY,
    config=Config(signature_version='s3v4')
)

def get_content_type(key):
    """Determina o Content-Type baseado na extensão do arquivo."""
    if key.endswith('.jpg') or key.endswith('.jpeg'):
        return 'image/jpeg'
    elif key.endswith('.png'):
        return 'image/png'
    elif key.endswith('.webp'):
        return 'image/webp'
    elif key.endswith('.gif'):
        return 'image/gif'
    else:
        return 'application/octet-stream'

def atualizar_cache_imagens():
    """Atualiza o Cache-Control de todas as imagens no bucket."""
    
    print("=" * 60)
    print("ATUALIZADOR DE CACHE - CLOUDFLARE R2")
    print("=" * 60)
    print(f"Bucket: {R2_BUCKET_NAME}")
    print(f"Cache-Control: public, max-age=31536000, immutable")
    print("=" * 60)
    
    # Listar todos os objetos no bucket
    try:
        paginator = s3.get_paginator('list_objects_v2')
        pages = paginator.paginate(Bucket=R2_BUCKET_NAME, Prefix='noticias/imagens/')
        
        total = 0
        sucesso = 0
        erro = 0
        
        for page in pages:
            if 'Contents' not in page:
                print("Nenhum objeto encontrado no bucket.")
                return
            
            for obj in page['Contents']:
                key = obj['Key']
                total += 1
                
                try:
                    content_type = get_content_type(key)
                    
                    # Copiar o objeto para ele mesmo com novos metadados
                    s3.copy_object(
                        Bucket=R2_BUCKET_NAME,
                        CopySource={'Bucket': R2_BUCKET_NAME, 'Key': key},
                        Key=key,
                        ContentType=content_type,
                        CacheControl='public, max-age=31536000, immutable',
                        MetadataDirective='REPLACE'
                    )
                    
                    print(f"✓ {key}")
                    sucesso += 1
                    
                except Exception as e:
                    print(f"✗ {key} - Erro: {e}")
                    erro += 1
        
        print("=" * 60)
        print(f"RESUMO: {sucesso}/{total} objetos atualizados com sucesso")
        if erro > 0:
            print(f"Erros: {erro}")
        print("=" * 60)
        
    except Exception as e:
        print(f"Erro ao listar objetos: {e}")

if __name__ == "__main__":
    atualizar_cache_imagens()
