#!/usr/bin/env python3
"""
Módulo de Análise Semântica de Títulos para Seleção de Imagens

Este módulo analisa o título e conteúdo de uma notícia para determinar:
1. O tema principal (não necessariamente uma pessoa)
2. O tipo de contexto visual esperado
3. Palavras-chave para busca de imagens

Prioridade de contexto:
1. Conceito/Símbolo (ex: FGTS, carteira de trabalho, urna eletrônica)
2. Instituição (ex: STF, Congresso, Banco Central)
3. Evento/Ação (ex: votação, prisão, julgamento)
4. Pessoa (apenas quando é claramente o foco principal)
"""

import re
from typing import Dict, List, Tuple

# Mapeamento de temas para palavras-chave de busca de imagens
MAPEAMENTO_TEMAS = {
    # === ECONOMIA E TRABALHO ===
    'fgts': {
        'palavras_chave': ['FGTS', 'carteira de trabalho', 'Caixa Econômica Federal', 'trabalhador'],
        'categoria_acervo': 'economia',
        'tipo_contexto': 'conceito',
        'prioridade': 1
    },
    'abono salarial': {
        'palavras_chave': ['abono salarial', 'PIS', 'PASEP', 'carteira de trabalho'],
        'categoria_acervo': 'economia',
        'tipo_contexto': 'conceito',
        'prioridade': 1
    },
    'inflação': {
        'palavras_chave': ['Banco Central', 'IPCA', 'inflação', 'economia brasileira'],
        'categoria_acervo': 'economia',
        'tipo_contexto': 'instituicao',
        'prioridade': 2
    },
    'selic': {
        'palavras_chave': ['Banco Central', 'Copom', 'taxa de juros', 'política monetária'],
        'categoria_acervo': 'economia',
        'tipo_contexto': 'instituicao',
        'prioridade': 2
    },
    'pib': {
        'palavras_chave': ['economia brasileira', 'crescimento econômico', 'IBGE'],
        'categoria_acervo': 'economia',
        'tipo_contexto': 'conceito',
        'prioridade': 2
    },
    'bolsa': {
        'palavras_chave': ['B3', 'Bovespa', 'mercado financeiro', 'ações'],
        'categoria_acervo': 'economia',
        'tipo_contexto': 'instituicao',
        'prioridade': 2
    },
    'dólar': {
        'palavras_chave': ['dólar', 'câmbio', 'moeda', 'Banco Central'],
        'categoria_acervo': 'economia',
        'tipo_contexto': 'conceito',
        'prioridade': 2
    },
    
    # === SISTEMA PRISIONAL E JUSTIÇA ===
    'indulto': {
        'palavras_chave': ['presídio', 'penitenciária', 'sistema prisional', 'prisão'],
        'categoria_acervo': 'seguranca',
        'tipo_contexto': 'conceito',
        'prioridade': 1
    },
    'prisão domiciliar': {
        'palavras_chave': [],  # Quando é prisão domiciliar de pessoa específica, foco na pessoa
        'categoria_acervo': 'pessoas',
        'tipo_contexto': 'pessoa',
        'prioridade': 1  # Alta prioridade para capturar antes de 'prisão' genérica
    },
    'prisão': {
        'palavras_chave': ['presídio', 'penitenciária', 'prisão', 'cela'],
        'categoria_acervo': 'seguranca',
        'tipo_contexto': 'conceito',
        'prioridade': 2
    },
    'acareação': {
        'palavras_chave': ['STF', 'Supremo Tribunal Federal', 'plenário STF', 'julgamento'],
        'categoria_acervo': 'judiciario',
        'tipo_contexto': 'instituicao',
        'prioridade': 2
    },
    'julgamento': {
        'palavras_chave': ['STF', 'tribunal', 'plenário', 'justiça'],
        'categoria_acervo': 'judiciario',
        'tipo_contexto': 'instituicao',
        'prioridade': 2
    },
    'investigação': {
        'palavras_chave': ['Polícia Federal', 'PF', 'investigação'],
        'categoria_acervo': 'seguranca',
        'tipo_contexto': 'instituicao',
        'prioridade': 2
    },
    
    # === INSTITUIÇÕES ===
    'stf': {
        'palavras_chave': ['STF', 'Supremo Tribunal Federal', 'plenário STF'],
        'categoria_acervo': 'judiciario',
        'tipo_contexto': 'instituicao',
        'prioridade': 2
    },
    'congresso': {
        'palavras_chave': ['Congresso Nacional', 'Câmara dos Deputados', 'Senado'],
        'categoria_acervo': 'legislativo',
        'tipo_contexto': 'instituicao',
        'prioridade': 2
    },
    'câmara': {
        'palavras_chave': ['Câmara dos Deputados', 'plenário Câmara', 'votação'],
        'categoria_acervo': 'legislativo',
        'tipo_contexto': 'instituicao',
        'prioridade': 2
    },
    'senado': {
        'palavras_chave': ['Senado Federal', 'plenário Senado'],
        'categoria_acervo': 'legislativo',
        'tipo_contexto': 'instituicao',
        'prioridade': 2
    },
    'planalto': {
        'palavras_chave': ['Palácio do Planalto', 'Presidência da República'],
        'categoria_acervo': 'executivo',
        'tipo_contexto': 'instituicao',
        'prioridade': 2
    },
    'banco central': {
        'palavras_chave': ['Banco Central', 'BC', 'Bacen'],
        'categoria_acervo': 'economia',
        'tipo_contexto': 'instituicao',
        'prioridade': 2
    },
    
    # === ELEIÇÕES ===
    'eleição': {
        'palavras_chave': ['urna eletrônica', 'votação', 'eleições', 'TSE'],
        'categoria_acervo': 'eleicoes',
        'tipo_contexto': 'conceito',
        'prioridade': 1
    },
    'votação': {
        'palavras_chave': ['votação', 'plenário', 'Congresso'],
        'categoria_acervo': 'legislativo',
        'tipo_contexto': 'evento',
        'prioridade': 2
    },
    
    # === SAÚDE (pessoa é o foco) ===
    'procedimento médico': {
        'palavras_chave': [],
        'categoria_acervo': 'pessoas',
        'tipo_contexto': 'pessoa',
        'prioridade': 3
    },
    'internado': {
        'palavras_chave': [],
        'categoria_acervo': 'pessoas',
        'tipo_contexto': 'pessoa',
        'prioridade': 3
    },
    'hospital': {
        'palavras_chave': [],
        'categoria_acervo': 'pessoas',
        'tipo_contexto': 'pessoa',
        'prioridade': 3
    },
}

# Mapeamento de pessoas conhecidas
PESSOAS_CONHECIDAS = {
    'lula': {'nome_completo': 'Luiz Inácio Lula da Silva', 'arquivo_acervo': 'lula_oficial'},
    'bolsonaro': {'nome_completo': 'Jair Bolsonaro', 'arquivo_acervo': 'bolsonaro'},
    'alexandre de moraes': {'nome_completo': 'Alexandre de Moraes', 'arquivo_acervo': 'alexandre_moraes'},
    'moraes': {'nome_completo': 'Alexandre de Moraes', 'arquivo_acervo': 'alexandre_moraes'},
    'heleno': {'nome_completo': 'Augusto Heleno', 'arquivo_acervo': 'augusto_heleno'},
    'augusto heleno': {'nome_completo': 'Augusto Heleno', 'arquivo_acervo': 'augusto_heleno'},
    'general heleno': {'nome_completo': 'Augusto Heleno', 'arquivo_acervo': 'augusto_heleno'},
}


def analisar_titulo(titulo: str, conteudo: str = "") -> Dict:
    """
    Analisa o título (e opcionalmente o conteúdo) de uma notícia
    para determinar o contexto visual mais apropriado.
    
    Retorna:
        {
            'tema_principal': str,
            'tipo_contexto': str,  # 'conceito', 'instituicao', 'evento', 'pessoa'
            'palavras_chave_busca': List[str],
            'categoria_acervo': str,
            'pessoa_identificada': str ou None,
            'usar_foto_pessoa': bool
        }
    """
    titulo_lower = titulo.lower()
    texto_completo = f"{titulo} {conteudo}".lower()
    
    # Resultado padrão
    resultado = {
        'tema_principal': None,
        'tipo_contexto': 'generico',
        'palavras_chave_busca': [],
        'categoria_acervo': 'executivo',
        'pessoa_identificada': None,
        'usar_foto_pessoa': False
    }
    
    # 1. Identificar temas no título (ordenados por prioridade)
    temas_encontrados = []
    for tema, config in MAPEAMENTO_TEMAS.items():
        if tema in titulo_lower:
            temas_encontrados.append((tema, config, config['prioridade']))
    
    # Ordenar por prioridade (menor número = maior prioridade)
    temas_encontrados.sort(key=lambda x: x[2])
    
    # 2. Identificar pessoas mencionadas
    pessoa_encontrada = None
    for pessoa, info in PESSOAS_CONHECIDAS.items():
        if pessoa in titulo_lower:
            pessoa_encontrada = info
            resultado['pessoa_identificada'] = info['nome_completo']
            break
    
    # 3. Determinar o contexto visual
    if temas_encontrados:
        tema_principal, config, _ = temas_encontrados[0]
        resultado['tema_principal'] = tema_principal
        resultado['tipo_contexto'] = config['tipo_contexto']
        resultado['categoria_acervo'] = config['categoria_acervo']
        
        # Se o tema tem palavras-chave específicas, usar elas
        if config['palavras_chave']:
            resultado['palavras_chave_busca'] = config['palavras_chave']
            resultado['usar_foto_pessoa'] = False
        else:
            # Tema indica foco na pessoa (ex: procedimento médico, prisão domiciliar)
            resultado['usar_foto_pessoa'] = True
            if pessoa_encontrada:
                resultado['palavras_chave_busca'] = [pessoa_encontrada['nome_completo']]
    
    elif pessoa_encontrada:
        # Se não encontrou tema específico mas encontrou pessoa, usar foto da pessoa
        resultado['tema_principal'] = pessoa_encontrada['nome_completo']
        resultado['tipo_contexto'] = 'pessoa'
        resultado['categoria_acervo'] = 'pessoas'
        resultado['palavras_chave_busca'] = [pessoa_encontrada['nome_completo']]
        resultado['usar_foto_pessoa'] = True
    
    # 4. Fallback - análise de palavras-chave genéricas
    if not resultado['palavras_chave_busca']:
        resultado['palavras_chave_busca'] = _extrair_palavras_chave_genericas(titulo)
    
    return resultado


def _extrair_palavras_chave_genericas(titulo: str) -> List[str]:
    """Extrai palavras-chave genéricas do título quando não há mapeamento específico."""
    # Remover palavras comuns
    stopwords = ['o', 'a', 'os', 'as', 'de', 'da', 'do', 'das', 'dos', 'em', 'no', 'na', 
                 'nos', 'nas', 'para', 'por', 'com', 'e', 'é', 'são', 'foi', 'ser', 'ter',
                 'que', 'se', 'um', 'uma', 'uns', 'umas', 'ao', 'aos', 'à', 'às']
    
    palavras = re.findall(r'\b[A-Za-zÀ-ú]{4,}\b', titulo)
    palavras_filtradas = [p for p in palavras if p.lower() not in stopwords]
    
    return palavras_filtradas[:5]  # Retornar até 5 palavras-chave


def sugerir_imagem_acervo(titulo: str, acervo_disponivel: Dict[str, List[str]]) -> Tuple[str, str]:
    """
    Sugere a melhor imagem do acervo para uma notícia.
    
    Args:
        titulo: Título da notícia
        acervo_disponivel: Dicionário {categoria: [lista de arquivos]}
    
    Returns:
        Tupla (categoria, arquivo) ou (None, None) se não encontrar
    """
    analise = analisar_titulo(titulo)
    
    categoria = analise['categoria_acervo']
    
    # Se deve usar foto de pessoa
    if analise['usar_foto_pessoa'] and analise['pessoa_identificada']:
        for pessoa, info in PESSOAS_CONHECIDAS.items():
            if info['nome_completo'] == analise['pessoa_identificada']:
                # Buscar arquivo da pessoa no acervo
                if 'pessoas' in acervo_disponivel:
                    for arquivo in acervo_disponivel['pessoas']:
                        if info['arquivo_acervo'] in arquivo.lower():
                            return ('pessoas', arquivo)
    
    # Buscar na categoria sugerida
    if categoria in acervo_disponivel and acervo_disponivel[categoria]:
        # Retornar primeira imagem disponível na categoria
        return (categoria, acervo_disponivel[categoria][0])
    
    return (None, None)


# Teste do módulo
if __name__ == "__main__":
    # Testar com os títulos das notícias de hoje
    titulos_teste = [
        "Mudanças no FGTS e prazos para saque do abono salarial impactam trabalhadores",
        "Mercado financeiro revisa projeções de inflação para 2025 e 2026",
        "Presidência concede indulto de Natal a presos no Brasil",
        "General Heleno e Prisão Domiciliar: Atualizações e Contexto",
        "Acareação e Investigações Envolvendo Ministro Alexandre de Moraes e Banco Master",
        "Bolsonaro passa por novo procedimento médico após crise de soluços"
    ]
    
    print("=" * 70)
    print("TESTE DE ANÁLISE SEMÂNTICA DE TÍTULOS")
    print("=" * 70)
    
    for titulo in titulos_teste:
        print(f"\n📰 {titulo[:60]}...")
        analise = analisar_titulo(titulo)
        print(f"   Tema: {analise['tema_principal']}")
        print(f"   Tipo: {analise['tipo_contexto']}")
        print(f"   Categoria: {analise['categoria_acervo']}")
        print(f"   Palavras-chave: {analise['palavras_chave_busca']}")
        print(f"   Usar foto pessoa: {analise['usar_foto_pessoa']}")
        if analise['pessoa_identificada']:
            print(f"   Pessoa: {analise['pessoa_identificada']}")
