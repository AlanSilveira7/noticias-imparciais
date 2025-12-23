"""
Módulo de Coleta de Notícias - Notícias Imparciais
===================================================

Este módulo é responsável por coletar notícias de múltiplas fontes
com diferentes vieses editoriais para posterior análise e síntese.

Fontes Configuradas:
- UOL (viés: esquerda)
- G1/Globo (viés: esquerda)
- Revista Oeste (viés: direita) [a implementar]
- Brasil Paralelo (viés: direita) [a implementar]

Autor: Manus AI
Data: 22/12/2025
Projeto: Notícias Imparciais
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict
from enum import Enum


class ViésEditorial(Enum):
    """Classificação do viés editorial da fonte."""
    ESQUERDA = "esquerda"
    CENTRO = "centro"
    DIREITA = "direita"
    INDEFINIDO = "indefinido"


class Secao(Enum):
    """Seções de notícias suportadas."""
    POLITICA = "politica"
    ECONOMIA = "economia"


@dataclass
class Noticia:
    """Estrutura de dados para uma notícia coletada."""
    id: str
    fonte: str
    fonte_id: str
    vies_editorial: str
    secao: str
    titulo: str
    url: str
    resumo: Optional[str]
    texto_completo: Optional[str]
    data_publicacao: str
    data_coleta: str
    
    def to_dict(self) -> Dict:
        """Converte para dicionário."""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Noticia':
        """Cria instância a partir de dicionário."""
        return cls(**data)


@dataclass
class FonteNoticia:
    """Configuração de uma fonte de notícias."""
    id: str
    nome: str
    vies: ViésEditorial
    urls: Dict[str, str]
    ativo: bool = True


class ColetorNoticias:
    """
    Classe principal para coleta de notícias de múltiplas fontes.
    
    Esta classe gerencia a coleta, armazenamento e recuperação de notícias
    de diferentes portais com vieses editoriais distintos.
    """
    
    # Configuração das fontes de notícias
    FONTES = {
        'uol': FonteNoticia(
            id='uol',
            nome='UOL',
            vies=ViésEditorial.ESQUERDA,
            urls={
                'politica': 'https://noticias.uol.com.br/politica/',
                'economia': 'https://economia.uol.com.br/'
            }
        ),
        'globo': FonteNoticia(
            id='globo',
            nome='G1/Globo',
            vies=ViésEditorial.ESQUERDA,
            urls={
                'politica': 'https://g1.globo.com/politica/',
                'economia': 'https://g1.globo.com/economia/'
            }
        ),
        'oeste': FonteNoticia(
            id='oeste',
            nome='Revista Oeste',
            vies=ViésEditorial.DIREITA,
            urls={
                'politica': 'https://revistaoeste.com/politica/',
                'economia': 'https://revistaoeste.com/economia/'
            },
            ativo=True
        ),
        'brasil_paralelo': FonteNoticia(
            id='brasil_paralelo',
            nome='Brasil Paralelo',
            vies=ViésEditorial.DIREITA,
            urls={
                'politica': 'https://www.brasilparalelo.com.br/noticias',
                'economia': 'https://www.brasilparalelo.com.br/noticias'
            },
            ativo=True
        )
    }
    
    def __init__(self, data_dir: str = '/home/ubuntu/noticias_imparciais/scraper/data'):
        """
        Inicializa o coletor de notícias.
        
        Args:
            data_dir: Diretório para armazenamento dos dados coletados
        """
        self.data_dir = data_dir
        self.banco_arquivo = os.path.join(data_dir, 'banco_noticias.json')
        os.makedirs(data_dir, exist_ok=True)
        self._carregar_banco()
    
    def _carregar_banco(self):
        """Carrega o banco de notícias do arquivo."""
        if os.path.exists(self.banco_arquivo):
            with open(self.banco_arquivo, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.noticias = [Noticia.from_dict(n) for n in data.get('noticias', [])]
                self.ultima_atualizacao = data.get('ultima_atualizacao')
        else:
            self.noticias = []
            self.ultima_atualizacao = None
    
    def _salvar_banco(self):
        """Salva o banco de notícias no arquivo."""
        data = {
            'noticias': [n.to_dict() for n in self.noticias],
            'ultima_atualizacao': datetime.now().isoformat(),
            'total': len(self.noticias)
        }
        with open(self.banco_arquivo, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def _gerar_id(self, url: str) -> str:
        """Gera ID único para a notícia."""
        return f"news_{hash(url) % 10**10}"
    
    def _extrair_data(self, texto: str) -> str:
        """Extrai e formata data de um texto."""
        import re
        
        # Padrão: 22/12/2025 19h04
        match = re.search(r'(\d{2}/\d{2}/\d{4})\s*(\d{2})h(\d{2})', texto)
        if match:
            try:
                data_str = match.group(1)
                hora = match.group(2)
                minuto = match.group(3)
                dt = datetime.strptime(f"{data_str} {hora}:{minuto}", "%d/%m/%Y %H:%M")
                return dt.isoformat()
            except ValueError:
                pass
        
        # Padrão ISO
        match = re.search(r'(\d{4}-\d{2}-\d{2})', texto)
        if match:
            return f"{match.group(1)}T00:00:00"
        
        return datetime.now().isoformat()
    
    def importar_json(self, arquivo: str, fonte_id: str, secao: str) -> int:
        """
        Importa notícias de um arquivo JSON para o banco.
        
        Args:
            arquivo: Caminho do arquivo JSON
            fonte_id: ID da fonte (uol, globo, etc.)
            secao: Seção das notícias (politica, economia)
            
        Returns:
            Número de notícias importadas
        """
        if not os.path.exists(arquivo):
            print(f"[ERRO] Arquivo não encontrado: {arquivo}")
            return 0
        
        fonte = self.FONTES.get(fonte_id)
        if not fonte:
            print(f"[ERRO] Fonte não configurada: {fonte_id}")
            return 0
        
        with open(arquivo, 'r', encoding='utf-8') as f:
            dados = json.load(f)
        
        urls_existentes = {n.url for n in self.noticias}
        importadas = 0
        
        for item in dados:
            url = item.get('url', '')
            if not url or url in urls_existentes:
                continue
            
            noticia = Noticia(
                id=self._gerar_id(url),
                fonte=fonte.nome,
                fonte_id=fonte_id,
                vies_editorial=fonte.vies.value,
                secao=secao,
                titulo=item.get('titulo', ''),
                url=url,
                resumo=item.get('resumo'),
                texto_completo=item.get('texto_completo'),
                data_publicacao=self._extrair_data(item.get('data', '')),
                data_coleta=datetime.now().isoformat()
            )
            
            self.noticias.append(noticia)
            urls_existentes.add(url)
            importadas += 1
        
        if importadas > 0:
            self._salvar_banco()
            print(f"[OK] {importadas} notícias importadas de {fonte.nome} ({secao})")
        
        return importadas
    
    def buscar_por_fonte(self, fonte_id: str) -> List[Noticia]:
        """Retorna notícias de uma fonte específica."""
        return [n for n in self.noticias if n.fonte_id == fonte_id]
    
    def buscar_por_vies(self, vies: str) -> List[Noticia]:
        """Retorna notícias de um viés específico."""
        return [n for n in self.noticias if n.vies_editorial == vies]
    
    def buscar_por_secao(self, secao: str) -> List[Noticia]:
        """Retorna notícias de uma seção específica."""
        return [n for n in self.noticias if n.secao == secao]
    
    def buscar_por_data(self, data: str) -> List[Noticia]:
        """Retorna notícias de uma data específica (formato: YYYY-MM-DD)."""
        return [n for n in self.noticias if n.data_publicacao.startswith(data)]
    
    def buscar_por_termo(self, termo: str) -> List[Noticia]:
        """Busca notícias que contenham o termo no título."""
        termo_lower = termo.lower()
        return [n for n in self.noticias if termo_lower in n.titulo.lower()]
    
    def agrupar_por_tema(self) -> Dict[str, List[Noticia]]:
        """
        Agrupa notícias por tema/assunto similar.
        
        Identifica notícias de diferentes fontes que tratam do mesmo assunto
        para posterior comparação e síntese.
        
        Returns:
            Dicionário com temas como chaves e listas de notícias como valores
        """
        # Palavras-chave para identificar temas
        temas = {}
        
        for noticia in self.noticias:
            titulo_lower = noticia.titulo.lower()
            
            # Identificar tema principal
            tema_encontrado = None
            
            # Lista de palavras-chave para agrupamento
            palavras_chave = [
                ('ramagem', 'Caso Ramagem'),
                ('heleno', 'Caso Augusto Heleno'),
                ('moraes', 'Ministro Alexandre de Moraes'),
                ('lula', 'Presidente Lula'),
                ('bolsonaro', 'Família Bolsonaro'),
                ('passaporte', 'Passaportes Diplomáticos'),
                ('8 de janeiro', '8 de Janeiro'),
                ('stf', 'STF'),
                ('congresso', 'Congresso Nacional'),
                ('economia', 'Economia'),
                ('dólar', 'Câmbio/Dólar'),
                ('inflação', 'Inflação'),
            ]
            
            for palavra, tema in palavras_chave:
                if palavra in titulo_lower:
                    tema_encontrado = tema
                    break
            
            if not tema_encontrado:
                tema_encontrado = 'Outros'
            
            if tema_encontrado not in temas:
                temas[tema_encontrado] = []
            
            temas[tema_encontrado].append(noticia)
        
        return temas
    
    def obter_estatisticas(self) -> Dict:
        """Retorna estatísticas do banco de notícias."""
        stats = {
            'total': len(self.noticias),
            'por_fonte': {},
            'por_vies': {},
            'por_secao': {},
            'ultima_atualizacao': self.ultima_atualizacao
        }
        
        for noticia in self.noticias:
            # Por fonte
            fonte = noticia.fonte
            stats['por_fonte'][fonte] = stats['por_fonte'].get(fonte, 0) + 1
            
            # Por viés
            vies = noticia.vies_editorial
            stats['por_vies'][vies] = stats['por_vies'].get(vies, 0) + 1
            
            # Por seção
            secao = noticia.secao
            stats['por_secao'][secao] = stats['por_secao'].get(secao, 0) + 1
        
        return stats
    
    def listar_todas(self) -> List[Noticia]:
        """Retorna todas as notícias."""
        return self.noticias
    
    def exportar_para_analise(self, arquivo: str = None) -> str:
        """
        Exporta notícias em formato otimizado para análise de IA.
        
        Args:
            arquivo: Caminho do arquivo de saída (opcional)
            
        Returns:
            Caminho do arquivo exportado
        """
        if not arquivo:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            arquivo = os.path.join(self.data_dir, f'noticias_para_analise_{timestamp}.json')
        
        # Agrupar por tema para facilitar comparação
        temas = self.agrupar_por_tema()
        
        export_data = {
            'data_exportacao': datetime.now().isoformat(),
            'total_noticias': len(self.noticias),
            'temas': {}
        }
        
        for tema, noticias in temas.items():
            export_data['temas'][tema] = {
                'total': len(noticias),
                'fontes_esquerda': [n.to_dict() for n in noticias if n.vies_editorial == 'esquerda'],
                'fontes_direita': [n.to_dict() for n in noticias if n.vies_editorial == 'direita'],
                'fontes_centro': [n.to_dict() for n in noticias if n.vies_editorial == 'centro']
            }
        
        with open(arquivo, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, ensure_ascii=False, indent=2)
        
        print(f"[OK] Dados exportados para análise: {arquivo}")
        return arquivo


def main():
    """Função principal para teste do módulo."""
    print("=" * 60)
    print("COLETOR DE NOTÍCIAS - NOTÍCIAS IMPARCIAIS")
    print("=" * 60)
    
    # Inicializar coletor
    coletor = ColetorNoticias()
    
    # Importar notícias coletadas
    print("\n[1] Importando notícias coletadas...")
    
    # Fontes de esquerda
    coletor.importar_json(
        '/home/ubuntu/noticias_imparciais/scraper/data/uol_politica.json',
        'uol',
        'politica'
    )
    
    coletor.importar_json(
        '/home/ubuntu/noticias_imparciais/scraper/data/globo_politica.json',
        'globo',
        'politica'
    )
    
    # Fontes de direita
    coletor.importar_json(
        '/home/ubuntu/noticias_imparciais/scraper/data/oeste_politica.json',
        'oeste',
        'politica'
    )
    
    coletor.importar_json(
        '/home/ubuntu/noticias_imparciais/scraper/data/brasil_paralelo_politica.json',
        'brasil_paralelo',
        'politica'
    )
    
    # Mostrar estatísticas
    print("\n[2] Estatísticas do banco:")
    stats = coletor.obter_estatisticas()
    print(f"    Total de notícias: {stats['total']}")
    print(f"    Por fonte: {stats['por_fonte']}")
    print(f"    Por viés: {stats['por_vies']}")
    
    # Agrupar por tema
    print("\n[3] Agrupamento por tema:")
    temas = coletor.agrupar_por_tema()
    for tema, noticias in temas.items():
        if len(noticias) > 1:
            print(f"    {tema}: {len(noticias)} notícias")
    
    # Exportar para análise
    print("\n[4] Exportando para análise de IA...")
    coletor.exportar_para_analise()
    
    print("\n" + "=" * 60)
    print("COLETA CONCLUÍDA!")
    print("=" * 60)


if __name__ == "__main__":
    main()
