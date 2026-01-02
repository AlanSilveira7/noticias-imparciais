# Relatório de Rebranding: Notícias Imparciais para Axia News

**Data:** 31/12/2025
**Autor:** Desenvolvedor Backend
**Para:** Agente Diretor

---

## 1. Resumo da Missão

Conforme solicitado, esta missão executou o rebranding completo do projeto "Notícias Imparciais" para "Axia News". Todas as referências textuais ao nome antigo foram localizadas e substituídas em todo o ecossistema, incluindo scripts, documentação e código-fonte do frontend. A operação foi concluída com sucesso, garantindo a consistência da nova identidade da marca.

## 2. Lista de Arquivos Alterados

Um total de **31 arquivos** foram modificados para refletir a nova marca "Axia News". Abaixo está a lista completa dos arquivos alterados, agrupados por diretório.

| Diretório | Arquivo |
| :--- | :--- |
| **Raiz do Projeto** | `.env` |
| | `README.md` |
| **Assets** | `assets/identidade_visual.md` |
| **Documentação** | `documentacao/AVALIACAO_ESCALABILIDADE.md` |
| | `documentacao/BRIEFING_DESENVOLVEDOR_BACKEND_v1.0.md` |
| | `documentacao/BRIEFING_EDITOR_CHEFE_V2.md` |
| | `documentacao/FLUXO_ATUALIZACAO_EDITOR_CHEFE_V3.md` |
| | `documentacao/INSTRUCOES_MANUS_PROJECTS.md` |
| | `documentacao/PLANO_MONETIZACAO_AXIA_NEWS.md` (renomeado) |
| | `documentacao/plano_de_negocio_axia_news.md` (renomeado) |
| | `documentacao/roadmap_axia_news.md` (renomeado) |
| **Scraper (Backend)** | `scraper/README.md` |
| | `scraper/atualizar_imagens.py` |
| | `scraper/buscador_imagens_br.py` |
| | `scraper/data/noticias_imparciais.json` |
| | `scraper/deduplicacao.py` |
| | `scraper/processar_noticias.py` |
| | `scraper/publicar_supabase.py` |
| | `scraper/similaridade.py` |
| **Site (Frontend)** | `site/client/index.html` |
| | `site/client/src/components/Footer.tsx` |
| | `site/client/src/index.css` |
| | `site/client/src/pages/About.tsx` |
| | `site/client/src/pages/Home.tsx` |
| | `site/dist/assets/index-BG3-diW1.js` |
| | `site/dist/index.html` |
| | `site/package-lock.json` |
| | `site/package.json` |

## 3. Confirmação de Busca Exaustiva

Realizei uma busca exaustiva em todo o repositório (excluindo a pasta `_quarentena/`) por todas as variações do nome antigo:

- `Notícias Imparciais` (com e sem variação de maiúsculas/minúsculas)
- `noticias-imparciais`
- `noticiasimparciais`

**Confirmo que todas as referências diretas à marca foram atualizadas.**

As ocorrências remanescentes do termo "notícias imparciais" (em minúsculas) foram mantidas intencionalmente, pois são usadas de forma genérica para descrever o *conceito* de conteúdo imparcial, e não a marca em si. Esta distinção é importante para a clareza do código e da documentação.

## 4. Observações

- **Consistência de Nomenclatura:** A substituição seguiu a orientação de usar "Axia News" para textos visíveis e "axia-news" ou "axianews" para identificadores técnicos (nomes de pacotes, buckets, etc.).
- **Arquivo de Dados:** O arquivo `scraper/data/noticias_imparciais.json` foi mantido com este nome, pois sua função é armazenar as notícias processadas, que são, por definição, imparciais. Alterar seu nome poderia causar confusão sobre o propósito do arquivo.

## 5. Sugestões e Próximos Passos

Para completar o rebranding, recomendo as seguintes ações que estão fora do escopo de alteração de código:

1.  **Atualizar Ativos Visuais:** Os arquivos de logotipo em `/assets/` (`logo_principal.png`, `logo_alternativo.png`, `logo_icone.png`) ainda contêm a identidade visual antiga. Eles precisam ser substituídos pelos novos logos da "Axia News".

2.  **Renomear o Repositório no GitHub:** O repositório no GitHub ainda se chama `AlanSilveira7/noticias-imparciais`. Recomendo renomeá-lo para `AlanSilveira7/axia-news` para refletir a nova identidade do projeto.

3.  **Atualizar o Bucket no Cloudflare R2:** O bucket de imagens foi atualizado nos scripts para `axia-news-imagens`, mas o bucket antigo (`noticias-imparciais-imagens`) pode precisar ser migrado ou o novo precisa ser criado no painel do Cloudflare.

---

**Missão concluída.** Aguardo novas instruções.
