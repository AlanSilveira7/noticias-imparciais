# Progresso único — piloto Axia News

**Plano vigente até nova ratificação/merge:** v1.2.1, aceita em 30/09/2026 21:31 -03; consultar a versão preservada no [`main` do merge P01](https://github.com/AlanSilveira7/noticias-imparciais/blob/86d9351bcd3cf42797f9f7dd88badd0d1d071a74/documentacao/piloto/PLANO_GERAL.md), SHA-256 `558b7e0ba14d5fcc30e507488744983831d15916e47f3c6a74648b50c46e88e1`. **Nesta PR #3:** [v1.3.0 proposta](PLANO_GERAL.md), SHA-256 `1a83444d01590c9b0e7134c3a08869daad66869b3d8baab1ae2eeb811f3f38c1`, **ainda sem aceite**. P01 aceita/integrada; somente P02 acionada; P03 não iniciada.  
**Referência de partida:** `main` em `385828c4eae2e29854b879993dd6f1b6fe2b9001`, consultada antes de P01; checkout limpo, nenhum PR aberto naquele instante. Consultar novamente em **cada** acionamento.  
**Importante:** a PR #1/A01 de configuração R2 é um marco **legado** já integrado; não é P01 do piloto, não prova conclusão de ação futura. Marketing está fora deste piloto por decisão do proprietário.

## Quadro de ações

| ID | Estado | Responsável | Commit-base | Branch/PR/commit ou entrega | Testes e evidências | Decisão de aceite (quem/quando/link) | Bloqueios |
|---|---|---|---|---|---|---|---|
| P01 | aceita | Diretor | `385828c4` | [PR #2](https://github.com/AlanSilveira7/noticias-imparciais/pull/2), branch `piloto/p01-governanca-20260930` (verificar integração no link) | 27 documentos; 23 fichas e 23 linhas de progresso; links locais e escopo verificados; `git -c core.whitespace=-blank-at-eol diff --check` e checks da PR passaram | Proprietário, 30/09/2026 21:38 -03, na tarefa Manus `oL4cl7lhZdPwJCsjHza6zn`: “Ok, ação aceita, conclua a P01”; [transcrição identificada na PR](https://github.com/AlanSilveira7/noticias-imparciais/pull/2#issuecomment-5922348226) | —; confirmar PR integrada antes de P02 |
| P02 | entregue para revisão | Diretor | `86d9351b` | [PR #3](https://github.com/AlanSilveira7/noticias-imparciais/pull/3), branch `piloto/p02-arquitetura-20260930` | [A01–A06 propostas](DECISOES_ARQUITETURA.md) e [plano v1.3](PLANO_GERAL.md) com foco no POC; nenhuma alteração funcional; serviço remoto ainda não ensaiado | **PENDENTE — proprietário solicitou revisão conjunta em 22:13/22:16 -03, não aceitou plano v1.3 nem entrega P02** | Só decisão material do proprietário sobre esta proposta; testes remotos cabem a P07/P21/P23, não à P02 documental |
| P03 | pendente | Editor-Chefe | — (verificar no acionamento) | — | — | **PENDENTE** | Aguardar aceite das anteriores e acionamento expresso |
| P04 | pendente | Editor-Chefe | — (verificar no acionamento) | — | — | **PENDENTE** | Aguardar aceite das anteriores e acionamento expresso |
| P05 | pendente | Editor-Chefe | — (verificar no acionamento) | — | — | **PENDENTE** | Aguardar aceite das anteriores e acionamento expresso |
| P06 | pendente | Backend | — (verificar no acionamento) | — | — | **PENDENTE** | Aguardar aceite das anteriores e acionamento expresso |
| P07 | pendente | Backend | — (verificar no acionamento) | — | — | **PENDENTE** | Aguardar aceite das anteriores e acionamento expresso |
| P08 | pendente | Backend | — (verificar no acionamento) | — | — | **PENDENTE** | Aguardar aceite das anteriores e acionamento expresso |
| P09 | pendente | Frontend | — (verificar no acionamento) | — | — | **PENDENTE** | Aguardar aceite das anteriores e acionamento expresso |
| P10 | pendente | Backend | — (verificar no acionamento) | — | — | **PENDENTE** | Aguardar aceite das anteriores e acionamento expresso |
| P11 | pendente | Backend | — (verificar no acionamento) | — | — | **PENDENTE** | Aguardar aceite das anteriores e acionamento expresso |
| P12 | pendente | Backend | — (verificar no acionamento) | — | — | **PENDENTE** | Aguardar aceite das anteriores e acionamento expresso |
| P13 | pendente | Backend | — (verificar no acionamento) | — | — | **PENDENTE** | Aguardar aceite das anteriores e acionamento expresso |
| P14 | pendente | Backend | — (verificar no acionamento) | — | — | **PENDENTE** | Aguardar aceite das anteriores e acionamento expresso |
| P15 | pendente | Backend | — (verificar no acionamento) | — | — | **PENDENTE** | Aguardar aceite das anteriores e acionamento expresso |
| P16 | pendente | Backend | — (verificar no acionamento) | — | — | **PENDENTE** | Aguardar aceite das anteriores e acionamento expresso |
| P17 | pendente | Frontend | — (verificar no acionamento) | — | — | **PENDENTE** | Aguardar aceite das anteriores e acionamento expresso |
| P18 | pendente | Frontend | — (verificar no acionamento) | — | — | **PENDENTE** | Aguardar aceite das anteriores e acionamento expresso |
| P19 | pendente | Frontend | — (verificar no acionamento) | — | — | **PENDENTE** | Aguardar aceite das anteriores e acionamento expresso |
| P20 | pendente | Frontend | — (verificar no acionamento) | — | — | **PENDENTE** | Aguardar aceite das anteriores e acionamento expresso |
| P21 | pendente | Backend | — (verificar no acionamento) | — | — | **PENDENTE** | Aguardar aceite das anteriores e acionamento expresso |
| P22 | pendente | Editor-Chefe | — (verificar no acionamento) | — | — | **PENDENTE** | Aguardar aceite das anteriores e acionamento expresso |
| P23 | pendente | Diretor | — (verificar no acionamento) | — | — | **PENDENTE** | Aguardar aceite das anteriores e acionamento expresso |

## Estados e regra de sequência

- `pendente`: não acionada; `em execução`: única ação acionada e em andamento; `entregue para revisão`: material disponível em PR/relatório, **sem aceite**; `bloqueada`: dependência ou pendência impeditiva; `aceita`: decisão explícita do proprietário **e** entrega integrada/reconciliada; `reaberta`: aceite anterior submetido a revisão, impedindo dependentes.
- Só iniciar P(n+1) após a ação Pn e todas as anteriores constarem `aceita` com decisão do proprietário **e integração das entregas aplicáveis**, e após novo pedido individual do proprietário. Não inferir aceite de número sequencial, PR aberto, teste verde ou merge isolado.
- Em caso de atraso/divergência deste registro, **parar e reconciliar** antes de nova ação. Não apagar histórico: anotar abaixo revisões, decisões, evidências e correções. O proprietário decide integração e aceite; o Diretor mantém o registro para P01 e, nas próximas ações, o responsável designado pelo proprietário registra a evidência com revisão da decisão.

## Registro de aceite enxuto (proposta v1.3)

O proprietário examina entrega/PR, **aceita expressamente ou pede ajuste**; o responsável registra em uma atualização simples a decisão, o link e a integração, sem segunda rodada ritual de assinatura. A ação seguinte continua dependendo de novo pedido individual. O histórico P01 abaixo comprova sua aprovação/merge e **não é reaberto** por esta simplificação; ver [parecer P01](REVISAO_P01_POC.md).

## Histórico de decisões e entregas

- **30/09/2026, 21:31 -03 — proprietário:** “Plano aceito, vamos começar os trabalhos [...] P01 [...]”. Escopo: versão 1.2.1; **não** é aceite da entrega P01. [Índice de decisões](DECISOES.md).
- **30/09/2026 — preflight P01 (Diretor):** `main` local/remoto em `385828c4`, checkout limpo, PRs abertos: nenhum, documentos `documentacao/piloto/` ausentes. A versão candidata aceita antes de versionamento tinha SHA-256 `9503f9f504fd43353d42f515f0a5d48a01b2d4cce35c05143e1edc2c6d8feaaa`; nesta cópia canônica foram atualizados **somente os dois campos de cabeçalho e a nota final** que ainda tratavam o plano como pendente de aprovação.
- **30/09/2026 — entrega P01 (Diretor):** [PR #2](https://github.com/AlanSilveira7/noticias-imparciais/pull/2) aberta com plano, progresso, índice e fichas P01–P23; testes estruturais e links locais passaram. **Entregue para revisão; não aceita, não integrada; P02 não acionada.**
- **30/09/2026, 21:38 -03 — aceite P01 (proprietário):** “Ok, ação aceita, conclua a P01, para que eu possa seguir com as demais ações.” [Transcrição operacional identificada na PR #2](https://github.com/AlanSilveira7/noticias-imparciais/pull/2#issuecomment-5922348226). O Diretor registra o aceite nesta mesma ação e integra a PR; **nenhuma autorização para iniciar P02 foi dada**.
- **30/09/2026, 21:41 -03 — acionamento P02 (proprietário):** P01 declarada concluída; pedido individual para fechar arquitetura privada, responsabilidades e contratos entre componentes. Preflight: `main`/PR #2 em `86d9351b`, branch limpa, nenhum PR aberto; P01 aceita. O proprietário autorizou em 21:48 -03 seguir apesar dos redeploys automáticos do legado, sem autorizar exposição do piloto. A leitura do projeto Vercel via conector retornou `403` por escopo; a P02 documenta essa limitação e reserva validação real para P07. **P03 não acionada.**
- **30/09/2026 — entrega P02 (Diretor):** [PR #3](https://github.com/AlanSilveira7/noticias-imparciais/pull/3) com decisões A01–A10 e limites de evidência. **Entregue para revisão; sem ratificação ou aceite; P03 não acionada.**
- **30/09/2026, 22:03 -03 — revisão P02 solicitada (proprietário):** questionou a necessidade de criar outro projeto Vercel e propôs **reaproveitar o existente e ajustá-lo**. O Diretor acata a direção, revê a PR #3 para reutilizar a hospedagem atual, mantém isolamento de dados e gates de privacidade. **Não houve aceite da P02 nem acionamento de P03.**
- **30/09/2026, 22:13/22:16 -03 — nova diretriz e exceção documental (proprietário):** priorizar a demonstração do piloto funcional, diferir controles avançados de segurança/escala; preservar site remoto restrito, aprovação específica antes de publicar e afirmações rastreáveis. Autorizou revisão conjunta de **plano, P01 já integrada e P02 ainda aberta**, sem P03. O Diretor preparou proposta v1.3.0, [parecer de P01](REVISAO_P01_POC.md) e [P02 enxuta](DECISOES_ARQUITETURA.md) na PR #3. **A versão e a P02 ainda aguardam ratificação; P01 continua aceita.**
