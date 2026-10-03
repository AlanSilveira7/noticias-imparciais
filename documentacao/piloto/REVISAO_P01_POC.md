# Revisão da P01 — preservar a governança, retirar o excesso

**Status:** parecer corretivo solicitado pelo proprietário em 30/09/2026, 22:13 -03; **P01 continua aceita e integrada** pela [PR #2](https://github.com/AlanSilveira7/noticias-imparciais/pull/2). A exceção para revisar P01, plano e P02 conjuntamente foi autorizada em 22:16 -03. Este arquivo não desfaz o aceite nem atribui implementação de P03 a ninguém.

## Entendimento do Diretor

O objetivo **não é certificar um produto pronto para grande audiência nesta rodada**. É provar que o Axia News consegue coletar, comparar, redigir, revisar, obter **aprovação específica do proprietário**, publicar no **piloto restrito** e oferecer um **site completo de leitura**, com notícias reais, contexto, imagens e afirmações rastreáveis. Não há notícia de incidente ou dado sensível que justifique transformar cada ação em auditoria de segurança. O lançamento público e o endurecimento de segurança pertencem a uma fase posterior, se o conceito for viável.

## O que a P01 acertou

A PR #2 deixou um ponto único no repositório para plano, progresso e fichas, com responsável, estado e decisão de aceite. Isso evita trabalhos paralelos sobre o mesmo arquivo e impede que o agente seguinte confunda PR aberto com ação concluída. O proprietário aceitou expressamente e a entrega está em `main`. **Não refazer P01** nem reescrever seu histórico.

## O que pesou e como a revisão corrige

| Excesso observado | Correção nesta proposta v1.3 |
|---|---|
| Fichas longas repetem várias páginas do plano e podem desviar o agente para testar muitos cenários periféricos antes do primeiro fluxo real. | As 23 fichas ficam curtas: ação, demonstração/aceite, leitura inicial e limites mínimos. O plano concentra a visão de ponta a ponta. |
| Toda divergência de conta/serviço era tratada como bloqueio geral, mesmo para trabalho local independente. | Só uma divergência **material à ação e ao resultado** bloqueia aquela etapa. O agente avança no que independe dela, registra a pendência e não afirma que o serviço remoto funciona sem ensaio. |
| Revisões de infraestrutura, RLS, mídia/cache e backup foram colocadas cedo como aceites do piloto. | Controles avançados vão para plano pós-P23; agora há apenas acesso restrito ao site, segredos fora do código, aprovação do proprietário e rastreabilidade do conteúdo. |
| O registro de progresso passou a exigir relatos extensos para cada passo. | Basta ação, status, PR/artefato, **um teste/demonstração relevante**, pendência real e decisão do proprietário. Preservar os 23 estados e as decisões históricas, sem novo formulário. |

## Veredito P01

**Concluída e útil como trilha leve, não como freio de desenvolvimento.** A revisão documental da governança entra na PR da proposta v1.3/P02 por exceção expressa; o aceite histórico da P01 **permanece**. A única regra temporal indispensável é: proprietário aciona/aceita uma ação por vez; o responsável consulta plano, progresso, ficha e estado do repo antes de editar; mostra teste pertinente e PR; não inicia a próxima sem ordem. O piloto **não** está concluído por causa da P01, e seu critério de sucesso continua a demonstração integral de P23.
