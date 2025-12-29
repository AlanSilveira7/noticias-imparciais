#!/usr/bin/env python3
"""
GERADOR DE REQUISIÇÕES DE BUSCA DE IMAGENS - NOTÍCIAS IMPARCIAIS
=================================================================
Este módulo analisa notícias sem cobertura adequada e gera requisições
de busca específicas para o contexto brasileiro.

Para cada notícia sem imagem adequada, gera:
- Tipo de busca (PESSOA, INSTITUIÇÃO, TEMA)
- Termos de busca em português
- Fontes recomendadas
- Diretório de destino no acervo

Versão: 1.0
Data: 29/12/2025
"""

import os
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

# Importar módulos do projeto
import sys
sys.path.insert(0, str(Path(__file__).parent))
from seletor_temas_v4 import identificar_tema, PESSOAS_COMO_TEMA, MAPA_TEMAS

# Diretórios
DATA_DIR = Path(__file__).parent / 'data'
REQUISICOES_DIR = DATA_DIR / 'requisicoes_imagens'
REQUISICOES_DIR.mkdir(parents=True, exist_ok=True)

# Mapeamento de temas para termos de busca específicos
TERMOS_BUSCA_BR = {
    # Pessoas públicas
    "lula": {
        "tipo": "PESSOA",
        "termos": ["Presidente Lula", "Luiz Inácio Lula da Silva", "Lula 2025"],
        "fontes": ["Wikimedia Commons", "Agência Brasil", "Planalto.gov.br"],
        "diretorio": "pessoas",
        "filtro_nome": "lula"
    },
    "bolsonaro": {
        "tipo": "PESSOA",
        "termos": ["Jair Bolsonaro", "Ex-presidente Bolsonaro", "Bolsonaro 2025"],
        "fontes": ["Wikimedia Commons", "Agência Brasil"],
        "diretorio": "pessoas",
        "filtro_nome": "bolsonaro"
    },
    "general_heleno": {
        "tipo": "PESSOA",
        "termos": ["General Augusto Heleno", "Augusto Heleno GSI"],
        "fontes": ["Wikimedia Commons", "Agência Brasil"],
        "diretorio": "pessoas",
        "filtro_nome": "general_heleno"
    },
    "ramagem": {
        "tipo": "PESSOA",
        "termos": ["Alexandre Ramagem", "Ramagem PF", "Ramagem ABIN"],
        "fontes": ["Wikimedia Commons", "Agência Brasil"],
        "diretorio": "pessoas",
        "filtro_nome": "ramagem"
    },
    "eduardo_bolsonaro": {
        "tipo": "PESSOA",
        "termos": ["Eduardo Bolsonaro", "Deputado Eduardo Bolsonaro"],
        "fontes": ["Wikimedia Commons", "Câmara dos Deputados"],
        "diretorio": "pessoas",
        "filtro_nome": "eduardo_bolsonaro"
    },
    
    # Instituições
    "judiciario": {
        "tipo": "INSTITUIÇÃO",
        "termos": ["STF plenário", "Supremo Tribunal Federal", "Ministros STF sessão"],
        "fontes": ["Wikimedia Commons", "STF.jus.br", "Agência Brasil"],
        "diretorio": "judiciario",
        "filtro_nome": "stf"
    },
    "legislativo": {
        "tipo": "INSTITUIÇÃO",
        "termos": ["Câmara dos Deputados plenário", "Senado Federal", "Congresso Nacional votação"],
        "fontes": ["Wikimedia Commons", "Câmara.leg.br", "Senado.leg.br", "Agência Brasil"],
        "diretorio": "legislativo",
        "filtro_nome": "camara"
    },
    "executivo": {
        "tipo": "INSTITUIÇÃO",
        "termos": ["Palácio do Planalto fachada", "Planalto Brasília arquitetura", "Esplanada dos Ministérios", "Praça dos Três Poderes"],
        "fontes": ["Wikimedia Commons", "Planalto.gov.br", "Agência Brasil"],
        "diretorio": "executivo",
        "filtro_nome": "planalto"
    },
    "economia": {
        "tipo": "TEMA",
        "termos": ["Banco Central do Brasil", "B3 Bovespa", "Real moeda brasileira"],
        "fontes": ["Wikimedia Commons", "BCB.gov.br", "Agência Brasil"],
        "diretorio": "economia",
        "filtro_nome": "banco_central"
    },
    "eleicoes": {
        "tipo": "TEMA",
        "termos": ["Urna eletrônica Brasil", "TSE eleições", "Votação eletrônica"],
        "fontes": ["Wikimedia Commons", "TSE.jus.br", "Agência Brasil"],
        "diretorio": "eleicoes",
        "filtro_nome": "urna"
    },
    "seguranca": {
        "tipo": "INSTITUIÇÃO",
        "termos": ["Polícia Federal operação", "PF Brasil", "Sede Polícia Federal"],
        "fontes": ["Wikimedia Commons", "PF.gov.br", "Agência Brasil"],
        "diretorio": "seguranca",
        "filtro_nome": "pf"
    },
    
    # Temas específicos
    "havaianas": {
        "tipo": "MARCA",
        "termos": ["Havaianas sandália", "Loja Havaianas", "Havaianas Brasil"],
        "fontes": ["Wikimedia Commons", "Flickr CC"],
        "diretorio": "marcas",
        "filtro_nome": "havaianas"
    },
    "rio_janeiro": {
        "tipo": "ESTADO",
        "termos": ["ALERJ Rio de Janeiro", "Assembleia Legislativa RJ", "Governo Rio de Janeiro"],
        "fontes": ["Wikimedia Commons", "ALERJ.rj.gov.br"],
        "diretorio": "estados",
        "filtro_nome": "alerj"
    },
    "rodoanel": {
        "tipo": "INFRAESTRUTURA",
        "termos": ["Rodoanel São Paulo", "Rodoanel Mário Covas", "Trecho Norte Rodoanel"],
        "fontes": ["Wikimedia Commons", "Governo SP"],
        "diretorio": "estados",
        "filtro_nome": "rodoanel"
    }
}


def log(msg: str, level: str = "INFO"):
    """Log formatado com timestamp."""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] [{level}] {msg}")


def gerar_requisicao_busca(titulo: str, tema_identificado: str = None) -> Dict:
    """
    Gera uma requisição de busca de imagem para uma notícia.
    
    Args:
        titulo: Título da notícia
        tema_identificado: Tema já identificado (opcional)
    
    Returns:
        Dict com informações da requisição de busca
    """
    # Identificar tema se não fornecido
    if not tema_identificado:
        tema_id, score, descricao, config = identificar_tema(titulo)
        tema_identificado = tema_id
    
    # Obter configuração de busca para o tema
    config_busca = TERMOS_BUSCA_BR.get(tema_identificado, {
        "tipo": "GENÉRICO",
        "termos": [tema_identificado, f"{tema_identificado} Brasil"],
        "fontes": ["Wikimedia Commons", "Agência Brasil"],
        "diretorio": "executivo",
        "filtro_nome": tema_identificado
    })
    
    requisicao = {
        "titulo_noticia": titulo,
        "tema_identificado": tema_identificado,
        "tipo_busca": config_busca["tipo"],
        "termos_busca": config_busca["termos"],
        "fontes_recomendadas": config_busca["fontes"],
        "diretorio_destino": config_busca["diretorio"],
        "filtro_nome_arquivo": config_busca["filtro_nome"],
        "status": "PENDENTE",
        "timestamp": datetime.now().isoformat()
    }
    
    return requisicao


def processar_noticias_sem_cobertura(noticias_sem_cobertura: List[Dict]) -> List[Dict]:
    """
    Processa lista de notícias sem cobertura e gera requisições de busca.
    
    Args:
        noticias_sem_cobertura: Lista de notícias que precisam de imagens
    
    Returns:
        Lista de requisições de busca geradas
    """
    requisicoes = []
    
    for noticia in noticias_sem_cobertura:
        titulo = noticia.get('titulo', noticia.get('title', ''))
        tema = noticia.get('tema_identificado', noticia.get('tema', None))
        
        if not titulo:
            continue
        
        requisicao = gerar_requisicao_busca(titulo, tema)
        requisicoes.append(requisicao)
        
        log(f"📋 Requisição gerada: {titulo[:50]}...")
        log(f"   Tipo: {requisicao['tipo_busca']} | Tema: {requisicao['tema_identificado']}")
        log(f"   Termos: {', '.join(requisicao['termos_busca'][:2])}")
    
    return requisicoes


def salvar_requisicoes(requisicoes: List[Dict], nome_arquivo: str = None) -> Path:
    """
    Salva requisições em arquivo JSON.
    
    Args:
        requisicoes: Lista de requisições
        nome_arquivo: Nome do arquivo (opcional)
    
    Returns:
        Caminho do arquivo salvo
    """
    if not nome_arquivo:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        nome_arquivo = f"requisicoes_{timestamp}.json"
    
    arquivo = REQUISICOES_DIR / nome_arquivo
    
    dados = {
        "data_geracao": datetime.now().isoformat(),
        "total_requisicoes": len(requisicoes),
        "requisicoes": requisicoes
    }
    
    with open(arquivo, 'w', encoding='utf-8') as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)
    
    return arquivo


def carregar_requisicoes_pendentes() -> List[Dict]:
    """
    Carrega todas as requisições pendentes.
    
    Returns:
        Lista de requisições com status PENDENTE
    """
    requisicoes_pendentes = []
    
    for arquivo in REQUISICOES_DIR.glob("requisicoes_*.json"):
        with open(arquivo, 'r', encoding='utf-8') as f:
            dados = json.load(f)
        
        for req in dados.get('requisicoes', []):
            if req.get('status') == 'PENDENTE':
                req['arquivo_origem'] = str(arquivo)
                requisicoes_pendentes.append(req)
    
    return requisicoes_pendentes


def gerar_relatorio_requisicoes(requisicoes: List[Dict]) -> str:
    """
    Gera relatório das requisições de busca.
    
    Args:
        requisicoes: Lista de requisições
    
    Returns:
        Relatório formatado
    """
    linhas = [
        "=" * 70,
        "RELATÓRIO DE REQUISIÇÕES DE BUSCA DE IMAGENS",
        f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}",
        "=" * 70,
        "",
        f"Total de requisições: {len(requisicoes)}",
        "",
    ]
    
    # Agrupar por tipo
    por_tipo = {}
    for req in requisicoes:
        tipo = req.get('tipo_busca', 'OUTROS')
        if tipo not in por_tipo:
            por_tipo[tipo] = []
        por_tipo[tipo].append(req)
    
    for tipo, reqs in sorted(por_tipo.items()):
        linhas.append(f"\n### {tipo} ({len(reqs)} requisições)")
        linhas.append("-" * 50)
        
        for req in reqs:
            linhas.append(f"\n📰 {req['titulo_noticia'][:60]}...")
            linhas.append(f"   Tema: {req['tema_identificado']}")
            linhas.append(f"   Termos: {', '.join(req['termos_busca'][:2])}")
            linhas.append(f"   Fontes: {', '.join(req['fontes_recomendadas'][:2])}")
            linhas.append(f"   Destino: acervo_temas/{req['diretorio_destino']}/")
    
    linhas.extend([
        "",
        "=" * 70,
    ])
    
    return "\n".join(linhas)


# Teste do módulo
if __name__ == '__main__':
    # Testar com alguns títulos de exemplo
    titulos_teste = [
        "Presidente Lula assina indulto de Natal excluindo condenados pelo 8 de janeiro",
        "Gustavo Feliciano assume Ministério do Turismo após saída de Sabino",
        "STF decide sobre aposentadoria integral em casos de doença grave",
        "General Heleno inicia cumprimento de prisão domiciliar",
    ]
    
    print("\n" + "=" * 70)
    print("🔍 GERADOR DE REQUISIÇÕES DE BUSCA")
    print("=" * 70)
    
    requisicoes = []
    for titulo in titulos_teste:
        req = gerar_requisicao_busca(titulo)
        requisicoes.append(req)
    
    # Mostrar relatório
    print(gerar_relatorio_requisicoes(requisicoes))
    
    # Salvar requisições
    arquivo = salvar_requisicoes(requisicoes)
    log(f"\n📝 Requisições salvas em: {arquivo}")
