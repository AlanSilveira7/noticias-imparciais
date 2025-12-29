#!/usr/bin/env python3
"""
Script para agrupar notícias por tema e identificar cobertura múltipla
"""

import json
import os
from datetime import datetime

# Diretório de coleta
COLETA_DIR = "/home/ubuntu/noticias_imparciais/scraper/data/coleta_22dez2025"

def carregar_noticias():
    """Carrega todas as notícias coletadas"""
    todas_noticias = []
    
    for arquivo in os.listdir(COLETA_DIR):
        if arquivo.endswith('.json'):
            with open(os.path.join(COLETA_DIR, arquivo), 'r', encoding='utf-8') as f:
                dados = json.load(f)
                fonte = dados.get('fonte', 'Desconhecida')
                vies = dados.get('vies', 'neutro')
                secao = dados.get('secao', 'geral')
                
                for noticia in dados.get('noticias', []):
                    noticia['fonte'] = fonte
                    noticia['vies'] = vies
                    noticia['secao'] = secao
                    todas_noticias.append(noticia)
    
    return todas_noticias

def identificar_temas(noticias):
    """Identifica temas principais nas notícias"""
    
    # Palavras-chave para agrupamento
    temas = {
        "Augusto Heleno - Prisão Domiciliar": ["heleno", "general heleno", "prisão domiciliar", "alzheimer"],
        "Alexandre Ramagem - Extradição": ["ramagem", "extradição", "cassação", "passaporte"],
        "Moraes e Banco Master": ["moraes", "master", "banco master", "galípolo"],
        "Orçamento e Emendas Parlamentares": ["orçamento", "emendas", "congresso aprova"],
        "Lula - Sanções e Vetos": ["lula sanciona", "lula veta", "reajuste", "judiciário"],
        "Tarcísio e Rodoanel": ["tarcísio", "rodoanel", "mercadante"],
        "Polêmica Havaianas": ["havaianas", "chinelos", "pé direito"],
        "Bolsonaro - Prisão": ["bolsonaro preso", "bolsonaro prisão", "entrevista bolsonaro"],
        "Eleições 2026 - Zema e Flávio": ["zema", "flávio bolsonaro", "kassab"],
        "Dólar e Mercado Financeiro": ["dólar", "bolsa", "câmbio"],
        "Criminosos Mais Procurados": ["mais procurados", "criminosos", "ministério da justiça"],
        "Regime de Recuperação Fiscal RJ": ["toffoli", "recuperação fiscal", "rj"],
        "STF e Aposentadoria": ["stf nega", "aposentadoria", "previdência"],
        "Dino e Emendas": ["dino", "emendas", "tensão stf"],
        "Eduardo Bolsonaro - Passaporte": ["eduardo", "passaporte diplomático"]
    }
    
    noticias_por_tema = {tema: [] for tema in temas}
    noticias_sem_tema = []
    
    for noticia in noticias:
        titulo_lower = noticia.get('titulo', '').lower()
        resumo_lower = noticia.get('resumo', '').lower()
        texto = titulo_lower + " " + resumo_lower
        
        tema_encontrado = False
        for tema, palavras in temas.items():
            for palavra in palavras:
                if palavra in texto:
                    noticias_por_tema[tema].append(noticia)
                    tema_encontrado = True
                    break
            if tema_encontrado:
                break
        
        if not tema_encontrado:
            noticias_sem_tema.append(noticia)
    
    return noticias_por_tema, noticias_sem_tema

def analisar_cobertura(noticias_por_tema):
    """Analisa a cobertura de cada tema por viés"""
    
    analise = {}
    
    for tema, noticias in noticias_por_tema.items():
        if not noticias:
            continue
            
        fontes_esquerda = [n for n in noticias if n.get('vies') == 'esquerda']
        fontes_direita = [n for n in noticias if n.get('vies') == 'direita']
        
        analise[tema] = {
            "total": len(noticias),
            "esquerda": len(fontes_esquerda),
            "direita": len(fontes_direita),
            "cobertura_multipla": len(fontes_esquerda) > 0 and len(fontes_direita) > 0,
            "noticias": noticias,
            "fontes_esquerda": [n.get('fonte') for n in fontes_esquerda],
            "fontes_direita": [n.get('fonte') for n in fontes_direita]
        }
    
    return analise

def main():
    print("=" * 60)
    print("AGRUPAMENTO DE NOTÍCIAS POR TEMA")
    print(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    print("=" * 60)
    
    # Carregar notícias
    noticias = carregar_noticias()
    print(f"\nTotal de notícias coletadas: {len(noticias)}")
    
    # Agrupar por tema
    noticias_por_tema, noticias_sem_tema = identificar_temas(noticias)
    
    # Analisar cobertura
    analise = analisar_cobertura(noticias_por_tema)
    
    # Separar temas com e sem cobertura múltipla
    temas_multiplos = {k: v for k, v in analise.items() if v.get('cobertura_multipla')}
    temas_unicos = {k: v for k, v in analise.items() if not v.get('cobertura_multipla')}
    
    print("\n" + "=" * 60)
    print("TEMAS COM COBERTURA MÚLTIPLA (ESQUERDA + DIREITA)")
    print("=" * 60)
    
    for tema, dados in sorted(temas_multiplos.items(), key=lambda x: x[1]['total'], reverse=True):
        print(f"\n📰 {tema}")
        print(f"   Total: {dados['total']} notícias")
        print(f"   Esquerda: {dados['esquerda']} ({', '.join(set(dados['fontes_esquerda']))})")
        print(f"   Direita: {dados['direita']} ({', '.join(set(dados['fontes_direita']))})")
    
    print("\n" + "=" * 60)
    print("TEMAS COM COBERTURA ÚNICA (APENAS UM VIÉS)")
    print("=" * 60)
    
    for tema, dados in sorted(temas_unicos.items(), key=lambda x: x[1]['total'], reverse=True):
        if dados['total'] > 0:
            vies_predominante = "Esquerda" if dados['esquerda'] > 0 else "Direita"
            print(f"\n📰 {tema}")
            print(f"   Total: {dados['total']} notícias")
            print(f"   Viés: {vies_predominante}")
    
    print(f"\n📌 Notícias sem tema identificado: {len(noticias_sem_tema)}")
    
    # Salvar análise
    resultado = {
        "data_analise": datetime.now().isoformat(),
        "total_noticias": len(noticias),
        "temas_cobertura_multipla": temas_multiplos,
        "temas_cobertura_unica": temas_unicos,
        "noticias_sem_tema": noticias_sem_tema
    }
    
    with open(os.path.join(COLETA_DIR, "analise_temas.json"), 'w', encoding='utf-8') as f:
        json.dump(resultado, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Análise salva em: {COLETA_DIR}/analise_temas.json")
    
    return resultado

if __name__ == "__main__":
    main()
