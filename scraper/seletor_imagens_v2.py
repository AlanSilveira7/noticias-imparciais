#!/usr/bin/env python3
"""
Seletor de Imagens v2 - Extração inteligente de palavras-chave
Analisa o título da notícia e seleciona a imagem mais contextual do acervo.
"""

import os
import re
import random
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).parent.parent / '.env')

R2_PUBLIC_URL = os.getenv('R2_PUBLIC_URL')

# Mapeamento de palavras-chave para categorias e imagens específicas
MAPEAMENTO_CONTEXTUAL = {
    # STF - Supremo Tribunal Federal
    'stf': {
        'palavras': ['stf', 'supremo', 'ministro', 'moraes', 'alexandre', 'toffoli', 'barroso', 
                     'nunes marques', 'gilmar', 'mendes', 'fux', 'carmen lucia', 'dino', 'flavio dino',
                     'aposentadoria', 'constitucional', 'inconstitucional', 'ação direta'],
        'imagens': ['stf_plenario_vista.jpg', 'stf_sessao_plenaria.jpg', 'stf_plenario_completo.jpg',
                    'stf_sessao_votacao.jpg', 'stf_plenario_ministros.jpg', 'stf_fachada_2023.jpg',
                    'stf_fachada_niemeyer.jpg', 'stf_estatua_justica.jpg', 'stf_fachada_lateral.jpg']
    },
    
    # Congresso Nacional
    'congresso': {
        'palavras': ['congresso', 'câmara', 'camara', 'deputados', 'senado', 'senadores',
                     'votação', 'votacao', 'orçamento', 'orcamento', 'pec', 'projeto de lei',
                     'aprovação', 'aprovacao', 'legislativo', 'parlamentar', 'emenda'],
        'imagens': ['camara_plenario_amplo.jpg', 'congresso_espelho_agua.jpg', 'congresso_fachada_gramado.jpg',
                    'congresso_lateral.jpg', 'congresso_niemeyer.jpg', 'senado_plenario.jpg',
                    'camara_plenario_cadeiras.jpg', 'camara_plenario_vazio.jpg']
    },
    
    # Planalto / Presidência
    'planalto': {
        'palavras': ['lula', 'presidente', 'planalto', 'governo federal', 'sanção', 'sancao',
                     'decreto', 'medida provisória', 'mp', 'ministro de estado', 'ministério',
                     'ministerio', 'bolsonaro', 'executivo', 'indulto'],
        'imagens': ['planalto_espelho.jpg', 'planalto_lateral_agua.jpg', 'planalto_noite.jpg',
                    'planalto_fachada_flores.jpg', 'planalto_bandeira.jpg', 'planalto_rampa_posse.jpg',
                    'planalto_vista_lateral.jpg']
    },
    
    # Economia
    'economia': {
        'palavras': ['dólar', 'dolar', 'real', 'bolsa', 'b3', 'ibovespa', 'inflação', 'inflacao',
                     'selic', 'juros', 'banco central', 'bacen', 'pib', 'economia', 'mercado',
                     'fgts', 'saque', 'financeiro', 'fiscal', 'tributário', 'tributario'],
        'imagens': ['b3_touro_lateral.jpg', 'b3_touro_fachada.jpg', 'b3_touro_close.jpg',
                    'banco_central_fachada.jpg', 'banco_central_aereo.jpg', 'banco_central_noite.jpg',
                    'real_cedulas.jpg', 'real_notas_antigas.jpg']
    },
    
    # Justiça / Polícia Federal
    'justica': {
        'palavras': ['polícia federal', 'policia federal', 'pf', 'operação', 'operacao',
                     'prisão', 'prisao', 'mandado', 'investigação', 'investigacao', 'crime',
                     'criminoso', 'procurado', 'extradição', 'extradicao', 'stj', 'justiça federal',
                     'passaporte', 'inquérito', 'inquerito', 'ministério da justiça', 'ministerio da justica'],
        'imagens': ['pf_operacao_agentes.jpg', 'pf_operacao_tatica.jpg', 'pf_viatura_close.jpg',
                    'pf_viaturas_frota.jpg', 'pf_sede_brasilia.jpg', 'pf_viatura_predio.jpg',
                    'stj_fachada.jpg']
    },
    
    # Eleições
    'eleicoes': {
        'palavras': ['eleição', 'eleicao', 'eleitoral', 'tse', 'urna', 'voto', 'candidato',
                     'candidatura', 'campanha eleitoral', 'partido', 'coligação', 'coligacao', '2026',
                     'zema', 'flávio bolsonaro', 'flavio bolsonaro'],
        'imagens': ['urna_eletronica_frontal.jpg', 'urna_votacao_mao.jpg', 'tse_fachada_placa.jpg',
                    'tse_sede_nova.jpg', 'tse_predio_por_sol.jpg']
    }
}

# Mapeamento de categoria de notícia para categoria de acervo padrão
CATEGORIA_PADRAO = {
    'Política': 'planalto',
    'Economia': 'economia',
    'Brasil': 'planalto',
    'Mundo': 'planalto'
}

# Palavras que indicam que NÃO é sobre política/governo (marcas, empresas, etc.)
PALAVRAS_COMERCIAIS = ['havaianas', 'publicidade', 'publicitária', 'publicitario', 'comercial',
                       'marca', 'empresa', 'produto', 'marketing']


def eh_noticia_comercial(titulo: str) -> bool:
    """Verifica se a notícia é sobre marcas/empresas e não sobre política"""
    titulo_lower = titulo.lower()
    return any(palavra in titulo_lower for palavra in PALAVRAS_COMERCIAIS)


def extrair_palavras_chave(titulo: str) -> list:
    """Extrai palavras-chave relevantes do título"""
    titulo_lower = titulo.lower()
    palavras_encontradas = []
    
    # Se for notícia comercial, não extrair palavras-chave políticas
    if eh_noticia_comercial(titulo):
        return []
    
    for categoria, config in MAPEAMENTO_CONTEXTUAL.items():
        for palavra in config['palavras']:
            if palavra in titulo_lower:
                palavras_encontradas.append((categoria, palavra, len(palavra)))
    
    # Ordenar por tamanho da palavra (mais específica primeiro)
    palavras_encontradas.sort(key=lambda x: x[2], reverse=True)
    
    return palavras_encontradas


def selecionar_categoria(titulo: str, categoria_noticia: str = None) -> str:
    """Seleciona a categoria de acervo mais adequada baseada no título"""
    palavras = extrair_palavras_chave(titulo)
    
    if palavras:
        # Retorna a categoria da palavra-chave mais específica
        return palavras[0][0]
    
    # Fallback para categoria padrão baseada na categoria da notícia
    if categoria_noticia and categoria_noticia in CATEGORIA_PADRAO:
        return CATEGORIA_PADRAO[categoria_noticia]
    
    return 'planalto'  # Fallback final


def selecionar_imagem(titulo: str, categoria_noticia: str = None, imagens_ja_usadas: set = None) -> dict:
    """
    Seleciona a imagem mais adequada para uma notícia.
    
    Args:
        titulo: Título da notícia
        categoria_noticia: Categoria da notícia (Política, Economia, etc.)
        imagens_ja_usadas: Set de URLs de imagens já usadas (para evitar repetições)
    
    Returns:
        dict com 'url', 'imagem', 'categoria_acervo' e 'palavras_chave'
    """
    if imagens_ja_usadas is None:
        imagens_ja_usadas = set()
    
    # Extrair palavras-chave e determinar categoria
    palavras = extrair_palavras_chave(titulo)
    categoria = selecionar_categoria(titulo, categoria_noticia)
    
    # Obter lista de imagens da categoria
    imagens_disponiveis = MAPEAMENTO_CONTEXTUAL[categoria]['imagens'].copy()
    
    # Filtrar imagens já usadas
    imagens_filtradas = []
    for img in imagens_disponiveis:
        url = f"{R2_PUBLIC_URL}/noticias/acervo/{categoria}/{img}"
        if url not in imagens_ja_usadas:
            imagens_filtradas.append(img)
    
    # Se todas foram usadas, usar qualquer uma
    if not imagens_filtradas:
        imagens_filtradas = imagens_disponiveis
    
    # Selecionar imagem aleatoriamente entre as disponíveis
    imagem_selecionada = random.choice(imagens_filtradas)
    url = f"{R2_PUBLIC_URL}/noticias/acervo/{categoria}/{imagem_selecionada}"
    
    return {
        'url': url,
        'imagem': imagem_selecionada,
        'categoria_acervo': categoria,
        'palavras_chave': [p[1] for p in palavras[:3]]  # Top 3 palavras-chave
    }


def analisar_noticias_exemplo():
    """Testa o seletor com exemplos de notícias"""
    exemplos = [
        ("STF decide sobre aposentadoria integral em casos de doença grave não ocupacional", "Política"),
        ("Ministério da Justiça divulga lista de criminosos mais procurados por estado", "Política"),
        ("Dólar se mantém acima de R$ 5,50 e Bolsa de Valores registra fechamento em alta", "Economia"),
        ("Cenário Eleitoral 2026: Discussões sobre as candidaturas de Zema e Flávio Bolsonaro", "Política"),
        ("Lula sanciona reajuste para servidores do Judiciário e veta aumentos futuros", "Política"),
        ("Congresso Nacional aprova Orçamento da União para o próximo exercício", "Economia"),
        ("Polícia Federal faz operação contra quadrilha de tráfico internacional", "Política"),
        ("Ministro Alexandre de Moraes concede prisão domiciliar a réu", "Política"),
        ("Campanha Publicitária da Havaianas Gera Debate nas Redes Sociais", "Política"),
        ("Eduardo Bolsonaro pode perder passaporte após decisão judicial", "Política"),
        ("General Heleno inicia cumprimento de prisão domiciliar", "Política"),
        ("Inflação registra alta em 2025 enquanto mercado aguarda decisão do Copom", "Economia"),
    ]
    
    print("TESTE DO SELETOR DE IMAGENS V2")
    print("=" * 80)
    
    imagens_usadas = set()
    
    for titulo, categoria in exemplos:
        resultado = selecionar_imagem(titulo, categoria, imagens_usadas)
        imagens_usadas.add(resultado['url'])
        
        print(f"\n📰 {titulo[:60]}...")
        print(f"   Categoria notícia: {categoria}")
        print(f"   Palavras-chave: {resultado['palavras_chave']}")
        print(f"   Categoria acervo: {resultado['categoria_acervo']}")
        print(f"   Imagem: {resultado['imagem']}")


if __name__ == '__main__':
    analisar_noticias_exemplo()
