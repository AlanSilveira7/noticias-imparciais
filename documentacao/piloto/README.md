# Piloto Axia News — ponto de entrada dos agentes

**[Plano v1.3.1 vigente](PLANO_GERAL.md)**, aceito pelo proprietário em 03/10/2026 e integrado pela [PR #3](https://github.com/AlanSilveira7/noticias-imparciais/pull/3). [P01 e P02 estão aceitas](PROGRESSO.md); **P03 não foi acionada**. O aceite de uma ação não autoriza a seguinte: cada especialista aguarda novo pedido individual do proprietário.

## Antes de cada ação acionada pelo proprietário

1. Ler a **versão efetivamente vigente em `main`** do [plano](PLANO_GERAL.md), o [progresso](PROGRESSO.md) e a [ficha Pnn](ACOES/) da ação recebida. Ler contratos pertinentes, quando existirem, sem transformar documentação histórica em ordem.
2. Conferir `main`, `git status`, branches/PRs e o aceite da ação anterior. Tratar **divergência material para sua entrega**, sem refazer auditoria global nem pedir acesso a serviços que sua ação não usa.
3. Executar **só a ação atribuída**. Código em branch/PR; mostrar resultado/teste pertinente e limitação concreta; o proprietário aceita ou pede ajuste e só ele aciona a seguinte.

## Prioridade do POC

Provar coleta agendada de **duas fontes independentes**, proposta automática de agrupamento/comparação e rascunho gerado, com revisão humana, afirmações rastreáveis, imagem de uso permitido e **aprovação específica do proprietário** antes da publicação **somente no site remoto restrito**. Rodada agendada vazia não prova a cadeia. O proprietário deve poder ler notícias completas como leitor comum; Home, busca, editorias habilitadas, cartões, artigo, contexto e imagens **funcionam**, não são mock. **Marketing e lançamento público ficam fora.** Controles avançados de RLS, proxy de mídia, cache, backup integral e escala passam a um plano posterior se o conceito for viável.

**Trilha de auditoria:** [plano](PLANO_GERAL.md) · [parecer P01 sem reabrir aceite](REVISAO_P01_POC.md) · [decisões P02 simplificadas](DECISOES_ARQUITETURA.md) · [índice de decisões](DECISOES.md) · [fichas P01–P23](ACOES/) · [progresso](PROGRESSO.md).
