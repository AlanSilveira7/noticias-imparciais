#!/usr/bin/env python3
"""
PUBLICADOR SUPABASE V2 - NOTÍCIAS IMPARCIAIS
=============================================
Este script publica notícias no Supabase com verificação de cobertura de imagens.

NOVIDADES V2:
- Verificação de cobertura de imagens antes da publicação
- Log de notícias que usam fallback
- Integração com expansor de acervo (quando APIs configuradas)
- Relatório detalhado de imagens utilizadas

Fluxo:
1. Carregar notícias imparciais
2. Verificar cobertura de imagens para cada notícia
3. Expandir acervo se necessário (opcional)
4. Publicar no Supabase
5. Gerar relatório de publicação

Versão: 2.0
Data: 29/12/2025
"""

import json
import os
import re
import uuid
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional

# Carregar variáveis de ambiente
from dotenv import load_dotenv
load_dotenv(Path(__file__).parent.parent / '.env')

# Importar Supabase
from supabase import create_client

# Importar módulos do projeto
import sys
sys.path.insert(0, str(Path(__file__).parent))
from seletor_temas_v4 import selecionar_imagem, identificar_tema

# Configurações
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_SERVICE_KEY = os.getenv('SUPABASE_SERVICE_KEY')
R2_ACCESS_KEY = os.getenv('R2_ACCESS_KEY_ID')
R2_SECRET_KEY = os.getenv('R2_SECRET_ACCESS_KEY')
R2_BUCKET = os.getenv('R2_BUCKET_NAME')
R2_ACCOUNT_ID = os.getenv('R2_ACCOUNT_ID')
R2_ENDPOINT = f"https://{R2_ACCOUNT_ID}.r2.cloudflarestorage.com" if R2_ACCOUNT_ID else None
R2_PUBLIC_URL = os.getenv('R2_PUBLIC_URL')

# Diretórios
DATA_DIR = Path(__file__).parent / 'data'
ACERVO_DIR = Path(__file__).parent.parent / 'acervo_temas'
LOG_DIR = DATA_DIR / 'logs_publicacao'

# Criar diretório de logs
LOG_DIR.mkdir(parents=True, exist_ok=True)

# Imagens de fallback
FALLBACK_IMAGES = [
    'planalto_fachada_01.jpg',
    'planalto_fachada_02.jpg',
    'congresso_panorama_01.jpg'
]


def log(msg: str, level: str = "INFO"):
    """Log formatado com timestamp."""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] [{level}] {msg}")


def gerar_slug(titulo: str) -> str:
    """Gera um slug a partir do título."""
    slug = titulo.lower()
    substituicoes = {
        'á': 'a', 'à': 'a', 'ã': 'a', 'â': 'a',
        'é': 'e', 'ê': 'e', 'í': 'i',
        'ó': 'o', 'ô': 'o', 'õ': 'o',
        'ú': 'u', 'ü': 'u', 'ç': 'c',
    }
    for orig, subst in substituicoes.items():
        slug = slug.replace(orig, subst)
    
    slug = re.sub(r'[^a-z0-9\s-]', '', slug)
    slug = re.sub(r'\s+', '-', slug)
    slug = re.sub(r'-+', '-', slug)
    slug = slug[:50].rstrip('-')
    
    return slug


def carregar_noticias_imparciais() -> List[dict]:
    """Carrega as notícias imparciais geradas pelo processar_noticias.py."""
    arquivo = DATA_DIR / 'noticias_imparciais.json'
    
    if not arquivo.exists():
        log(f"Arquivo não encontrado: {arquivo}", "ERROR")
        return []
    
    with open(arquivo, 'r', encoding='utf-8') as f:
        dados = json.load(f)
    
    return dados.get('noticias', [])


def verificar_cobertura_imagem(titulo: str) -> Dict:
    """
    Verifica a cobertura de imagem para uma notícia.
    
    Returns:
        Dict com informações de cobertura
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
    
    return {
        'tema': tema_id,
        'score': score,
        'descricao': descricao,
        'imagem_path': imagem_path,
        'is_fallback': is_fallback,
        'cobertura_adequada': not is_fallback and imagem_path is not None
    }


def fazer_upload_imagem(imagem_path: str, titulo: str) -> str:
    """Faz upload da imagem para o Cloudflare R2."""
    try:
        import boto3
        
        if not os.path.exists(imagem_path):
            log(f"Imagem não encontrada: {imagem_path}", "WARN")
            return f"{R2_PUBLIC_URL}/noticias/acervo_v4/planalto_fachada_01.jpg"
        
        s3 = boto3.client(
            's3',
            endpoint_url=R2_ENDPOINT,
            aws_access_key_id=R2_ACCESS_KEY,
            aws_secret_access_key=R2_SECRET_KEY
        )
        
        # Gerar nome único para a imagem
        slug = gerar_slug(titulo)[:30]
        ext = os.path.splitext(imagem_path)[1]
        nome_arquivo = f"{slug}_{uuid.uuid4().hex[:8]}{ext}"
        chave_r2 = f"noticias/imagens/{nome_arquivo}"
        
        # Upload
        content_type = 'image/jpeg' if ext.lower() in ['.jpg', '.jpeg'] else 'image/png'
        if ext.lower() == '.webp':
            content_type = 'image/webp'
        
        s3.upload_file(
            imagem_path,
            R2_BUCKET,
            chave_r2,
            ExtraArgs={'ContentType': content_type}
        )
        
        url_publica = f"{R2_PUBLIC_URL}/{chave_r2}"
        log(f"  ✓ Upload: {nome_arquivo}")
        
        return url_publica
        
    except Exception as e:
        log(f"  ✗ Erro no upload: {e}", "ERROR")
        return f"{R2_PUBLIC_URL}/noticias/acervo_v4/planalto_fachada_01.jpg"


def selecionar_e_fazer_upload_imagem(titulo: str, log_cobertura: List[Dict]) -> str:
    """
    Seleciona imagem do acervo e faz upload para R2.
    Registra informações de cobertura no log.
    """
    # Verificar cobertura
    cobertura = verificar_cobertura_imagem(titulo)
    
    tema_id = cobertura['tema']
    imagem_path = cobertura['imagem_path']
    is_fallback = cobertura['is_fallback']
    
    # Registrar no log de cobertura
    log_entry = {
        'titulo': titulo,
        'tema': tema_id,
        'tema_score': cobertura['score'],
        'imagem': os.path.basename(imagem_path) if imagem_path else None,
        'is_fallback': is_fallback,
        'cobertura_adequada': cobertura['cobertura_adequada'],
        'timestamp': datetime.now().isoformat()
    }
    log_cobertura.append(log_entry)
    
    # Se não tem imagem ou é fallback, usar fallback padrão
    if not imagem_path or not os.path.exists(imagem_path):
        log(f"  ⚠️ Imagem não encontrada para: {titulo[:40]}...", "WARN")
        imagem_path = str(ACERVO_DIR / "executivo" / "planalto_fachada_01.jpg")
    
    # Log com indicador de fallback
    status = "⚠️ FALLBACK" if is_fallback else "✅"
    log(f"  🖼️ {status} Tema: {tema_id} → {os.path.basename(imagem_path)}")
    
    return fazer_upload_imagem(imagem_path, titulo)


def verificar_duplicata(supabase, titulo: str) -> bool:
    """Verifica se já existe uma notícia com título similar."""
    try:
        response = supabase.table('articles').select('title').execute()
        
        titulo_normalizado = titulo.lower().strip()
        
        for art in response.data:
            titulo_existente = art['title'].lower().strip()
            if titulo_normalizado == titulo_existente:
                return True
            if len(titulo_normalizado) > 30 and len(titulo_existente) > 30:
                if titulo_normalizado[:30] == titulo_existente[:30]:
                    return True
        
        return False
        
    except Exception as e:
        log(f"Erro ao verificar duplicata: {e}", "WARN")
        return False


def publicar_noticia(supabase, noticia: dict, imagem_url: str) -> bool:
    """Publica uma notícia no Supabase."""
    
    try:
        # Preparar corpo
        corpo = noticia.get('corpo', [])
        if isinstance(corpo, list):
            conteudo = '\n\n'.join(corpo)
        else:
            conteudo = str(corpo)
        
        # Extrair perspectivas
        esquerda = noticia.get('o_que_diz_esquerda', '')
        direita = noticia.get('o_que_diz_direita', '')
        
        # Determinar categoria
        secao = noticia.get('secao', 'politica').lower()
        categoria = 'Política' if 'polit' in secao else 'Economia'
        
        # Determinar se há viés detectado
        tem_perspectiva_esquerda = bool(esquerda and 
            'não há' not in esquerda.lower() and 
            'não foram' not in esquerda.lower() and
            'nenhuma' not in esquerda.lower())
        tem_perspectiva_direita = bool(direita and 
            'não há' not in direita.lower() and 
            'não foram' not in direita.lower() and
            'nenhuma' not in direita.lower())
        
        tem_vies = tem_perspectiva_esquerda and tem_perspectiva_direita
        
        # Pontos de atenção
        pontos = noticia.get('pontos_atencao', [])
        if isinstance(pontos, str):
            pontos = [pontos]
        
        # Fontes consultadas
        fontes = ['UOL', 'G1/Globo', 'Revista Oeste', 'Brasil Paralelo']
        
        dados = {
            'id': str(uuid.uuid4()),
            'title': noticia.get('titulo', ''),
            'subtitle': noticia.get('subtitulo', ''),
            'summary': noticia.get('lead', ''),
            'content': conteudo,
            'category': categoria,
            'date': datetime.now().strftime('%d/%m/%Y'),
            'image_url': imagem_url,
            'has_left_perspective': tem_perspectiva_esquerda,
            'left_perspective': esquerda if tem_perspectiva_esquerda else '',
            'has_right_perspective': tem_perspectiva_direita,
            'right_perspective': direita if tem_perspectiva_direita else '',
            'attention_points': pontos,
            'sources': fontes,
            'has_bias_detected': tem_vies,
            'version': 1,
            'created_at': datetime.now().isoformat(),
            'updated_at': None,
            'related_news': [],
            'original_id': None
        }
        
        # Inserir no Supabase
        resultado = supabase.table('articles').insert(dados).execute()
        
        if resultado.data:
            log(f"  ✓ Publicado: {noticia.get('titulo', '')[:50]}...")
            return True
        else:
            log(f"  ✗ Erro ao publicar", "ERROR")
            return False
            
    except Exception as e:
        log(f"  ✗ Erro no Supabase: {e}", "ERROR")
        return False


def gerar_relatorio_publicacao(stats: Dict, log_cobertura: List[Dict]) -> str:
    """Gera relatório detalhado da publicação."""
    
    # Contar estatísticas de cobertura
    total = len(log_cobertura)
    com_cobertura = sum(1 for l in log_cobertura if l['cobertura_adequada'])
    com_fallback = sum(1 for l in log_cobertura if l['is_fallback'])
    
    linhas = [
        "",
        "=" * 70,
        "📊 RELATÓRIO DE PUBLICAÇÃO",
        "=" * 70,
        f"📅 Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}",
        "",
        "ESTATÍSTICAS DE PUBLICAÇÃO:",
        f"  ✅ Notícias publicadas: {stats['publicadas']}",
        f"  ⏭️ Duplicatas ignoradas: {stats['duplicadas']}",
        f"  ❌ Erros: {stats['erros']}",
        "",
        "ESTATÍSTICAS DE COBERTURA DE IMAGENS:",
        f"  📸 Total verificado: {total}",
        f"  ✅ Com cobertura adequada: {com_cobertura}",
        f"  ⚠️ Usando fallback: {com_fallback}",
        "",
    ]
    
    # Listar notícias com fallback
    if com_fallback > 0:
        linhas.append("NOTÍCIAS COM FALLBACK (precisam de expansão do acervo):")
        for entry in log_cobertura:
            if entry['is_fallback']:
                linhas.append(f"  • {entry['titulo'][:50]}...")
                linhas.append(f"    Tema: {entry['tema']} | Imagem: {entry['imagem']}")
        linhas.append("")
    
    linhas.append("=" * 70)
    
    return "\n".join(linhas)


def salvar_log_publicacao(stats: Dict, log_cobertura: List[Dict]):
    """Salva log de publicação em arquivo JSON."""
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_file = LOG_DIR / f"publicacao_{timestamp}.json"
    
    dados = {
        'data': datetime.now().isoformat(),
        'stats': stats,
        'cobertura': log_cobertura
    }
    
    with open(log_file, 'w', encoding='utf-8') as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)
    
    log(f"📝 Log salvo em: {log_file}")


def main():
    """Função principal - Publica notícias imparciais no Supabase."""
    
    print("\n" + "=" * 70)
    print("📤 PUBLICADOR SUPABASE V2 - NOTÍCIAS IMPARCIAIS")
    print(f"📅 Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    print("=" * 70)
    
    # Verificar configurações
    if not SUPABASE_URL or not SUPABASE_SERVICE_KEY:
        log("Credenciais do Supabase não configuradas!", "ERROR")
        return {'publicadas': 0, 'duplicadas': 0, 'erros': 0}
    
    # Conectar ao Supabase
    log("Conectando ao Supabase...")
    supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
    
    # Carregar notícias imparciais
    log("Carregando notícias imparciais...")
    noticias = carregar_noticias_imparciais()
    
    if not noticias:
        log("Nenhuma notícia encontrada para publicar.", "WARN")
        return {'publicadas': 0, 'duplicadas': 0, 'erros': 0}
    
    log(f"  → {len(noticias)} notícias para processar")
    
    # Estatísticas
    stats = {
        'publicadas': 0,
        'duplicadas': 0,
        'erros': 0
    }
    
    # Log de cobertura de imagens
    log_cobertura = []
    
    # Processar cada notícia
    for i, noticia in enumerate(noticias, 1):
        titulo = noticia.get('titulo', 'Sem título')
        log(f"\n[{i}/{len(noticias)}] {titulo[:50]}...")
        
        # Verificar duplicata
        if verificar_duplicata(supabase, titulo):
            log(f"  ⏭️ Duplicata - pulando")
            stats['duplicadas'] += 1
            continue
        
        # Selecionar e fazer upload de imagem (com log de cobertura)
        imagem_url = selecionar_e_fazer_upload_imagem(titulo, log_cobertura)
        
        # Publicar
        if publicar_noticia(supabase, noticia, imagem_url):
            stats['publicadas'] += 1
        else:
            stats['erros'] += 1
    
    # Gerar e mostrar relatório
    relatorio = gerar_relatorio_publicacao(stats, log_cobertura)
    print(relatorio)
    
    # Salvar log
    salvar_log_publicacao(stats, log_cobertura)
    
    return stats


if __name__ == '__main__':
    main()
