#!/usr/bin/env python3
"""
EXPANSOR DE ACERVO DE IMAGENS - NOTÍCIAS IMPARCIAIS
====================================================
Este módulo verifica a cobertura do acervo de imagens e expande automaticamente
quando não há imagem adequada para um tema/pessoa identificado.

Fontes de imagens:
- Pexels API (gratuito, licença comercial)
- Pixabay API (gratuito, licença comercial)
- Wikimedia Commons (domínio público/CC)

Diretrizes:
- Somente imagens reais (NÃO usar IA)
- Sem marca d'água
- Licença comercial/domínio público
- Resolução mínima: 1200px de largura

Versão: 1.0
Data: 29/12/2025
"""

import os
import re
import json
import requests
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List, Tuple
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv(Path(__file__).parent.parent / '.env')

# Configurações
PEXELS_API_KEY = os.getenv('PEXELS_API_KEY')
PIXABAY_API_KEY = os.getenv('PIXABAY_API_KEY')

# Diretórios
ACERVO_BASE = Path(__file__).parent.parent / 'acervo_temas'
LOG_DIR = Path(__file__).parent / 'data'

# Resolução mínima exigida
MIN_WIDTH = 1200

# Mapeamento de temas para termos de busca em inglês
TEMA_PARA_BUSCA = {
    # Temas institucionais
    "judiciario": ["supreme court brazil", "brazilian justice", "court building brazil"],
    "legislativo": ["congress brazil brasilia", "brazilian parliament", "chamber deputies brazil"],
    "executivo": ["planalto palace brazil", "brazilian government", "brasilia government"],
    "economia": ["brazil economy", "stock market brazil", "brazilian currency real"],
    "eleicoes": ["election brazil", "voting brazil", "ballot box brazil"],
    "seguranca": ["federal police brazil", "brazilian police", "security brazil"],
    
    # Estados
    "estados": ["brazil state government", "brazilian state capitol"],
    "rio_janeiro": ["rio de janeiro government", "alerj rio de janeiro"],
    
    # Pessoas públicas (usar com cuidado - preferir fotos oficiais)
    "lula": ["lula brazil president official"],
    "bolsonaro": ["bolsonaro brazil official"],
    "general_heleno": ["brazil military general official"],
    "ramagem": ["brazil federal police director"],
    
    # Marcas
    "havaianas": ["havaianas sandals brazil", "brazilian flip flops"],
}

# Mapeamento de diretórios do acervo
TEMA_PARA_DIRETORIO = {
    "judiciario": "judiciario",
    "legislativo": "legislativo",
    "executivo": "executivo",
    "economia": "economia",
    "eleicoes": "eleicoes",
    "seguranca": "seguranca",
    "estados": "estados",
    "rio_janeiro": "estados",
    "lula": "pessoas",
    "bolsonaro": "pessoas",
    "general_heleno": "pessoas",
    "ramagem": "pessoas",
    "havaianas": "marcas",
}


def log(msg: str, level: str = "INFO"):
    """Log formatado com timestamp."""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] [{level}] {msg}")


def verificar_cobertura_acervo() -> Dict:
    """
    Verifica a cobertura atual do acervo de imagens.
    
    Returns:
        Dict com estatísticas de cobertura por tema
    """
    cobertura = {}
    
    for tema, diretorio in TEMA_PARA_DIRETORIO.items():
        dir_path = ACERVO_BASE / diretorio
        
        if not dir_path.exists():
            cobertura[tema] = {"total": 0, "imagens": []}
            continue
        
        # Listar imagens no diretório
        imagens = []
        for f in dir_path.iterdir():
            if f.suffix.lower() in ['.jpg', '.jpeg', '.png', '.webp']:
                # Verificar se a imagem corresponde ao tema (para diretórios compartilhados)
                if tema in ["rio_janeiro", "rodoanel"]:
                    if tema == "rio_janeiro" and "alerj" in f.name.lower():
                        imagens.append(f.name)
                    elif tema == "rodoanel" and "rodoanel" in f.name.lower():
                        imagens.append(f.name)
                elif tema in ["lula", "bolsonaro", "general_heleno", "ramagem"]:
                    if tema.replace("_", "") in f.name.lower().replace("_", ""):
                        imagens.append(f.name)
                else:
                    imagens.append(f.name)
        
        cobertura[tema] = {
            "total": len(imagens),
            "imagens": imagens,
            "diretorio": str(dir_path)
        }
    
    return cobertura


def buscar_imagem_pexels(query: str, orientation: str = "landscape") -> Optional[Dict]:
    """
    Busca uma imagem no Pexels.
    
    Args:
        query: Termos de busca
        orientation: Orientação da imagem
    
    Returns:
        Dict com informações da imagem ou None
    """
    if not PEXELS_API_KEY:
        log("PEXELS_API_KEY não configurada", "WARN")
        return None
    
    headers = {
        "Authorization": PEXELS_API_KEY
    }
    
    params = {
        "query": query,
        "orientation": orientation,
        "per_page": 15,
        "size": "large"  # Garantir imagens grandes
    }
    
    try:
        response = requests.get(
            "https://api.pexels.com/v1/search",
            headers=headers,
            params=params,
            timeout=15
        )
        
        if response.status_code == 200:
            data = response.json()
            photos = data.get("photos", [])
            
            # Filtrar por resolução mínima
            fotos_validas = [
                p for p in photos 
                if p.get("width", 0) >= MIN_WIDTH
            ]
            
            if fotos_validas:
                # Selecionar baseado em hash da query para consistência
                query_hash = int(hashlib.md5(query.encode()).hexdigest(), 16)
                foto = fotos_validas[query_hash % len(fotos_validas)]
                
                return {
                    "id": foto["id"],
                    "url": foto["src"]["large2x"],  # Alta resolução
                    "url_original": foto["src"]["original"],
                    "width": foto["width"],
                    "height": foto["height"],
                    "photographer": foto["user"]["name"],
                    "photographer_url": foto["user"]["url"],
                    "pexels_url": foto["url"],
                    "alt": foto.get("alt", ""),
                    "fonte": "Pexels",
                    "licenca": "Pexels License (Free for commercial use)"
                }
        
        elif response.status_code == 401:
            log("Erro de autenticação Pexels - verifique a API key", "ERROR")
        elif response.status_code == 429:
            log("Rate limit Pexels excedido", "WARN")
        else:
            log(f"Erro Pexels: {response.status_code}", "WARN")
            
    except Exception as e:
        log(f"Erro na requisição Pexels: {e}", "ERROR")
    
    return None


def buscar_imagem_pixabay(query: str, orientation: str = "horizontal") -> Optional[Dict]:
    """
    Busca uma imagem no Pixabay.
    
    Args:
        query: Termos de busca
        orientation: Orientação (horizontal, vertical, all)
    
    Returns:
        Dict com informações da imagem ou None
    """
    if not PIXABAY_API_KEY:
        log("PIXABAY_API_KEY não configurada", "WARN")
        return None
    
    params = {
        "key": PIXABAY_API_KEY,
        "q": query,
        "orientation": orientation,
        "per_page": 15,
        "min_width": MIN_WIDTH,
        "safesearch": "true",
        "image_type": "photo"  # Apenas fotos reais
    }
    
    try:
        response = requests.get(
            "https://pixabay.com/api/",
            params=params,
            timeout=15
        )
        
        if response.status_code == 200:
            data = response.json()
            hits = data.get("hits", [])
            
            if hits:
                # Selecionar baseado em hash da query
                query_hash = int(hashlib.md5(query.encode()).hexdigest(), 16)
                foto = hits[query_hash % len(hits)]
                
                return {
                    "id": foto["id"],
                    "url": foto["largeImageURL"],
                    "url_original": foto.get("fullHDURL", foto["largeImageURL"]),
                    "width": foto["imageWidth"],
                    "height": foto["imageHeight"],
                    "photographer": foto["user"],
                    "photographer_url": f"https://pixabay.com/users/{foto['user']}-{foto['user_id']}/",
                    "pixabay_url": foto["pageURL"],
                    "fonte": "Pixabay",
                    "licenca": "Pixabay License (Free for commercial use)"
                }
                
    except Exception as e:
        log(f"Erro na requisição Pixabay: {e}", "ERROR")
    
    return None


def baixar_imagem(url: str, destino: Path) -> bool:
    """
    Baixa uma imagem para o sistema de arquivos.
    
    Args:
        url: URL da imagem
        destino: Caminho de destino
    
    Returns:
        True se baixado com sucesso
    """
    try:
        response = requests.get(url, timeout=60, stream=True)
        
        if response.status_code == 200:
            # Verificar tamanho do arquivo
            content_length = response.headers.get('content-length')
            if content_length and int(content_length) < 10000:  # < 10KB provavelmente é erro
                log(f"Imagem muito pequena: {content_length} bytes", "WARN")
                return False
            
            # Criar diretório se não existir
            destino.parent.mkdir(parents=True, exist_ok=True)
            
            with open(destino, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            log(f"  ✓ Imagem salva: {destino.name}")
            return True
            
    except Exception as e:
        log(f"Erro ao baixar imagem: {e}", "ERROR")
    
    return False


def gerar_nome_arquivo(tema: str, fonte: str, foto_id: str) -> str:
    """
    Gera um nome de arquivo padronizado para a imagem.
    
    Args:
        tema: Tema da imagem
        fonte: Fonte (pexels, pixabay, etc)
        foto_id: ID da foto na fonte
    
    Returns:
        Nome do arquivo
    """
    # Normalizar tema
    tema_norm = tema.lower().replace(" ", "_")
    
    # Contar imagens existentes do tema
    dir_path = ACERVO_BASE / TEMA_PARA_DIRETORIO.get(tema, "executivo")
    
    contador = 1
    if dir_path.exists():
        existentes = [f for f in dir_path.iterdir() if tema_norm in f.name.lower()]
        contador = len(existentes) + 1
    
    return f"{tema_norm}_{fonte.lower()}_{contador:02d}.jpg"


def expandir_acervo_para_tema(tema: str, quantidade: int = 2) -> List[Dict]:
    """
    Expande o acervo para um tema específico.
    
    Args:
        tema: Tema a expandir
        quantidade: Quantidade de imagens a adicionar
    
    Returns:
        Lista de imagens adicionadas
    """
    log(f"\n📸 Expandindo acervo para: {tema}")
    
    queries = TEMA_PARA_BUSCA.get(tema, [f"{tema} brazil"])
    diretorio = TEMA_PARA_DIRETORIO.get(tema, "executivo")
    dir_destino = ACERVO_BASE / diretorio
    
    imagens_adicionadas = []
    
    for i, query in enumerate(queries):
        if len(imagens_adicionadas) >= quantidade:
            break
        
        log(f"  🔍 Buscando: '{query}'")
        
        # Tentar Pexels primeiro
        foto = buscar_imagem_pexels(query)
        
        # Se não encontrar no Pexels, tentar Pixabay
        if not foto:
            foto = buscar_imagem_pixabay(query)
        
        if foto:
            # Gerar nome do arquivo
            nome_arquivo = gerar_nome_arquivo(tema, foto["fonte"], str(foto["id"]))
            destino = dir_destino / nome_arquivo
            
            # Verificar se já existe
            if destino.exists():
                log(f"  ⏭️ Imagem já existe: {nome_arquivo}")
                continue
            
            # Baixar imagem
            url_download = foto.get("url_original", foto["url"])
            if baixar_imagem(url_download, destino):
                registro = {
                    "arquivo": nome_arquivo,
                    "tema": tema,
                    "diretorio": str(dir_destino),
                    "fonte": foto["fonte"],
                    "licenca": foto["licenca"],
                    "fotografo": foto["photographer"],
                    "url_original": foto.get("pexels_url") or foto.get("pixabay_url"),
                    "resolucao": f"{foto['width']}x{foto['height']}",
                    "data_adicao": datetime.now().isoformat()
                }
                imagens_adicionadas.append(registro)
                log(f"  ✅ Adicionada: {nome_arquivo} ({foto['fonte']})")
    
    return imagens_adicionadas


def verificar_e_expandir_para_noticia(titulo: str, tema_identificado: str = None) -> Dict:
    """
    Verifica se há imagem adequada para uma notícia e expande se necessário.
    
    Args:
        titulo: Título da notícia
        tema_identificado: Tema já identificado (opcional)
    
    Returns:
        Dict com resultado da verificação/expansão
    """
    from seletor_temas_v4 import identificar_tema
    
    # Identificar tema se não fornecido
    if not tema_identificado:
        tema_id, score, descricao, config = identificar_tema(titulo)
        tema_identificado = tema_id
    
    log(f"\n🔎 Verificando cobertura para: {titulo[:50]}...")
    log(f"   Tema identificado: {tema_identificado}")
    
    # Verificar cobertura atual
    cobertura = verificar_cobertura_acervo()
    tema_cobertura = cobertura.get(tema_identificado, {"total": 0})
    
    resultado = {
        "titulo": titulo,
        "tema": tema_identificado,
        "imagens_existentes": tema_cobertura.get("total", 0),
        "expansao_necessaria": False,
        "imagens_adicionadas": []
    }
    
    # Se não há imagens suficientes, expandir
    if tema_cobertura.get("total", 0) < 2:
        log(f"   ⚠️ Cobertura insuficiente ({tema_cobertura.get('total', 0)} imagens)")
        resultado["expansao_necessaria"] = True
        
        # Expandir acervo
        novas_imagens = expandir_acervo_para_tema(tema_identificado, quantidade=3)
        resultado["imagens_adicionadas"] = novas_imagens
    else:
        log(f"   ✅ Cobertura adequada ({tema_cobertura.get('total', 0)} imagens)")
    
    return resultado


def relatorio_cobertura() -> str:
    """
    Gera um relatório de cobertura do acervo.
    
    Returns:
        Relatório em formato texto
    """
    cobertura = verificar_cobertura_acervo()
    
    linhas = [
        "=" * 70,
        "RELATÓRIO DE COBERTURA DO ACERVO DE IMAGENS",
        f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}",
        "=" * 70,
        ""
    ]
    
    total_imagens = 0
    temas_sem_cobertura = []
    
    for tema, dados in sorted(cobertura.items()):
        total = dados.get("total", 0)
        total_imagens += total
        
        status = "✅" if total >= 2 else "⚠️" if total == 1 else "❌"
        linhas.append(f"{status} {tema}: {total} imagens")
        
        if total < 2:
            temas_sem_cobertura.append(tema)
    
    linhas.extend([
        "",
        "-" * 70,
        f"Total de imagens no acervo: {total_imagens}",
        f"Temas com cobertura insuficiente: {len(temas_sem_cobertura)}",
    ])
    
    if temas_sem_cobertura:
        linhas.append(f"   → {', '.join(temas_sem_cobertura)}")
    
    linhas.append("=" * 70)
    
    return "\n".join(linhas)


def main():
    """Função principal - Verifica e expande o acervo."""
    
    print("\n" + "=" * 70)
    print("🖼️  EXPANSOR DE ACERVO - NOTÍCIAS IMPARCIAIS")
    print(f"📅 Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    print("=" * 70)
    
    # Verificar configuração de APIs
    apis_configuradas = []
    if PEXELS_API_KEY:
        apis_configuradas.append("Pexels")
    if PIXABAY_API_KEY:
        apis_configuradas.append("Pixabay")
    
    if not apis_configuradas:
        log("Nenhuma API de imagens configurada!", "ERROR")
        log("Configure PEXELS_API_KEY ou PIXABAY_API_KEY no .env", "INFO")
        return
    
    log(f"APIs configuradas: {', '.join(apis_configuradas)}")
    
    # Mostrar relatório de cobertura
    print(relatorio_cobertura())
    
    # Identificar temas que precisam de expansão
    cobertura = verificar_cobertura_acervo()
    temas_para_expandir = [
        tema for tema, dados in cobertura.items() 
        if dados.get("total", 0) < 2
    ]
    
    if not temas_para_expandir:
        log("\n✅ Todos os temas têm cobertura adequada!")
        return
    
    log(f"\n📋 Temas para expandir: {', '.join(temas_para_expandir)}")
    
    # Expandir cada tema
    todas_imagens_adicionadas = []
    
    for tema in temas_para_expandir:
        novas = expandir_acervo_para_tema(tema, quantidade=2)
        todas_imagens_adicionadas.extend(novas)
    
    # Salvar log de expansão
    if todas_imagens_adicionadas:
        log_file = LOG_DIR / f"expansao_acervo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump({
                "data": datetime.now().isoformat(),
                "imagens_adicionadas": todas_imagens_adicionadas
            }, f, ensure_ascii=False, indent=2)
        
        log(f"\n📝 Log salvo em: {log_file}")
    
    # Relatório final
    print("\n" + "=" * 70)
    print("📊 RESUMO DA EXPANSÃO")
    print("=" * 70)
    print(f"  Imagens adicionadas: {len(todas_imagens_adicionadas)}")
    
    for img in todas_imagens_adicionadas:
        print(f"    • {img['arquivo']} ({img['fonte']}) - {img['licenca']}")
    
    print("=" * 70)


if __name__ == '__main__':
    main()
