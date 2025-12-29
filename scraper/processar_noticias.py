#!/usr/bin/env python3
"""
Script para processar notícias coletadas, analisar vieses e gerar notícias imparciais.
Projeto: Notícias Imparciais
Data: 29/12/2025
"""

import json
import os
from datetime import datetime
from pathlib import Path
from openai import OpenAI
from deduplicacao import GerenciadorDeduplicacao

# Configurar cliente OpenAI
client = OpenAI()

DATA_DIR = '/home/ubuntu/noticias-imparciais/scraper/data'

def carregar_noticias_fonte(arquivo: str) -> list:
    """Carrega notícias de um arquivo JSON."""
    caminho = os.path.join(DATA_DIR, arquivo)
    if os.path.exists(caminho):
        with open(caminho, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def identificar_temas_comuns(noticias_esquerda: list, noticias_direita: list) -> list:
    """Identifica temas comuns entre notícias de diferentes vieses."""
    
    # Palavras-chave para agrupamento
    temas_keywords = {
        'Bolsonaro e Cirurgia': ['bolsonaro', 'cirurgia', 'saúde', 'internado', 'entrevista'],
        'Ministro Moraes e Banco Master': ['moraes', 'master', 'galípolo', 'magnitsky', 'bc'],
        'General Heleno e Prisão Domiciliar': ['heleno', 'prisão domiciliar', 'domiciliar'],
        'Indulto de Natal': ['indulto', 'natal', '8 de janeiro'],
        'Ministério do Turismo': ['turismo', 'feliciano', 'sabino', 'motta'],
        'Havaianas e Boicote': ['havaianas', 'boicote', 'alpargatas'],
        'Economia e Inflação': ['dólar', 'inflação', 'ipca', 'bolsa', 'economia'],
        'FGTS e Trabalhadores': ['fgts', 'saque', 'trabalhador'],
        'Eduardo Bolsonaro e Passaporte': ['eduardo', 'passaporte', 'cassação'],
    }
    
    temas_encontrados = {}
    
    todas_noticias = [
        {'noticia': n, 'vies': 'esquerda'} for n in noticias_esquerda
    ] + [
        {'noticia': n, 'vies': 'direita'} for n in noticias_direita
    ]
    
    for tema, keywords in temas_keywords.items():
        noticias_tema = []
        for item in todas_noticias:
            titulo_lower = item['noticia'].get('titulo', '').lower()
            if any(kw in titulo_lower for kw in keywords):
                noticias_tema.append(item)
        
        if noticias_tema:
            esquerda = [n for n in noticias_tema if n['vies'] == 'esquerda']
            direita = [n for n in noticias_tema if n['vies'] == 'direita']
            
            if esquerda or direita:
                temas_encontrados[tema] = {
                    'esquerda': esquerda,
                    'direita': direita,
                    'total': len(noticias_tema)
                }
    
    return temas_encontrados


def gerar_noticia_imparcial(tema: str, noticias_esquerda: list, noticias_direita: list) -> dict:
    """Gera uma notícia imparcial a partir de notícias de diferentes vieses."""
    
    # Preparar resumos
    resumo_esquerda = "\n".join([
        f"- [{n['noticia'].get('url', 'UOL/G1')}] {n['noticia']['titulo']}"
        for n in noticias_esquerda
    ]) if noticias_esquerda else "Nenhuma notícia encontrada."
    
    resumo_direita = "\n".join([
        f"- [{n['noticia'].get('url', 'Oeste/BP')}] {n['noticia']['titulo']}"
        for n in noticias_direita
    ]) if noticias_direita else "Nenhuma notícia encontrada."
    
    prompt = f"""Você é o editor-chefe do portal "Notícias Imparciais", com o slogan "Os fatos, sem filtro."

Com base nas manchetes abaixo de diferentes fontes, gere uma NOTÍCIA IMPARCIAL sobre o tema "{tema}".

## FONTES DE ESQUERDA (UOL, G1/Globo):
{resumo_esquerda}

## FONTES DE DIREITA (Revista Oeste, Brasil Paralelo):
{resumo_direita}

## INSTRUÇÕES:

1. **TÍTULO**: Neutro, factual, sem adjetivos carregados
2. **SUBTÍTULO**: Resumo objetivo do acontecimento principal
3. **LEAD**: Responder O quê, Quem, Quando, Onde, Como
4. **CORPO**: 3-4 parágrafos com os fatos objetivos
5. **SEÇÃO "O QUE DIZ CADA LADO"**: Resumir perspectivas de cada viés
6. **PONTOS DE ATENÇÃO**: Alertas para o leitor sobre possíveis vieses

Responda em JSON com as chaves:
- titulo (string)
- subtitulo (string)
- secao (string: "politica" ou "economia")
- lead (string)
- corpo (lista de parágrafos)
- o_que_diz_esquerda (string)
- o_que_diz_direita (string)
- pontos_atencao (lista de strings)
- tags (lista de strings)
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "Você é um jornalista imparcial comprometido com a verdade factual. Sua missão é informar sem influenciar, apresentando todos os lados de forma equilibrada."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            response_format={"type": "json_object"}
        )
        
        noticia = json.loads(response.choices[0].message.content)
        noticia['tema'] = tema
        noticia['data_publicacao'] = datetime.now().strftime('%Y-%m-%d')
        noticia['data_geracao'] = datetime.now().isoformat()
        noticia['fontes_esquerda'] = [n['noticia']['titulo'] for n in noticias_esquerda]
        noticia['fontes_direita'] = [n['noticia']['titulo'] for n in noticias_direita]
        
        return noticia
        
    except Exception as e:
        print(f"Erro ao gerar notícia: {e}")
        return None


def main():
    """Função principal."""
    print("=" * 60)
    print("PROCESSADOR DE NOTÍCIAS - NOTÍCIAS IMPARCIAIS")
    print(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    print("=" * 60)
    
    # Carregar notícias de todas as fontes
    print("\n[1] Carregando notícias coletadas...")
    
    # Fontes de esquerda
    uol_politica = carregar_noticias_fonte('uol_politica_novo.json')
    uol_economia = carregar_noticias_fonte('uol_economia_novo.json')
    globo_politica = carregar_noticias_fonte('globo_politica_novo.json')
    globo_economia = carregar_noticias_fonte('globo_economia_novo.json')
    
    # Fontes de direita
    oeste_politica = carregar_noticias_fonte('oeste_politica_novo.json')
    oeste_economia = carregar_noticias_fonte('oeste_economia_novo.json')
    bp_politica = carregar_noticias_fonte('brasil_paralelo_politica_novo.json')
    
    # Consolidar por viés
    noticias_esquerda = uol_politica + uol_economia + globo_politica + globo_economia
    noticias_direita = oeste_politica + oeste_economia + bp_politica
    
    print(f"    - Fontes de esquerda: {len(noticias_esquerda)} notícias")
    print(f"    - Fontes de direita: {len(noticias_direita)} notícias")
    
    # Identificar temas comuns
    print("\n[2] Identificando temas comuns...")
    temas = identificar_temas_comuns(noticias_esquerda, noticias_direita)
    
    for tema, dados in temas.items():
        print(f"    - {tema}: {len(dados['esquerda'])} esquerda, {len(dados['direita'])} direita")
    
    # Gerar notícias imparciais
    print("\n[3] Gerando notícias imparciais...")
    noticias_geradas = []
    
    for tema, dados in temas.items():
        if dados['esquerda'] or dados['direita']:
            print(f"    Processando: {tema}...")
            noticia = gerar_noticia_imparcial(tema, dados['esquerda'], dados['direita'])
            if noticia:
                noticias_geradas.append(noticia)
                print(f"    ✓ Gerada: {noticia.get('titulo', tema)[:50]}...")
    
    # Deduplicação Inteligente
    print("\n[4] Aplicando deduplicação inteligente...")
    historico_path = os.path.join(DATA_DIR, 'historico_supabase.json')
    if os.path.exists(historico_path):
        with open(historico_path, 'r', encoding='utf-8') as f:
            historico = json.load(f)
    else:
        historico = []
        
    gerenciador = GerenciadorDeduplicacao(dias_comparacao=7)
    
    # Adaptar formato para o deduplicador (espera 'title')
    for n in noticias_geradas:
        n['title'] = n.get('titulo', '')
        
    noticias_imparciais, _ = gerenciador.processar_noticias(noticias_geradas, historico)
    
    # Salvar resultados
    print("\n[5] Salvando resultados...")
    
    # Salvar notícias imparciais
    output_path = os.path.join(DATA_DIR, 'noticias_imparciais.json')
    resultado = {
        'data_geracao': datetime.now().isoformat(),
        'total_noticias': len(noticias_imparciais),
        'fontes_utilizadas': {
            'esquerda': ['UOL', 'G1/Globo'],
            'direita': ['Revista Oeste', 'Brasil Paralelo']
        },
        'noticias': noticias_imparciais
    }
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(resultado, f, ensure_ascii=False, indent=2)
    
    print(f"    ✓ Salvo: {output_path}")
    
    # Atualizar banco de notícias
    banco_path = os.path.join(DATA_DIR, 'banco_noticias.json')
    if os.path.exists(banco_path):
        with open(banco_path, 'r', encoding='utf-8') as f:
            banco = json.load(f)
    else:
        banco = {'noticias': [], 'ultima_atualizacao': None}
    
    # Adicionar novas notícias ao banco
    urls_existentes = {n.get('url', '') for n in banco.get('noticias', [])}
    novas = 0
    
    for n in noticias_esquerda + noticias_direita:
        url = n.get('url', '')
        if url and url not in urls_existentes:
            banco['noticias'].append({
                'titulo': n.get('titulo', ''),
                'url': url,
                'data': n.get('data', ''),
                'resumo': n.get('resumo', ''),
                'data_coleta': datetime.now().isoformat()
            })
            urls_existentes.add(url)
            novas += 1
    
    banco['ultima_atualizacao'] = datetime.now().isoformat()
    banco['total'] = len(banco['noticias'])
    
    with open(banco_path, 'w', encoding='utf-8') as f:
        json.dump(banco, f, ensure_ascii=False, indent=2)
    
    print(f"    ✓ Banco atualizado: {novas} novas notícias adicionadas")
    
    # Exportar para análise
    analise_path = os.path.join(DATA_DIR, f"noticias_para_analise_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
    with open(analise_path, 'w', encoding='utf-8') as f:
        json.dump({
            'data_exportacao': datetime.now().isoformat(),
            'noticias_esquerda': noticias_esquerda,
            'noticias_direita': noticias_direita,
            'temas_identificados': list(temas.keys())
        }, f, ensure_ascii=False, indent=2)
    
    print(f"    ✓ Exportado para análise: {analise_path}")
    
    print("\n" + "=" * 60)
    print(f"PROCESSAMENTO CONCLUÍDO!")
    print(f"  - {len(noticias_imparciais)} notícias imparciais finais (após deduplicação)")
    print(f"  - {novas} novas notícias no banco")
    print("=" * 60)
    
    return resultado


if __name__ == '__main__':
    main()
