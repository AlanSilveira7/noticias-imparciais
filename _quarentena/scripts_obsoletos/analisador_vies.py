#!/usr/bin/env python3
"""
Módulo de Análise de Viés - Notícias Imparciais
Utiliza IA para analisar e comparar notícias de diferentes fontes.
"""

import json
import os
from datetime import datetime
from pathlib import Path
from openai import OpenAI

# Configurar cliente OpenAI
client = OpenAI()

def carregar_texto_noticia(caminho: str) -> dict:
    """Carrega e parseia um arquivo de texto de notícia."""
    with open(caminho, 'r', encoding='utf-8') as f:
        conteudo = f.read()
    
    # Extrair metadados
    linhas = conteudo.split('\n')
    metadados = {}
    texto = []
    em_texto = False
    
    for linha in linhas:
        if linha.strip() == '---':
            em_texto = True
            continue
        
        if not em_texto:
            if linha.startswith('FONTE:'):
                metadados['fonte'] = linha.replace('FONTE:', '').strip()
            elif linha.startswith('VIÉS:'):
                metadados['vies'] = linha.replace('VIÉS:', '').strip()
            elif linha.startswith('TÍTULO:'):
                metadados['titulo'] = linha.replace('TÍTULO:', '').strip()
            elif linha.startswith('DATA:'):
                metadados['data'] = linha.replace('DATA:', '').strip()
            elif linha.startswith('URL:'):
                metadados['url'] = linha.replace('URL:', '').strip()
        else:
            texto.append(linha)
    
    metadados['texto'] = '\n'.join(texto).strip()
    return metadados


def analisar_vies_noticia(noticia: dict) -> dict:
    """Analisa o viés de uma única notícia usando IA."""
    
    prompt = f"""Analise a seguinte notícia e identifique:

1. FATOS OBJETIVOS: Liste apenas os fatos concretos e verificáveis mencionados.
2. LINGUAGEM CARREGADA: Identifique palavras ou expressões que revelam viés (positivo ou negativo).
3. OMISSÕES POTENCIAIS: O que poderia estar faltando nesta cobertura?
4. ENQUADRAMENTO: Como a notícia enquadra os personagens (heróis, vilões, vítimas)?
5. SCORE DE VIÉS: De -10 (extrema esquerda) a +10 (extrema direita), qual o viés percebido?

FONTE: {noticia['fonte']}
VIÉS DECLARADO: {noticia['vies']}
TÍTULO: {noticia['titulo']}

TEXTO:
{noticia['texto'][:3000]}

Responda em formato JSON com as chaves: fatos_objetivos (lista), linguagem_carregada (lista de dicts com 'termo' e 'conotacao'), omissoes_potenciais (lista), enquadramento (dict com personagens como chaves), score_vies (número), justificativa_score (string).
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "Você é um analista de mídia especializado em identificar vieses editoriais em notícias brasileiras. Seja objetivo e imparcial em sua análise."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            response_format={"type": "json_object"}
        )
        
        resultado = json.loads(response.choices[0].message.content)
        resultado['fonte'] = noticia['fonte']
        resultado['titulo'] = noticia['titulo']
        resultado['vies_declarado'] = noticia['vies']
        return resultado
        
    except Exception as e:
        print(f"Erro ao analisar notícia: {e}")
        return None


def comparar_coberturas(tema: str, noticias_esquerda: list, noticias_direita: list) -> dict:
    """Compara como o mesmo tema é coberto por fontes de diferentes vieses."""
    
    # Preparar resumos das notícias
    resumo_esquerda = "\n\n".join([
        f"[{n['fonte']}] {n['titulo']}\n{n['texto'][:1500]}" 
        for n in noticias_esquerda
    ])
    
    resumo_direita = "\n\n".join([
        f"[{n['fonte']}] {n['titulo']}\n{n['texto'][:1500]}" 
        for n in noticias_direita
    ]) if noticias_direita else "Nenhuma notícia encontrada nas fontes de direita sobre este tema."
    
    prompt = f"""Compare como o tema "{tema}" é coberto por fontes de diferentes orientações editoriais.

## FONTES DE ESQUERDA (UOL, G1/Globo):
{resumo_esquerda}

## FONTES DE DIREITA (Revista Oeste, Brasil Paralelo):
{resumo_direita}

Analise e responda em JSON:

1. FATOS EM COMUM: Quais fatos são reportados por ambos os lados?
2. FATOS EXCLUSIVOS ESQUERDA: O que só as fontes de esquerda mencionam?
3. FATOS EXCLUSIVOS DIREITA: O que só as fontes de direita mencionam?
4. DIFERENÇAS DE ENQUADRAMENTO: Como cada lado enquadra a história?
5. LINGUAGEM COMPARADA: Diferenças de tom e vocabulário entre os lados.
6. VERSÃO IMPARCIAL: Escreva um resumo factual e neutro do acontecimento (3-4 parágrafos).
7. PONTOS DE ATENÇÃO: O que um leitor deve considerar ao ler sobre este tema?

Responda em JSON com as chaves: fatos_comuns (lista), fatos_exclusivos_esquerda (lista), fatos_exclusivos_direita (lista), diferencas_enquadramento (dict com 'esquerda' e 'direita'), linguagem_comparada (dict), versao_imparcial (string), pontos_atencao (lista).
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "Você é um editor-chefe de um portal de notícias imparcial. Sua missão é analisar coberturas de diferentes vieses e produzir uma síntese factual e equilibrada."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            response_format={"type": "json_object"}
        )
        
        resultado = json.loads(response.choices[0].message.content)
        resultado['tema'] = tema
        resultado['fontes_esquerda'] = [n['fonte'] for n in noticias_esquerda]
        resultado['fontes_direita'] = [n['fonte'] for n in noticias_direita] if noticias_direita else []
        return resultado
        
    except Exception as e:
        print(f"Erro ao comparar coberturas: {e}")
        return None


def gerar_relatorio_analise(analises: list, comparacoes: list, output_path: str):
    """Gera um relatório completo de análise de viés."""
    
    relatorio = {
        "data_analise": datetime.now().isoformat(),
        "analises_individuais": analises,
        "comparacoes_tematicas": comparacoes,
        "estatisticas": {
            "total_noticias_analisadas": len(analises),
            "total_temas_comparados": len(comparacoes)
        }
    }
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(relatorio, f, ensure_ascii=False, indent=2)
    
    return relatorio


def main():
    """Função principal para executar análise de viés."""
    print("=" * 60)
    print("ANALISADOR DE VIÉS - NOTÍCIAS IMPARCIAIS")
    print("=" * 60)
    
    # Diretório de textos
    textos_dir = Path('/home/ubuntu/noticias_imparciais/scraper/data/textos')
    
    # Carregar notícias
    print("\n[1] Carregando notícias...")
    noticias = {}
    for arquivo in textos_dir.glob('*.txt'):
        noticia = carregar_texto_noticia(str(arquivo))
        noticias[arquivo.stem] = noticia
        print(f"    - {noticia['fonte']}: {noticia['titulo'][:50]}...")
    
    # Agrupar por tema
    print("\n[2] Agrupando por tema...")
    
    # Tema 1: Caso Ramagem
    ramagem_esquerda = [n for k, n in noticias.items() if 'ramagem' in k.lower() and n['vies'].lower() == 'esquerda']
    ramagem_direita = [n for k, n in noticias.items() if 'ramagem' in k.lower() and n['vies'].lower() == 'direita']
    
    # Tema 2: Moraes/Master
    moraes_esquerda = [n for k, n in noticias.items() if 'moraes' in k.lower() and n['vies'].lower() == 'esquerda']
    moraes_direita = [n for k, n in noticias.items() if 'moraes' in k.lower() and n['vies'].lower() == 'direita']
    
    print(f"    Caso Ramagem: {len(ramagem_esquerda)} esquerda, {len(ramagem_direita)} direita")
    print(f"    Ministro Moraes: {len(moraes_esquerda)} esquerda, {len(moraes_direita)} direita")
    
    # Analisar individualmente
    print("\n[3] Analisando viés individual...")
    analises = []
    for nome, noticia in noticias.items():
        print(f"    Analisando: {noticia['titulo'][:40]}...")
        analise = analisar_vies_noticia(noticia)
        if analise:
            analises.append(analise)
    
    # Comparar coberturas
    print("\n[4] Comparando coberturas por tema...")
    comparacoes = []
    
    if ramagem_esquerda:
        print("    Comparando: Caso Ramagem...")
        comp_ramagem = comparar_coberturas("Caso Ramagem - Extradição e Cassação", ramagem_esquerda, ramagem_direita)
        if comp_ramagem:
            comparacoes.append(comp_ramagem)
    
    if moraes_esquerda or moraes_direita:
        print("    Comparando: Ministro Moraes e Banco Master...")
        comp_moraes = comparar_coberturas("Ministro Alexandre de Moraes e Banco Master", moraes_esquerda, moraes_direita)
        if comp_moraes:
            comparacoes.append(comp_moraes)
    
    # Gerar relatório
    print("\n[5] Gerando relatório...")
    output_path = '/home/ubuntu/noticias_imparciais/scraper/data/relatorio_analise_vies.json'
    relatorio = gerar_relatorio_analise(analises, comparacoes, output_path)
    
    print(f"\n[OK] Relatório salvo em: {output_path}")
    print(f"    - {len(analises)} notícias analisadas")
    print(f"    - {len(comparacoes)} temas comparados")
    
    print("\n" + "=" * 60)
    print("ANÁLISE CONCLUÍDA!")
    print("=" * 60)
    
    return relatorio


if __name__ == '__main__':
    main()
