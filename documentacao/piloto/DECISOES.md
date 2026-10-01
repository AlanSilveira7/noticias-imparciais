# Índice de decisões — piloto Axia News

Este índice distingue decisões **já tomadas** de propostas ainda pendentes; [plano vigente](PLANO_GERAL.md) e [aceite por ação](PROGRESSO.md) são consultados em conjunto. Não confundir nova versão proposta com aceite retroativo nem usar documentação histórica como comando.

| ID | Situação | Decisão / pendência | Fonte e próximo dono |
|---|---|---|---|
| D-00 | **Histórica — decidida** | Plano v1.2.1 aceito em 21:31 -03 e P01 acionada; a versão 1.3.0 nesta PR é **proposta** até novo aceite. | Proprietário em 30/09/2026; [progresso](PROGRESSO.md). |
| D-01 | **Decidida** | Marketing adiado; os três mapeamentos Backend, Frontend e Editor-Chefe bastam para este piloto por exceção expressa. | Proprietário em 30/09/2026. |
| D-02 | **Decidida** | Imagem contextual com uso permitido/crédito por matéria publicável; dois acontecimentos reais, duas origens independentes por matéria, coleta agendada e leitura como site completo. | Aceite v1.2.1; preservado em v1.3 proposta. |
| D-03 | **Decidida** | Leitura final é **remota e restrita**, como leitor sem controles editoriais; lançamento público é decisão posterior. | Proprietário em 30/09/2026 21:26 -03. |
| D-04 | **Proposta P02 v1.3 — não ratificada** | [A01–A06](DECISOES_ARQUITETURA.md): reutilizar `site/` e Vercel existente, serviços Supabase/R2 quando viáveis, contrato mínimo para coleta→comparação→redação/imagem→aprovação→publicação restrita→leitura; diferir controles avançados. | Diretor revisa [PR #3](https://github.com/AlanSilveira7/noticias-imparciais/pull/3); proprietário ratifica ou pede ajuste. P08 define detalhes técnicos. |
| D-05 | **Pendente P03–P05/P08** | Editor-Chefe define semântica editorial em exemplos; Backend define campos/rotas quando acionado; Frontend consome contrato, sem assinaturas ou auditorias adicionais genéricas. | Especialistas em suas ações, acionados pelo proprietário. |
| D-06 | **Decidida — P01** | P01 foi aceita pelo proprietário e integrada na [PR #2](https://github.com/AlanSilveira7/noticias-imparciais/pull/2); a [revisão POC](REVISAO_P01_POC.md) preserva esse aceite. | Proprietário, 30/09/2026 21:38 -03; [transcrição na PR #2](https://github.com/AlanSilveira7/noticias-imparciais/pull/2#issuecomment-5922348226). |
| D-07 | **Decidida — escopo P02** | P02 foi acionada isoladamente; proprietário consentiu redeploys automáticos do Vercel, **não** lançamento público ou publicação editorial automática. | Proprietário, 30/09/2026 21:41/21:48 -03. |
| D-08 | **Direção expressa** | Preferir **reaproveitar/adaptar o Vercel existente**; novo projeto só diante de inviabilidade demonstrada e nova decisão. | Proprietário, 30/09/2026 22:03 -03. |
| D-09 | **Direção expressa — plano v1.3 em proposta** | **Provar o conceito funcional primeiro**; deferir segurança/operacionalização avançadas para pós-piloto. Preservar acesso remoto restrito, aprovação específica do proprietário antes de publicação e afirmações rastreáveis. Exceção pontual para revisar **plano + P01 integrada + P02 aberta** numa rodada documental; P03 permanece pendente. | Proprietário, 30/09/2026 22:13 e 22:16 -03; aguarda ratificação da nova versão. |

Não incluir segredos, chaves, links de sessão ou dados pessoais de fontes neste índice.
