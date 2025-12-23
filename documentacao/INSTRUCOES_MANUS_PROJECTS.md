# Instruções para os Manus Projects - Notícias Imparciais

**Data:** 23/12/2025  
**Versão:** 2.0 (com acúmulo de notícias)

---

## Visão Geral da Arquitetura

O projeto utiliza o GitHub como base centralizada e três Manus Projects especializados:

1. **Coleta e Análise** — Coleta notícias e gera versões imparciais
2. **Publicação** — Atualiza o site com as novas notícias (ACUMULANDO histórico)
3. **Marketing** — Cria conteúdo para redes sociais

---

## Project 1: Notícias Imparciais - Coleta e Análise

### Master Instruction (Atualizada)

> *Sua tarefa é executar o ciclo de coleta de notícias. Conecte-se ao repositório GitHub 'noticias-imparciais', execute os scripts da pasta /scraper para coletar notícias das fontes (UOL, G1, Revista Oeste, Brasil Paralelo), analise os vieses, gere as notícias imparciais em formato JSON e salve na pasta /scraper/data. Faça commit das alterações no GitHub.*

### Fluxo de Trabalho

1. Clonar o repositório `noticias-imparciais`
2. Acessar as fontes de notícias (UOL, G1, Revista Oeste, Brasil Paralelo)
3. Coletar manchetes de Política e Economia
4. Identificar temas com cobertura de múltiplas fontes
5. Analisar vieses e gerar notícias imparciais
6. Salvar em `/scraper/data/noticias_imparciais.json`
7. Fazer commit e push para o GitHub

### Arquivos Relevantes

- `/scraper/coletor_noticias.py` — Script de coleta
- `/scraper/analisador_vies.py` — Análise de viés
- `/scraper/sintetizador_imparcial.py` — Geração de notícias
- `/scraper/processar_noticias.py` — Processamento completo
- `/scraper/data/noticias_imparciais.json` — Output das notícias

---

## Project 2: Notícias Imparciais - Publicação

### Master Instruction (Atualizada - IMPORTANTE)

> *Sua tarefa é atualizar o site ACUMULANDO as notícias novas ao histórico existente. Conecte-se ao repositório GitHub 'noticias-imparciais', execute o script /scraper/atualizar_site.py que irá: (1) ler as notícias imparciais de /scraper/data/noticias_imparciais.json, (2) mesclar com o histórico existente em /scraper/data/historico_noticias_site.json, (3) gerar o arquivo /site/client/src/data/news.ts com TODAS as notícias (novas no topo), e (4) fazer commit no GitHub. O Vercel fará o deploy automaticamente.*

### Fluxo de Trabalho

1. Clonar o repositório `noticias-imparciais`
2. Executar: `python3 scraper/atualizar_site.py`
3. O script automaticamente:
   - Carrega notícias novas de `noticias_imparciais.json`
   - Carrega histórico de `historico_noticias_site.json`
   - Mescla evitando duplicatas (novas no topo)
   - Gera o arquivo `news.ts` atualizado
   - Atualiza o histórico
4. Fazer commit e push para o GitHub
5. O Vercel detecta o commit e faz deploy automático

### Arquivos Relevantes

- `/scraper/atualizar_site.py` — Script principal de atualização
- `/scraper/data/noticias_imparciais.json` — Notícias novas (input)
- `/scraper/data/historico_noticias_site.json` — Histórico completo
- `/site/client/src/data/news.ts` — Arquivo do site (output)

### IMPORTANTE: Acúmulo de Notícias

O sistema foi projetado para **ACUMULAR** notícias, não substituir. Isso significa:

- Notícias antigas são preservadas
- Novas notícias aparecem no topo
- O histórico cresce ao longo do tempo
- Isso é essencial para SEO e indexação no Google

---

## Project 3: Notícias Imparciais - Marketing

### Master Instruction

> *Sua tarefa é criar conteúdo de marketing. Conecte-se ao repositório GitHub 'noticias-imparciais', acesse as notícias mais recentes na pasta /scraper/data e os assets de marca na pasta /assets para criar imagens e textos para posts no Instagram.*

### Fluxo de Trabalho

1. Clonar o repositório `noticias-imparciais`
2. Ler as notícias mais recentes de `/scraper/data/noticias_imparciais.json`
3. Acessar assets de marca em `/assets/`
4. Criar posts para Instagram com:
   - Manchete da notícia
   - Resumo imparcial
   - Hashtags relevantes
   - Visual alinhado à identidade da marca

### Arquivos Relevantes

- `/scraper/data/noticias_imparciais.json` — Notícias recentes
- `/assets/logo_principal.png` — Logo principal
- `/assets/identidade_visual.md` — Guia de marca

---

## Comandos Rápidos

### Para Coleta
```
Execute o ciclo de coleta de notícias de hoje.
```

### Para Publicação
```
Atualize o site com as notícias mais recentes, preservando o histórico.
```

### Para Marketing
```
Crie 3 posts para Instagram com as notícias de hoje.
```

---

## Estrutura do Repositório

```
noticias-imparciais/
├── site/                    # Código do site React
│   └── client/src/data/
│       └── news.ts          # Banco de notícias do site
├── scraper/                 # Scripts Python
│   ├── data/                # Dados JSON
│   │   ├── noticias_imparciais.json
│   │   └── historico_noticias_site.json
│   ├── atualizar_site.py    # Script de publicação
│   └── processar_noticias.py
├── documentacao/            # Documentação
├── assets/                  # Logos e identidade visual
└── README_DEPLOY.md
```

---

## Notas Importantes

1. **Sempre use o script `atualizar_site.py`** para publicar notícias — ele garante o acúmulo correto
2. **Nunca substitua o `news.ts` manualmente** — use sempre o script
3. **O histórico é persistido** em `historico_noticias_site.json`
4. **O script dispara o deploy automaticamente** via Deploy Hook do Vercel
5. **Não é necessário fazer commit** para o deploy funcionar — o Deploy Hook é independente

---

## Deploy Hook do Vercel

O script `atualizar_site.py` utiliza um Deploy Hook para disparar o deploy automaticamente:

```
https://api.vercel.com/v1/integrations/deploy/prj_voMU8PT7Aj80coLKjayjtnDB5yNi/9GsbAASQml
```

**IMPORTANTE:** Esta URL é secreta. Não compartilhe publicamente.
