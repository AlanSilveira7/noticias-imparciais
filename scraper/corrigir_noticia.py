#!/usr/bin/env python3
"""
Script para corrigir uma notícia publicada.
Exclui a versão antiga e republica a versão corrigida.
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from supabase import create_client

# Carregar variáveis de ambiente
load_dotenv(Path(__file__).parent.parent / '.env')

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_SERVICE_KEY = os.getenv('SUPABASE_SERVICE_KEY')

def excluir_noticia_por_titulo(titulo_parcial: str):
    """Exclui notícias que contenham o título parcial."""
    
    supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
    
    # Buscar notícias com título similar
    response = supabase.table('articles').select('id, title').execute()
    
    excluidas = 0
    for art in response.data:
        if titulo_parcial.lower() in art['title'].lower():
            print(f"Excluindo: {art['title'][:60]}...")
            supabase.table('articles').delete().eq('id', art['id']).execute()
            excluidas += 1
    
    print(f"\n{excluidas} notícia(s) excluída(s).")
    return excluidas

if __name__ == '__main__':
    # Excluir notícias sobre Daniel Vorcaro / Banco Master publicadas hoje
    excluir_noticia_por_titulo("Polícia Federal ouve Daniel Vorcaro")
