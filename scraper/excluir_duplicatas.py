#!/usr/bin/env python3
"""
Script para excluir notícias duplicadas do Supabase.
Exclui as 3 notícias publicadas erroneamente em 30/12/2025.
"""

import os
from dotenv import load_dotenv
from supabase import create_client

# Carregar variáveis de ambiente
load_dotenv()

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_SERVICE_KEY')

def main():
    print("=" * 60)
    print("EXCLUSÃO DE NOTÍCIAS DUPLICADAS")
    print("=" * 60)
    
    # Conectar ao Supabase
    print("\n[1] Conectando ao Supabase...")
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("    ✓ Conectado")
    
    # Buscar notícias publicadas hoje (30/12/2025) que são duplicatas
    print("\n[2] Buscando notícias duplicadas de 30/12/2025...")
    
    # Títulos das notícias duplicadas a serem excluídas
    titulos_duplicados = [
        "Alterações no FGTS e prazos para saque do abono salarial movimentam trabalhadores em 2025",
        "Presidente concede indulto de Natal a presos no país",
        "Ministro Alexandre de Moraes e Banco Master: Acareação e Investigações em Curso"
    ]
    
    excluidas = 0
    
    for titulo in titulos_duplicados:
        print(f"\n    Buscando: {titulo[:50]}...")
        
        # Buscar a notícia pelo título
        response = supabase.table('articles').select('id, title, date').eq('title', titulo).execute()
        
        if response.data:
            for noticia in response.data:
                noticia_id = noticia['id']
                noticia_date = noticia.get('date', 'N/A')
                
                # Verificar se é de 30/12/2025
                if '30/12/2025' in str(noticia_date) or '2025-12-30' in str(noticia_date):
                    print(f"    → Excluindo ID: {noticia_id} (data: {noticia_date})")
                    
                    # Excluir a notícia
                    delete_response = supabase.table('articles').delete().eq('id', noticia_id).execute()
                    
                    if delete_response.data:
                        print(f"    ✓ Excluída com sucesso")
                        excluidas += 1
                    else:
                        print(f"    ✗ Erro ao excluir")
                else:
                    print(f"    → Ignorando (data diferente: {noticia_date})")
        else:
            print(f"    → Não encontrada")
    
    print("\n" + "=" * 60)
    print(f"RESULTADO: {excluidas} notícias excluídas")
    print("=" * 60)

if __name__ == '__main__':
    main()
