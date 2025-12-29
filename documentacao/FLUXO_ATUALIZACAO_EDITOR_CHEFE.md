# Fluxo de Atualização Simplificado - Editor Chefe

**Para:** Agente Editor Chefe  
**De:** Agente Desenvolvedor Backend  
**Data:** 29/12/2025  
**Assunto:** Roteiro de atualização do site, simples e eficiente.

---

## 1. Resumo da Mudança

O fluxo de atualização foi **simplificado**. A etapa de sincronização com o arquivo `news.ts` (`atualizar_site.py`) foi **removida**, pois o site agora lê as notícias diretamente do banco de dados Supabase.

Isso torna o processo mais rápido e menos propenso a erros.

## 2. Fluxo de Atualização (2 Etapas)

O ciclo completo de atualização consiste em **duas etapas principais**:

### Etapa 1: Coletar, Processar e Deduplicar Notícias

Este comando executa a coleta de notícias dos 4 portais (UOL, G1, Oeste, Brasil Paralelo), gera as versões imparciais e aplica a **deduplicação inteligente** automaticamente.

```bash
python3 scraper/processar_noticias.py
```

**O que faz:**
- Coleta notícias das 4 fontes configuradas
- Identifica temas com cobertura de múltiplas fontes
- Analisa vieses de cada fonte
- Gera notícias imparciais com seções "O Que Diz Cada Lado"
- **Aplica deduplicação inteligente** (similaridade > 85% = duplicata)
- Salva resultado em `noticias_imparciais.json`

### Etapa 2: Publicar no Banco de Dados

Este comando publica as notícias no Supabase e aplica a lógica de seleção de imagens:
- Análise semântica do título
- Seleção de imagem do acervo local
- **Busca automática no Wikimedia Commons** (se não encontrar no acervo)
- Upload para Cloudflare R2

```bash
python3 scraper/publicar_supabase.py
```

**Premissas de Imagens:**
- Resolução mínima: **1280px de largura**
- Licença: Creative Commons ou Domínio Público
- Sem marca d'água
- Formato: JPEG, PNG ou WebP

## 3. Comandos de Execução (Resumo)

Para executar o ciclo completo manualmente:

```bash
# 1. Coletar, Processar e Deduplicar
python3 scraper/processar_noticias.py

# 2. Publicar no Banco de Dados (Produção)
python3 scraper/publicar_supabase.py

# 3. Salvar Alterações no GitHub (Opcional, mas recomendado)
git add .
git commit -m "Ciclo de notícias [DATA]"
git push origin main
```

## 4. Requisitos de Ambiente

Para que o fluxo funcione, você precisa garantir que seu ambiente está configurado corretamente:

**1. Repositório Atualizado:** Sempre execute `git pull origin main` antes de iniciar o ciclo para garantir que está com a versão mais recente dos scripts.

**2. Dependências Python:** Instale as dependências necessárias com o comando:
```bash
pip install python-dotenv supabase boto3 requests openai
```

**3. Arquivo `.env` (CRÍTICO):** Crie um arquivo chamado `.env` na raiz do projeto com as seguintes credenciais:
```
SUPABASE_URL=...
SUPABASE_SERVICE_KEY=...
R2_ACCOUNT_ID=...
R2_ACCESS_KEY_ID=...
R2_SECRET_ACCESS_KEY=...
R2_BUCKET_NAME=...
R2_PUBLIC_URL=...
R2_ENDPOINT=...
```

---

Este fluxo é robusto e garante que as imagens sejam sempre contextuais e de alta qualidade. Se tiver qualquer dúvida, estou à disposição.
