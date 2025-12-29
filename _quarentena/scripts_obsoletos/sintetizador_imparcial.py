#!/usr/bin/env python3
"""
Módulo de Síntese Imparcial - Notícias Imparciais
Gera notícias imparciais a partir da análise de viés de múltiplas fontes.
"""

import json
import os
from datetime import datetime
from pathlib import Path
from openai import OpenAI

# Configurar cliente OpenAI
client = OpenAI()

def carregar_analise_vies(caminho: str) -> dict:
    """Carrega o relatório de análise de viés."""
    with open(caminho, 'r', encoding='utf-8') as f:
        return json.load(f)


def gerar_noticia_imparcial(tema: str, comparacao: dict, analises: list) -> dict:
    """Gera uma notícia imparcial a partir da análise de viés."""
    
    # Preparar contexto das análises individuais
    analises_relevantes = [a for a in analises if tema.lower() in a.get('titulo', '').lower() or 
                          any(palavra in a.get('titulo', '').lower() for palavra in tema.lower().split()[:2])]
    
    contexto_analises = ""
    for a in analises_relevantes:
        contexto_analises += f"""
FONTE: {a.get('fonte')} (Viés declarado: {a.get('vies_declarado')})
TÍTULO: {a.get('titulo')}
FATOS OBJETIVOS: {json.dumps(a.get('fatos_objetivos', []), ensure_ascii=False)}
LINGUAGEM CARREGADA: {json.dumps(a.get('linguagem_carregada', []), ensure_ascii=False)}
OMISSÕES POTENCIAIS: {json.dumps(a.get('omissoes_potenciais', []), ensure_ascii=False)}
SCORE DE VIÉS: {a.get('score_vies')}
---
"""

    prompt = f"""Você é o editor-chefe do portal "Notícias Imparciais", com o slogan "Os fatos, sem filtro."

Com base na análise de viés abaixo, escreva uma NOTÍCIA IMPARCIAL completa sobre o tema "{tema}".

## DADOS DA ANÁLISE COMPARATIVA:

FATOS EM COMUM (reportados por ambos os lados):
{json.dumps(comparacao.get('fatos_comuns', []), ensure_ascii=False, indent=2)}

FATOS EXCLUSIVOS DA ESQUERDA:
{json.dumps(comparacao.get('fatos_exclusivos_esquerda', []), ensure_ascii=False, indent=2)}

FATOS EXCLUSIVOS DA DIREITA:
{json.dumps(comparacao.get('fatos_exclusivos_direita', []), ensure_ascii=False, indent=2)}

DIFERENÇAS DE ENQUADRAMENTO:
- Esquerda: {comparacao.get('diferencas_enquadramento', {}).get('esquerda', 'N/A')}
- Direita: {comparacao.get('diferencas_enquadramento', {}).get('direita', 'N/A')}

PONTOS DE ATENÇÃO:
{json.dumps(comparacao.get('pontos_atencao', []), ensure_ascii=False, indent=2)}

## ANÁLISES INDIVIDUAIS DAS FONTES:
{contexto_analises}

## INSTRUÇÕES PARA A NOTÍCIA IMPARCIAL:

1. **TÍTULO**: Neutro, factual, sem adjetivos carregados
2. **SUBTÍTULO**: Resumo objetivo do acontecimento principal
3. **LEAD**: Responder O quê, Quem, Quando, Onde, Como (sem Por quê tendencioso)
4. **CORPO**: 
   - Apresentar TODOS os fatos objetivos de AMBOS os lados
   - Usar linguagem neutra (evitar termos como "trama golpista" ou "perseguição política")
   - Incluir contexto necessário para compreensão
   - Apresentar diferentes perspectivas de forma equilibrada
5. **SEÇÃO "O QUE DIZ CADA LADO"**: 
   - Resumir como fontes de esquerda abordam o tema
   - Resumir como fontes de direita abordam o tema
6. **SEÇÃO "PONTOS DE ATENÇÃO"**: Alertas para o leitor sobre possíveis vieses
7. **FONTES CONSULTADAS**: Listar todas as fontes utilizadas

Responda em JSON com as chaves:
- titulo (string)
- subtitulo (string)
- data_publicacao (string no formato "DD de mês de AAAA")
- lead (string - primeiro parágrafo)
- corpo (lista de parágrafos)
- o_que_diz_esquerda (string)
- o_que_diz_direita (string)
- pontos_atencao (lista de strings)
- fontes_consultadas (lista de strings)
- tags (lista de strings para categorização)
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "Você é um jornalista imparcial comprometido com a verdade factual. Sua missão é informar sem influenciar, apresentando todos os lados de forma equilibrada."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            response_format={"type": "json_object"}
        )
        
        noticia = json.loads(response.choices[0].message.content)
        noticia['tema'] = tema
        noticia['fontes_esquerda'] = comparacao.get('fontes_esquerda', [])
        noticia['fontes_direita'] = comparacao.get('fontes_direita', [])
        noticia['data_geracao'] = datetime.now().isoformat()
        
        return noticia
        
    except Exception as e:
        print(f"Erro ao gerar notícia: {e}")
        return None


def formatar_noticia_html(noticia: dict) -> str:
    """Formata a notícia em HTML para publicação no site."""
    
    corpo_html = "\n".join([f"<p>{p}</p>" for p in noticia.get('corpo', [])])
    pontos_html = "\n".join([f"<li>{p}</li>" for p in noticia.get('pontos_atencao', [])])
    fontes_html = "\n".join([f"<li>{f}</li>" for f in noticia.get('fontes_consultadas', [])])
    tags_html = " ".join([f'<span class="tag">{t}</span>' for t in noticia.get('tags', [])])
    
    html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{noticia.get('titulo', '')} | Notícias Imparciais</title>
    <style>
        :root {{
            --primary: #1A365D;
            --secondary: #64748B;
            --background: #F8FAFC;
            --border: #E2E8F0;
            --left-color: #DC2626;
            --right-color: #2563EB;
            --neutral-color: #16A34A;
        }}
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: var(--background);
            color: #1a1a1a;
            line-height: 1.7;
        }}
        
        .container {{
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }}
        
        header {{
            background: var(--primary);
            color: white;
            padding: 20px;
            text-align: center;
            margin-bottom: 30px;
        }}
        
        header h1 {{
            font-size: 1.5rem;
            font-weight: 700;
        }}
        
        header .slogan {{
            font-size: 0.9rem;
            opacity: 0.8;
            margin-top: 5px;
        }}
        
        article {{
            background: white;
            border-radius: 8px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            padding: 30px;
            margin-bottom: 20px;
        }}
        
        .article-header {{
            border-bottom: 2px solid var(--neutral-color);
            padding-bottom: 20px;
            margin-bottom: 20px;
        }}
        
        .article-title {{
            font-size: 1.8rem;
            color: var(--primary);
            margin-bottom: 10px;
            line-height: 1.3;
        }}
        
        .article-subtitle {{
            font-size: 1.1rem;
            color: var(--secondary);
            margin-bottom: 15px;
        }}
        
        .article-meta {{
            font-size: 0.85rem;
            color: var(--secondary);
        }}
        
        .article-lead {{
            font-size: 1.15rem;
            font-weight: 500;
            margin-bottom: 20px;
            padding: 15px;
            background: #f0f9ff;
            border-left: 4px solid var(--neutral-color);
        }}
        
        .article-body p {{
            margin-bottom: 15px;
            text-align: justify;
        }}
        
        .perspectives {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin: 30px 0;
        }}
        
        .perspective {{
            padding: 20px;
            border-radius: 8px;
        }}
        
        .perspective-left {{
            background: #fef2f2;
            border-left: 4px solid var(--left-color);
        }}
        
        .perspective-right {{
            background: #eff6ff;
            border-left: 4px solid var(--right-color);
        }}
        
        .perspective h3 {{
            font-size: 0.9rem;
            text-transform: uppercase;
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        
        .perspective-left h3 {{
            color: var(--left-color);
        }}
        
        .perspective-right h3 {{
            color: var(--right-color);
        }}
        
        .perspective p {{
            font-size: 0.95rem;
            color: #333;
        }}
        
        .attention-box {{
            background: #fffbeb;
            border: 1px solid #fbbf24;
            border-radius: 8px;
            padding: 20px;
            margin: 30px 0;
        }}
        
        .attention-box h3 {{
            color: #b45309;
            font-size: 1rem;
            margin-bottom: 10px;
        }}
        
        .attention-box ul {{
            margin-left: 20px;
        }}
        
        .attention-box li {{
            margin-bottom: 8px;
            font-size: 0.9rem;
        }}
        
        .sources {{
            background: var(--background);
            padding: 20px;
            border-radius: 8px;
            margin-top: 30px;
        }}
        
        .sources h3 {{
            font-size: 0.9rem;
            color: var(--secondary);
            margin-bottom: 10px;
        }}
        
        .sources ul {{
            list-style: none;
        }}
        
        .sources li {{
            font-size: 0.85rem;
            color: var(--secondary);
            padding: 5px 0;
        }}
        
        .tags {{
            margin-top: 20px;
            padding-top: 20px;
            border-top: 1px solid var(--border);
        }}
        
        .tag {{
            display: inline-block;
            background: var(--primary);
            color: white;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.75rem;
            margin-right: 8px;
            margin-bottom: 8px;
        }}
        
        footer {{
            text-align: center;
            padding: 30px;
            color: var(--secondary);
            font-size: 0.85rem;
        }}
        
        @media (max-width: 768px) {{
            .perspectives {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <header>
        <h1>⚖️ Notícias Imparciais</h1>
        <p class="slogan">Os fatos, sem filtro.</p>
    </header>
    
    <div class="container">
        <article>
            <div class="article-header">
                <h1 class="article-title">{noticia.get('titulo', '')}</h1>
                <p class="article-subtitle">{noticia.get('subtitulo', '')}</p>
                <p class="article-meta">📅 {noticia.get('data_publicacao', '')} | ✅ Notícia verificada e balanceada</p>
            </div>
            
            <div class="article-lead">
                {noticia.get('lead', '')}
            </div>
            
            <div class="article-body">
                {corpo_html}
            </div>
            
            <div class="perspectives">
                <div class="perspective perspective-left">
                    <h3>🔴 O que dizem fontes de esquerda</h3>
                    <p>{noticia.get('o_que_diz_esquerda', 'Não há cobertura disponível.')}</p>
                </div>
                <div class="perspective perspective-right">
                    <h3>🔵 O que dizem fontes de direita</h3>
                    <p>{noticia.get('o_que_diz_direita', 'Não há cobertura disponível.')}</p>
                </div>
            </div>
            
            <div class="attention-box">
                <h3>⚠️ Pontos de Atenção</h3>
                <ul>
                    {pontos_html}
                </ul>
            </div>
            
            <div class="sources">
                <h3>📚 Fontes Consultadas</h3>
                <ul>
                    {fontes_html}
                </ul>
            </div>
            
            <div class="tags">
                {tags_html}
            </div>
        </article>
    </div>
    
    <footer>
        <p>© 2025 Notícias Imparciais | Todos os direitos reservados</p>
        <p>Comprometidos com a verdade factual e o jornalismo equilibrado.</p>
    </footer>
</body>
</html>
"""
    return html


def formatar_noticia_markdown(noticia: dict) -> str:
    """Formata a notícia em Markdown."""
    
    corpo_md = "\n\n".join(noticia.get('corpo', []))
    pontos_md = "\n".join([f"- {p}" for p in noticia.get('pontos_atencao', [])])
    fontes_md = "\n".join([f"- {f}" for f in noticia.get('fontes_consultadas', [])])
    tags_md = " | ".join([f"`{t}`" for t in noticia.get('tags', [])])
    
    md = f"""# {noticia.get('titulo', '')}

**{noticia.get('subtitulo', '')}**

📅 {noticia.get('data_publicacao', '')} | ✅ Notícia verificada e balanceada

---

> {noticia.get('lead', '')}

---

{corpo_md}

---

## O Que Diz Cada Lado

### 🔴 Fontes de Esquerda
{noticia.get('o_que_diz_esquerda', 'Não há cobertura disponível.')}

### 🔵 Fontes de Direita
{noticia.get('o_que_diz_direita', 'Não há cobertura disponível.')}

---

## ⚠️ Pontos de Atenção

{pontos_md}

---

## 📚 Fontes Consultadas

{fontes_md}

---

**Tags:** {tags_md}

---

*Notícia gerada pelo portal Notícias Imparciais — "Os fatos, sem filtro."*
"""
    return md


def main():
    """Função principal para gerar notícias imparciais."""
    print("=" * 60)
    print("SINTETIZADOR IMPARCIAL - NOTÍCIAS IMPARCIAIS")
    print("=" * 60)
    
    # Carregar análise de viés
    print("\n[1] Carregando análise de viés...")
    analise_path = '/home/ubuntu/noticias_imparciais/scraper/data/relatorio_analise_vies.json'
    analise = carregar_analise_vies(analise_path)
    
    comparacoes = analise.get('comparacoes_tematicas', [])
    analises_individuais = analise.get('analises_individuais', [])
    
    print(f"    - {len(comparacoes)} temas para sintetizar")
    print(f"    - {len(analises_individuais)} análises individuais disponíveis")
    
    # Gerar notícias imparciais
    print("\n[2] Gerando notícias imparciais...")
    noticias_geradas = []
    
    for comp in comparacoes:
        tema = comp.get('tema', 'Tema não identificado')
        print(f"    Gerando: {tema}...")
        
        noticia = gerar_noticia_imparcial(tema, comp, analises_individuais)
        if noticia:
            noticias_geradas.append(noticia)
            
            # Salvar em diferentes formatos
            slug = tema.lower().replace(' ', '_').replace('-', '_')[:50]
            
            # JSON
            json_path = f'/home/ubuntu/noticias_imparciais/scraper/data/noticias/{slug}.json'
            os.makedirs(os.path.dirname(json_path), exist_ok=True)
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(noticia, f, ensure_ascii=False, indent=2)
            
            # HTML
            html_path = f'/home/ubuntu/noticias_imparciais/scraper/data/noticias/{slug}.html'
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(formatar_noticia_html(noticia))
            
            # Markdown
            md_path = f'/home/ubuntu/noticias_imparciais/scraper/data/noticias/{slug}.md'
            with open(md_path, 'w', encoding='utf-8') as f:
                f.write(formatar_noticia_markdown(noticia))
            
            print(f"        ✓ Salvo em JSON, HTML e Markdown")
    
    print(f"\n[OK] {len(noticias_geradas)} notícias imparciais geradas!")
    print("\n" + "=" * 60)
    print("SÍNTESE CONCLUÍDA!")
    print("=" * 60)
    
    return noticias_geradas


if __name__ == '__main__':
    main()
