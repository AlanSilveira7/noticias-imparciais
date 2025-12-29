# Instruções para os Manus Projects - Notícias Imparciais

**Data:** 29/12/2025  
**Versão:** 3.0 (com análise semântica de imagens e busca automática)

---

## Visão Geral da Arquitetura

O projeto utiliza o GitHub como base centralizada e três Manus Projects especializados:

1. **Coleta e Análise** — Coleta notícias e gera versões imparciais
2. **Publicação** — Publica no Supabase com seleção inteligente de imagens
3. **Marketing** — Cria conteúdo para redes sociais

---

## Project 1: Notícias Imparciais - Coleta e Análise

### Master Instruction

> *Sua tarefa é executar o ciclo de coleta de notícias. Conecte-se ao repositório GitHub 'noticias-imparciais', execute o script /scraper/processar_noticias.py para coletar notícias das fontes (UOL, G1, Revista Oeste, Brasil Paralelo), analise os vieses, gere as notícias imparciais em formato JSON e salve na pasta /scraper/data. Faça commit das alterações no GitHub.*

### Fluxo de Trabalho

1. Clonar o repositório `noticias-imparciais`
2. Acessar as fontes de notícias (UOL, G1, Revista Oeste, Brasil Paralelo)
3. Coletar manchetes de Política e Economia
4. Identificar temas com cobertura de múltiplas fontes
5. Analisar vieses e gerar notícias imparciais
6. Salvar em `/scraper/data/noticias_imparciais.json`
7. Fazer commit e push para o GitHub

### Arquivos Relevantes

- `/scraper/processar_noticias.py` — Script principal de coleta e processamento
- `/scraper/data/noticias_imparciais.json` — Output das notícias

---

## Project 2: Notícias Imparciais - Publicação

### Master Instruction (ATUALIZADA - v3.0)

> *Sua tarefa é publicar as notícias no banco de dados Supabase. Conecte-se ao repositório GitHub 'noticias-imparciais', configure o arquivo .env com as credenciais necessárias, e execute o script /scraper/publicar_supabase.py. O script irá: (1) ler as notícias de /scraper/data/noticias_imparciais.json, (2) selecionar imagens contextuais usando análise semântica, (3) buscar automaticamente no Wikimedia Commons se não houver imagem adequada, (4) fazer upload das imagens para o Cloudflare R2, e (5) publicar no Supabase. Faça commit das alterações no GitHub.*

### Fluxo de Trabalho Simplificado

O ciclo de publicação agora consiste em apenas **duas etapas principais**:

```bash
# 1. Coletar e Processar
python3 scraper/processar_noticias.py

# 2. Publicar no Banco de Dados (Produção)
python3 scraper/publicar_supabase.py

# 3. Salvar Alterações no GitHub (Opcional, mas recomendado)
git add .
git commit -m "Ciclo de notícias [DATA]"
git push origin main
```

### Arquivos Relevantes

- `/scraper/publicar_supabase.py` — Script principal de publicação (v2.1)
- `/scraper/analisador_contexto.py` — Módulo de análise semântica
- `/scraper/buscador_imagens_br.py` — Módulo de busca de imagens no Wikimedia
- `/scraper/data/noticias_imparciais.json` — Notícias a publicar (input)
- `/acervo_temas/` — Banco de imagens locais

### Configuração do Arquivo .env (CRÍTICO)

O arquivo `.env` **não está no repositório** por segurança. Crie-o na raiz do projeto com as seguintes variáveis:

```
# Supabase
SUPABASE_URL=https://rlrnqrgempxjymhiisua.supabase.co
SUPABASE_SERVICE_KEY=sua_chave_aqui

# Cloudflare R2
R2_ACCOUNT_ID=seu_account_id
R2_ACCESS_KEY_ID=sua_access_key
R2_SECRET_ACCESS_KEY=sua_secret_key
R2_BUCKET_NAME=noticias-imparciais-imagens
R2_PUBLIC_URL=https://pub-xxx.r2.dev
R2_ENDPOINT=https://xxx.r2.cloudflarestorage.com
```

### Dependências Python

Instale as dependências necessárias uma única vez:

```bash
pip install python-dotenv supabase boto3 requests
```

### Sistema de Imagens Inteligente

O novo sistema de publicação possui duas camadas de inteligência:

**Camada 1 - Análise Semântica:** Analisa o título da notícia e identifica o tema principal, classificando-o como:
- **Conceito/Símbolo** (FGTS → carteira de trabalho, indulto → presídio)
- **Instituição** (acareação → STF, inflação → Banco Central)
- **Pessoa** (quando é o foco principal, como saúde ou prisão domiciliar)

**Camada 2 - Busca Automática:** Quando não há imagem adequada no acervo local, o sistema:
1. Busca automaticamente no Wikimedia Commons
2. Baixa a imagem em alta resolução (mínimo 1280px)
3. Valida a licença (Creative Commons ou domínio público)
4. Adiciona ao acervo local para uso futuro

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

### Para Coleta e Publicação Completa
```
Execute o ciclo completo de atualização do site: colete as notícias de hoje, processe-as e publique no Supabase.
```

### Para Marketing
```
Crie 3 posts para Instagram com as notícias de hoje.
```

---

## Estrutura do Repositório

```
noticias-imparciais/
├── README.md                    # Documentação principal
├── .env                         # Credenciais (NÃO está no git)
├── .gitignore                   # Configuração git
│
├── scraper/                     # Scripts Python (4 essenciais)
│   ├── processar_noticias.py    # Coleta e processa notícias
│   ├── publicar_supabase.py     # Publica no Supabase
│   ├── analisador_contexto.py   # Análise semântica
│   ├── buscador_imagens_br.py   # Busca imagens Wikimedia
│   └── data/                    # Dados de operação
│
├── acervo_temas/                # Banco de imagens HD
│   ├── economia/
│   ├── executivo/
│   ├── judiciario/
│   ├── legislativo/
│   ├── pessoas/
│   └── ...
│
├── documentacao/                # Documentação do projeto
├── assets/                      # Logos e identidade visual
├── site/                        # Frontend React
└── _quarentena/                 # Arquivos para exclusão (05/01/2026)
```

---

## Notas Importantes

1. **O site agora lê diretamente do Supabase** — não é mais necessário atualizar o arquivo `news.ts`
2. **O script `atualizar_site.py` foi descontinuado** — use apenas `publicar_supabase.py`
3. **As imagens são armazenadas no Cloudflare R2** — não mais no repositório
4. **O arquivo `.env` é obrigatório** — sem ele, a publicação não funciona
5. **A busca automática de imagens é ativada** quando não há imagem adequada no acervo

---

## Troubleshooting

### Erro de Credencial (Supabase ou R2)
Verifique se o arquivo `.env` existe na raiz do projeto e contém todas as variáveis necessárias.

### Imagem não encontrada
O sistema buscará automaticamente no Wikimedia Commons. Se ainda não encontrar, usará uma imagem de fallback da categoria.

### Módulo não encontrado
Execute: `pip install python-dotenv supabase boto3 requests`
