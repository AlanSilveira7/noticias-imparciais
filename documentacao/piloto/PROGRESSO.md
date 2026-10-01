# Progresso único — piloto Axia News

**Plano vigente:** [v1.2.1](PLANO_GERAL.md), aceito pelo proprietário na conversa da tarefa Manus `oL4cl7lhZdPwJCsjHza6zn` em 30/09/2026, 21:31 -03; autorização **somente da P01**. A cópia versionada do plano tem SHA-256 `558b7e0ba14d5fcc30e507488744983831d15916e47f3c6a74648b50c46e88e1`.  
**Referência de partida:** `main` em `385828c4eae2e29854b879993dd6f1b6fe2b9001`, consultada antes de P01; checkout limpo, nenhum PR aberto naquele instante. Consultar novamente em **cada** acionamento.  
**Importante:** a PR #1/A01 de configuração R2 é um marco **legado** já integrado; não é P01 do piloto, não prova conclusão de ação futura. Marketing está fora deste piloto por decisão do proprietário.

## Quadro de ações

| ID | Estado | Responsável | Commit-base | Branch/PR/commit ou entrega | Testes e evidências | Decisão de aceite (quem/quando/link) | Bloqueios |
|---|---|---|---|---|---|---|---|
| P01 | aceita | Diretor | `385828c4` | [PR #2](https://github.com/AlanSilveira7/noticias-imparciais/pull/2), branch `piloto/p01-governanca-20260930` (verificar integração no link) | 27 documentos; 23 fichas e 23 linhas de progresso; links locais e escopo verificados; `git -c core.whitespace=-blank-at-eol diff --check` e checks da PR passaram | Proprietário, 30/09/2026 21:38 -03, na tarefa Manus `oL4cl7lhZdPwJCsjHza6zn`: “Ok, ação aceita, conclua a P01”; [transcrição identificada na PR](https://github.com/AlanSilveira7/noticias-imparciais/pull/2#issuecomment-5922348226) | —; confirmar PR integrada antes de P02 |
| P02 | pendente | Diretor | — (verificar no acionamento) | — | — | **PENDENTE** | Aguardar aceite das anteriores e acionamento expresso |
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

## Procedimento operacional para P01 (sem ação extra implícita)

1. O Diretor entrega PR de P01 com esta linha em `entregue para revisão`, links e resultados. O proprietário examina o diff e, se concordar, registra no PR decisão **explícita** de aceitar P01, com data/identidade. Se pedir correção, permanece em revisão.
2. O Diretor, **ainda dentro do escopo P01**, atualiza esta linha para `aceita`, citando o comentário de aceite e o PR/commit e preservando o histórico da decisão. Pode fazê-lo na mesma PR antes do merge, caso em que o proprietário revê o último diff antes de integrar; ou em PR documental vinculada à P01 após merge, também sujeita à revisão do proprietário.
3. Conferir que `main` contém plano/fichas/progresso e que o registro de P01 referencia a aprovação explícita e o merge. Enquanto qualquer elo faltar, P01 não terminou. Somente depois o proprietário poderá **acionar P02 separadamente**.

## Histórico de decisões e entregas

- **30/09/2026, 21:31 -03 — proprietário:** “Plano aceito, vamos começar os trabalhos [...] P01 [...]”. Escopo: versão 1.2.1; **não** é aceite da entrega P01. [Índice de decisões](DECISOES.md).
- **30/09/2026 — preflight P01 (Diretor):** `main` local/remoto em `385828c4`, checkout limpo, PRs abertos: nenhum, documentos `documentacao/piloto/` ausentes. A versão candidata aceita antes de versionamento tinha SHA-256 `9503f9f504fd43353d42f515f0a5d48a01b2d4cce35c05143e1edc2c6d8feaaa`; nesta cópia canônica foram atualizados **somente os dois campos de cabeçalho e a nota final** que ainda tratavam o plano como pendente de aprovação.
- **30/09/2026 — entrega P01 (Diretor):** [PR #2](https://github.com/AlanSilveira7/noticias-imparciais/pull/2) aberta com plano, progresso, índice e fichas P01–P23; testes estruturais e links locais passaram. **Entregue para revisão; não aceita, não integrada; P02 não acionada.**
- **30/09/2026, 21:38 -03 — aceite P01 (proprietário):** “Ok, ação aceita, conclua a P01, para que eu possa seguir com as demais ações.” [Transcrição operacional identificada na PR #2](https://github.com/AlanSilveira7/noticias-imparciais/pull/2#issuecomment-5922348226). O Diretor registra o aceite nesta mesma ação e integra a PR; **nenhuma autorização para iniciar P02 foi dada**.
