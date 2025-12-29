#!/usr/bin/env python3
"""
Script de migração: news.ts -> Supabase
Lê os dados do arquivo TypeScript e insere no banco de dados Supabase.
"""

import os
import re
import json
from datetime import datetime
from dotenv import load_dotenv
from supabase import create_client, Client

# Carregar variáveis de ambiente
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_ANON_KEY')

def parse_news_ts(file_path: str) -> list:
    """
    Parseia o arquivo news.ts e extrai os objetos de notícias usando regex robusto.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    articles = []
    
    # Encontrar cada bloco de artigo
    # Padrão: { id: "...", ... }
    pattern = r'\{\s*id:\s*"([^"]+)"'
    
    # Dividir por cada início de objeto
    parts = re.split(r'\n\s*\{', content)
    
    for part in parts[1:]:  # Pular a primeira parte (antes do primeiro {)
        try:
            obj_text = '{' + part
            
            # Extrair campos usando regex
            article = {}
            
            # Campos de texto simples
            text_fields = ['id', 'title', 'subtitle', 'summary', 'content', 'category', 'date', 'imageUrl', 
                          'leftPerspective', 'rightPerspective', 'originalId']
            
            for field in text_fields:
                match = re.search(rf'{field}:\s*"((?:[^"\\]|\\.)*)"', obj_text, re.DOTALL)
                if match:
                    article[field] = match.group(1).replace('\\n', '\n').replace('\\"', '"')
                else:
                    # Verificar se é null
                    null_match = re.search(rf'{field}:\s*null', obj_text)
                    if null_match:
                        article[field] = None
            
            # Campos booleanos
            bool_fields = ['hasLeftPerspective', 'hasRightPerspective', 'hasBiasDetected']
            for field in bool_fields:
                match = re.search(rf'{field}:\s*(true|false)', obj_text)
                if match:
                    article[field] = match.group(1) == 'true'
            
            # Campo numérico
            match = re.search(r'version:\s*(\d+)', obj_text)
            if match:
                article['version'] = int(match.group(1))
            
            # Campos de array
            array_fields = ['attentionPoints', 'sources', 'relatedNews']
            for field in array_fields:
                match = re.search(rf'{field}:\s*\[(.*?)\]', obj_text, re.DOTALL)
                if match:
                    array_content = match.group(1)
                    # Extrair strings do array
                    items = re.findall(r'"((?:[^"\\]|\\.)*)"', array_content)
                    article[field] = [item.replace('\\n', '\n').replace('\\"', '"') for item in items]
                else:
                    article[field] = []
            
            # Campos de data
            for field in ['createdAt', 'updatedAt']:
                match = re.search(rf'{field}:\s*"([^"]*)"', obj_text)
                if match:
                    article[field] = match.group(1)
                else:
                    null_match = re.search(rf'{field}:\s*null', obj_text)
                    if null_match:
                        article[field] = None
            
            # Verificar se temos pelo menos o ID
            if 'id' in article and article['id']:
                articles.append(article)
                
        except Exception as e:
            continue
    
    return articles

def convert_to_db_format(article: dict) -> dict:
    """
    Converte um artigo do formato TypeScript para o formato do banco de dados.
    Remove campos com valor None para deixar o banco usar o default.
    """
    db_article = {
        'id': article.get('id'),
        'title': article.get('title', ''),
        'subtitle': article.get('subtitle', ''),
        'summary': article.get('summary', ''),
        'content': article.get('content', ''),
        'category': article.get('category', ''),
        'date': article.get('date', ''),
        'image_url': article.get('imageUrl', ''),
        'has_left_perspective': article.get('hasLeftPerspective', False),
        'has_right_perspective': article.get('hasRightPerspective', False),
        'attention_points': article.get('attentionPoints', []),
        'sources': article.get('sources', []),
        'has_bias_detected': article.get('hasBiasDetected', False),
        'version': article.get('version', 1),
        'related_news': article.get('relatedNews', []),
    }
    
    # Adicionar campos opcionais apenas se tiverem valor
    left_persp = article.get('leftPerspective')
    if left_persp:
        db_article['left_perspective'] = left_persp
    
    right_persp = article.get('rightPerspective')
    if right_persp:
        db_article['right_perspective'] = right_persp
    
    original_id = article.get('originalId')
    if original_id:
        db_article['original_id'] = original_id
    
    # created_at será definido pelo banco
    # updated_at será null por padrão
    
    return db_article

def migrate_to_supabase():
    """
    Função principal de migração.
    """
    print("=" * 60)
    print("MIGRAÇÃO: news.ts -> Supabase")
    print("=" * 60)
    
    # Verificar credenciais
    if not SUPABASE_URL or not SUPABASE_KEY:
        print("ERRO: Credenciais do Supabase não encontradas!")
        print(f"URL: {SUPABASE_URL}")
        print(f"KEY: {'***' if SUPABASE_KEY else 'Não definida'}")
        return
    
    print(f"\n✓ URL do Supabase: {SUPABASE_URL}")
    print(f"✓ Chave configurada: {'Sim' if SUPABASE_KEY else 'Não'}")
    
    # Conectar ao Supabase
    print("\n[1/4] Conectando ao Supabase...")
    try:
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        print("✓ Conexão estabelecida!")
    except Exception as e:
        print(f"ERRO ao conectar: {e}")
        return
    
    # Ler arquivo news.ts
    print("\n[2/4] Lendo arquivo news.ts...")
    news_file = os.path.join(os.path.dirname(__file__), '..', 'site', 'client', 'src', 'data', 'news.ts')
    
    try:
        articles = parse_news_ts(news_file)
        print(f"✓ {len(articles)} artigos encontrados!")
    except Exception as e:
        print(f"ERRO ao ler arquivo: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Converter e inserir
    print("\n[3/4] Inserindo artigos no Supabase...")
    success_count = 0
    error_count = 0
    
    for i, article in enumerate(articles, 1):
        try:
            db_article = convert_to_db_format(article)
            
            # Debug: mostrar o artigo sendo inserido
            print(f"\n  [{i}/{len(articles)}] Inserindo: {db_article['id'][:40]}...")
            
            # Usar upsert para evitar duplicatas
            result = supabase.table('articles').upsert(db_article, on_conflict='id').execute()
            
            print(f"  ✓ Sucesso!")
            success_count += 1
        except Exception as e:
            print(f"  ✗ Erro: {e}")
            error_count += 1
    
    # Resumo
    print("\n" + "=" * 60)
    print("RESUMO DA MIGRAÇÃO")
    print("=" * 60)
    print(f"Total de artigos: {len(articles)}")
    print(f"Sucesso: {success_count}")
    print(f"Erros: {error_count}")
    print("=" * 60)
    
    if success_count > 0:
        print("\n✓ Migração concluída com sucesso!")
    else:
        print("\n✗ Migração falhou!")

if __name__ == '__main__':
    migrate_to_supabase()
