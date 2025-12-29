#!/usr/bin/env python3
"""
EXPANSOR DE ACERVO INTEGRADO - NOTÍCIAS IMPARCIAIS
===================================================
Este script integra todo o fluxo de expansão do acervo:
1. Verifica cobertura de imagens para notícias
2. Gera requisições de busca para notícias sem cobertura
3. Busca imagens em fontes brasileiras (Wikimedia Commons)
4. Adiciona ao acervo local
5. Gera relatório completo

Pode ser executado:
- Standalone: python3 expansor_acervo_integrado.py
- Integrado ao ciclo de publicação

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

from seletor_temas_v4 import selecionar_imagem, identificar_tema
from gerador_requisicoes import gerar_requisicao_busca, salvar_requisicoes, gerar_relatorio_requisicoes
from buscador_imagens_br import processar_requisicoes, gerar_relatorio_busca, salvar_log_busca

# Diretórios
DATA_DIR = Path(__file__).parent / 'data'
ACERVO_DIR = Path(__file__).parent.parent / 'acervo_temas'
LOG_DIR = DATA_DIR / 'logs_expansao'
LOG_DIR.mkdir(parents=True, exist_ok=True)

# Imagens de fallback conhecidas (imagens muito genéricas)
FALLBACK_IMAGES = [
    'planalto_fachada_01.jpg',
    'congresso_panorama_01.jpg'
]


def log(msg: str, level: str = "INFO"):
    """Log formatado com timestamp."""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] [{level}] {msg}")


def verificar_cobertura_noticia(titulo: str) -> Dict:
    """
    Verifica se uma notícia tem cobertura de imagem adequada.
    
    Args:
        titulo: Título da notícia
    
    Returns:
        Dict com resultado da verificação
    """
    # Identificar tema
    tema_id, score, descricao, config = identificar_tema(titulo)
    
    # Selecionar imagem
    resultado = selecionar_imagem(titulo)
    imagem_path = resultado.get('imagem')
    
    # Verificar se é fallback
    is_fallback = False
    if imagem_path:
        nome_imagem = os.path.basename(imagem_path)
        is_fallback = nome_imagem in FALLBACK_IMAGES
    else:
        is_fallback = True
    
    # Verificar se é imagem genérica para o tema
    is_generic = False
    if tema_id in ['lula', 'bolsonaro', 'general_heleno', 'ramagem', 'eduardo_bolsonaro']:
        # Para pessoas, verificar se a imagem contém o nome
        if imagem_path:
            nome_imagem = os.path.basename(imagem_path).lower()
            nome_tema = tema_id.replace('_', '')
            is_generic = nome_tema not in nome_imagem.replace('_', '')
    
    return {
        'titulo': titulo,
        'tema': tema_id,
        'tema_score': score,
        'imagem': imagem_path,
        'imagem_nome': os.path.basename(imagem_path) if imagem_path else None,
        'is_fallback': is_fallback,
        'is_generic': is_generic,
        'cobertura_adequada': not is_fallback and not is_generic
    }


def verificar_lote_noticias(noticias: List[Dict]) -> Dict:
    """
    Verifica cobertura para um lote de notícias.
    
    Args:
        noticias: Lista de notícias
    
    Returns:
        Dict com resultados
    """
    resultados = {
        'total': len(noticias),
        'com_cobertura': 0,
        'sem_cobertura': 0,
        'detalhes': []
    }
    
    for noticia in noticias:
        titulo = noticia.get('titulo', noticia.get('title', ''))
        if not titulo:
            continue
        
        verificacao = verificar_cobertura_noticia(titulo)
        resultados['detalhes'].append(verificacao)
        
        if verificacao['cobertura_adequada']:
            resultados['com_cobertura'] += 1
        else:
            resultados['sem_cobertura'] += 1
    
    return resultados


def expandir_acervo_para_noticias(noticias: List[Dict], auto_buscar: bool = True) -> Dict:
    """
    Fluxo completo de expansão do acervo para um lote de notícias.
    
    Args:
        noticias: Lista de notícias
        auto_buscar: Se True, busca imagens automaticamente
    
    Returns:
        Dict com resultado completo
    """
    print("\n" + "=" * 70)
    print("🖼️ EXPANSOR DE ACERVO INTEGRADO")
    print(f"📅 Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    print("=" * 70)
    
    resultado = {
        'data': datetime.now().isoformat(),
        'verificacao': None,
        'requisicoes': [],
        'busca': None,
        'imagens_adicionadas': []
    }
    
    # ETAPA 1: Verificar cobertura
    log("\n📋 ETAPA 1: Verificando cobertura de imagens...")
    verificacao = verificar_lote_noticias(noticias)
    resultado['verificacao'] = verificacao
    
    log(f"   Total de notícias: {verificacao['total']}")
    log(f"   ✅ Com cobertura: {verificacao['com_cobertura']}")
    log(f"   ⚠️ Sem cobertura: {verificacao['sem_cobertura']}")
    
    # Mostrar detalhes
    for det in verificacao['detalhes']:
        status = "✅" if det['cobertura_adequada'] else "⚠️"
        log(f"   {status} {det['titulo'][:50]}...")
        log(f"      Tema: {det['tema']} | Imagem: {det['imagem_nome'] or 'N/A'}")
    
    # Se todas têm cobertura, encerrar
    if verificacao['sem_cobertura'] == 0:
        log("\n✅ Todas as notícias têm cobertura adequada!")
        return resultado
    
    # ETAPA 2: Gerar requisições de busca
    log("\n📋 ETAPA 2: Gerando requisições de busca...")
    
    noticias_sem_cobertura = [
        d for d in verificacao['detalhes']
        if not d['cobertura_adequada']
    ]
    
    requisicoes = []
    for noticia in noticias_sem_cobertura:
        req = gerar_requisicao_busca(noticia['titulo'], noticia['tema'])
        requisicoes.append(req)
        log(f"   📋 {req['tipo_busca']}: {noticia['titulo'][:40]}...")
    
    resultado['requisicoes'] = requisicoes
    
    # Salvar requisições
    arquivo_req = salvar_requisicoes(requisicoes)
    log(f"   📝 Requisições salvas em: {arquivo_req}")
    
    # ETAPA 3: Buscar imagens (se auto_buscar)
    if auto_buscar and requisicoes:
        log("\n📋 ETAPA 3: Buscando imagens no Wikimedia Commons...")
        
        resultado_busca = processar_requisicoes(requisicoes)
        resultado['busca'] = resultado_busca
        resultado['imagens_adicionadas'] = resultado_busca.get('imagens_adicionadas', [])
        
        # Mostrar relatório de busca
        print(gerar_relatorio_busca(resultado_busca))
        
        # Salvar log de busca
        log_busca = salvar_log_busca(resultado_busca)
        log(f"📝 Log de busca salvo em: {log_busca}")
    
    # Salvar resultado completo
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_file = LOG_DIR / f"expansao_{timestamp}.json"
    with open(log_file, 'w', encoding='utf-8') as f:
        json.dump(resultado, f, ensure_ascii=False, indent=2, default=str)
    log(f"📝 Log completo salvo em: {log_file}")
    
    return resultado


def carregar_noticias_do_arquivo() -> List[Dict]:
    """Carrega notícias do arquivo de dados."""
    arquivo = DATA_DIR / 'noticias_imparciais.json'
    
    if not arquivo.exists():
        log(f"Arquivo não encontrado: {arquivo}", "WARN")
        return []
    
    with open(arquivo, 'r', encoding='utf-8') as f:
        dados = json.load(f)
    
    return dados.get('noticias', [])


def gerar_relatorio_final(resultado: Dict) -> str:
    """
    Gera relatório final da expansão.
    
    Args:
        resultado: Resultado da expansão
    
    Returns:
        Relatório formatado
    """
    linhas = [
        "",
        "=" * 70,
        "📊 RELATÓRIO FINAL DE EXPANSÃO DO ACERVO",
        "=" * 70,
        f"📅 Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}",
        "",
    ]
    
    # Verificação
    verificacao = resultado.get('verificacao', {})
    linhas.extend([
        "VERIFICAÇÃO DE COBERTURA:",
        f"  Total de notícias: {verificacao.get('total', 0)}",
        f"  ✅ Com cobertura adequada: {verificacao.get('com_cobertura', 0)}",
        f"  ⚠️ Sem cobertura adequada: {verificacao.get('sem_cobertura', 0)}",
        "",
    ])
    
    # Requisições
    requisicoes = resultado.get('requisicoes', [])
    if requisicoes:
        linhas.extend([
            "REQUISIÇÕES DE BUSCA GERADAS:",
            f"  Total: {len(requisicoes)}",
        ])
        for req in requisicoes:
            linhas.append(f"  • {req.get('tipo_busca', 'N/A')}: {req.get('titulo_noticia', '')[:40]}...")
        linhas.append("")
    
    # Imagens adicionadas
    imagens = resultado.get('imagens_adicionadas', [])
    if imagens:
        linhas.extend([
            "IMAGENS ADICIONADAS AO ACERVO:",
            f"  Total: {len(imagens)}",
        ])
        for img in imagens:
            linhas.append(f"  📷 {img.get('arquivo', 'N/A')}")
            linhas.append(f"     Fonte: {img.get('fonte', 'N/A')}")
            linhas.append(f"     Licença: {img.get('licenca', 'N/A')}")
        linhas.append("")
    else:
        linhas.extend([
            "IMAGENS ADICIONADAS AO ACERVO:",
            "  Nenhuma imagem foi adicionada.",
            "",
        ])
    
    linhas.append("=" * 70)
    
    return "\n".join(linhas)


# Função principal para integração com publicar_supabase.py
def verificar_e_expandir_antes_publicacao(noticias: List[Dict]) -> Dict:
    """
    Função para ser chamada antes da publicação.
    Verifica cobertura e expande o acervo se necessário.
    
    Args:
        noticias: Lista de notícias a serem publicadas
    
    Returns:
        Dict com resultado da expansão
    """
    return expandir_acervo_para_noticias(noticias, auto_buscar=True)


# Execução standalone
if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Expansor de Acervo Integrado')
    parser.add_argument('--auto', action='store_true', help='Buscar imagens automaticamente')
    parser.add_argument('--arquivo', type=str, help='Arquivo JSON com notícias')
    args = parser.parse_args()
    
    # Carregar notícias
    if args.arquivo:
        with open(args.arquivo, 'r', encoding='utf-8') as f:
            dados = json.load(f)
        noticias = dados.get('noticias', dados) if isinstance(dados, dict) else dados
    else:
        noticias = carregar_noticias_do_arquivo()
    
    if not noticias:
        log("Nenhuma notícia encontrada!", "ERROR")
        exit(1)
    
    # Executar expansão
    resultado = expandir_acervo_para_noticias(noticias, auto_buscar=args.auto)
    
    # Mostrar relatório final
    print(gerar_relatorio_final(resultado))
