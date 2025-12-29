#!/usr/bin/env python3
"""
Script para listar e excluir imagens antigas do R2 que não são mais necessárias.
"""

import os
import boto3
from botocore.config import Config
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv('../.env')

# Configuração do R2
R2_ACCOUNT_ID = os.getenv('R2_ACCOUNT_ID')
R2_ACCESS_KEY_ID = os.getenv('R2_ACCESS_KEY_ID')
R2_SECRET_ACCESS_KEY = os.getenv('R2_SECRET_ACCESS_KEY')
R2_BUCKET_NAME = os.getenv('R2_BUCKET_NAME')
R2_PUBLIC_URL = os.getenv('R2_PUBLIC_URL')
R2_ENDPOINT = os.getenv('R2_ENDPOINT')

# Inicializar cliente S3
s3_client = boto3.client(
    's3',
    endpoint_url=R2_ENDPOINT,
    aws_access_key_id=R2_ACCESS_KEY_ID,
    aws_secret_access_key=R2_SECRET_ACCESS_KEY,
    config=Config(signature_version='s3v4'),
    region_name='auto'
)

def list_all_objects():
    """Lista todos os objetos no bucket."""
    objects = []
    paginator = s3_client.get_paginator('list_objects_v2')
    
    for page in paginator.paginate(Bucket=R2_BUCKET_NAME, Prefix='noticias/imagens/'):
        if 'Contents' in page:
            for obj in page['Contents']:
                objects.append(obj['Key'])
    
    return objects

def delete_object(key):
    """Exclui um objeto do bucket."""
    s3_client.delete_object(Bucket=R2_BUCKET_NAME, Key=key)

def main():
    print("=" * 60)
    print("LISTANDO IMAGENS NO R2")
    print("=" * 60)
    
    # Listar todos os objetos
    all_objects = list_all_objects()
    
    # URLs das imagens que estão sendo usadas atualmente (as novas)
    imagens_em_uso = [
        'noticias/imagens/bolsonaro-passa-por-novo-procedimento-me_48c4612d.jpg',
        'noticias/imagens/acareacao-e-investigacoes-envolvendo-min_e3ccf2ab.jpeg',
        'noticias/imagens/general-heleno-e-prisao-domiciliar_b8d1b1c8.jpeg',
        'noticias/imagens/presidencia-concede-indulto-de-natal_5c65294e.jpeg',
        'noticias/imagens/mercado-financeiro-revisa-projecoes-de-i_8acc9223.jpg',
        'noticias/imagens/mudancas-no-fgts-e-prazos-para-saque_516fd38d.jpg'
    ]
    
    print(f"\n📁 Total de objetos encontrados: {len(all_objects)}")
    print(f"📌 Imagens em uso: {len(imagens_em_uso)}")
    
    # Identificar imagens para exclusão
    imagens_para_excluir = [obj for obj in all_objects if obj not in imagens_em_uso]
    
    print(f"\n🗑️  Imagens para exclusão: {len(imagens_para_excluir)}")
    
    if imagens_para_excluir:
        print("\nImagens que serão excluídas:")
        for img in imagens_para_excluir:
            print(f"   - {img}")
        
        print("\n" + "=" * 60)
        print("EXCLUINDO IMAGENS ANTIGAS...")
        print("=" * 60)
        
        for img in imagens_para_excluir:
            try:
                delete_object(img)
                print(f"   ✅ Excluído: {img}")
            except Exception as e:
                print(f"   ❌ Erro ao excluir {img}: {e}")
    else:
        print("\n✅ Nenhuma imagem para excluir!")
    
    print("\n" + "=" * 60)
    print("PROCESSO CONCLUÍDO!")
    print("=" * 60)

if __name__ == "__main__":
    main()
