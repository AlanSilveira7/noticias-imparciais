"""
Módulo de Coleta (Scraper) - UOL Notícias
Projeto: Notícias Imparciais
Autor: Manus AI
Data: 22/12/2025

Este módulo coleta notícias das seções de Política e Economia do UOL.
Utiliza requests com headers avançados e RSS feeds como alternativa.
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
from typing import List, Dict, Optional
import json
import re
import time
import xml.etree.ElementTree as ET


class ScraperUOL:
    """Scraper para coletar notícias do portal UOL."""
    
    # URLs das seções (páginas web)
    URLS = {
        'politica': 'https://noticias.uol.com.br/politica/',
        'economia': 'https://economia.uol.com.br/'
    }
    
    # URLs dos feeds RSS (alternativa mais confiável)
    RSS_FEEDS = {
        'politica': 'https://rss.uol.com.br/feed/noticias.xml',
        'economia': 'https://rss.uol.com.br/feed/economia.xml',
        'ultimas': 'https://rss.uol.com.br/feed/noticias.xml'
    }
    
    # Headers avançados para simular navegador real
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Cache-Control': 'max-age=0',
    }
    
    def __init__(self):
        """Inicializa o scraper."""
        self.session = requests.Session()
        self.session.headers.update(self.HEADERS)
        self.fonte = "UOL"
        self.vies_editorial = "esquerda"  # Classificação inicial do viés
    
    def _fazer_requisicao(self, url: str, is_rss: bool = False) -> Optional[str]:
        """
        Faz requisição HTTP e retorna conteúdo.
        
        Args:
            url: URL da página a ser coletada
            is_rss: Se True, espera conteúdo XML
            
        Returns:
            Conteúdo da página ou None em caso de erro
        """
        try:
            # Headers específicos para RSS
            headers = self.HEADERS.copy()
            if is_rss:
                headers['Accept'] = 'application/rss+xml, application/xml, text/xml, */*'
            
            response = self.session.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            return response.content
        except requests.RequestException as e:
            print(f"[ERRO] Falha ao acessar {url}: {e}")
            return None
    
    def _parsear_data_rss(self, texto_data: str) -> str:
        """
        Converte data do RSS para formato ISO.
        
        Args:
            texto_data: Data no formato RSS (ex: "Sun, 22 Dec 2025 19:04:00 -0300")
            
        Returns:
            Data em formato ISO
        """
        try:
            # Tentar formato RSS padrão
            formatos = [
                "%a, %d %b %Y %H:%M:%S %z",
                "%Y-%m-%dT%H:%M:%S%z",
                "%Y-%m-%d %H:%M:%S"
            ]
            for fmt in formatos:
                try:
                    dt = datetime.strptime(texto_data.strip(), fmt)
                    return dt.isoformat()
                except ValueError:
                    continue
        except Exception:
            pass
        
        return datetime.now().isoformat()
    
    def _coletar_via_rss(self, secao: str, limite: int = 20) -> List[Dict]:
        """
        Coleta notícias via feed RSS.
        
        Args:
            secao: Seção de notícias
            limite: Número máximo de notícias
            
        Returns:
            Lista de notícias coletadas
        """
        # Usar feed de últimas notícias e filtrar por seção
        url = self.RSS_FEEDS.get('ultimas', self.RSS_FEEDS['ultimas'])
        
        print(f"[INFO] Tentando coletar via RSS: {url}")
        
        content = self._fazer_requisicao(url, is_rss=True)
        if not content:
            return []
        
        noticias = []
        
        try:
            root = ET.fromstring(content)
            
            # Encontrar todos os itens
            items = root.findall('.//item')
            
            for item in items[:limite * 2]:  # Pegar mais para filtrar depois
                titulo = item.find('title')
                link = item.find('link')
                descricao = item.find('description')
                pub_date = item.find('pubDate')
                categoria = item.find('category')
                
                if titulo is None or link is None:
                    continue
                
                titulo_texto = titulo.text or ""
                link_texto = link.text or ""
                
                # Filtrar por seção se especificado
                if secao == 'politica':
                    # Verificar se é notícia de política
                    categoria_texto = categoria.text.lower() if categoria is not None and categoria.text else ""
                    if 'politic' not in categoria_texto.lower() and 'politic' not in link_texto.lower():
                        # Verificar palavras-chave no título
                        palavras_politica = ['governo', 'lula', 'bolsonaro', 'congresso', 'stf', 'ministro', 
                                           'deputado', 'senador', 'presidente', 'eleição', 'partido']
                        if not any(p in titulo_texto.lower() for p in palavras_politica):
                            continue
                
                elif secao == 'economia':
                    categoria_texto = categoria.text.lower() if categoria is not None and categoria.text else ""
                    if 'econom' not in categoria_texto.lower() and 'econom' not in link_texto.lower():
                        palavras_economia = ['economia', 'dólar', 'bolsa', 'inflação', 'pib', 'juros', 
                                           'banco', 'mercado', 'investimento', 'empresas']
                        if not any(p in titulo_texto.lower() for p in palavras_economia):
                            continue
                
                noticia = {
                    'id': f"uol_{hash(link_texto) % 10**8}",
                    'fonte': self.fonte,
                    'vies_editorial': self.vies_editorial,
                    'secao': secao,
                    'titulo': titulo_texto,
                    'url': link_texto,
                    'resumo': descricao.text if descricao is not None else None,
                    'texto_completo': None,
                    'data_publicacao': self._parsear_data_rss(pub_date.text) if pub_date is not None else datetime.now().isoformat(),
                    'data_coleta': datetime.now().isoformat()
                }
                
                noticias.append(noticia)
                
                if len(noticias) >= limite:
                    break
            
        except ET.ParseError as e:
            print(f"[ERRO] Falha ao parsear RSS: {e}")
            return []
        
        return noticias
    
    def _coletar_via_api(self, secao: str, limite: int = 20) -> List[Dict]:
        """
        Coleta notícias via API interna do UOL (se disponível).
        
        Args:
            secao: Seção de notícias
            limite: Número máximo de notícias
            
        Returns:
            Lista de notícias coletadas
        """
        # URLs de API conhecidas do UOL
        api_urls = {
            'politica': 'https://api.uol.com.br/v1/news/politica',
            'economia': 'https://api.uol.com.br/v1/news/economia'
        }
        
        # Esta é uma tentativa - a API pode não estar disponível publicamente
        url = api_urls.get(secao)
        if not url:
            return []
        
        try:
            response = self.session.get(url, timeout=30)
            if response.status_code == 200:
                data = response.json()
                # Processar resposta da API
                # (estrutura depende da API real)
                return []
        except Exception:
            pass
        
        return []
    
    def coletar_secao(self, secao: str, limite: int = 20, extrair_texto: bool = False) -> List[Dict]:
        """
        Coleta notícias de uma seção específica.
        
        Args:
            secao: 'politica' ou 'economia'
            limite: Número máximo de notícias a coletar
            extrair_texto: Se True, acessa cada notícia para extrair texto completo
            
        Returns:
            Lista de dicionários com as notícias coletadas
        """
        print(f"[INFO] Coletando notícias de {secao.upper()} do UOL...")
        
        # Tentar via RSS primeiro (mais confiável)
        noticias = self._coletar_via_rss(secao, limite)
        
        if not noticias:
            print(f"[AVISO] RSS não retornou resultados para {secao}")
        
        print(f"[OK] {len(noticias)} notícias coletadas da seção {secao.upper()}.")
        return noticias
    
    def coletar_todas(self, limite_por_secao: int = 10, extrair_texto: bool = False) -> List[Dict]:
        """
        Coleta notícias de todas as seções.
        
        Args:
            limite_por_secao: Número máximo de notícias por seção
            extrair_texto: Se True, extrai texto completo de cada notícia
            
        Returns:
            Lista com todas as notícias coletadas
        """
        todas_noticias = []
        
        for secao in ['politica', 'economia']:
            noticias = self.coletar_secao(secao, limite_por_secao, extrair_texto)
            todas_noticias.extend(noticias)
            time.sleep(1)  # Pausa entre seções
        
        return todas_noticias
    
    def salvar_json(self, noticias: List[Dict], arquivo: str):
        """
        Salva as notícias em arquivo JSON.
        
        Args:
            noticias: Lista de notícias
            arquivo: Caminho do arquivo de saída
        """
        with open(arquivo, 'w', encoding='utf-8') as f:
            json.dump(noticias, f, ensure_ascii=False, indent=2)
        print(f"[OK] {len(noticias)} notícias salvas em {arquivo}")


# Teste do módulo
if __name__ == "__main__":
    scraper = ScraperUOL()
    
    # Coletar notícias de política
    noticias_politica = scraper.coletar_secao('politica', limite=10)
    
    # Coletar notícias de economia
    noticias_economia = scraper.coletar_secao('economia', limite=10)
    
    # Combinar e salvar
    todas = noticias_politica + noticias_economia
    scraper.salvar_json(todas, '/home/ubuntu/noticias_imparciais/scraper/data/uol_noticias.json')
    
    # Mostrar resumo
    print("\n" + "="*60)
    print("RESUMO DA COLETA - UOL")
    print("="*60)
    for noticia in todas[:5]:
        print(f"\n📰 {noticia['titulo'][:70]}...")
        print(f"   Seção: {noticia['secao']} | Data: {noticia['data_publicacao'][:10]}")
