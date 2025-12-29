#!/usr/bin/env python3
"""
Script para extrair notícias dos temas selecionados para análise de viés.
"""

import json
from pathlib import Path

def carregar_banco():
    """Carrega o banco de notícias."""
    with open('/home/ubuntu/noticias_imparciais/scraper/data/banco_noticias.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def filtrar_por_tema(noticias, palavras_chave):
    """Filtra notícias que contenham as palavras-chave no título."""
    resultado = []
    for noticia in noticias:
        titulo_lower = noticia['titulo'].lower()
        if any(palavra.lower() in titulo_lower for palavra in palavras_chave):
            resultado.append(noticia)
    return resultado

def agrupar_por_vies(noticias):
    """Agrupa notícias por viés editorial."""
    esquerda = [n for n in noticias if n['vies_editorial'] == 'esquerda']
    direita = [n for n in noticias if n['vies_editorial'] == 'direita']
    return {'esquerda': esquerda, 'direita': direita}

def main():
    # Carregar banco
    banco = carregar_banco()
    noticias = banco['noticias']
    
    print(f"Total de notícias no banco: {len(noticias)}")
    print("=" * 60)
    
    # Tema 1: Caso Ramagem
    print("\n### TEMA 1: CASO RAMAGEM ###")
    palavras_ramagem = ['ramagem', 'extradição', 'deportado', 'cassação']
    noticias_ramagem = filtrar_por_tema(noticias, palavras_ramagem)
    ramagem_por_vies = agrupar_por_vies(noticias_ramagem)
    
    print(f"\nTotal: {len(noticias_ramagem)} notícias")
    print(f"Esquerda: {len(ramagem_por_vies['esquerda'])}")
    print(f"Direita: {len(ramagem_por_vies['direita'])}")
    
    print("\n--- Fontes de ESQUERDA ---")
    for n in ramagem_por_vies['esquerda']:
        print(f"  [{n['fonte']}] {n['titulo']}")
        print(f"    URL: {n['url']}")
    
    print("\n--- Fontes de DIREITA ---")
    for n in ramagem_por_vies['direita']:
        print(f"  [{n['fonte']}] {n['titulo']}")
        print(f"    URL: {n['url']}")
    
    # Tema 2: Ministro Alexandre de Moraes
    print("\n" + "=" * 60)
    print("\n### TEMA 2: MINISTRO ALEXANDRE DE MORAES ###")
    palavras_moraes = ['moraes', 'master', 'stf']
    noticias_moraes = filtrar_por_tema(noticias, palavras_moraes)
    moraes_por_vies = agrupar_por_vies(noticias_moraes)
    
    print(f"\nTotal: {len(noticias_moraes)} notícias")
    print(f"Esquerda: {len(moraes_por_vies['esquerda'])}")
    print(f"Direita: {len(moraes_por_vies['direita'])}")
    
    print("\n--- Fontes de ESQUERDA ---")
    for n in moraes_por_vies['esquerda']:
        print(f"  [{n['fonte']}] {n['titulo']}")
        print(f"    URL: {n['url']}")
    
    print("\n--- Fontes de DIREITA ---")
    for n in moraes_por_vies['direita']:
        print(f"  [{n['fonte']}] {n['titulo']}")
        print(f"    URL: {n['url']}")
    
    # Salvar dados para análise
    dados_analise = {
        'caso_ramagem': {
            'esquerda': ramagem_por_vies['esquerda'],
            'direita': ramagem_por_vies['direita']
        },
        'ministro_moraes': {
            'esquerda': moraes_por_vies['esquerda'],
            'direita': moraes_por_vies['direita']
        }
    }
    
    output_path = '/home/ubuntu/noticias_imparciais/scraper/data/temas_para_analise.json'
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(dados_analise, f, ensure_ascii=False, indent=2)
    
    print(f"\n\nDados salvos em: {output_path}")

if __name__ == '__main__':
    main()
