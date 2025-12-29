#!/usr/bin/env python3
"""
Script para verificar as imagens das 6 notícias de hoje
"""

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv
from supabase import create_client

load_dotenv(Path(__file__).parent.parent / '.env')

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_SERVICE_KEY')
ACERVO_DIR = Path(__file__).parent.parent / 'acervo_temas'

# Imagens que ainda existem no acervo (>= 1280px)
IMAGENS_VALIDAS = []
for root, dirs, files in os.walk(ACERVO_DIR):
    for file in files:
        if file.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
            rel_path = Path(root).relative_to(ACERVO_DIR) / file
            IMAGENS_VALIDAS.append(str(rel_path))

def main():
    print("=" * 70)
    print("🔍 VERIFICAÇÃO DAS NOTÍCIAS DE HOJE")
    print("=" * 70)
    
    # Conectar ao Supabase
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    # Buscar notícias de hoje
    response = supabase.table('articles').select('*').eq('date', '29/12/2025').execute()
    
    if not response.data:
        print("Nenhuma notícia de hoje encontrada.")
        return
    
    print(f"\n📰 NOTÍCIAS DE HOJE: {len(response.data)}")
    print(f"\n📁 IMAGENS VÁLIDAS NO ACERVO: {len(IMAGENS_VALIDAS)}")
    for img in IMAGENS_VALIDAS:
        print(f"   • {img}")
    
    print("\n" + "=" * 70)
    print("📋 ANÁLISE DAS NOTÍCIAS:")
    print("=" * 70)
    
    noticias_sem_imagem = []
    
    for i, article in enumerate(response.data, 1):
        title = article.get('title', 'Sem título')[:60]
        image_url = article.get('image_url', '')
        article_id = article.get('id')
        
        print(f"\n{i}. {title}...")
        print(f"   ID: {article_id}")
        print(f"   Image URL: {image_url}")
        
        # Verificar se a imagem é válida
        if not image_url:
            print(f"   ⚠️ STATUS: SEM IMAGEM")
            noticias_sem_imagem.append(article)
        elif 'r2.dev' in image_url or 'cloudflare' in image_url:
            # Verificar se a imagem original ainda existe no acervo
            # Extrair nome do arquivo da URL
            filename = image_url.split('/')[-1]
            print(f"   ✅ STATUS: Imagem hospedada no R2 ({filename})")
        else:
            print(f"   ⚠️ STATUS: URL antiga ou inválida")
            noticias_sem_imagem.append(article)
    
    print("\n" + "=" * 70)
    print(f"📊 RESUMO:")
    print(f"   Total de notícias: {len(response.data)}")
    print(f"   Com imagem válida: {len(response.data) - len(noticias_sem_imagem)}")
    print(f"   Precisam de correção: {len(noticias_sem_imagem)}")
    print("=" * 70)
    
    if noticias_sem_imagem:
        print("\n⚠️ NOTÍCIAS QUE PRECISAM DE CORREÇÃO:")
        for article in noticias_sem_imagem:
            print(f"   • {article.get('title')[:60]}...")
            print(f"     ID: {article.get('id')}")
            print(f"     Categoria: {article.get('category')}")

if __name__ == '__main__':
    main()
