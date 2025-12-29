#!/usr/bin/env python3
"""
VERIFICADOR DE COBERTURA DE IMAGENS - NOTÍCIAS IMPARCIAIS
==========================================================
Este script verifica se as notícias têm imagens adequadas antes da publicação
e registra quando o sistema usa fallback.

Integra-se ao fluxo de publicação para:
1. Verificar cobertura antes de publicar
2. Logar notícias sem match adequado
3. Acionar expansão automática do acervo quando necessário

Versão: 1.0
Data: 29/12/2025
"""

import os
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Tuple
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv(Path(__file__).parent.parent / '.env')

# Importar módulos do projeto
import sys
sys.path.insert(0, str(Path(__file__).parent))
from seletor_temas_v4 import selecionar_imagem, identificar_tema

# Diretórios
ACERVO_BASE = Path(__file__).parent.parent / 'acervo_temas'
DATA_DIR = Path(__file__).parent / 'data'
LOG_DIR = DATA_DIR / 'logs_cobertura'

# Criar diretório de logs se não existir
LOG_DIR.mkdir(parents=True, exist_ok=True)

# Imagens de fallback conhecidas (imagens muito genéricas que não representam bem o tema)
# Nota: planalto_03.jpg e planalto_04.jpg são imagens da Esplanada, mais contextuais
FALLBACK_IMAGES = [
    'planalto_fachada_01.jpg',  # Muito genérica
    'congresso_panorama_01.jpg'  # Muito genérica
]


def log(msg: str, level: str = "INFO"):
    """Log formatado com timestamp."""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] [{level}] {msg}")


def verificar_imagem_para_noticia(titulo: str) -> Dict:
    """
    Verifica se há imagem adequada para uma notícia.
    
    Args:
        titulo: Título da notícia
    
    Returns:
        Dict com resultado da verificação
    """
    # Identificar tema
    tema_id, score, descricao, config = identificar_tema(titulo)
    
    # Selecionar imagem
    resultado_selecao = selecionar_imagem(titulo)
    
    imagem_path = resultado_selecao.get('imagem')
    
    # Verificar se é fallback
    is_fallback = False
    is_generic = False
    
    if imagem_path:
        nome_imagem = os.path.basename(imagem_path)
        is_fallback = nome_imagem in FALLBACK_IMAGES
        
        # Verificar se é imagem genérica (não específica do tema)
        if tema_id in ['lula', 'bolsonaro', 'general_heleno', 'ramagem']:
            # Para pessoas, verificar se a imagem contém o nome
            is_generic = tema_id.replace('_', '') not in nome_imagem.lower().replace('_', '')
    else:
        is_fallback = True
    
    return {
        'titulo': titulo,
        'tema_identificado': tema_id,
        'tema_score': score,
        'tema_descricao': descricao,
        'imagem_selecionada': imagem_path,
        'imagem_nome': os.path.basename(imagem_path) if imagem_path else None,
        'is_fallback': is_fallback,
        'is_generic': is_generic,
        'cobertura_adequada': not is_fallback and not is_generic,
        'timestamp': datetime.now().isoformat()
    }


def verificar_lote_noticias(noticias: List[Dict]) -> Dict:
    """
    Verifica cobertura de imagens para um lote de notícias.
    
    Args:
        noticias: Lista de notícias (com campo 'titulo')
    
    Returns:
        Dict com resultados da verificação
    """
    resultados = {
        'data_verificacao': datetime.now().isoformat(),
        'total_noticias': len(noticias),
        'com_cobertura': 0,
        'sem_cobertura': 0,
        'usando_fallback': 0,
        'usando_generico': 0,
        'detalhes': []
    }
    
    for noticia in noticias:
        titulo = noticia.get('titulo', noticia.get('title', ''))
        if not titulo:
            continue
        
        verificacao = verificar_imagem_para_noticia(titulo)
        resultados['detalhes'].append(verificacao)
        
        if verificacao['cobertura_adequada']:
            resultados['com_cobertura'] += 1
        else:
            resultados['sem_cobertura'] += 1
            
            if verificacao['is_fallback']:
                resultados['usando_fallback'] += 1
            if verificacao['is_generic']:
                resultados['usando_generico'] += 1
    
    return resultados


def gerar_relatorio_cobertura(resultados: Dict) -> str:
    """
    Gera relatório de cobertura em formato texto.
    
    Args:
        resultados: Resultados da verificação
    
    Returns:
        Relatório formatado
    """
    linhas = [
        "=" * 70,
        "RELATÓRIO DE COBERTURA DE IMAGENS",
        f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}",
        "=" * 70,
        "",
        f"Total de notícias verificadas: {resultados['total_noticias']}",
        f"✅ Com cobertura adequada: {resultados['com_cobertura']}",
        f"⚠️ Sem cobertura adequada: {resultados['sem_cobertura']}",
        f"   → Usando fallback: {resultados['usando_fallback']}",
        f"   → Usando imagem genérica: {resultados['usando_generico']}",
        "",
        "-" * 70,
        "DETALHES POR NOTÍCIA:",
        "-" * 70,
    ]
    
    for detalhe in resultados['detalhes']:
        status = "✅" if detalhe['cobertura_adequada'] else "⚠️"
        linhas.append(f"\n{status} {detalhe['titulo'][:60]}...")
        linhas.append(f"   Tema: {detalhe['tema_identificado']} (score: {detalhe['tema_score']})")
        linhas.append(f"   Imagem: {detalhe['imagem_nome'] or 'N/A'}")
        
        if not detalhe['cobertura_adequada']:
            if detalhe['is_fallback']:
                linhas.append("   ⚠️ USANDO FALLBACK")
            if detalhe['is_generic']:
                linhas.append("   ⚠️ IMAGEM GENÉRICA (não específica do tema)")
    
    linhas.extend([
        "",
        "=" * 70,
    ])
    
    return "\n".join(linhas)


def salvar_log_cobertura(resultados: Dict) -> Path:
    """
    Salva log de cobertura em arquivo JSON.
    
    Args:
        resultados: Resultados da verificação
    
    Returns:
        Caminho do arquivo salvo
    """
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_file = LOG_DIR / f"cobertura_{timestamp}.json"
    
    with open(log_file, 'w', encoding='utf-8') as f:
        json.dump(resultados, f, ensure_ascii=False, indent=2)
    
    return log_file


def obter_noticias_sem_cobertura(resultados: Dict) -> List[Dict]:
    """
    Retorna lista de notícias sem cobertura adequada.
    
    Args:
        resultados: Resultados da verificação
    
    Returns:
        Lista de notícias que precisam de expansão do acervo
    """
    return [
        d for d in resultados['detalhes']
        if not d['cobertura_adequada']
    ]


def expandir_acervo_se_necessario(resultados: Dict) -> Dict:
    """
    Expande o acervo automaticamente se houver notícias sem cobertura.
    
    Args:
        resultados: Resultados da verificação
    
    Returns:
        Dict com resultado da expansão
    """
    noticias_sem_cobertura = obter_noticias_sem_cobertura(resultados)
    
    if not noticias_sem_cobertura:
        return {"expansao_necessaria": False, "imagens_adicionadas": []}
    
    log(f"\n🔄 Iniciando expansão automática do acervo...")
    log(f"   {len(noticias_sem_cobertura)} notícias precisam de imagens")
    
    # Importar expansor
    try:
        from expansor_acervo import expandir_acervo_para_tema, PEXELS_API_KEY, PIXABAY_API_KEY
        
        if not PEXELS_API_KEY and not PIXABAY_API_KEY:
            log("Nenhuma API de imagens configurada - expansão não disponível", "WARN")
            return {"expansao_necessaria": True, "imagens_adicionadas": [], "erro": "APIs não configuradas"}
        
        # Identificar temas únicos que precisam de expansão
        temas_para_expandir = set()
        for noticia in noticias_sem_cobertura:
            temas_para_expandir.add(noticia['tema_identificado'])
        
        log(f"   Temas para expandir: {', '.join(temas_para_expandir)}")
        
        # Expandir cada tema
        todas_imagens = []
        for tema in temas_para_expandir:
            novas = expandir_acervo_para_tema(tema, quantidade=2)
            todas_imagens.extend(novas)
        
        return {
            "expansao_necessaria": True,
            "temas_expandidos": list(temas_para_expandir),
            "imagens_adicionadas": todas_imagens
        }
        
    except ImportError as e:
        log(f"Erro ao importar expansor: {e}", "ERROR")
        return {"expansao_necessaria": True, "imagens_adicionadas": [], "erro": str(e)}


def verificar_e_reportar(noticias: List[Dict], expandir: bool = False) -> Dict:
    """
    Função principal - verifica cobertura e opcionalmente expande o acervo.
    
    Args:
        noticias: Lista de notícias para verificar
        expandir: Se True, expande o acervo automaticamente
    
    Returns:
        Dict com resultados completos
    """
    print("\n" + "=" * 70)
    print("🔍 VERIFICADOR DE COBERTURA DE IMAGENS")
    print(f"📅 Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    print("=" * 70)
    
    # Verificar cobertura
    resultados = verificar_lote_noticias(noticias)
    
    # Mostrar relatório
    print(gerar_relatorio_cobertura(resultados))
    
    # Salvar log
    log_file = salvar_log_cobertura(resultados)
    log(f"\n📝 Log salvo em: {log_file}")
    
    # Expandir se necessário e solicitado
    if expandir and resultados['sem_cobertura'] > 0:
        resultado_expansao = expandir_acervo_se_necessario(resultados)
        resultados['expansao'] = resultado_expansao
    
    return resultados


# Teste do módulo
if __name__ == '__main__':
    # Carregar notícias do arquivo de dados
    noticias_file = DATA_DIR / 'noticias_imparciais.json'
    
    if noticias_file.exists():
        with open(noticias_file, 'r', encoding='utf-8') as f:
            dados = json.load(f)
        
        noticias = dados.get('noticias', [])
        
        if noticias:
            resultados = verificar_e_reportar(noticias, expandir=False)
        else:
            log("Nenhuma notícia encontrada no arquivo", "WARN")
    else:
        log(f"Arquivo não encontrado: {noticias_file}", "ERROR")
        
        # Testar com notícias de exemplo
        noticias_teste = [
            {"titulo": "STF decide sobre aposentadoria integral em casos de doença grave"},
            {"titulo": "General Heleno inicia cumprimento de prisão domiciliar"},
            {"titulo": "Dólar se mantém acima de R$ 5,50 e Bolsa registra alta"},
            {"titulo": "Lula sanciona reajuste para servidores do Judiciário"},
            {"titulo": "Congresso aprova Orçamento da União para 2026"},
        ]
        
        resultados = verificar_e_reportar(noticias_teste, expandir=False)
