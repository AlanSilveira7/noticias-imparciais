#!/usr/bin/env python3
"""
Sistema de Categorização Inteligente de Imagens para Notícias Imparciais

Este módulo seleciona a imagem mais adequada do acervo brasileiro
baseado no título, categoria e conteúdo da notícia.
"""

import os
import random
import hashlib
from pathlib import Path
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv(dotenv_path=Path(__file__).parent.parent / '.env')

R2_PUBLIC_URL = os.getenv('R2_PUBLIC_URL')
ACERVO_BASE_URL = f"{R2_PUBLIC_URL}/noticias/acervo"

# Catálogo de imagens disponíveis no acervo
CATALOGO_IMAGENS = {
    'stf': [
        'stf_estatua_justica.jpg',
        'stf_fachada_niemeyer.jpg',
        'stf_fachada_lateral.jpg',
        'stf_sessao_plenaria.jpg',
        'stf_plenario_vista.jpg',
        'stf_plenario_ministros.jpg',
        'stf_estatua_frente.jpg',
        'stf_fachada_2023.jpg',
    ],
    'congresso': [
        'congresso_fachada_gramado.jpg',
        'congresso_niemeyer.jpg',
        'congresso_espelho_agua.jpg',
        'camara_plenario_oficial.jpg',
        'camara_plenario_amplo.jpg',
        'camara_plenario_cadeiras.jpg',
        'senado_plenario.jpg',
        'congresso_lateral.jpg',
    ],
    'planalto': [
        'planalto_fachada_flores.jpg',
        'planalto_lateral_agua.jpg',
        'planalto_bandeira.jpg',
        'planalto_espelho.jpg',
        'planalto_noite.jpg',
        'planalto_rampa_posse.jpg',
        'planalto_vista_lateral.jpg',
    ],
    'economia': [
        'b3_touro_fachada.jpg',
        'b3_touro_lateral.jpg',
        'b3_touro_close.jpg',
        'banco_central_noite.jpg',
        'banco_central_fachada.jpg',
        'banco_central_aereo.jpg',
        'real_notas_antigas.jpg',
        'real_cedulas.jpg',
    ],
    'justica': [
        'pf_viatura_close.jpg',
        'pf_operacao_agentes.jpg',
        'pf_operacao_tatica.jpg',
        'pf_sede_brasilia.jpg',
        'pf_viaturas_frota.jpg',
        'pf_viatura_predio.jpg',
        'stj_fachada.jpg',
    ],
    'eleicoes': [
        'urna_eletronica_frontal.jpg',
        'urna_votacao_mao.jpg',
        'urna_digitando.jpg',
        'tse_predio_por_sol.jpg',
        'tse_sede_nova.jpg',
        'tse_fachada_placa.jpg',
    ],
}

# Mapeamento de palavras-chave para categorias
MAPEAMENTO_KEYWORDS = {
    # STF
    'stf': 'stf',
    'supremo': 'stf',
    'supremo tribunal': 'stf',
    'ministro do stf': 'stf',
    'moraes': 'stf',
    'alexandre de moraes': 'stf',
    'barroso': 'stf',
    'toffoli': 'stf',
    'nunes marques': 'stf',
    'gilmar': 'stf',
    'fux': 'stf',
    'carmen lucia': 'stf',
    'aposentadoria integral': 'stf',
    
    # Congresso
    'congresso': 'congresso',
    'câmara': 'congresso',
    'camara': 'congresso',
    'senado': 'congresso',
    'deputado': 'congresso',
    'senador': 'congresso',
    'orçamento': 'congresso',
    'orcamento': 'congresso',
    'votação': 'congresso',
    'plenário': 'congresso',
    'emenda': 'congresso',
    'projeto de lei': 'congresso',
    'pl ': 'congresso',
    'pec': 'congresso',
    
    # Planalto / Presidente
    'planalto': 'planalto',
    'presidente': 'planalto',
    'lula': 'planalto',
    'bolsonaro': 'planalto',
    'governo federal': 'planalto',
    'sanciona': 'planalto',
    'veta': 'planalto',
    'indulto': 'planalto',
    'decreto': 'planalto',
    'ministério': 'planalto',
    'ministro': 'planalto',  # fallback se não for STF
    'heleno': 'planalto',
    'turismo': 'planalto',
    
    # Economia
    'economia': 'economia',
    'econômico': 'economia',
    'dólar': 'economia',
    'dolar': 'economia',
    'bolsa': 'economia',
    'b3': 'economia',
    'ibovespa': 'economia',
    'inflação': 'economia',
    'inflacao': 'economia',
    'selic': 'economia',
    'juros': 'economia',
    'banco central': 'economia',
    'bacen': 'economia',
    'pib': 'economia',
    'fgts': 'economia',
    'real': 'economia',
    'moeda': 'economia',
    
    # Justiça / Polícia
    'polícia federal': 'justica',
    'policia federal': 'justica',
    'pf ': 'justica',
    'operação': 'justica',
    'operacao': 'justica',
    'prisão': 'justica',
    'prisao': 'justica',
    'criminoso': 'justica',
    'crime': 'justica',
    'justiça': 'justica',
    'justica': 'justica',
    'stj': 'justica',
    'tribunal': 'justica',
    'passaporte': 'justica',
    'extradição': 'justica',
    
    # Eleições
    'eleição': 'eleicoes',
    'eleicao': 'eleicoes',
    'eleitoral': 'eleicoes',
    'urna': 'eleicoes',
    'tse': 'eleicoes',
    'candidatura': 'eleicoes',
    'candidato': 'eleicoes',
    'voto': 'eleicoes',
    'votação': 'eleicoes',
    '2026': 'eleicoes',
}

# Histórico de imagens usadas (para evitar repetições)
_imagens_usadas = {}

def _gerar_hash_titulo(titulo: str) -> str:
    """Gera um hash do título para consistência"""
    return hashlib.md5(titulo.encode()).hexdigest()[:8]

def _detectar_categoria(titulo: str, categoria_noticia: str = '') -> str:
    """
    Detecta a categoria mais adequada baseada no título e categoria da notícia.
    Retorna a categoria do acervo.
    """
    titulo_lower = titulo.lower()
    categoria_lower = categoria_noticia.lower()
    
    # Verificar palavras-chave no título (ordem de prioridade)
    # Primeiro, verificar termos mais específicos
    termos_ordenados = sorted(MAPEAMENTO_KEYWORDS.keys(), key=len, reverse=True)
    
    for termo in termos_ordenados:
        if termo in titulo_lower:
            return MAPEAMENTO_KEYWORDS[termo]
    
    # Fallback por categoria da notícia
    if 'economia' in categoria_lower:
        return 'economia'
    elif 'política' in categoria_lower or 'politica' in categoria_lower:
        return 'planalto'  # fallback genérico para política
    
    # Fallback final
    return 'planalto'

def selecionar_imagem(titulo: str, categoria_noticia: str = '', article_id: str = None) -> dict:
    """
    Seleciona a imagem mais adequada do acervo para uma notícia.
    
    Args:
        titulo: Título da notícia
        categoria_noticia: Categoria da notícia (Política, Economia, etc.)
        article_id: ID único do artigo (para consistência)
    
    Returns:
        dict com 'url' e 'categoria' da imagem selecionada
    """
    # Detectar categoria do acervo
    categoria_acervo = _detectar_categoria(titulo, categoria_noticia)
    
    # Obter lista de imagens da categoria
    imagens_disponiveis = CATALOGO_IMAGENS.get(categoria_acervo, CATALOGO_IMAGENS['planalto'])
    
    # Usar hash do título para seleção consistente (mesma notícia = mesma imagem)
    if article_id:
        hash_seed = article_id
    else:
        hash_seed = _gerar_hash_titulo(titulo)
    
    # Selecionar imagem baseada no hash (determinístico)
    indice = int(hash_seed, 16) % len(imagens_disponiveis) if hash_seed.isalnum() else hash(hash_seed) % len(imagens_disponiveis)
    imagem_selecionada = imagens_disponiveis[abs(indice)]
    
    # Construir URL completa
    url = f"{ACERVO_BASE_URL}/{categoria_acervo}/{imagem_selecionada}"
    
    return {
        'url': url,
        'categoria_acervo': categoria_acervo,
        'imagem': imagem_selecionada,
    }

def selecionar_imagem_sem_repeticao(titulo: str, categoria_noticia: str = '', 
                                     imagens_ja_usadas: set = None) -> dict:
    """
    Seleciona uma imagem evitando repetições recentes.
    
    Args:
        titulo: Título da notícia
        categoria_noticia: Categoria da notícia
        imagens_ja_usadas: Set de URLs de imagens já usadas recentemente
    
    Returns:
        dict com 'url' e 'categoria' da imagem selecionada
    """
    if imagens_ja_usadas is None:
        imagens_ja_usadas = set()
    
    # Detectar categoria do acervo
    categoria_acervo = _detectar_categoria(titulo, categoria_noticia)
    
    # Obter lista de imagens da categoria
    imagens_disponiveis = CATALOGO_IMAGENS.get(categoria_acervo, CATALOGO_IMAGENS['planalto'])
    
    # Filtrar imagens já usadas
    imagens_livres = [img for img in imagens_disponiveis 
                      if f"{ACERVO_BASE_URL}/{categoria_acervo}/{img}" not in imagens_ja_usadas]
    
    # Se todas já foram usadas, usar qualquer uma
    if not imagens_livres:
        imagens_livres = imagens_disponiveis
    
    # Selecionar aleatoriamente entre as disponíveis
    imagem_selecionada = random.choice(imagens_livres)
    
    # Construir URL completa
    url = f"{ACERVO_BASE_URL}/{categoria_acervo}/{imagem_selecionada}"
    
    return {
        'url': url,
        'categoria_acervo': categoria_acervo,
        'imagem': imagem_selecionada,
    }

# Teste
if __name__ == '__main__':
    # Testar com alguns títulos
    titulos_teste = [
        ("STF decide sobre aposentadoria integral em casos de doença grave", "Política"),
        ("Ministério da Justiça divulga lista de criminosos mais procurados", "Política"),
        ("Dólar se mantém acima de R$ 5,50 e Bolsa registra alta", "Economia"),
        ("Cenário Eleitoral 2026: Discussões sobre candidaturas", "Política"),
        ("Lula sanciona reajuste para servidores do Judiciário", "Política"),
        ("Congresso Nacional aprova Orçamento da União", "Política"),
        ("Polícia Federal faz operação contra quadrilha", "Política"),
        ("Inflação registra alta em 2025", "Economia"),
    ]
    
    print("TESTE DO SELETOR DE IMAGENS")
    print("=" * 70)
    
    for titulo, categoria in titulos_teste:
        resultado = selecionar_imagem(titulo, categoria)
        print(f"\n📰 {titulo[:50]}...")
        print(f"   Categoria: {resultado['categoria_acervo']}")
        print(f"   Imagem: {resultado['imagem']}")
