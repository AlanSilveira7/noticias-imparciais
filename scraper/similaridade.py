#!/usr/bin/env python3
"""
Módulo de Similaridade de Texto
Projeto: Axia News
Data: 23/12/2025

Este módulo calcula a similaridade entre textos para detectar
notícias duplicadas ou relacionadas.
"""

import re
import unicodedata
from difflib import SequenceMatcher
from typing import List, Tuple, Optional


def normalizar_texto(texto: str) -> str:
    """
    Normaliza o texto para comparação:
    - Remove acentos
    - Converte para minúsculas
    - Remove pontuação
    - Remove espaços extras
    """
    if not texto:
        return ""
    
    # Remove acentos
    texto = unicodedata.normalize('NFD', texto)
    texto = ''.join(c for c in texto if unicodedata.category(c) != 'Mn')
    
    # Converte para minúsculas
    texto = texto.lower()
    
    # Remove pontuação
    texto = re.sub(r'[^\w\s]', ' ', texto)
    
    # Remove espaços extras
    texto = ' '.join(texto.split())
    
    return texto


def extrair_palavras_chave(texto: str, min_length: int = 3) -> set:
    """
    Extrai palavras-chave de um texto, removendo stopwords comuns.
    """
    stopwords = {
        'que', 'para', 'com', 'por', 'uma', 'seu', 'sua', 'dos', 'das',
        'nos', 'nas', 'pelo', 'pela', 'sobre', 'como', 'mais', 'foi',
        'ser', 'tem', 'são', 'esta', 'este', 'esse', 'essa', 'isso',
        'aqui', 'ali', 'onde', 'quando', 'porque', 'ainda', 'mesmo',
        'muito', 'pode', 'deve', 'apos', 'entre', 'desde', 'antes',
        'depois', 'durante', 'contra', 'sem', 'sob', 'ate', 'cada',
        'todo', 'toda', 'todos', 'todas', 'outro', 'outra', 'outros',
        'outras', 'qual', 'quais', 'quem', 'cujo', 'cuja', 'cujos',
        'cujas', 'quanto', 'quanta', 'quantos', 'quantas', 'the', 'and',
        'for', 'are', 'but', 'not', 'you', 'all', 'can', 'had', 'her',
        'was', 'one', 'our', 'out', 'dia', 'ano', 'mes', 'vez', 'caso'
    }
    
    texto_normalizado = normalizar_texto(texto)
    palavras = texto_normalizado.split()
    
    return {p for p in palavras if len(p) >= min_length and p not in stopwords}


def calcular_similaridade_sequencia(texto1: str, texto2: str) -> float:
    """
    Calcula a similaridade entre dois textos usando SequenceMatcher.
    Retorna um valor entre 0 (totalmente diferentes) e 1 (idênticos).
    """
    if not texto1 or not texto2:
        return 0.0
    
    texto1_norm = normalizar_texto(texto1)
    texto2_norm = normalizar_texto(texto2)
    
    return SequenceMatcher(None, texto1_norm, texto2_norm).ratio()


def calcular_similaridade_jaccard(texto1: str, texto2: str) -> float:
    """
    Calcula a similaridade de Jaccard entre dois textos.
    Baseado na interseção/união das palavras-chave.
    """
    palavras1 = extrair_palavras_chave(texto1)
    palavras2 = extrair_palavras_chave(texto2)
    
    if not palavras1 or not palavras2:
        return 0.0
    
    intersecao = palavras1 & palavras2
    uniao = palavras1 | palavras2
    
    return len(intersecao) / len(uniao)


def calcular_similaridade(texto1: str, texto2: str, peso_sequencia: float = 0.6) -> float:
    """
    Calcula a similaridade combinada entre dois textos.
    
    Combina:
    - Similaridade de sequência (60%) - captura ordem das palavras
    - Similaridade de Jaccard (40%) - captura palavras em comum
    
    Args:
        texto1: Primeiro texto
        texto2: Segundo texto
        peso_sequencia: Peso da similaridade de sequência (0-1)
    
    Returns:
        Valor entre 0 (totalmente diferentes) e 1 (idênticos)
    """
    sim_sequencia = calcular_similaridade_sequencia(texto1, texto2)
    sim_jaccard = calcular_similaridade_jaccard(texto1, texto2)
    
    peso_jaccard = 1 - peso_sequencia
    
    return (sim_sequencia * peso_sequencia) + (sim_jaccard * peso_jaccard)


def classificar_similaridade(similaridade: float) -> str:
    """
    Classifica o nível de similaridade.
    
    Returns:
        'duplicata': > 85% - Notícia praticamente idêntica
        'relacionada': 50-85% - Mesmo tema, conteúdo diferente
        'nova': < 50% - Notícia completamente nova
    """
    if similaridade > 0.85:
        return 'duplicata'
    elif similaridade >= 0.50:
        return 'relacionada'
    else:
        return 'nova'


def encontrar_noticias_similares(
    noticia_nova: dict,
    historico: List[dict],
    dias_comparacao: int = 2,
    campo_titulo: str = 'title',
    campo_data: str = 'date'
) -> List[Tuple[dict, float, str]]:
    """
    Encontra notícias similares no histórico.
    
    Args:
        noticia_nova: Notícia a ser comparada
        historico: Lista de notícias do histórico
        dias_comparacao: Quantos dias para trás comparar
        campo_titulo: Nome do campo de título
        campo_data: Nome do campo de data
    
    Returns:
        Lista de tuplas (noticia, similaridade, classificacao) ordenada por similaridade
    """
    from datetime import datetime, timedelta
    
    titulo_novo = noticia_nova.get(campo_titulo, '')
    
    # Filtrar notícias dos últimos N dias
    hoje = datetime.now()
    data_limite = hoje - timedelta(days=dias_comparacao)
    
    similares = []
    
    for noticia in historico:
        # Tentar parsear a data da notícia
        data_str = noticia.get(campo_data, '')
        try:
            # Tenta formato DD/MM/YYYY
            data_noticia = datetime.strptime(data_str, '%d/%m/%Y')
        except:
            try:
                # Tenta formato YYYY-MM-DD
                data_noticia = datetime.strptime(data_str[:10], '%Y-%m-%d')
            except:
                # Se não conseguir parsear, inclui na comparação
                data_noticia = hoje
        
        # Verifica se está dentro do período
        if data_noticia >= data_limite:
            titulo_historico = noticia.get(campo_titulo, '')
            similaridade = calcular_similaridade(titulo_novo, titulo_historico)
            
            if similaridade > 0.30:  # Threshold mínimo para considerar
                classificacao = classificar_similaridade(similaridade)
                similares.append((noticia, similaridade, classificacao))
    
    # Ordena por similaridade (maior primeiro)
    similares.sort(key=lambda x: x[1], reverse=True)
    
    return similares


def decidir_acao(
    noticia_nova: dict,
    historico: List[dict],
    dias_comparacao: int = 2
) -> Tuple[str, Optional[dict], List[dict]]:
    """
    Decide qual ação tomar com base na similaridade.
    
    Returns:
        Tupla com:
        - acao: 'publicar_nova', 'atualizar_existente', 'publicar_relacionada'
        - noticia_principal: Notícia a ser atualizada (se aplicável)
        - relacionadas: Lista de notícias relacionadas
    """
    similares = encontrar_noticias_similares(
        noticia_nova, 
        historico, 
        dias_comparacao
    )
    
    if not similares:
        return ('publicar_nova', None, [])
    
    # Pega a mais similar
    mais_similar, similaridade, classificacao = similares[0]
    
    # Coleta todas as relacionadas (exceto duplicatas)
    relacionadas = [
        n for n, sim, cls in similares 
        if cls == 'relacionada' and sim >= 0.50
    ]
    
    if classificacao == 'duplicata':
        return ('atualizar_existente', mais_similar, relacionadas)
    elif classificacao == 'relacionada':
        return ('publicar_relacionada', None, relacionadas)
    else:
        return ('publicar_nova', None, relacionadas)


# Testes
if __name__ == '__main__':
    # Teste básico
    titulo1 = "Bolsonaro cancela entrevista e tem cirurgia agendada para o Natal"
    titulo2 = "Bolsonaro cancela entrevista por motivo de cirurgia no Natal"
    titulo3 = "Lula assina indulto de Natal excluindo condenados do 8 de janeiro"
    titulo4 = "Dólar fecha em alta nesta segunda-feira"
    
    print("=== Testes de Similaridade ===\n")
    
    print(f"Título 1: {titulo1}")
    print(f"Título 2: {titulo2}")
    sim = calcular_similaridade(titulo1, titulo2)
    print(f"Similaridade: {sim:.2%} - {classificar_similaridade(sim)}")
    print()
    
    print(f"Título 1: {titulo1}")
    print(f"Título 3: {titulo3}")
    sim = calcular_similaridade(titulo1, titulo3)
    print(f"Similaridade: {sim:.2%} - {classificar_similaridade(sim)}")
    print()
    
    print(f"Título 1: {titulo1}")
    print(f"Título 4: {titulo4}")
    sim = calcular_similaridade(titulo1, titulo4)
    print(f"Similaridade: {sim:.2%} - {classificar_similaridade(sim)}")
