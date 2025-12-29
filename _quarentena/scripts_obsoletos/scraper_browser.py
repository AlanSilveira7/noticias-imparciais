"""
Módulo de Coleta (Scraper) - Versão Browser
Projeto: Notícias Imparciais
Autor: Manus AI
Data: 22/12/2025

Este módulo coleta notícias usando navegador automatizado (Playwright/Selenium).
É mais robusto contra proteções anti-bot dos sites.
"""

import json
import re
from datetime import datetime
from typing import List, Dict, Optional
import subprocess
import os


class ScraperBrowser:
    """
    Scraper que utiliza navegador automatizado para coletar notícias.
    Projetado para ser executado via Manus com acesso ao browser.
    """
    
    # Configuração das fontes
    FONTES = {
        'uol': {
            'nome': 'UOL',
            'vies': 'esquerda',
            'urls': {
                'politica': 'https://noticias.uol.com.br/politica/',
                'economia': 'https://economia.uol.com.br/'
            }
        },
        'globo': {
            'nome': 'G1/Globo',
            'vies': 'esquerda',
            'urls': {
                'politica': 'https://g1.globo.com/politica/',
                'economia': 'https://g1.globo.com/economia/'
            }
        },
        'oeste': {
            'nome': 'Revista Oeste',
            'vies': 'direita',
            'urls': {
                'politica': 'https://revistaoeste.com/politica/',
                'economia': 'https://revistaoeste.com/economia/'
            }
        },
        'brasil_paralelo': {
            'nome': 'Brasil Paralelo',
            'vies': 'direita',
            'urls': {
                'politica': 'https://www.brasilparalelo.com.br/noticias',
                'economia': 'https://www.brasilparalelo.com.br/noticias'
            }
        }
    }
    
    def __init__(self, data_dir: str = '/home/ubuntu/noticias_imparciais/scraper/data'):
        """
        Inicializa o scraper.
        
        Args:
            data_dir: Diretório para salvar os dados coletados
        """
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)
    
    def _gerar_id(self, url: str) -> str:
        """Gera ID único para a notícia baseado na URL."""
        return f"news_{hash(url) % 10**10}"
    
    def _extrair_data(self, texto: str) -> str:
        """
        Extrai e formata data de um texto.
        
        Args:
            texto: Texto contendo informação de data/hora
            
        Returns:
            Data em formato ISO
        """
        # Padrões comuns de data
        padroes = [
            r'(\d{2}/\d{2}/\d{4})\s*(\d{2})h(\d{2})',  # 22/12/2025 19h04
            r'(\d{2}/\d{2}/\d{4})',  # 22/12/2025
            r'Há\s+(\d+)\s+(minuto|hora|dia)',  # Há X minutos/horas/dias
        ]
        
        for padrao in padroes:
            match = re.search(padrao, texto, re.IGNORECASE)
            if match:
                if 'Há' in padrao:
                    # Calcular data relativa
                    return datetime.now().isoformat()
                else:
                    try:
                        if len(match.groups()) == 3:
                            data_str = match.group(1)
                            hora = match.group(2)
                            minuto = match.group(3)
                            dt = datetime.strptime(f"{data_str} {hora}:{minuto}", "%d/%m/%Y %H:%M")
                        else:
                            dt = datetime.strptime(match.group(1), "%d/%m/%Y")
                        return dt.isoformat()
                    except ValueError:
                        pass
        
        return datetime.now().isoformat()
    
    def processar_dados_coletados(self, dados_brutos: List[Dict], fonte_id: str, secao: str) -> List[Dict]:
        """
        Processa dados brutos coletados do navegador.
        
        Args:
            dados_brutos: Lista de dicionários com {titulo, url, resumo, data}
            fonte_id: ID da fonte (uol, globo, etc.)
            secao: Seção (politica, economia)
            
        Returns:
            Lista de notícias formatadas
        """
        fonte_config = self.FONTES.get(fonte_id, {})
        noticias = []
        
        urls_vistas = set()
        
        for item in dados_brutos:
            url = item.get('url', '')
            titulo = item.get('titulo', '')
            
            # Validações básicas
            if not url or not titulo:
                continue
            
            # Evitar duplicatas
            if url in urls_vistas:
                continue
            urls_vistas.add(url)
            
            # Filtrar títulos muito curtos
            if len(titulo) < 15:
                continue
            
            noticia = {
                'id': self._gerar_id(url),
                'fonte': fonte_config.get('nome', fonte_id),
                'fonte_id': fonte_id,
                'vies_editorial': fonte_config.get('vies', 'indefinido'),
                'secao': secao,
                'titulo': titulo.strip(),
                'url': url,
                'resumo': item.get('resumo', '').strip() if item.get('resumo') else None,
                'texto_completo': item.get('texto_completo'),
                'data_publicacao': self._extrair_data(item.get('data', '')),
                'data_coleta': datetime.now().isoformat()
            }
            
            noticias.append(noticia)
        
        return noticias
    
    def salvar_noticias(self, noticias: List[Dict], nome_arquivo: str = None) -> str:
        """
        Salva notícias em arquivo JSON.
        
        Args:
            noticias: Lista de notícias
            nome_arquivo: Nome do arquivo (opcional)
            
        Returns:
            Caminho do arquivo salvo
        """
        if not nome_arquivo:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            nome_arquivo = f"noticias_{timestamp}.json"
        
        caminho = os.path.join(self.data_dir, nome_arquivo)
        
        with open(caminho, 'w', encoding='utf-8') as f:
            json.dump(noticias, f, ensure_ascii=False, indent=2)
        
        print(f"[OK] {len(noticias)} notícias salvas em {caminho}")
        return caminho
    
    def carregar_noticias(self, nome_arquivo: str) -> List[Dict]:
        """
        Carrega notícias de arquivo JSON.
        
        Args:
            nome_arquivo: Nome do arquivo
            
        Returns:
            Lista de notícias
        """
        caminho = os.path.join(self.data_dir, nome_arquivo)
        
        if not os.path.exists(caminho):
            return []
        
        with open(caminho, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def gerar_instrucoes_coleta(self, fonte_id: str, secao: str) -> str:
        """
        Gera instruções para coleta manual via Manus browser.
        
        Args:
            fonte_id: ID da fonte
            secao: Seção a coletar
            
        Returns:
            Instruções em texto
        """
        fonte_config = self.FONTES.get(fonte_id, {})
        url = fonte_config.get('urls', {}).get(secao, '')
        
        instrucoes = f"""
=== INSTRUÇÕES DE COLETA: {fonte_config.get('nome', fonte_id)} - {secao.upper()} ===

URL: {url}

Para cada notícia visível na página, extrair:
1. TÍTULO: Texto principal da manchete
2. URL: Link completo da notícia
3. RESUMO: Subtítulo ou descrição (se disponível)
4. DATA: Data/hora de publicação (se visível)

Formato de saída esperado (JSON):
[
  {{
    "titulo": "Título da notícia",
    "url": "https://...",
    "resumo": "Resumo ou subtítulo",
    "data": "22/12/2025 19h04"
  }},
  ...
]

Limite: 10-15 notícias mais recentes
"""
        return instrucoes


# Estrutura de dados para armazenar notícias coletadas
class BancoDados:
    """Gerenciador simples de banco de dados JSON para notícias."""
    
    def __init__(self, arquivo: str = '/home/ubuntu/noticias_imparciais/scraper/data/banco_noticias.json'):
        self.arquivo = arquivo
        self.noticias = self._carregar()
    
    def _carregar(self) -> Dict:
        """Carrega banco de dados do arquivo."""
        if os.path.exists(self.arquivo):
            with open(self.arquivo, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {'noticias': [], 'ultima_atualizacao': None}
    
    def _salvar(self):
        """Salva banco de dados no arquivo."""
        self.noticias['ultima_atualizacao'] = datetime.now().isoformat()
        with open(self.arquivo, 'w', encoding='utf-8') as f:
            json.dump(self.noticias, f, ensure_ascii=False, indent=2)
    
    def adicionar(self, novas_noticias: List[Dict]):
        """
        Adiciona novas notícias ao banco, evitando duplicatas.
        
        Args:
            novas_noticias: Lista de notícias a adicionar
        """
        urls_existentes = {n['url'] for n in self.noticias.get('noticias', [])}
        
        adicionadas = 0
        for noticia in novas_noticias:
            if noticia['url'] not in urls_existentes:
                self.noticias['noticias'].append(noticia)
                urls_existentes.add(noticia['url'])
                adicionadas += 1
        
        if adicionadas > 0:
            self._salvar()
            print(f"[OK] {adicionadas} novas notícias adicionadas ao banco.")
        else:
            print("[INFO] Nenhuma notícia nova para adicionar.")
    
    def buscar_por_fonte(self, fonte_id: str) -> List[Dict]:
        """Busca notícias de uma fonte específica."""
        return [n for n in self.noticias.get('noticias', []) if n.get('fonte_id') == fonte_id]
    
    def buscar_por_secao(self, secao: str) -> List[Dict]:
        """Busca notícias de uma seção específica."""
        return [n for n in self.noticias.get('noticias', []) if n.get('secao') == secao]
    
    def buscar_por_data(self, data_inicio: str, data_fim: str = None) -> List[Dict]:
        """Busca notícias em um intervalo de datas."""
        if data_fim is None:
            data_fim = datetime.now().isoformat()
        
        return [
            n for n in self.noticias.get('noticias', [])
            if data_inicio <= n.get('data_publicacao', '') <= data_fim
        ]
    
    def listar_todas(self) -> List[Dict]:
        """Retorna todas as notícias."""
        return self.noticias.get('noticias', [])
    
    def total(self) -> int:
        """Retorna total de notícias no banco."""
        return len(self.noticias.get('noticias', []))


if __name__ == "__main__":
    # Exemplo de uso
    scraper = ScraperBrowser()
    
    # Mostrar instruções de coleta
    print(scraper.gerar_instrucoes_coleta('uol', 'politica'))
    print(scraper.gerar_instrucoes_coleta('globo', 'politica'))
