#!/usr/bin/env python3
"""
BUSCADOR DE IMAGENS BRASILEIRAS - NOTÍCIAS IMPARCIAIS
======================================================
Este módulo busca imagens em fontes confiáveis com contexto brasileiro:
- Wikimedia Commons (API pública, sem necessidade de chave)

Todas as imagens são validadas quanto a:
- Resolução mínima (1200px de largura)
- Licença adequada (CC ou domínio público)
- Ausência de duplicatas

Versão: 1.1
Data: 29/12/2025
"""

import os
import re
import json
import time
import hashlib
import requests
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Set
from urllib.parse import quote, unquote

# Diretórios
ACERVO_DIR = Path(__file__).parent.parent / 'acervo_temas'
DATA_DIR = Path(__file__).parent / 'data'
CACHE_DIR = DATA_DIR / 'cache_imagens'
LOG_DIR = DATA_DIR / 'logs_busca'

# Criar diretórios
CACHE_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)

# Configurações
MIN_WIDTH = 1200  # Largura mínima em pixels
USER_AGENT = "NoticiasImparciais/1.0 (https://imparcial.manus.space; contato@noticiasimparciais.com.br)"

# Headers para requisições
HEADERS = {
    'User-Agent': USER_AGENT,
    'Accept': 'application/json'
}

# Licenças aceitas
LICENCAS_ACEITAS = [
    'cc-by', 'cc-by-sa', 'cc-zero', 'pd', 'public domain',
    'cc-by-3.0', 'cc-by-4.0', 'cc-by-sa-3.0', 'cc-by-sa-4.0',
    'cc0', 'gfdl'
]

# Cache global de URLs já baixadas para evitar duplicatas na sessão
_urls_baixadas_sessao: Set[str] = set()


def log(msg: str, level: str = "INFO"):
    """Log formatado com timestamp."""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] [{level}] {msg}")


def normalizar_nome_arquivo(nome: str) -> str:
    """Normaliza nome para uso em arquivo."""
    nome = nome.lower()
    substituicoes = {
        'á': 'a', 'à': 'a', 'ã': 'a', 'â': 'a',
        'é': 'e', 'ê': 'e', 'í': 'i',
        'ó': 'o', 'ô': 'o', 'õ': 'o',
        'ú': 'u', 'ü': 'u', 'ç': 'c',
        ' ': '_', '-': '_'
    }
    for orig, subst in substituicoes.items():
        nome = nome.replace(orig, subst)
    nome = re.sub(r'[^a-z0-9_]', '', nome)
    nome = re.sub(r'_+', '_', nome)
    return nome[:50].strip('_')


def verificar_licenca_aceita(licenca: str) -> bool:
    """Verifica se a licença é aceita."""
    if not licenca:
        return False
    licenca_lower = licenca.lower()
    return any(lic in licenca_lower for lic in LICENCAS_ACEITAS)


class WikimediaCommons:
    """Cliente para busca de imagens no Wikimedia Commons."""
    
    BASE_URL = "https://commons.wikimedia.org/w/api.php"
    
    @classmethod
    def buscar_imagens(cls, termo: str, limite: int = 10) -> List[Dict]:
        """
        Busca imagens no Wikimedia Commons.
        
        Args:
            termo: Termo de busca
            limite: Número máximo de resultados
        
        Returns:
            Lista de imagens encontradas
        """
        log(f"🔍 Buscando no Wikimedia Commons: '{termo}'")
        
        params = {
            'action': 'query',
            'format': 'json',
            'generator': 'search',
            'gsrnamespace': '6',  # Namespace de arquivos
            'gsrsearch': f'filetype:bitmap {termo}',
            'gsrlimit': limite,
            'prop': 'imageinfo',
            'iiprop': 'url|size|extmetadata',
            'iiurlwidth': 1920
        }
        
        try:
            response = requests.get(cls.BASE_URL, params=params, headers=HEADERS, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            imagens = []
            pages = data.get('query', {}).get('pages', {})
            
            for page_id, page_data in pages.items():
                if page_id == '-1':
                    continue
                
                imageinfo = page_data.get('imageinfo', [{}])[0]
                extmetadata = imageinfo.get('extmetadata', {})
                
                # Extrair informações
                largura = imageinfo.get('width', 0)
                altura = imageinfo.get('height', 0)
                url = imageinfo.get('url', '')
                url_thumb = imageinfo.get('thumburl', url)
                
                # Extrair licença
                licenca = extmetadata.get('LicenseShortName', {}).get('value', '')
                if not licenca:
                    licenca = extmetadata.get('License', {}).get('value', '')
                
                # Extrair descrição
                descricao = extmetadata.get('ImageDescription', {}).get('value', '')
                if descricao:
                    descricao = re.sub(r'<[^>]+>', '', descricao)[:200]
                
                # Extrair autor
                autor = extmetadata.get('Artist', {}).get('value', '')
                if autor:
                    autor = re.sub(r'<[^>]+>', '', autor)[:100]
                
                imagem = {
                    'titulo': page_data.get('title', '').replace('File:', ''),
                    'url': url,
                    'url_thumb': url_thumb,
                    'largura': largura,
                    'altura': altura,
                    'licenca': licenca,
                    'descricao': descricao,
                    'autor': autor,
                    'fonte': 'Wikimedia Commons',
                    'pagina': f"https://commons.wikimedia.org/wiki/{quote(page_data.get('title', ''))}"
                }
                
                imagens.append(imagem)
            
            log(f"   → {len(imagens)} imagens encontradas")
            return imagens
            
        except Exception as e:
            log(f"   ✗ Erro na busca: {e}", "ERROR")
            return []
    
    @classmethod
    def filtrar_imagens_validas(cls, imagens: List[Dict], urls_excluir: Set[str] = None) -> List[Dict]:
        """
        Filtra imagens que atendem aos critérios de qualidade.
        
        Args:
            imagens: Lista de imagens
            urls_excluir: Set de URLs a excluir (já baixadas)
        
        Returns:
            Lista filtrada
        """
        if urls_excluir is None:
            urls_excluir = set()
        
        validas = []
        
        for img in imagens:
            # Verificar se já foi baixada
            if img.get('url', '') in urls_excluir:
                continue
            
            # Verificar resolução
            if img.get('largura', 0) < MIN_WIDTH:
                continue
            
            # Verificar licença
            if not verificar_licenca_aceita(img.get('licenca', '')):
                continue
            
            # Verificar se não é SVG ou GIF
            url = img.get('url', '').lower()
            if url.endswith('.svg') or url.endswith('.gif'):
                continue
            
            validas.append(img)
        
        return validas


def baixar_imagem(url: str, destino: Path) -> bool:
    """
    Baixa uma imagem para o destino especificado.
    
    Args:
        url: URL da imagem
        destino: Caminho de destino
    
    Returns:
        True se sucesso, False caso contrário
    """
    try:
        log(f"   ⬇️ Baixando: {url[:60]}...")
        
        response = requests.get(url, headers=HEADERS, timeout=60, stream=True)
        response.raise_for_status()
        
        # Verificar tamanho
        content_length = response.headers.get('content-length')
        if content_length and int(content_length) < 10000:  # Menor que 10KB
            log(f"   ⚠️ Imagem muito pequena, ignorando", "WARN")
            return False
        
        # Salvar
        with open(destino, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        log(f"   ✅ Salvo em: {destino.name}")
        return True
        
    except Exception as e:
        log(f"   ✗ Erro ao baixar: {e}", "ERROR")
        return False


def contar_imagens_existentes(diretorio: Path, prefixo: str) -> int:
    """Conta quantas imagens com o prefixo existem no diretório."""
    if not diretorio.exists():
        return 0
    
    count = 0
    for arquivo in diretorio.iterdir():
        if arquivo.stem.startswith(prefixo):
            count += 1
    return count


def buscar_e_adicionar_ao_acervo(
    termos: List[str],
    diretorio_destino: str,
    filtro_nome: str,
    quantidade: int = 2
) -> List[Dict]:
    """
    Busca imagens e adiciona ao acervo local.
    Evita duplicatas usando cache de sessão.
    
    Args:
        termos: Lista de termos de busca
        diretorio_destino: Subdiretório no acervo
        filtro_nome: Prefixo para nome do arquivo
        quantidade: Quantidade de imagens a buscar
    
    Returns:
        Lista de imagens adicionadas
    """
    global _urls_baixadas_sessao
    
    log(f"\n🔄 Buscando imagens para: {filtro_nome}")
    log(f"   Termos: {', '.join(termos[:2])}")
    
    # Diretório de destino
    destino_dir = ACERVO_DIR / diretorio_destino
    destino_dir.mkdir(parents=True, exist_ok=True)
    
    # Contar imagens existentes
    num_existentes = contar_imagens_existentes(destino_dir, filtro_nome)
    
    imagens_adicionadas = []
    
    for termo in termos:
        if len(imagens_adicionadas) >= quantidade:
            break
        
        # Buscar no Wikimedia Commons
        resultados = WikimediaCommons.buscar_imagens(termo, limite=15)
        
        # Filtrar válidas (excluindo URLs já baixadas)
        validas = WikimediaCommons.filtrar_imagens_validas(resultados, _urls_baixadas_sessao)
        
        log(f"   → {len(validas)} imagens válidas para '{termo}'")
        
        for img in validas:
            if len(imagens_adicionadas) >= quantidade:
                break
            
            # Verificar novamente se URL já foi baixada
            if img['url'] in _urls_baixadas_sessao:
                log(f"   ⏭️ Imagem já baixada, pulando")
                continue
            
            # Gerar nome do arquivo
            num = num_existentes + len(imagens_adicionadas) + 1
            extensao = Path(img['url']).suffix.lower()
            if extensao not in ['.jpg', '.jpeg', '.png', '.webp']:
                extensao = '.jpg'
            
            nome_arquivo = f"{filtro_nome}_{num:02d}{extensao}"
            caminho_destino = destino_dir / nome_arquivo
            
            # Verificar se já existe
            if caminho_destino.exists():
                continue
            
            # Baixar imagem
            if baixar_imagem(img['url'], caminho_destino):
                img['arquivo_local'] = str(caminho_destino)
                img['nome_arquivo'] = nome_arquivo
                imagens_adicionadas.append(img)
                
                # Marcar URL como baixada
                _urls_baixadas_sessao.add(img['url'])
        
        # Pequena pausa entre buscas
        time.sleep(0.5)
    
    return imagens_adicionadas


def processar_requisicoes(requisicoes: List[Dict]) -> Dict:
    """
    Processa lista de requisições de busca de imagens.
    Agrupa requisições por tema para evitar duplicatas.
    
    Args:
        requisicoes: Lista de requisições
    
    Returns:
        Relatório de processamento
    """
    global _urls_baixadas_sessao
    
    # Limpar cache de sessão
    _urls_baixadas_sessao.clear()
    
    log("\n" + "=" * 70)
    log("🖼️ PROCESSADOR DE REQUISIÇÕES DE IMAGENS")
    log("=" * 70)
    
    resultado = {
        'data_processamento': datetime.now().isoformat(),
        'total_requisicoes': len(requisicoes),
        'sucesso': 0,
        'falha': 0,
        'imagens_adicionadas': []
    }
    
    # Agrupar requisições por tema para evitar buscas duplicadas
    temas_processados = set()
    
    for i, req in enumerate(requisicoes, 1):
        tema = req.get('filtro_nome_arquivo', 'imagem')
        
        # Se já processamos este tema, apenas marcar como sucesso
        if tema in temas_processados:
            log(f"\n[{i}/{len(requisicoes)}] {req.get('titulo_noticia', 'N/A')[:50]}...")
            log(f"   ⏭️ Tema '{tema}' já processado, reutilizando imagens")
            resultado['sucesso'] += 1
            req['status'] = 'REUTILIZADO'
            continue
        
        log(f"\n[{i}/{len(requisicoes)}] {req.get('titulo_noticia', 'N/A')[:50]}...")
        
        try:
            imagens = buscar_e_adicionar_ao_acervo(
                termos=req.get('termos_busca', []),
                diretorio_destino=req.get('diretorio_destino', 'executivo'),
                filtro_nome=req.get('filtro_nome_arquivo', 'imagem'),
                quantidade=2
            )
            
            if imagens:
                resultado['sucesso'] += 1
                temas_processados.add(tema)
                
                for img in imagens:
                    resultado['imagens_adicionadas'].append({
                        'requisicao': req.get('titulo_noticia', ''),
                        'arquivo': img.get('nome_arquivo', ''),
                        'fonte': img.get('fonte', ''),
                        'licenca': img.get('licenca', ''),
                        'autor': img.get('autor', ''),
                        'url_original': img.get('pagina', '')
                    })
                req['status'] = 'CONCLUIDO'
            else:
                resultado['falha'] += 1
                req['status'] = 'SEM_RESULTADO'
                log(f"   ⚠️ Nenhuma imagem encontrada", "WARN")
                
        except Exception as e:
            resultado['falha'] += 1
            req['status'] = 'ERRO'
            log(f"   ✗ Erro: {e}", "ERROR")
    
    return resultado


def gerar_relatorio_busca(resultado: Dict) -> str:
    """
    Gera relatório de busca de imagens.
    
    Args:
        resultado: Resultado do processamento
    
    Returns:
        Relatório formatado
    """
    linhas = [
        "",
        "=" * 70,
        "📊 RELATÓRIO DE BUSCA DE IMAGENS",
        "=" * 70,
        f"📅 Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}",
        "",
        f"Total de requisições: {resultado['total_requisicoes']}",
        f"✅ Sucesso: {resultado['sucesso']}",
        f"❌ Falha: {resultado['falha']}",
        f"📸 Imagens adicionadas: {len(resultado['imagens_adicionadas'])}",
        "",
    ]
    
    if resultado['imagens_adicionadas']:
        linhas.append("-" * 70)
        linhas.append("IMAGENS ADICIONADAS AO ACERVO:")
        linhas.append("-" * 70)
        
        for img in resultado['imagens_adicionadas']:
            linhas.append(f"\n📷 {img['arquivo']}")
            linhas.append(f"   Para: {img['requisicao'][:50]}...")
            linhas.append(f"   Fonte: {img['fonte']}")
            linhas.append(f"   Licença: {img['licenca']}")
            if img.get('autor'):
                linhas.append(f"   Autor: {img['autor'][:50]}")
    
    linhas.extend([
        "",
        "=" * 70,
    ])
    
    return "\n".join(linhas)


def salvar_log_busca(resultado: Dict) -> Path:
    """Salva log de busca em arquivo JSON."""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_file = LOG_DIR / f"busca_{timestamp}.json"
    
    with open(log_file, 'w', encoding='utf-8') as f:
        json.dump(resultado, f, ensure_ascii=False, indent=2)
    
    return log_file


# Teste do módulo
if __name__ == '__main__':
    # Testar busca no Wikimedia Commons
    print("\n" + "=" * 70)
    print("🧪 TESTE DO BUSCADOR DE IMAGENS")
    print("=" * 70)
    
    # Teste 1: Buscar imagens do STF
    print("\n📌 Teste 1: Buscar imagens do STF")
    resultados = WikimediaCommons.buscar_imagens("Supremo Tribunal Federal Brasil", limite=5)
    validas = WikimediaCommons.filtrar_imagens_validas(resultados)
    
    print(f"   Encontradas: {len(resultados)}")
    print(f"   Válidas: {len(validas)}")
    
    for img in validas[:2]:
        print(f"\n   📷 {img['titulo'][:50]}...")
        print(f"      Resolução: {img['largura']}x{img['altura']}")
        print(f"      Licença: {img['licenca']}")
    
    # Teste 2: Buscar imagens do Planalto
    print("\n📌 Teste 2: Buscar imagens do Palácio do Planalto")
    resultados = WikimediaCommons.buscar_imagens("Palácio do Planalto Brasília", limite=5)
    validas = WikimediaCommons.filtrar_imagens_validas(resultados)
    
    print(f"   Encontradas: {len(resultados)}")
    print(f"   Válidas: {len(validas)}")
    
    for img in validas[:2]:
        print(f"\n   📷 {img['titulo'][:50]}...")
        print(f"      Resolução: {img['largura']}x{img['altura']}")
        print(f"      Licença: {img['licenca']}")
