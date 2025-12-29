#!/usr/bin/env python3
"""
Script para gerar notícias imparciais em lote usando IA
"""

import json
import os
import requests
from datetime import datetime

# Configurações
COLETA_DIR = "/home/ubuntu/noticias_imparciais/scraper/data/coleta_22dez2025"
OUTPUT_DIR = "/home/ubuntu/noticias_imparciais/scraper/data/noticias_22dez2025"
API_URL = os.environ.get("BUILT_IN_FORGE_API_URL", "")
API_KEY = os.environ.get("BUILT_IN_FORGE_API_KEY", "")

def chamar_ia(prompt, max_tokens=2000):
    """Chama a API de IA para gerar conteúdo"""
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "anthropic/claude-sonnet-4",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens
    }
    
    response = requests.post(f"{API_URL}/v1/chat/completions", headers=headers, json=payload)
    
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        print(f"Erro na API: {response.status_code}")
        return None

def gerar_noticia_imparcial(tema, noticias, tem_cobertura_multipla):
    """Gera uma notícia imparcial para um tema"""
    
    # Preparar contexto das notícias
    contexto_esquerda = []
    contexto_direita = []
    
    for n in noticias:
        info = f"- {n.get('titulo', '')} ({n.get('fonte', '')})"
        if n.get('resumo'):
            info += f"\n  Resumo: {n.get('resumo', '')}"
        
        if n.get('vies') == 'esquerda':
            contexto_esquerda.append(info)
        else:
            contexto_direita.append(info)
    
    if tem_cobertura_multipla:
        prompt = f"""Você é um jornalista imparcial do portal "Notícias Imparciais". 
Sua missão é criar uma notícia neutra e factual sobre o tema: "{tema}"

FONTES DE ESQUERDA (UOL, G1/Globo):
{chr(10).join(contexto_esquerda) if contexto_esquerda else "Nenhuma cobertura"}

FONTES DE DIREITA (Revista Oeste, Brasil Paralelo):
{chr(10).join(contexto_direita) if contexto_direita else "Nenhuma cobertura"}

Gere uma notícia no formato JSON com a seguinte estrutura:
{{
    "titulo": "Título neutro e factual",
    "subtitulo": "Subtítulo explicativo",
    "resumo": "Resumo em 2-3 frases",
    "texto": "Texto completo da notícia (3-4 parágrafos)",
    "perspectiva_esquerda": "O que as fontes de esquerda enfatizam",
    "perspectiva_direita": "O que as fontes de direita enfatizam",
    "pontos_atencao": ["Lista de pontos de atenção sobre vieses detectados"],
    "tem_vies_detectado": true,
    "fontes": ["Lista das fontes consultadas"]
}}

REGRAS:
1. Título deve ser neutro, sem termos carregados
2. Texto deve apresentar apenas fatos confirmados
3. Perspectivas devem resumir as ênfases de cada lado
4. Pontos de atenção devem alertar sobre vieses ou omissões
5. Responda APENAS com o JSON, sem texto adicional"""
    else:
        # Notícia sem cobertura múltipla - mais simples
        vies_fonte = "esquerda" if contexto_esquerda else "direita"
        contexto = contexto_esquerda if contexto_esquerda else contexto_direita
        
        prompt = f"""Você é um jornalista imparcial do portal "Notícias Imparciais". 
Sua missão é criar uma notícia neutra e factual sobre o tema: "{tema}"

FONTES DISPONÍVEIS ({vies_fonte}):
{chr(10).join(contexto)}

Gere uma notícia no formato JSON com a seguinte estrutura:
{{
    "titulo": "Título neutro e factual",
    "subtitulo": "Subtítulo explicativo",
    "resumo": "Resumo em 2-3 frases",
    "texto": "Texto completo da notícia (3-4 parágrafos)",
    "perspectiva_esquerda": null,
    "perspectiva_direita": null,
    "pontos_atencao": ["Notícia baseada apenas em fontes de {vies_fonte}. Não foi possível verificar cobertura do outro espectro político."],
    "tem_vies_detectado": false,
    "fontes": ["Lista das fontes consultadas"]
}}

REGRAS:
1. Título deve ser neutro, sem termos carregados
2. Texto deve apresentar apenas fatos confirmados
3. Responda APENAS com o JSON, sem texto adicional"""
    
    resposta = chamar_ia(prompt)
    
    if resposta:
        try:
            # Limpar resposta e extrair JSON
            resposta = resposta.strip()
            if resposta.startswith("```json"):
                resposta = resposta[7:]
            if resposta.startswith("```"):
                resposta = resposta[3:]
            if resposta.endswith("```"):
                resposta = resposta[:-3]
            
            noticia = json.loads(resposta.strip())
            noticia["tema"] = tema
            noticia["data_geracao"] = datetime.now().isoformat()
            noticia["secao"] = "politica"
            return noticia
        except json.JSONDecodeError as e:
            print(f"Erro ao parsear JSON para tema '{tema}': {e}")
            return None
    
    return None

def main():
    print("=" * 60)
    print("GERAÇÃO DE NOTÍCIAS IMPARCIAIS")
    print(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    print("=" * 60)
    
    # Criar diretório de saída
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Carregar análise de temas
    with open(os.path.join(COLETA_DIR, "analise_temas.json"), 'r', encoding='utf-8') as f:
        analise = json.load(f)
    
    temas_multiplos = analise.get("temas_cobertura_multipla", {})
    temas_unicos = analise.get("temas_cobertura_unica", {})
    
    noticias_geradas = []
    
    # Gerar notícias para temas com cobertura múltipla (prioridade)
    print("\n📰 Gerando notícias com análise de viés...")
    for tema, dados in temas_multiplos.items():
        if dados.get("total", 0) > 0:
            print(f"   → {tema}...")
            noticia = gerar_noticia_imparcial(tema, dados.get("noticias", []), True)
            if noticia:
                noticias_geradas.append(noticia)
                print(f"     ✅ Gerada: {noticia.get('titulo', '')[:50]}...")
    
    # Gerar notícias para temas com cobertura única (se precisar de mais)
    print("\n📰 Gerando notícias de cobertura única...")
    for tema, dados in temas_unicos.items():
        if dados.get("total", 0) > 0 and len(noticias_geradas) < 12:
            print(f"   → {tema}...")
            noticia = gerar_noticia_imparcial(tema, dados.get("noticias", []), False)
            if noticia:
                noticias_geradas.append(noticia)
                print(f"     ✅ Gerada: {noticia.get('titulo', '')[:50]}...")
    
    # Salvar todas as notícias
    output_file = os.path.join(OUTPUT_DIR, "noticias_imparciais.json")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            "data_geracao": datetime.now().isoformat(),
            "total": len(noticias_geradas),
            "noticias": noticias_geradas
        }, f, ensure_ascii=False, indent=2)
    
    print("\n" + "=" * 60)
    print(f"✅ Total de notícias geradas: {len(noticias_geradas)}")
    print(f"📁 Salvas em: {output_file}")
    print("=" * 60)
    
    return noticias_geradas

if __name__ == "__main__":
    main()
