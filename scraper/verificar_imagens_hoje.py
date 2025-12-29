#!/usr/bin/env python3
"""
Script para verificar imagens das notícias de hoje
Identifica quais notícias estão usando fallback ou imagens inadequadas
"""

import os
import json
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from supabase import create_client

# Carregar variáveis de ambiente
load_dotenv(Path(__file__).parent.parent / '.env')

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_SERVICE_KEY = os.getenv('SUPABASE_SERVICE_KEY')
R2_PUBLIC_URL = os.getenv('R2_PUBLIC_URL')

# Imagens de fallback conhecidas
FALLBACK_IMAGES = [
    'planalto_fachada_01.jpg',
    'planalto_fachada_02.jpg',
    'congresso_panorama_01.jpg'
]

def main():
    print("=" * 70)
    print("VERIFICAÇÃO DE IMAGENS - NOTÍCIAS DE HOJE")
    print(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    print("=" * 70)
    
    # Conectar ao Supabase
    supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
    
    # Buscar todas as notícias
    response = supabase.table('articles').select('id, title, image_url, date, created_at, category').order('created_at', desc=True).execute()
    
    todas_noticias = response.data
    print(f"\nTotal de notícias no banco: {len(todas_noticias)}")
    
    # Filtrar notícias de hoje (29/12/2025)
    hoje = datetime.now().strftime('%d/%m/%Y')
    noticias_hoje = [n for n in todas_noticias if n.get('date') == hoje or (n.get('created_at') and '2025-12-29' in n.get('created_at', ''))]
    
    print(f"Notícias de hoje ({hoje}): {len(noticias_hoje)}")
    
    # Analisar cada notícia
    noticias_com_fallback = []
    noticias_ok = []
    
    print("\n" + "-" * 70)
    print("ANÁLISE DAS NOTÍCIAS DE HOJE:")
    print("-" * 70)
    
    for noticia in noticias_hoje:
        titulo = noticia.get('title', 'Sem título')
        image_url = noticia.get('image_url', '')
        categoria = noticia.get('category', 'N/A')
        
        # Verificar se é fallback
        is_fallback = False
        for fallback in FALLBACK_IMAGES:
            if fallback in image_url:
                is_fallback = True
                break
        
        # Verificar se é imagem genérica do acervo_v4
        is_generic = 'acervo_v4' in image_url
        
        status = "⚠️ FALLBACK" if is_fallback else ("📁 ACERVO_V4" if is_generic else "✅ OK")
        
        print(f"\n{status} | {categoria}")
        print(f"   Título: {titulo[:60]}...")
        print(f"   Imagem: {image_url.split('/')[-1] if image_url else 'N/A'}")
        
        if is_fallback or is_generic:
            noticias_com_fallback.append({
                'id': noticia.get('id'),
                'titulo': titulo,
                'image_url': image_url,
                'categoria': categoria,
                'is_fallback': is_fallback,
                'is_generic': is_generic
            })
        else:
            noticias_ok.append(noticia)
    
    # Se não houver notícias de hoje, mostrar as mais recentes
    if not noticias_hoje:
        print("\n⚠️ Nenhuma notícia encontrada para hoje.")
        print("\nMostrando as 10 notícias mais recentes:")
        for noticia in todas_noticias[:10]:
            titulo = noticia.get('title', 'Sem título')
            image_url = noticia.get('image_url', '')
            data = noticia.get('date', 'N/A')
            
            is_fallback = any(fb in image_url for fb in FALLBACK_IMAGES)
            is_generic = 'acervo_v4' in image_url
            status = "⚠️ FALLBACK" if is_fallback else ("📁 ACERVO_V4" if is_generic else "✅ OK")
            
            print(f"\n{status} | {data}")
            print(f"   Título: {titulo[:60]}...")
            print(f"   Imagem: {image_url.split('/')[-1] if image_url else 'N/A'}")
            
            if is_fallback or is_generic:
                noticias_com_fallback.append({
                    'id': noticia.get('id'),
                    'titulo': titulo,
                    'image_url': image_url,
                    'categoria': noticia.get('category'),
                    'data': data,
                    'is_fallback': is_fallback,
                    'is_generic': is_generic
                })
    
    # Resumo
    print("\n" + "=" * 70)
    print("RESUMO:")
    print("=" * 70)
    print(f"✅ Notícias com imagem adequada: {len(noticias_ok)}")
    print(f"⚠️ Notícias com fallback/genérica: {len(noticias_com_fallback)}")
    
    # Salvar resultado para uso posterior
    resultado = {
        'data_verificacao': datetime.now().isoformat(),
        'total_noticias': len(todas_noticias),
        'noticias_hoje': len(noticias_hoje),
        'noticias_com_fallback': noticias_com_fallback,
        'noticias_ok': len(noticias_ok)
    }
    
    output_file = Path(__file__).parent / 'data' / 'verificacao_imagens.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(resultado, f, ensure_ascii=False, indent=2)
    
    print(f"\nResultado salvo em: {output_file}")
    
    return resultado

if __name__ == '__main__':
    main()
