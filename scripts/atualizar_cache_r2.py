"""
Script para adicionar Cache-Control nas imagens existentes do Cloudflare R2.
Este script copia cada objeto para ele mesmo, adicionando o header Cache-Control.
"""

import os

import boto3
from botocore.config import Config

def criar_cliente_s3():
    """Lê a configuração privada do ambiente sem armazenar credenciais no código."""
    nomes = (
        "R2_ACCOUNT_ID",
        "R2_ACCESS_KEY_ID",
        "R2_SECRET_ACCESS_KEY",
        "R2_BUCKET_NAME",
    )
    valores = {nome: os.environ.get(nome, "").strip() for nome in nomes}
    ausentes = [nome for nome, valor in valores.items() if not valor]
    if ausentes:
        raise ValueError("Variáveis de ambiente obrigatórias ausentes: " + ", ".join(ausentes))

    cliente = boto3.client(
        "s3",
        endpoint_url=f"https://{valores['R2_ACCOUNT_ID']}.r2.cloudflarestorage.com",
        aws_access_key_id=valores["R2_ACCESS_KEY_ID"],
        aws_secret_access_key=valores["R2_SECRET_ACCESS_KEY"],
        config=Config(signature_version="s3v4"),
    )
    return cliente, valores["R2_BUCKET_NAME"]


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
    
    s3, bucket_name = criar_cliente_s3()

    print("=" * 60)
    print("ATUALIZADOR DE CACHE - CLOUDFLARE R2")
    print("=" * 60)
    print(f"Bucket: {bucket_name}")
    print(f"Cache-Control: public, max-age=31536000, immutable")
    print("=" * 60)
    
    # Listar todos os objetos no bucket
    try:
        paginator = s3.get_paginator('list_objects_v2')
        pages = paginator.paginate(Bucket=bucket_name, Prefix='noticias/imagens/')
        
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
                        Bucket=bucket_name,
                        CopySource={'Bucket': bucket_name, 'Key': key},
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
    try:
        atualizar_cache_imagens()
    except ValueError as exc:
        raise SystemExit(str(exc)) from None
