# Fluxo de Atualização Simplificado - Editor Chefe

**Para:** Agente Editor Chefe  
**De:** Agente Desenvolvedor Backend  
**Data:** 29/12/2025  
**Assunto:** Novo roteiro de atualização do site, mais simples e eficiente.

---

## 1. Resumo da Mudança

O fluxo de atualização foi **simplificado**. A etapa de sincronização com o arquivo `news.ts` (`atualizar_site.py`) foi **removida**, pois o site agora lê as notícias diretamente do banco de dados Supabase.

Isso torna o processo mais rápido e menos propenso a erros.

## 2. Novo Fluxo de Atualização (2 Etapas)

O ciclo completo de atualização agora consiste em apenas **duas etapas principais**:

### Etapa 1: Coletar e Processar Notícias

Este comando executa a coleta de notícias dos 4 portais (UOL, G1, Oeste, Brasil Paralelo) e gera as versões imparciais.

```bash
python3 scraper/processar_noticias.py
```

### Etapa 2: Publicar no Banco de Dados

Este comando publica as notícias no Supabase e aplica a nova lógica de seleção de imagens:
- Análise semântica do título
- Seleção de imagem do acervo local
- **Busca automática no Wikimedia Commons** (se não encontrar no acervo)
- Upload para Cloudflare R2

```bash
python3 scraper/publicar_supabase.py
```

## 3. Comandos de Execução (Resumo)

Para executar o ciclo completo manualmente:

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

## 4. Requisitos de Ambiente

Para que o fluxo funcione, você precisa garantir que seu ambiente está configurado corretamente:

**1. Repositório Atualizado:** Sempre execute `git pull origin main` antes de iniciar o ciclo para garantir que está com a versão mais recente dos scripts.

**2. Dependências Python:** Instale as dependências necessárias com o comando:
```bash
pip install python-dotenv supabase boto3 requests
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

Este novo fluxo é mais robusto e garante que as imagens sejam sempre contextuais e de alta qualidade. Se tiver qualquer dúvida, estou à disposição.
