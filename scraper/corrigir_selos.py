#!/usr/bin/env python3
"""
Script para corrigir selos e textos de perspectiva das notícias.
- Muda selo de VIÉS para VERIFICADA quando não há cobertura de um dos lados
- Adiciona texto padrão quando a perspectiva está vazia
"""

import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_SERVICE_KEY = os.getenv('SUPABASE_SERVICE_KEY')

TEXTO_PADRAO_DIREITA = "Não foi encontrada cobertura jornalística sobre este tema nos portais de direita consultados."
TEXTO_PADRAO_ESQUERDA = "Não foi encontrada cobertura jornalística sobre este tema nos portais de esquerda consultados."

def main():
    print("\n" + "=" * 70)
    print("🔧 CORREÇÃO DE SELOS E TEXTOS DE PERSPECTIVA")
    print("=" * 70)
    
    supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
    
    # Buscar todas as notícias
    result = supabase.table('articles').select('id,title,has_bias_detected,left_perspective,right_perspective').execute()
    
    correcoes_realizadas = 0
    
    for n in result.data:
        titulo = n['title']
        id_noticia = n['id']
        selo_atual = n['has_bias_detected']
        esq = n['left_perspective'] or ''
        dir = n['right_perspective'] or ''
        
        # Verificar condições
        dir_vazia = not dir or len(dir.strip()) < 10
        dir_nao_encontrada = 'não foi encontrada' in dir.lower() or 'não encontrada' in dir.lower()
        esq_vazia = not esq or len(esq.strip()) < 10
        esq_nao_encontrada = 'não foi encontrada' in esq.lower() or 'não apresentaram cobertura' in esq.lower()
        
        # Preparar atualizações
        updates = {}
        
        # Corrigir selo: se é VIÉS mas não tem cobertura de um dos lados, mudar para VERIFICADA
        if selo_atual:  # has_bias_detected = True (VIÉS)
            if dir_vazia or dir_nao_encontrada or esq_vazia or esq_nao_encontrada:
                updates['has_bias_detected'] = False
                print(f"📝 {titulo[:50]}...")
                print(f"   Selo: VIÉS → VERIFICADA")
        
        # Adicionar texto padrão se direita está vazia
        if dir_vazia:
            updates['right_perspective'] = TEXTO_PADRAO_DIREITA
            updates['has_right_perspective'] = True
            if 'has_bias_detected' not in updates:
                print(f"📝 {titulo[:50]}...")
            print(f"   Direita: Adicionado texto padrão")
        
        # Adicionar texto padrão se esquerda está vazia
        if esq_vazia:
            updates['left_perspective'] = TEXTO_PADRAO_ESQUERDA
            updates['has_left_perspective'] = True
            if 'has_bias_detected' not in updates and not dir_vazia:
                print(f"📝 {titulo[:50]}...")
            print(f"   Esquerda: Adicionado texto padrão")
        
        # Aplicar atualizações se houver
        if updates:
            try:
                supabase.table('articles').update(updates).eq('id', id_noticia).execute()
                correcoes_realizadas += 1
                print(f"   ✅ Atualizado com sucesso")
                print()
            except Exception as e:
                print(f"   ❌ Erro ao atualizar: {e}")
                print()
    
    print("=" * 70)
    print(f"📊 RESUMO: {correcoes_realizadas} notícias corrigidas")
    print("=" * 70)

if __name__ == "__main__":
    main()
