#!/usr/bin/env python3
"""
Script para excluir notícias anteriores a hoje do Supabase
"""

import os
import sys
from datetime import datetime
from pathlib import Path

# Adicionar diretório pai ao path
sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv
from supabase import create_client

# Carregar variáveis de ambiente
load_dotenv(Path(__file__).parent.parent / '.env')

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_SERVICE_KEY')

def main():
    print("=" * 70)
    print("🗑️ LIMPEZA DE NOTÍCIAS ANTIGAS")
    print(f"   Data de hoje: 29/12/2025")
    print("=" * 70)
    
    # Conectar ao Supabase
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    # Buscar todas as notícias
    response = supabase.table('articles').select('id, title, date, created_at').execute()
    
    if not response.data:
        print("Nenhuma notícia encontrada no banco.")
        return
    
    print(f"\n📊 Total de notícias no banco: {len(response.data)}")
    
    # Separar notícias de hoje e antigas
    hoje = "29/12/2025"
    noticias_hoje = []
    noticias_antigas = []
    
    for article in response.data:
        if article.get('date') == hoje:
            noticias_hoje.append(article)
        else:
            noticias_antigas.append(article)
    
    print(f"   ✅ Notícias de hoje ({hoje}): {len(noticias_hoje)}")
    print(f"   ⚠️ Notícias antigas: {len(noticias_antigas)}")
    
    if noticias_antigas:
        print(f"\n📋 NOTÍCIAS A SEREM EXCLUÍDAS:")
        for article in noticias_antigas:
            print(f"   • [{article.get('date')}] {article.get('title')[:60]}...")
        
        print(f"\n🗑️ EXCLUINDO {len(noticias_antigas)} NOTÍCIAS ANTIGAS...")
        
        # Excluir notícias antigas
        ids_para_excluir = [a['id'] for a in noticias_antigas]
        for article_id in ids_para_excluir:
            try:
                supabase.table('articles').delete().eq('id', article_id).execute()
                print(f"   ✗ Excluída ID: {article_id}")
            except Exception as e:
                print(f"   Erro ao excluir ID {article_id}: {e}")
        
        print(f"\n✅ Limpeza concluída!")
    else:
        print("\n✅ Nenhuma notícia antiga para excluir!")
    
    # Mostrar notícias que permaneceram
    print(f"\n📰 NOTÍCIAS MANTIDAS ({len(noticias_hoje)}):")
    for article in noticias_hoje:
        print(f"   • {article.get('title')[:70]}...")

if __name__ == '__main__':
    main()
