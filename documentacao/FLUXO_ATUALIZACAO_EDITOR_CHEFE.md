# Fluxo de Atualização Completo - Editor-Chefe

**Para:** Agente Editor-Chefe  
**Data:** 30/12/2025  
**Versão:** 2.0  
**Assunto:** Roteiro completo do ciclo de atualização diário

---

## 1. Visão Geral

O ciclo de atualização do portal "Notícias Imparciais" consiste em **3 etapas principais**:

| Etapa | Responsável | Descrição |
|:---:|:---|:---|
| **0** | Editor-Chefe (manual) | Coletar notícias via navegador dos 4 portais |
| **1** | Script `processar_noticias.py` | Identificar temas, gerar notícias imparciais |
| **2** | Script `publicar_supabase.py` | Publicar no Supabase com imagens |

**IMPORTANTE:** O script de processamento **NÃO coleta** notícias automaticamente. A coleta deve ser feita **manualmente via navegador** antes de executar os scripts.

---

## 2. Regras Invioláveis

Antes de iniciar qualquer ciclo, relembre as regras que **NUNCA** podem ser violadas:

| Regra | Descrição |
|:---|:---|
| ⚠️ **NUNCA inventar informações** | Use APENAS os fatos presentes nas notícias coletadas (título e resumo) |
| ⚠️ **1 tema = 1 notícia** | Cada notícia deve ser sobre UM ÚNICO assunto. NUNCA misture temas |
| ⚠️ **Verificar antes de finalizar** | Sempre revise as notícias publicadas no site |

---

## 3. Pré-Requisitos

Antes de iniciar o ciclo, garanta que seu ambiente está pronto:

| Verificação | Comando / Ação | Frequência |
|:---|:---|:---|
| Repositório atualizado | `git pull origin main` | Diariamente |
| Dependências instaladas | `pip install python-dotenv supabase boto3 requests openai` | Uma vez |
| Arquivo `.env` configurado | Verificar se existe na raiz com todas as credenciais | Uma vez |

---

## 4. Etapa 0: Coleta Manual de Notícias

### 4.1 Por que a coleta é manual?

Os sites de notícias possuem proteções anti-bot que impedem a coleta automatizada. Por isso, a coleta deve ser feita **manualmente via navegador**.

### 4.2 Portais a Coletar

| Portal | Viés | URL | Seções |
|:---|:---|:---|:---|
| UOL | Esquerda | https://noticias.uol.com.br/politica/ | Política |
| G1/Globo | Esquerda | https://g1.globo.com/politica/ | Política |
| Revista Oeste | Direita | https://revistaoeste.com/politica/ | Política |
| Brasil Paralelo | Direita | https://www.brasilparalelo.com.br/noticias | Geral |

### 4.3 O que Coletar

Para cada notícia, colete:
- **Título** — Manchete principal
- **URL** — Link da notícia
- **Data** — Data de publicação (formato: DD/MM/AAAA)
- **Resumo** — Subtítulo ou primeiro parágrafo (se disponível)

### 4.4 Onde Salvar

Atualize os arquivos JSON na pasta `scraper/data/`:

| Arquivo | Fonte |
|:---|:---|
| `uol_politica_novo.json` | UOL Política |
| `globo_politica_novo.json` | G1 Política |
| `oeste_politica_novo.json` | Revista Oeste |
| `brasil_paralelo_politica_novo.json` | Brasil Paralelo |

### 4.5 Formato do JSON

```json
[
  {
    "titulo": "Título da notícia",
    "url": "https://...",
    "data": "30/12/2025",
    "resumo": "Resumo ou subtítulo da notícia"
  }
]
```

### 4.6 Dicas para Coleta

- Colete notícias **de hoje** — verifique a data de publicação
- Priorize notícias de **política e economia**
- Colete **8-10 notícias** de cada portal
- Inclua o **resumo** sempre que disponível (melhora a qualidade da geração)

---

## 5. Etapa 1: Processar Notícias

### 5.1 Comando

```bash
python3 scraper/processar_noticias.py
```

### 5.2 O que o Script Faz

1. **Carrega** os arquivos JSON da pasta `scraper/data/`
2. **Identifica temas** em comum entre fontes de esquerda e direita (via IA)
3. **Gera notícias imparciais** para cada tema identificado
4. **Aplica deduplicação** comparando com histórico (similaridade > 85% = duplicata)
5. **Salva** resultado em `scraper/data/noticias_imparciais.json`

### 5.3 Saída Esperada

```
============================================================
PROCESSADOR DE NOTÍCIAS - NOTÍCIAS IMPARCIAIS v2.1
(com identificação dinâmica de temas via IA)
Data: 30/12/2025 10:00
============================================================

[1] Carregando notícias coletadas...
    - Fontes de esquerda: 16 notícias
    - Fontes de direita: 19 notícias

[2] Identificando temas via IA...
    - Tema 1: 2 esquerda, 3 direita
    - Tema 2: 1 esquerda, 2 direita
    ...

[3] Gerando notícias imparciais...
    Processando: Tema 1...
    ✓ Gerada: Título da notícia...
    ...

[4] Aplicando deduplicação inteligente...

[5] Salvando resultados...
    ✓ Salvo: scraper/data/noticias_imparciais.json

============================================================
PROCESSAMENTO CONCLUÍDO!
  - X notícias imparciais finais (após deduplicação)
============================================================
```

---

## 6. Etapa 2: Publicar no Supabase

### 6.1 Comando

```bash
python3 scraper/publicar_supabase.py
```

### 6.2 O que o Script Faz

1. **Lê** o arquivo `noticias_imparciais.json`
2. **Verifica duplicatas** no Supabase antes de publicar
3. **Seleciona imagem** contextual (análise semântica + Wikimedia Commons)
4. **Faz upload** da imagem para Cloudflare R2
5. **Publica** a notícia no Supabase

### 6.3 Premissas de Imagens

| Padrão | Requisito |
|:---|:---|
| Resolução mínima | **1280px de largura** |
| Licença | Creative Commons ou Domínio Público |
| Marca d'água | Não permitido |
| Formato | JPEG, PNG, WebP |

### 6.4 Saída Esperada

```
======================================================================
📤 PUBLICADOR SUPABASE - NOTÍCIAS IMPARCIAIS v2.2
   (com análise semântica e busca automática de imagens)
📅 Data: 30/12/2025 10:05
======================================================================

[INFO] Carregando notícias de: scraper/data/noticias_imparciais.json
[INFO] Encontradas X notícias para publicar

[INFO] Processando: Título da notícia...
[INFO]   Análise: tema=economia, conceito=banco_master
[INFO]   Imagem selecionada: economia/banco_master_fachada_01.webp
[INFO]   ✓ Publicado: Título da notícia...

======================================================================
📊 RESUMO DA PUBLICAÇÃO
======================================================================
  ✓ Publicadas: X notícias
  ⚠ Duplicatas ignoradas: Y notícias
  ✗ Erros: 0
======================================================================
```

---

## 7. Verificação Pós-Publicação

### 7.1 Acessar o Site

Acesse: **https://noticias-imparciais.vercel.app/**

### 7.2 Checklist de Verificação

Para **cada notícia publicada**, verifique:

| Item | O que Verificar |
|:---|:---|
| **Título** | Neutro, factual, sem adjetivos carregados |
| **Conteúdo** | Baseado apenas nos fatos das fontes (sem invenções) |
| **Tema único** | Notícia sobre um único assunto (sem mistura de temas) |
| **Imagem** | Contextual e em alta resolução |
| **Perspectivas** | Seção "O Que Diz Cada Lado" com ambas as visões |

### 7.3 Corrigindo Problemas

| Problema | Solução |
|:---|:---|
| Notícia com informação inventada | Excluir do Supabase |
| Notícia misturando temas | Excluir do Supabase |
| Notícia duplicada | Excluir do Supabase |
| Imagem inadequada | Atualizar imagem no Supabase |

### 7.4 Excluindo Notícias do Supabase

```python
# Script para excluir notícia por título
from supabase import create_client
from dotenv import load_dotenv
import os

load_dotenv()
supabase = create_client(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_SERVICE_KEY'))

# Excluir por título (parcial)
titulo = "Parte do título da notícia"
result = supabase.table('articles').delete().ilike('title', f'%{titulo}%').execute()
print(f"Excluídas: {len(result.data)} notícias")
```

---

## 8. Salvar no GitHub (Opcional)

Após a publicação bem-sucedida, salve as alterações:

```bash
git add .
git commit -m "Ciclo de notícias 30/12/2025"
git push origin main
```

---

## 9. Reportar ao Diretor

Ao final do ciclo, envie um relatório ao Agente Diretor contendo:

1. **Quantidade de notícias coletadas** (por fonte)
2. **Quantidade de notícias publicadas**
3. **Duplicatas ignoradas** (se houver)
4. **Erros ou anomalias** (se houver)
5. **Confirmação** de que as notícias estão visíveis no site

---

## 10. Troubleshooting

### Erro: `ModuleNotFoundError`

**Problema:** Faltam dependências Python.  
**Solução:** `pip install python-dotenv supabase boto3 requests openai`

### Erro: Credenciais não encontradas

**Problema:** Arquivo `.env` ausente ou incompleto.  
**Solução:** Verificar se o arquivo `.env` existe na raiz e contém todas as variáveis.

### Erro: Notícias duplicadas publicadas

**Problema:** A deduplicação não identificou a similaridade.  
**Solução:** Excluir manualmente do Supabase e verificar o histórico.

### Erro: Imagem genérica ou inadequada

**Problema:** O acervo não tem imagem específica para o tema.  
**Solução:** Buscar imagem no Wikimedia Commons, adicionar ao acervo e atualizar a notícia.

### Erro: Notícia com informação inventada

**Problema:** A IA extrapolou além das fontes.  
**Solução:** Excluir a notícia do Supabase. As regras invioláveis no script devem prevenir isso.

### Erro: Notícia misturando temas

**Problema:** A IA combinou assuntos diferentes.  
**Solução:** Excluir a notícia do Supabase. As regras invioláveis no script devem prevenir isso.

---

## 11. Resumo do Fluxo

```
┌─────────────────────────────────────────────────────────────┐
│                    CICLO DE ATUALIZAÇÃO                     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ETAPA 0: COLETA MANUAL                                     │
│  ├── Acessar UOL, G1, Oeste, Brasil Paralelo               │
│  ├── Coletar notícias de hoje                              │
│  └── Atualizar arquivos JSON em scraper/data/              │
│                                                             │
│  ETAPA 1: PROCESSAMENTO                                     │
│  ├── python3 scraper/processar_noticias.py                 │
│  ├── Identifica temas via IA                               │
│  ├── Gera notícias imparciais                              │
│  └── Aplica deduplicação                                   │
│                                                             │
│  ETAPA 2: PUBLICAÇÃO                                        │
│  ├── python3 scraper/publicar_supabase.py                  │
│  ├── Seleciona imagens contextuais                         │
│  └── Publica no Supabase                                   │
│                                                             │
│  VERIFICAÇÃO                                                │
│  ├── Acessar site e revisar cada notícia                   │
│  ├── Corrigir problemas se necessário                      │
│  └── Reportar ao Diretor                                   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

*Este documento é a referência completa para o ciclo de atualização. Siga-o rigorosamente para garantir a qualidade do portal.*
