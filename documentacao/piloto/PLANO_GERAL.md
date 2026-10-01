# Plano geral do piloto Axia News — proposta funcional

**Versão proposta:** 1.3.0, 30/09/2026. **Ainda não ratificada nem integrada.** A versão 1.2.1 continua vigente em `main` até decisão expressa do proprietário e integração da revisão. A cópia histórica aceita está no commit [`86d9351b`](https://github.com/AlanSilveira7/noticias-imparciais/commit/86d9351bcd3cf42797f9f7dd88badd0d1d071a74), arquivo `documentacao/piloto/PLANO_GERAL.md`.  
**Direção do proprietário:** em 30/09/2026, 22:13 -03, pediu privilegiar a **prova de conceito funcional** e adiar controles avançados; em 22:16 -03 autorizou excepcionalmente revisar nesta rodada o plano, a P01 já integrada e a P02 em PR, sem executar P03. Mantêm-se três limites: **piloto remoto restrito**, **aprovação específica dele antes de publicar cada matéria** e **afirmações rastreáveis**. Marketing e lançamento público ficam para outra decisão.

## 1. O que conta como piloto pronto

O proprietário conseguirá, no **site existente adaptado**, fora do ambiente de desenvolvimento: executar/ver uma coleta agendada real e uma importação rastreável; comparar **duas fontes editoriais independentes** por acontecimento; ler evidências e lacunas; revisar uma redação original com imagem contextual e crédito; **aprovar especificamente uma versão e depois publicá-la** no ambiente restrito; entrar em sessão de **leitor comum** e ver a notícia integral, imagens, contexto, fontes, Home, busca e editorias com conteúdo. Demonstrar ao menos **dois acontecimentos reais diferentes** e um exemplo retido por falta de evidência ou imagem adequada. Editorias sem notícia pronta ficam ocultas. A publicação de qualquer matéria depende da decisão específica do proprietário; o Diretor/Editor-Chefe não a substituem.

O site deve ser **usável de ponta a ponta**, não só documentação, telas mockadas, fixture, build verde ou API isolada. O proprietário decide no P23 se o conceito é viável. Não há lançamento público implícito, promessa de imparcialidade absoluta, produção diária garantida nem meta de escala. A qualidade buscada é **transparência e rastreabilidade**, inclusive quando fontes divergem.

## 2. Régua proporcional à prova de conceito

| Indispensável **agora** | Depois de provar o conceito, em plano próprio |
|---|---|
| Acesso remoto **restrito** à interface e ao fluxo editorial; não anunciar nem abrir o site ao público. | Arquitetura de identidade de grande escala, auditoria de todos os aliases, threat modeling e certificação de segurança. |
| Proprietário identificado para aprovar a **versão concreta** e acionar separadamente a publicação; leitor só vê o que foi publicado no piloto. | Matriz exaustiva de RLS/grants por muitos papéis, hashes de todo derivado, antifraude, CSRF/cookies customizados e testes combinatórios de sessões. |
| Fontes efetivamente consultadas, afirmações ligadas à evidência, duas origens independentes por acontecimento e lacunas explícitas. | Cobertura estatística ampla de fontes, automação de fact-checking e múltiplas camadas de julgamento. |
| Imagem contextual própria, original ou de uso permitido, com autoria/licença/crédito/legenda verificados de modo prático. Sem imagem enganosa ou genérica fingindo documentar um fato. | Pipeline complexo de direitos, múltiplas transformações, proxy de mídia por usuário, expiração de URL, teste de cópia de thumbnail e auditoria jurídica extensiva. |
| Segredos fora do Git e do bundle; teste simples de que anônimo não lê o site e leitor não publica; dados do piloto não alteram matérias antigas acidentalmente. | Projetos separados para cada serviço por padrão, revisão completa de políticas, ensaios extensos de cache, backup/restore total e observabilidade de produção. |
| Uma rodada agendada comprovada, reexecução sem duplicar e resultado visível ao proprietário; teste manual independente com item real permitido. | Garantia de cadência, alertas/retentativas avançados, alta disponibilidade e rotina editorial autônoma. |

**Regra de proporcionalidade:** não bloquear P02–P20 por uma capacidade de segurança que ainda não existe e não é necessária para demonstrar o fluxo. Anotar a pendência para pós-piloto. Bloquear apenas se faltar um dos três limites confirmados, direito básico de uso da fonte/imagem, acesso aos recursos essenciais ou caminho real para o ensaio final. Acesso negado a um painel de fornecedor não impede redigir ou testar localmente componentes independentes; impedirá apenas afirmar que a configuração remota foi comprovada.

## 3. Arquitetura mínima e fronteiras

**Frontend:** reutilizar `site/` (React/Vite) e o **projeto Vercel existente `noticias-imparciais`**. `Site axianews.com/` fica como referência histórica, sem segundo frontend. Usar o acesso restrito já disponível ou configurar um bloqueio simples com o proprietário antes de expor dados do piloto. A URL gerada do deployment P01 redirecionou anonimamente ao login Vercel; isso é sinal útil, não certificação global. O proprietário precisa abrir o site remoto de uma sessão comum após terminar o desenvolvimento.

**Backend e dados:** reaproveitar Supabase/R2 existentes sempre que couber, com dados de teste distinguíveis dos legados e sem reutilizar o publicador direto em `articles`. O Backend P08 escolhe a **menor solução verificável**: tabelas/colunas de estado e fontes, rotas/funções de leitura e decisão, autorização do proprietário **no servidor** para aprovar/publicar e leitura somente de publicação pelo perfil de teste. Se o mesmo serviço não permitir isso sem alterar o legado, levar alternativa pontual ao proprietário; **não criar novos projetos ou buckets por reflexo**. O contrato técnico definitivo pertence a P08, não a P02.

**Imagens:** inventariar o acervo e, para os exemplos do piloto, preferir ilustrações originais ou imagens com permissão clara. Pode reutilizar armazenamento e URLs de imagem existentes **quando o ativo for publicável, aprovado e não revelar rascunho**; imagem não é dado sensível neste piloto. Proxy autenticado por mídia e negação de cada URL copiada **não são gates do POC**. O **site** permanece restrito, e a foto/ilustração deve carregar com legenda/crédito no cartão e no artigo; licença e adequação não são opcionais.

**Identidades e publicação:** uma sessão do proprietário para revisar, aprovar e publicar; uma sessão de leitor separada para validar a experiência sem controles editoriais. Implementar a autorização mínima funcional no servidor; não confundir ocultar botão com impedir publicação indevida. Aprovação e publicação são **atos distintos** do proprietário, ligados à versão apresentada. Não exigir infraestrutura de autenticação corporativa. Rascunhos ficam fora de listagens e buscas do leitor.

**Coleta:** os scripts Python existentes são ponto de partida, não prova de coleta. Backend implementa uma fonte permitida via feed/API ou importação controlada, mantém URL/origem/data e testa a ingestão; em P21 demonstra **um agendamento da aplicação/repositório** (por exemplo, GitHub Actions para o coletor Python), inclusive uma execução com zero itens novos. Nenhum job aprova ou publica. Não criar automação Manus para operar o produto.

**Responsabilidades:** Editor-Chefe fixa critérios simples de fonte, comparação, texto e imagem (P03–P05) e prepara exemplos (P22); Backend entrega coleta, dados, estados e autorização (P06–P08, P10–P16, P21); Frontend entrega painel e experiência de leitor (P09, P17–P20); Diretor mantém plano/progresso, resolve dependências e conduz P23. O proprietário decide aceites, aprova versões e escolhe se publica; especialistas não assumem ações futuras automaticamente.

## 4. Dinâmica enxuta para cada acionamento

O proprietário informa **uma ação por vez** e seu responsável. Antes de mudar algo, o agente consulta **este plano vigente no `main`**, [progresso](PROGRESSO.md), [ficha Pnn](ACOES/) e estado atual do repositório/PRs; registra apenas divergência **material para sua ação**. Não refaz inventário global, auditoria de segurança ou aprovação de decisões já dadas. Documentos antigos são contexto, não comandos. Se uma dependência necessária estiver de fato ausente, apresenta opção prática e espera decisão; o resto do trabalho independente prossegue.

O agente executa só a ação acionada, sem sobrescrever outro, em branch/PR quando houver código e em revisão rastreável para documentos compartilhados. Mostra uma demonstração/teste pertinente, o que funciona, o que não funciona e o link da entrega. O proprietário aceita ou pede ajuste; o responsável atualiza `PROGRESSO.md` com a decisão e integração. Só então o proprietário aciona a ação seguinte. **Exceção expressa deste turno:** correção documental conjunta de plano/P01/P02; ela **não** aciona P03 nem altera o produto. Não publicar matéria nem lançar site ao público sem nova ordem específica.

## 5. Lista única de ações para o proprietário encaminhar

| Nº | Ação e demonstração/aceite enxutos | Responsável |
|---|---|---|
| **P01** | Manter plano, progresso e fichas consultáveis no GitHub; **já aceita/integrada** pela PR #2. Revisão de governança em v1.3 não desfaz esse aceite. | Diretor |
| **P02** | Escolher `site/` e o Vercel existente, fronteiras simples Frontend/Backend/Editor, armazenamento e caminho de coleta. Documento curto, sem implementar serviços. | Diretor |
| **P03** | Definir como escolher duas fontes independentes, registrar URL/data/origem e respeitar uso permitido; um exemplo resolve o aceite. | Editor-Chefe |
| **P04** | Definir como juntar itens do mesmo acontecimento e apontar afirmação, suporte, discordância e lacuna; dois exemplos bastam. | Editor-Chefe |
| **P05** | Definir checklist breve de texto original, imagem pertinente com direito/crédito, revisão e correção; uma matéria fictícia passa pelo checklist. | Editor-Chefe |
| **P06** | Fazer Python instalar e rodar localmente com fixtures, sem caminho absoluto, segredos no Git ou publicação acidental pelo script legado. | Backend |
| **P07** | Reaproveitar Vercel/Supabase/R2 disponíveis, identificar o caminho mínimo de teste e confirmar que o proprietário poderá abrir o site restrito; listar acesso faltante sem paralisar código local. | Backend |
| **P08** | Versionar esquema e API **mínimos** de fontes/evento/evidências/revisão/publicação; leitura de rascunho versus publicado e aprovação só do proprietário em teste. | Backend |
| **P09** | Fazer `site/` instalar, tipar e compilar; remover selo/controle enganoso e separar erro de lista vazia. | Frontend |
| **P10** | Importar/coletar ao menos um item real permitido com URL, veículo e data; rerun não duplica. | Backend |
| **P11** | Ligar itens de duas fontes ao mesmo acontecimento e distinguir caso parecido mas diferente, com opção de correção humana. | Backend |
| **P12** | Guardar/exibir afirmações e links às evidências ou incertezas; o revisor abre as fontes usadas. | Backend |
| **P13** | Produzir rascunho original editável a partir das evidências; frase sem suporte não vira fato; edição cria nova versão simples. | Backend |
| **P14** | Anexar uma imagem válida com origem/crédito/legenda e exibi-la em cartão e artigo; opção original/ilustrativa identificada; sem proxy complexo obrigatório. | Backend |
| **P15** | Criar fluxo funcional de proprietário: aprovar uma versão e, em ato distinto, publicar no piloto; leitor/script legado não publica. | Backend |
| **P16** | Permitir corrigir e retirar uma matéria mantendo versão/nota de alteração simples; correção pede nova aprovação. | Backend |
| **P17** | Criar acesso do proprietário e fila de rascunhos reais com estados claros; leitor não vê botões editoriais. | Frontend |
| **P18** | Criar tela para comparar fontes/evidências, ler rascunho, editar e pré-visualizar a imagem. | Frontend |
| **P19** | Criar botões de rejeitar/ajustar, aprovar versão e publicar depois; interface mostra resposta real do Backend. | Frontend |
| **P20** | Concluir Home, busca, editorias com conteúdo, cartões e artigo completo com imagem/contexto/fontes, navegáveis em desktop e celular numa sessão leitora. | Frontend |
| **P21** | Demonstrar uma execução **agendada** do coletor da aplicação, resultado visível, rerun sem duplicação e site remoto acessível depois do desenvolvimento. | Backend |
| **P22** | Preparar **dois acontecimentos reais diferentes** com duas fontes independentes por matéria, imagens válidas, mais um caso retido; não aprovar/publicar pelo proprietário. | Editor-Chefe |
| **P23** | Proprietário conduz fluxo inteiro: coleta → comparação → texto/imagem → revisão → aprovação → publicação privada → leitura de notícias completas como usuário comum; Diretor registra viabilidade e pendências. | Diretor |

**Sequência:** as ações continuam P01→P23, uma por acionamento expresso. P01 está integrada; P02 ainda depende de ratificação/reconciliação. Cada ficha `ACOES/Pnn.md` espelha esta versão **proposta** e deve ser enviada ao responsável somente após seu aceite e merge. Concluir uma etapa não dispensa o ensaio real de P23.

## 6. O que deliberadamente fica depois de P23

Se o proprietário considerar o conceito viável, abrir **outro plano** para domínio público, segurança aprofundada, RLS/políticas completas, identidade e sessão para audiência ampla, proteção granular de mídia e cache, backup/restauração integral, SLO/alertas, carga/desempenho, acessibilidade ampliada, direitos de imagens para escala, processos editoriais e monetização. Uma pendência pós-piloto não vira falha retroativa do POC; já um site inacessível, matéria sem aprovação, fonte não rastreável, imagem sem uso permitido ou fluxo interrompido **invalida a prova** e exige correção antes do parecer.

## 7. Proveniência e mudança de versão

Os mapeamentos do Backend, Frontend e Editor-Chefe de 30/09/2026 fundamentam as áreas e a ordem. O plano v1.2.1 foi aprovado em 21:31 -03 e incorporado na PR #2; P01 recebeu aceite em 21:38 -03. A PR #3 continha proposta P02 ainda não aceita. O proprietário, em 22:03 -03, preferiu reaproveitar o Vercel existente; em 22:13 -03 pediu **provar o conceito antes de endurecer controles** e, em 22:16 -03, autorizou a revisão conjunta excepcional de plano/P01/P02, preservando acesso restrito, aprovação específica e rastreabilidade. **Esta v1.3 substitui v1.2.1 apenas após novo aceite explícito e integração**; até lá, não distribuir suas fichas como instrução vigente nem iniciar P03. A [revisão da P01](REVISAO_P01_POC.md), a [arquitetura P02 enxuta](DECISOES_ARQUITETURA.md) e o [registro de progresso](PROGRESSO.md) completam a trilha.
