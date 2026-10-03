# Piloto Axia News — ponto de entrada dos agentes

**Nesta PR: [plano v1.3.1 proposto após auditoria](PLANO_GERAL.md), ainda não ratificado.** Em `main`, v1.2.1 continua vigente até o proprietário aceitar e integrar esta revisão. [P01 está aceita](PROGRESSO.md); [P02 está em revisão](DECISOES_ARQUITETURA.md); **P03 não foi acionada**. Nunca tratar uma PR aberta ou uma ficha nova como autorização para executar a ação seguinte.

## Antes de cada ação acionada pelo proprietário

1. Ler a **versão efetivamente vigente em `main`** do [plano](PLANO_GERAL.md), o [progresso](PROGRESSO.md) e a [ficha Pnn](ACOES/) da ação recebida. Ler contratos pertinentes, quando existirem, sem transformar documentação histórica em ordem.
2. Conferir `main`, `git status`, branches/PRs e o aceite da ação anterior. Tratar **divergência material para sua entrega**, sem refazer auditoria global nem pedir acesso a serviços que sua ação não usa.
3. Executar **só a ação atribuída**. Código em branch/PR; mostrar resultado/teste pertinente e limitação concreta; o proprietário aceita ou pede ajuste e só ele aciona a seguinte.

## Prioridade do POC

Provar coleta agendada de **duas fontes independentes**, proposta automática de agrupamento/comparação e rascunho gerado, com revisão humana, afirmações rastreáveis, imagem de uso permitido e **aprovação específica do proprietário** antes da publicação **somente no site remoto restrito**. Rodada agendada vazia não prova a cadeia. O proprietário deve poder ler notícias completas como leitor comum; Home, busca, editorias habilitadas, cartões, artigo, contexto e imagens **funcionam**, não são mock. **Marketing e lançamento público ficam fora.** Controles avançados de RLS, proxy de mídia, cache, backup integral e escala passam a um plano posterior se o conceito for viável.

**Trilha de auditoria:** [plano](PLANO_GERAL.md) · [parecer P01 sem reabrir aceite](REVISAO_P01_POC.md) · [decisões P02 simplificadas](DECISOES_ARQUITETURA.md) · [índice de decisões](DECISOES.md) · [fichas P01–P23](ACOES/) · [progresso](PROGRESSO.md).
