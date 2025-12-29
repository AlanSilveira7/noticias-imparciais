# Notícias Imparciais

Portal de notícias que apresenta informações de forma equilibrada, coletando e analisando conteúdo de múltiplas fontes com diferentes perspectivas editoriais.

## Estrutura do Projeto

```
noticias-imparciais/
├── acervo_temas/       # Banco de imagens em HD organizadas por categoria
├── documentacao/       # Documentação técnica e de negócio
├── scraper/            # Scripts Python para coleta, análise e publicação
├── site/               # Frontend React hospedado na Vercel
└── assets/             # Recursos de identidade visual
```

## Tecnologias

| Componente | Tecnologia |
|:---|:---|
| Frontend | React + TypeScript + TailwindCSS |
| Backend | Python 3.11 |
| Banco de Dados | Supabase (PostgreSQL) |
| Armazenamento de Imagens | Cloudflare R2 |
| Hospedagem | Vercel |

## Fluxo de Atualização

O ciclo de atualização de notícias segue três etapas principais:

1. **Coleta** (`scraper_browser.py`) - Coleta notícias dos portais UOL, G1/Globo, Revista Oeste e Brasil Paralelo
2. **Processamento** (`processar_noticias.py`) - Analisa viés e gera versões imparciais das notícias
3. **Publicação** (`publicar_supabase.py`) - Publica no Supabase com seleção inteligente de imagens

## Documentação

A documentação completa está disponível na pasta `documentacao/`:

| Documento | Descrição |
|:---|:---|
| CONTEXTO_PROJETO_NOTICIAS_IMPARCIAIS.md | Visão geral do projeto |
| INSTRUCOES_ATUALIZACAO.md | Como executar o ciclo de atualização |
| CONFIGURACAO_AGENTE.md | Configuração para agentes de IA |
| AVALIACAO_ESCALABILIDADE.md | Análise de performance e segurança |

## Configuração

O projeto requer um arquivo `.env` na raiz com as seguintes variáveis:

```
SUPABASE_URL=
SUPABASE_ANON_KEY=
SUPABASE_SERVICE_KEY=
R2_ACCOUNT_ID=
R2_ACCESS_KEY_ID=
R2_SECRET_ACCESS_KEY=
R2_BUCKET_NAME=
R2_PUBLIC_URL=
R2_ENDPOINT=
```

## Licença

Projeto privado - Todos os direitos reservados.
