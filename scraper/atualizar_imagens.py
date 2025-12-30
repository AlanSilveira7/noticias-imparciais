#!/usr/bin/env python3
"""
Script para atualizar imagens de notícias específicas no Supabase.
Substitui imagens com marca d'água por imagens limpas.
"""

import os
import boto3
from dotenv import load_dotenv
from supabase import create_client
from datetime import datetime

# Carregar variáveis de ambiente
load_dotenv()

# Configuração Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

# Configuração Cloudflare R2
R2_ACCOUNT_ID = os.getenv("R2_ACCOUNT_ID")
R2_ACCESS_KEY = os.getenv("R2_ACCESS_KEY_ID")
R2_SECRET_KEY = os.getenv("R2_SECRET_ACCESS_KEY")
R2_BUCKET = os.getenv("R2_BUCKET_NAME")
R2_ENDPOINT = f"https://{R2_ACCOUNT_ID}.r2.cloudflarestorage.com"
R2_PUBLIC_URL = os.getenv("R2_PUBLIC_URL")

# Inicializar clientes
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

s3_client = boto3.client(
    's3',
    endpoint_url=R2_ENDPOINT,
    aws_access_key_id=R2_ACCESS_KEY,
    aws_secret_access_key=R2_SECRET_KEY
)

def upload_image_to_r2(local_path, remote_filename):
    """Faz upload de uma imagem para o Cloudflare R2."""
    try:
        content_type = 'image/jpeg'
        if local_path.endswith('.png'):
            content_type = 'image/png'
        elif local_path.endswith('.webp'):
            content_type = 'image/webp'
        
        s3_client.upload_file(
            local_path,
            R2_BUCKET,
            remote_filename,
            ExtraArgs={'ContentType': content_type}
        )
        
        public_url = f"{R2_PUBLIC_URL}/{remote_filename}"
        print(f"✅ Upload concluído: {public_url}")
        return public_url
    except Exception as e:
        print(f"❌ Erro no upload: {e}")
        return None

def update_noticia_image(titulo_parcial, nova_imagem_url):
    """Atualiza a imagem de uma notícia no Supabase."""
    try:
        # Buscar notícia pelo título parcial
        response = supabase.table("articles").select("*").ilike("title", f"%{titulo_parcial}%").execute()
        
        if response.data and len(response.data) > 0:
            noticia = response.data[0]
            noticia_id = noticia['id']
            titulo_completo = noticia['title']
            
            # Atualizar imagem
            update_response = supabase.table("articles").update({
                "image_url": nova_imagem_url
            }).eq("id", noticia_id).execute()
            
            print(f"✅ Atualizada: {titulo_completo}")
            return True
        else:
            print(f"❌ Notícia não encontrada: {titulo_parcial}")
            return False
    except Exception as e:
        print(f"❌ Erro ao atualizar: {e}")
        return False

def main():
    """Função principal para atualizar as 6 imagens problemáticas."""
    
    # Mapeamento: título parcial -> caminho da nova imagem
    atualizacoes = [
        {
            "titulo": "Mercado Reduz Projeção de Inflação",
            "imagem_local": "/home/ubuntu/noticias-imparciais/acervo_temas/economia/banco_central_sede_02.jpg",
            "nome_remoto": f"banco_central_sede_{datetime.now().strftime('%Y%m%d%H%M%S')}.jpg"
        },
        {
            "titulo": "Correios Precisarão de R$ 8 Bilhões",
            "imagem_local": "/home/ubuntu/noticias-imparciais/acervo_temas/economia/correios_sede_02.jpg",
            "nome_remoto": f"correios_sede_{datetime.now().strftime('%Y%m%d%H%M%S')}.jpg"
        },
        {
            "titulo": "Aeronautas Aprovam Acordo",
            "imagem_local": "/home/ubuntu/noticias-imparciais/acervo_temas/aviacao/avioes_aeroporto_01.jpg",
            "nome_remoto": f"avioes_aeroporto_{datetime.now().strftime('%Y%m%d%H%M%S')}.jpg"
        },
        {
            "titulo": "Calendário de Feriados",
            "imagem_local": "/home/ubuntu/noticias-imparciais/acervo_temas/executivo/calendario_2026_02.jpg",
            "nome_remoto": f"calendario_2026_{datetime.now().strftime('%Y%m%d%H%M%S')}.jpg"
        },
        {
            "titulo": "Espumante, Moscatel e Frisante",
            "imagem_local": "/home/ubuntu/noticias-imparciais/acervo_temas/consumo/espumante_brinde_02.jpg",
            "nome_remoto": f"espumante_brinde_{datetime.now().strftime('%Y%m%d%H%M%S')}.jpg"
        },
        {
            "titulo": "Ibovespa Dispara 33%",
            "imagem_local": "/home/ubuntu/noticias-imparciais/acervo_temas/economia/b3_pregao_03.jpg",
            "nome_remoto": f"b3_pregao_{datetime.now().strftime('%Y%m%d%H%M%S')}.jpg"
        }
    ]
    
    print("=" * 60)
    print("ATUALIZANDO IMAGENS DAS NOTÍCIAS")
    print("=" * 60)
    
    sucesso = 0
    falha = 0
    
    for item in atualizacoes:
        print(f"\n📷 Processando: {item['titulo']}")
        
        # Upload da nova imagem
        nova_url = upload_image_to_r2(item['imagem_local'], item['nome_remoto'])
        
        if nova_url:
            # Atualizar no Supabase
            if update_noticia_image(item['titulo'], nova_url):
                sucesso += 1
            else:
                falha += 1
        else:
            falha += 1
    
    print("\n" + "=" * 60)
    print(f"RESULTADO: {sucesso} atualizadas, {falha} falhas")
    print("=" * 60)

if __name__ == "__main__":
    main()
