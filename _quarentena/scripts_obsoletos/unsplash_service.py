#!/usr/bin/env python3
"""
Módulo de Integração com Unsplash API
Portal Notícias Imparciais

Este módulo busca imagens relevantes no Unsplash com base em palavras-chave
extraídas do título e conteúdo das notícias.

Data: 26/12/2025
"""

import os
import re
import requests
import hashlib
from pathlib import Path
from typing import Optional, List, Dict
from dotenv import load_dotenv

# Carregar variáveis de ambiente
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(env_path)

# Configurações
UNSPLASH_ACCESS_KEY = os.getenv('UNSPLASH_ACCESS_KEY')
UNSPLASH_API_URL = "https://api.unsplash.com"

# Mapeamento de termos em português para inglês (melhora resultados de busca)
TRADUCAO_TERMOS = {
    # Política
    'política': 'politics government',
    'politica': 'politics government',
    'congresso': 'congress parliament',
    'senado': 'senate parliament',
    'câmara': 'congress chamber',
    'camara': 'congress chamber',
    'deputado': 'politician congress',
    'senador': 'senator politician',
    'presidente': 'president government',
    'ministro': 'minister government',
    'stf': 'supreme court justice',
    'supremo': 'supreme court',
    'tribunal': 'court justice',
    'justiça': 'justice court',
    'eleição': 'election vote',
    'eleicao': 'election vote',
    'voto': 'vote election',
    'governo': 'government',
    'federal': 'federal government',
    'brasília': 'brasilia brazil government',
    'brasilia': 'brasilia brazil government',
    'planalto': 'government palace brazil',
    'lula': 'brazil president government',
    'bolsonaro': 'brazil politics',
    
    # Economia
    'economia': 'economy finance',
    'dólar': 'dollar currency money',
    'dolar': 'dollar currency money',
    'real': 'brazilian currency money',
    'bolsa': 'stock market finance',
    'mercado': 'market finance',
    'inflação': 'inflation economy',
    'inflacao': 'inflation economy',
    'juros': 'interest rate finance',
    'banco': 'bank finance',
    'pib': 'gdp economy',
    'orçamento': 'budget finance',
    'orcamento': 'budget finance',
    'imposto': 'tax finance',
    'fiscal': 'fiscal finance',
    'investimento': 'investment finance',
    'emprego': 'employment job',
    'desemprego': 'unemployment',
    'salário': 'salary wage',
    'salario': 'salary wage',
    'fgts': 'savings fund brazil',
    
    # Geral
    'brasil': 'brazil',
    'brasileiro': 'brazilian',
    'rio de janeiro': 'rio de janeiro brazil',
    'são paulo': 'sao paulo brazil',
    'sao paulo': 'sao paulo brazil',
}

# Palavras a ignorar na extração de keywords
STOPWORDS = {
    'de', 'da', 'do', 'das', 'dos', 'em', 'no', 'na', 'nos', 'nas',
    'por', 'para', 'com', 'sem', 'sob', 'sobre', 'entre', 'após',
    'que', 'qual', 'quais', 'como', 'onde', 'quando', 'porque',
    'um', 'uma', 'uns', 'umas', 'o', 'a', 'os', 'as',
    'é', 'são', 'foi', 'foram', 'ser', 'estar', 'ter', 'haver',
    'e', 'ou', 'mas', 'porém', 'contudo', 'todavia',
    'se', 'não', 'sim', 'já', 'ainda', 'também', 'apenas', 'só',
    'mais', 'menos', 'muito', 'pouco', 'bem', 'mal',
    'este', 'esta', 'esse', 'essa', 'aquele', 'aquela',
    'seu', 'sua', 'seus', 'suas', 'meu', 'minha',
    'pode', 'podem', 'deve', 'devem', 'vai', 'vão',
    'ano', 'anos', 'dia', 'dias', 'mês', 'meses',
    'novo', 'nova', 'novos', 'novas',
    'após', 'antes', 'durante', 'segundo',
}


def extrair_keywords(titulo: str, categoria: str = None) -> List[str]:
    """
    Extrai palavras-chave relevantes do título da notícia.
    
    Args:
        titulo: Título da notícia
        categoria: Categoria da notícia (Política, Economia, etc.)
    
    Returns:
        Lista de palavras-chave para busca
    """
    # Normalizar título
    titulo_lower = titulo.lower()
    
    # Remover pontuação
    titulo_clean = re.sub(r'[^\w\s]', ' ', titulo_lower)
    
    # Extrair palavras
    palavras = titulo_clean.split()
    
    # Filtrar stopwords e palavras muito curtas
    keywords = [p for p in palavras if p not in STOPWORDS and len(p) > 2]
    
    # Traduzir termos conhecidos para inglês
    keywords_traduzidas = []
    for kw in keywords:
        if kw in TRADUCAO_TERMOS:
            keywords_traduzidas.append(TRADUCAO_TERMOS[kw])
        else:
            keywords_traduzidas.append(kw)
    
    # Adicionar categoria como contexto
    if categoria:
        cat_lower = categoria.lower()
        if cat_lower in TRADUCAO_TERMOS:
            keywords_traduzidas.insert(0, TRADUCAO_TERMOS[cat_lower])
    
    # Limitar a 5 keywords principais
    return keywords_traduzidas[:5]


def buscar_imagem_unsplash(
    query: str,
    orientation: str = "landscape",
    per_page: int = 10
) -> Optional[Dict]:
    """
    Busca uma imagem no Unsplash com base na query.
    
    Args:
        query: Termos de busca
        orientation: Orientação da imagem (landscape, portrait, squarish)
        per_page: Número de resultados para escolher
    
    Returns:
        Dicionário com informações da imagem ou None se não encontrar
    """
    if not UNSPLASH_ACCESS_KEY:
        print("⚠ UNSPLASH_ACCESS_KEY não configurada!")
        return None
    
    headers = {
        "Authorization": f"Client-ID {UNSPLASH_ACCESS_KEY}",
        "Accept-Version": "v1"
    }
    
    params = {
        "query": query,
        "orientation": orientation,
        "per_page": per_page,
        "content_filter": "high"  # Filtro de conteúdo seguro
    }
    
    try:
        response = requests.get(
            f"{UNSPLASH_API_URL}/search/photos",
            headers=headers,
            params=params,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            results = data.get("results", [])
            
            if results:
                # Selecionar uma imagem baseada no hash da query (consistência)
                # Isso garante que a mesma query sempre retorna a mesma imagem
                query_hash = int(hashlib.md5(query.encode()).hexdigest(), 16)
                index = query_hash % len(results)
                
                foto = results[index]
                
                return {
                    "id": foto["id"],
                    "url_regular": foto["urls"]["regular"],  # 1080px
                    "url_small": foto["urls"]["small"],      # 400px
                    "url_thumb": foto["urls"]["thumb"],      # 200px
                    "url_raw": foto["urls"]["raw"],          # Original
                    "alt_description": foto.get("alt_description", ""),
                    "photographer": foto["user"]["name"],
                    "photographer_url": foto["user"]["links"]["html"],
                    "unsplash_url": foto["links"]["html"],
                    "download_url": foto["links"]["download_location"]
                }
        
        elif response.status_code == 401:
            print("⚠ Erro de autenticação com Unsplash. Verifique a Access Key.")
        elif response.status_code == 403:
            print("⚠ Rate limit excedido no Unsplash.")
        else:
            print(f"⚠ Erro na API Unsplash: {response.status_code}")
            
    except requests.exceptions.Timeout:
        print("⚠ Timeout na requisição ao Unsplash")
    except requests.exceptions.RequestException as e:
        print(f"⚠ Erro de conexão com Unsplash: {e}")
    
    return None


def registrar_download(download_url: str) -> bool:
    """
    Registra o download da imagem no Unsplash (obrigatório pelos termos de uso).
    
    Args:
        download_url: URL de registro de download
    
    Returns:
        True se registrado com sucesso
    """
    if not UNSPLASH_ACCESS_KEY:
        return False
    
    headers = {
        "Authorization": f"Client-ID {UNSPLASH_ACCESS_KEY}"
    }
    
    try:
        response = requests.get(download_url, headers=headers, timeout=5)
        return response.status_code == 200
    except:
        return False


def obter_imagem_para_noticia(
    titulo: str,
    categoria: str = None,
    fallback_queries: List[str] = None
) -> Optional[Dict]:
    """
    Obtém uma imagem relevante para uma notícia.
    
    Esta é a função principal a ser usada pelos scripts de geração de notícias.
    
    Args:
        titulo: Título da notícia
        categoria: Categoria (Política, Economia, etc.)
        fallback_queries: Queries alternativas se a principal não retornar resultados
    
    Returns:
        Dicionário com informações da imagem ou None
    """
    # Extrair keywords do título
    keywords = extrair_keywords(titulo, categoria)
    
    # Montar query principal
    query_principal = " ".join(keywords[:3])
    
    print(f"  🔍 Buscando imagem para: '{query_principal}'")
    
    # Tentar busca principal
    imagem = buscar_imagem_unsplash(query_principal)
    
    if imagem:
        # Registrar download (obrigatório pelos termos)
        registrar_download(imagem["download_url"])
        print(f"  ✓ Imagem encontrada: {imagem['id']} (por {imagem['photographer']})")
        return imagem
    
    # Tentar queries de fallback
    fallbacks = fallback_queries or []
    
    # Adicionar fallbacks baseados na categoria
    if categoria:
        cat_lower = categoria.lower()
        if 'polít' in cat_lower or 'polit' in cat_lower:
            fallbacks.extend(['brazil government', 'congress building', 'politics'])
        elif 'econom' in cat_lower:
            fallbacks.extend(['finance business', 'stock market', 'economy'])
    
    for fallback in fallbacks:
        print(f"  🔍 Tentando fallback: '{fallback}'")
        imagem = buscar_imagem_unsplash(fallback)
        if imagem:
            registrar_download(imagem["download_url"])
            print(f"  ✓ Imagem encontrada (fallback): {imagem['id']}")
            return imagem
    
    print("  ⚠ Nenhuma imagem encontrada")
    return None


def baixar_imagem(url: str, destino: str) -> bool:
    """
    Baixa uma imagem para o sistema de arquivos local.
    
    Args:
        url: URL da imagem
        destino: Caminho de destino
    
    Returns:
        True se baixado com sucesso
    """
    try:
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            with open(destino, 'wb') as f:
                f.write(response.content)
            return True
    except Exception as e:
        print(f"  ⚠ Erro ao baixar imagem: {e}")
    return False


# Teste do módulo
if __name__ == "__main__":
    print("=" * 60)
    print("TESTE DO MÓDULO UNSPLASH")
    print("=" * 60)
    
    # Testar extração de keywords
    titulo_teste = "STF decide sobre aposentadoria integral em casos de doença grave"
    print(f"\nTítulo: {titulo_teste}")
    
    keywords = extrair_keywords(titulo_teste, "Política")
    print(f"Keywords extraídas: {keywords}")
    
    # Testar busca de imagem
    print("\nBuscando imagem...")
    imagem = obter_imagem_para_noticia(titulo_teste, "Política")
    
    if imagem:
        print(f"\n✅ Imagem encontrada!")
        print(f"   ID: {imagem['id']}")
        print(f"   URL: {imagem['url_regular']}")
        print(f"   Fotógrafo: {imagem['photographer']}")
        print(f"   Link Unsplash: {imagem['unsplash_url']}")
    else:
        print("\n❌ Nenhuma imagem encontrada")
