// Dados de notícias do portal Notícias Imparciais
// Atualizado em: 22/12/2025 19:10

export interface NewsArticle {
  id: string;
  title: string;
  subtitle: string;
  summary: string;
  content: string;
  category: string;
  date: string;
  imageUrl: string;
  hasLeftPerspective: boolean;
  leftPerspective: string | null;
  hasRightPerspective: boolean;
  rightPerspective: string | null;
  attentionPoints: string[];
  sources: string[];
  hasBiasDetected: boolean;
}

// Imagens específicas para cada notícia
const newsImages: { [key: string]: string } = {
  "ministro-alexandre-de-moraes-concede-prisao-domici": "/images/noticias/stf_plenario.jpg",
  "ministerio-da-justica-avanca-em-processo-de-extrad": "/images/noticias/policia_federal.jpg",
  "relatos-indicam-que-alexandre-de-moraes-teria-inte": "/images/noticias/banco_central.jpg",
  "congresso-nacional-aprova-orcamento-da-uniao-para-": "/images/noticias/congresso_nacional.jpg",
  "lula-sanciona-reajuste-para-servidores-do-judiciar": "/images/noticias/planalto.jpg",
  "inauguracao-do-trecho-norte-do-rodoanel-mario-cova": "/images/noticias/rodoanel.jpg",
  "campanha-publicitaria-da-havaianas-gera-debate-nas": "/images/noticias/havaianas.jpg",
  "ministro-do-stf-prorroga-permanencia-do-rio-de-jan": "/images/noticias/rio_janeiro.jpg",
  "cenario-eleitoral-2026-discussoes-sobre-as-candida": "/images/noticias/urna_eletronica.jpg",
  "dolar-se-mantem-acima-de-r-5-50-e-bolsa-de-valores": "/images/noticias/b3_touro.jpg",
  "ministerio-da-justica-divulga-lista-de-criminosos-": "/images/noticias/policia_federal.jpg",
  "stf-decide-sobre-aposentadoria-integral-em-casos-d": "/images/noticias/stf_fachada.jpg",
};

// Função para obter imagem por ID
const getImageUrl = (id: string): string => newsImages[id] || "/images/noticias/stf_fachada.jpg";

export const newsArticles: NewsArticle[] = [
  {
    id: "ministro-alexandre-de-moraes-concede-prisao-domici",
    title: "Ministro Alexandre de Moraes concede prisão domiciliar a General Augusto Heleno",
    subtitle: "Decisão inclui uso de tornozeleira eletrônica e suspensão de porte de armas",
    summary: "O Ministro Alexandre de Moraes, do Supremo Tribunal Federal (STF), determinou a prisão domiciliar do General Augusto Heleno. A decisão impõe o uso de tornozeleira eletrônica, a suspensão de documentos de porte de arma de fogo e de CAC, e restringe as visitas a advogados, médicos e pessoas autorizadas pelo STF.",
    content: "O General Augusto Heleno foi colocado em prisão domiciliar por determinação do Ministro Alexandre de Moraes. A medida cautelar estabelece que o militar deverá utilizar tornozeleira eletrônica para monitoramento. Adicionalmente, todos os seus documentos relacionados a porte de arma de fogo e de Colecionador, Atirador Desportivo e Caçador (CAC) foram suspensos, conforme detalhado na decisão judicial.\n\nAs restrições impostas incluem a limitação de visitas na residência do General. Apenas advogados e médicos, além de indivíduos previamente autorizados pelo STF, terão permissão para acessar o local. A decisão não detalha a motivação completa da prisão, mas ocorre em um contexto onde a Polícia Federal (PF) estaria avaliando o estado de saúde do General, incluindo a suspeita de Alzheimer.\n\nEmbora a concessão da prisão domiciliar tenha sido efetivada, fontes apontam que a Justiça já havia negado pedidos de prisão domiciliar em casos anteriores, como o de um preso por pensão alimentícia com diagnóstico de Alzheimer, o que sugere uma análise individualizada das circunstâncias pelo STF.\n\nA decisão de Moraes é imediata e visa garantir o cumprimento das medidas cautelares enquanto o processo segue em andamento, mantendo o monitoramento do General Heleno por meio da tornozeleira eletrônica.",
    category: "Política",
    date: "22/12/2025",
    imageUrl: "/images/noticias/stf_plenario.jpg",
    hasLeftPerspective: true,
    leftPerspective: "As fontes de esquerda enfatizam as restrições impostas por Moraes, como o uso da tornozeleira eletrônica e a suspensão dos documentos de armas (CAC e porte), focando na rigidez das medidas cautelares. Também mencionam a negativa anterior de prisão domiciliar para outros presos com Alzheimer, sugerindo uma possível disparidade de tratamento.",
    hasRightPerspective: true,
    rightPerspective: "As fontes de direita destacam o aspecto 'humanitário' da decisão de Moraes, ligando a concessão da prisão domiciliar diretamente à condição de saúde do General, mencionando a suspeita de Alzheimer e a perícia da Polícia Federal para avaliar essa condição.",
    attentionPoints: ["A menção ao Alzheimer é usada pela direita para justificar a 'humanidade' da decisão, enquanto a esquerda usa um caso anterior de negativa de domiciliar para um preso com a mesma condição para questionar a equidade.", "A esquerda foca nas restrições (tornozeleira, suspensão de armas) para enfatizar a punição ou controle judicial.", "A omissão do motivo da prisão domiciliar no texto factual é necessária, pois as fontes não o detalham, focando apenas nas condições impostas.", "O termo 'humanitária' (usado pela direita) é um adjetivo interpretativo e não factual, devendo ser evitado no corpo da notícia neutra."],
    sources: ["UOL", "G1/Globo", "Revista Oeste", "Brasil Paralelo"],
    hasBiasDetected: true
  },
  {
    id: "ministerio-da-justica-avanca-em-processo-de-extrad",
    title: "Ministério da Justiça avança em processo de extradição de Alexandre Ramagem",
    subtitle: "Cancelamento de passaportes diplomáticos e retomada de processo no STF marcam o cenário atual",
    summary: "O Ministério da Justiça deu andamento ao processo de extradição do ex-diretor da ABIN, Alexandre Ramagem. Simultaneamente, a Câmara dos Deputados cancelou seu passaporte diplomático, e o Supremo Tribunal Federal (STF) retomou o processo para que ele responda por atos relacionados ao 8 de janeiro.",
    content: "O Ministério da Justiça e Segurança Pública (MJSP) confirmou o andamento do processo que visa a extradição de Alexandre Ramagem. Embora a natureza exata do processo não tenha sido detalhada, a movimentação indica uma ação formal do governo brasileiro em relação à situação jurídica do ex-diretor da Agência Brasileira de Inteligência (ABIN).\n\nParalelamente, a Câmara dos Deputados determinou o cancelamento do passaporte diplomático de Ramagem, uma medida que afeta sua capacidade de trânsito internacional. A decisão foi estendida a outros indivíduos, como o deputado Eduardo, gerando críticas por parte de alguns setores políticos.\n\nNo âmbito judicial, o Supremo Tribunal Federal (STF) retomou o processo criminal contra Ramagem referente aos atos de 8 de janeiro. A suspensão anterior da denúncia, que havia sido determinada após sua diplomação como deputado, foi revertida. Com isso, o relator da ação penal determinou que Ramagem seja processado também pelos crimes cometidos após sua posse.",
    category: "Política",
    date: "22/12/2025",
    imageUrl: "/images/noticias/policia_federal.jpg",
    hasLeftPerspective: true,
    leftPerspective: "As fontes de esquerda enfatizam o avanço das ações institucionais (MJSP, Câmara e STF) contra Ramagem, sugerindo que a extradição é provável e que a responsabilização judicial pelos atos de 8 de janeiro está sendo efetivada após o cancelamento da suspensão da denúncia.",
    hasRightPerspective: true,
    rightPerspective: "As fontes de direita concentram-se na crítica à decisão de cancelamento dos passaportes diplomáticos, interpretando a medida como uma ação política ou injustificada, conforme manifestação de indivíduos afetados, como o deputado Eduardo.",
    attentionPoints: ["A menção à 'aposta' de deportação por fontes de esquerda (Dani Lima) é especulativa e não um fato confirmado.", "A crítica de Eduardo ao cancelamento do passaporte diplomático é um posicionamento, não uma análise factual da legalidade da medida.", "O texto não detalha o motivo ou o país solicitante da extradição, informação que pode estar ausente nas fontes ou sob sigilo, mas é crucial para o entendimento completo do caso."],
    sources: ["UOL", "G1/Globo", "Revista Oeste"],
    hasBiasDetected: true
  },
  {
    id: "relatos-indicam-que-alexandre-de-moraes-teria-inte",
    title: "Relatos indicam que Alexandre de Moraes teria intercedido pelo Banco Master junto ao Banco Central",
    subtitle: "Ministro do STF é citado em notícias sobre suposta intervenção em favor da instituição financeira",
    summary: "Notícias veiculadas na imprensa apontam que o ministro do Supremo Tribunal Federal (STF), Alexandre de Moraes, teria procurado o ex-secretário-executivo do Ministério da Fazenda, Gabriel Galípolo, para interceder em nome do Banco Master junto ao Banco Central (BC). Os relatos geraram debates e críticas sobre a conduta do magistrado. Um senador também manifestou intenção de investigar o caso.",
    content: "O nome do ministro Alexandre de Moraes, do Supremo Tribunal Federal (STF), tem sido associado a uma suposta intercessão em favor do Banco Master junto ao Banco Central (BC). Segundo reportagens, Moraes teria procurado Gabriel Galípolo, então secretário-executivo do Ministério da Fazenda e atual diretor de Política Monetária do BC, para tratar de questões relacionadas à instituição financeira. O teor exato da conversa e a natureza da intervenção não foram detalhados publicamente pelo ministro ou pelo BC.\n\nA divulgação desses relatos provocou reações na esfera pública e política. Críticos argumentam que a ação, se confirmada, levantaria questões éticas sobre a separação de poderes e a imparcialidade de um membro do Judiciário em assuntos regulatórios e financeiros. O ministro não se manifestou publicamente sobre as alegações, mantendo o silêncio sobre o caso.\n\nNo campo político, um senador anunciou a intenção de iniciar uma investigação sobre o envolvimento de Moraes e o Banco Master, buscando esclarecer os fatos e as implicações da suposta intercessão. Paralelamente, o debate se estendeu para a atuação da esposa do ministro, que atua na defesa de grandes companhias, embora não haja ligação direta comprovada com o caso do Banco Master.\n\nO Banco Master não comentou os detalhes da suposta intercessão, e o Banco Central mantém sigilo sobre as comunicações internas relacionadas a processos de instituições financeiras. O caso segue em discussão na mídia e no meio político, aguardando manifestações oficiais ou a abertura de inquéritos formais.",
    category: "Política",
    date: "22/12/2025",
    imageUrl: "/images/noticias/banco_central.jpg",
    hasLeftPerspective: true,
    leftPerspective: "A ênfase é colocada na crítica à conduta ética de Moraes, argumentando que sua suposta intercessão pelo banco é 'inconcebível' e que 'salvar a democracia não dá licença para ajudar banco'. O foco é o conflito de interesses e o silêncio do ministro diante das acusações.",
    hasRightPerspective: true,
    rightPerspective: "O foco principal é a necessidade de investigação e a politização do caso. É destacada a promessa de um senador de investigar a relação entre Moraes e o Banco Master, e é mencionada a atuação profissional da esposa do ministro, buscando reforçar a narrativa de um possível uso de influência.",
    attentionPoints: ["Ambos os lados utilizam a suposta intercessão para fins de crítica política ou ética, sem apresentar provas diretas da ilegalidade da ação.", "A esquerda foca na falha ética e no silêncio de Moraes, usando linguagem de julgamento ('intolerável').", "A direita busca conectar o caso a outras questões (atuação da esposa) para construir uma narrativa mais ampla de uso de poder.", "Não há confirmação oficial ou detalhamento do teor da conversa entre Moraes e Galípolo."],
    sources: ["UOL", "Revista Oeste", "G1/Globo", "Brasil Paralelo"],
    hasBiasDetected: true
  },
  {
    id: "congresso-nacional-aprova-orcamento-da-uniao-para-",
    title: "Congresso Nacional aprova Orçamento da União para o próximo exercício",
    subtitle: "Discussões centram-se no volume de emendas parlamentares e na relação entre Poderes",
    summary: "O Congresso Nacional finalizou a votação do Orçamento Anual, definindo a distribuição de recursos para o próximo ano. Um dos pontos centrais do debate foi o aumento no montante destinado às emendas parlamentares. Paralelamente, a relação entre o Legislativo e o Judiciário foi mencionada em discussões sobre a execução desses recursos.",
    content: "O projeto de Lei Orçamentária Anual (LOA) foi aprovado pelo Congresso, estabelecendo as receitas e despesas da União. A versão final do texto incorporou modificações significativas, notadamente no que tange à alocação de verbas discricionárias para os parlamentares. Fontes indicam que o valor total destinado às emendas parlamentares sofreu um acréscimo de aproximadamente R$ 11 bilhões em comparação com a proposta inicial.\n\nA aprovação do Orçamento é um marco crucial para a gestão federal, pois define as prioridades de investimento em áreas como saúde, educação e infraestrutura. A distribuição dessas emendas, que são recursos indicados por deputados e senadores para suas bases eleitorais, é vista como um instrumento importante de articulação política entre o Executivo e o Legislativo.\n\nEm paralelo à tramitação orçamentária, foram levantadas discussões sobre a dinâmica de fiscalização e execução dessas verbas. A atuação de membros do Supremo Tribunal Federal (STF) em processos que envolvem a liberação e o controle das emendas tem gerado debates sobre os limites de atuação de cada Poder, adicionando um elemento de tensão institucional ao cenário político.\n\nO Poder Executivo agora deve sancionar o texto aprovado, podendo vetar pontos específicos. A forma como as emendas serão geridas e fiscalizadas nos próximos meses continuará sendo um tema central na agenda política nacional.",
    category: "Economia",
    date: "22/12/2025",
    imageUrl: "/images/noticias/congresso_nacional.jpg",
    hasLeftPerspective: true,
    leftPerspective: "O foco é dado ao volume financeiro do aumento das emendas parlamentares (R$ 11 bilhões a mais), destacando o crescimento da influência do Congresso sobre a distribuição de recursos públicos.",
    hasRightPerspective: true,
    rightPerspective: "A ênfase recai sobre a interferência ou atuação do Supremo Tribunal Federal (STF) na gestão das emendas, sugerindo que essa intervenção eleva a tensão institucional entre o Judiciário e o Legislativo.",
    attentionPoints: ["A fonte de esquerda foca no custo e no poder do Legislativo, omitindo a tensão institucional.", "A fonte de direita foca na tensão institucional e na ação do STF, podendo omitir o impacto financeiro do aumento das emendas.", "Ambas as perspectivas utilizam o Orçamento como pano de fundo para discutir dinâmicas de poder (custo vs. controle)."],
    sources: ["UOL", "G1/Globo", "Revista Oeste", "Brasil Paralelo"],
    hasBiasDetected: true
  },
  {
    id: "lula-sanciona-reajuste-para-servidores-do-judiciar",
    title: "Lula sanciona reajuste para servidores do Judiciário e veta aumentos futuros",
    subtitle: "Medida garante reajuste de 8% em 2026, mas impede novos aumentos de despesa após o fim do atual mandato presidencial",
    summary: "O presidente Luiz Inácio Lula da Silva sancionou o projeto de lei que concede reajuste de 8% para os servidores do Poder Judiciário a partir de 2026. Entretanto, o presidente vetou os trechos que previam aumentos adicionais de despesa com pessoal para os anos de 2027 e 2028. A decisão presidencial visa limitar o impacto orçamentário para mandatos futuros.",
    content: "O presidente Lula sancionou a lei que estabelece o reajuste salarial para os servidores do Poder Judiciário. A medida garante um aumento de 8% a ser implementado no ano de 2026. A sanção foi publicada em edição extra do Diário Oficial da União.\n\nNo entanto, o presidente optou por vetar os dispositivos que estendiam o aumento de despesa com pessoal para os anos subsequentes, especificamente 2027 e 2028. A justificativa para o veto, segundo o governo, está relacionada à responsabilidade fiscal e à decisão de não comprometer o orçamento de gestões futuras com aumentos de despesa criados no atual mandato.\n\nO reajuste de 8% para 2026 não se aplica aos ministros do Supremo Tribunal Federal (STF). O veto presidencial será agora analisado pelo Congresso Nacional, que pode mantê-lo ou derrubá-lo por maioria absoluta de votos de deputados e senadores.",
    category: "Política",
    date: "22/12/2025",
    imageUrl: "/images/noticias/planalto.jpg",
    hasLeftPerspective: true,
    leftPerspective: "As fontes de esquerda enfatizam que o veto presidencial foi aplicado especificamente aos trechos que estabeleciam aumentos de despesa com pessoal para anos seguintes ao término do mandato de Lula (2027 e 2028), destacando a cautela fiscal em relação a mandatos futuros. Também mencionam que o reajuste não alcança os ministros do STF.",
    hasRightPerspective: true,
    rightPerspective: "As fontes de direita focam na sanção do reajuste de 8% para os servidores do Judiciário em 2026, seguida pelo veto aos aumentos subsequentes. O foco é factual, registrando a ação do presidente de conceder o aumento imediato e barrar as progressões futuras.",
    attentionPoints: ["Ambas as perspectivas concordam no fato central (8% em 2026, veto em 2027/2028), indicando alta factualidade do evento.", "A ênfase da esquerda na 'responsabilidade fiscal' e na não inclusão dos ministros do STF pode ser uma tentativa de justificar positivamente a ação do governo.", "A direita apresenta o fato de forma mais seca, sem entrar na justificativa do veto, permitindo interpretações mais abertas sobre a motivação da decisão."],
    sources: ["G1/Globo", "Revista Oeste", "UOL"],
    hasBiasDetected: false
  },
  {
    id: "inauguracao-do-trecho-norte-do-rodoanel-mario-cova",
    title: "Inauguração do Trecho Norte do Rodoanel Mário Covas é Marcada por Declarações Políticas",
    subtitle: "Governador Tarcísio de Freitas e o presidente do BNDES, Aloizio Mercadante, participaram do evento",
    summary: "O Trecho Norte do Rodoanel Mário Covas, em São Paulo, foi inaugurado recentemente. O evento contou com a presença de autoridades e foi palco de trocas de declarações sobre o histórico da obra, que sofreu paralisações e atrasos.",
    content: "O Trecho Norte do Rodoanel Mário Covas, uma obra de infraestrutura aguardada há anos, foi oficialmente inaugurado em São Paulo. A conclusão deste segmento visa desafogar o tráfego na região metropolitana, conectando as rodovias Dutra e Fernão Dias. A cerimônia de inauguração reuniu diversas autoridades, incluindo o governador de São Paulo, Tarcísio de Freitas, e o presidente do Banco Nacional de Desenvolvimento Econômico e Social (BNDES), Aloizio Mercadante.\n\nDurante o evento, o histórico da construção, marcado por longos períodos de paralisação e estouros de orçamento, tornou-se um tema central. As declarações públicas de Freitas e Mercadante refletiram diferentes interpretações sobre as causas dos atrasos e a responsabilidade pela retomada e conclusão da infraestrutura.\n\nO Rodoanel Mário Covas é uma das maiores obras viárias do estado e sua finalização é vista como essencial para a logística de transporte de cargas. A gestão da obra passou por diferentes administrações estaduais e federais, e as investigações sobre desvios de recursos no passado foram amplamente noticiadas.",
    category: "Política",
    date: "22/12/2025",
    imageUrl: "/images/noticias/rodoanel.jpg",
    hasLeftPerspective: true,
    leftPerspective: "As fontes de esquerda enfatizam a troca de farpas entre o governador Tarcísio e o presidente do BNDES, Aloizio Mercadante, focando no debate político e na disputa de narrativas sobre quem tem o mérito da conclusão da obra, ou quem deve ser responsabilizado pelos atrasos.",
    hasRightPerspective: true,
    rightPerspective: "As fontes de direita enfatizam a declaração de Tarcísio de Freitas de que a corrupção foi o principal fator que paralisou a obra do Rodoanel Norte, direcionando o foco para a gestão anterior e a necessidade de combate a desvios para a finalização de projetos de infraestrutura.",
    attentionPoints: ["Omissão do contexto completo das 'farpas' trocadas (o que exatamente foi dito por cada um).", "A ênfase na 'corrupção' pela direita pode desviar a atenção de outros fatores técnicos ou de gestão que também contribuíram para o atraso.", "Nenhuma das perspectivas detalha o custo final da obra ou o cronograma exato de paralisação, focando apenas na disputa política."],
    sources: ["UOL", "G1/Globo", "Revista Oeste", "Brasil Paralelo"],
    hasBiasDetected: true
  },
  {
    id: "campanha-publicitaria-da-havaianas-gera-debate-nas",
    title: "Campanha Publicitária da Havaianas Gera Debate nas Redes Sociais",
    subtitle: "Comercial de Ano Novo com Fernanda Torres é alvo de críticas por parte de figuras conservadoras",
    summary: "Uma campanha publicitária da marca Havaianas para o Ano Novo, estrelada pela atriz Fernanda Torres, gerou controvérsia e debate nas redes sociais. O comercial, que sugere começar o ano 'com os dois pés' em vez de apenas o 'pé direito', foi criticado por parlamentares e influenciadores de espectro conservador, que interpretaram a mensagem como tendo conotações políticas.",
    content: "A campanha em questão, veiculada pela Havaianas para promover seus produtos na virada do ano, apresenta a atriz Fernanda Torres discutindo superstições de Ano Novo. O ponto central da peça publicitária é a inversão do ditado popular, encorajando o público a começar o ano 'com os dois pés', em vez da tradicional ênfase no 'pé direito'.\n\nA reação ao comercial foi imediata e polarizada. Figuras públicas e influenciadores identificados com a direita política brasileira manifestaram descontentamento nas plataformas digitais, interpretando a mensagem como uma crítica velada ou uma tomada de posição ideológica por parte da marca e da atriz. A crítica se concentrou na percepção de que a campanha estaria subvertendo valores tradicionais ou utilizando linguagem codificada para fins políticos.\n\nEm contrapartida, veículos de comunicação e comentaristas de esquerda analisaram a polêmica como uma reação exagerada e uma 'leitura da pior forma possível' de um comercial de chinelos. Eles argumentam que a discussão transcendeu o propósito original da campanha, que era meramente comercial, transformando-a em um tema de discussão política no país.",
    category: "Política",
    date: "22/12/2025",
    imageUrl: "/images/noticias/havaianas.jpg",
    hasLeftPerspective: true,
    leftPerspective: "Enfatiza que a polêmica é uma reação exagerada e uma 'leitura da pior forma possível' de um comercial que é essencialmente sobre chinelos, transformando uma campanha publicitária em discussão política.",
    hasRightPerspective: true,
    rightPerspective: "Questiona a neutralidade da campanha e da atriz envolvida, interpretando a mensagem de 'não começar com o pé direito' como uma possível conotação ideológica ou política, chegando a rotular o debate como 'Chinelos de esquerda'.",
    attentionPoints: ["O comercial não faz menção explícita a partidos políticos ou ideologias.", "A polarização da discussão é amplificada pela presença de figuras públicas e influenciadores em ambos os lados.", "O foco da controvérsia se deslocou do produto (chinelos) para a interpretação da linguagem utilizada ('pé direito' vs. 'dois pés')."],
    sources: ["Josias: 'Direita lê comercial da Havaianas da pior forma possível' (UOL)", "Como uma campanha publicitária de chinelos para o Ano Novo virou motivo de discussão política no Brasil (G1/Globo)", "Chinelos de esquerda? Entenda a polêmica envolvendo Fernanda Torres e a Havaianas (Brasil Paralelo)"],
    hasBiasDetected: true
  },
  {
    id: "ministro-do-stf-prorroga-permanencia-do-rio-de-jan",
    title: "Ministro do STF prorroga permanência do Rio de Janeiro no Regime de Recuperação Fiscal",
    subtitle: "Decisão de Toffoli estende prazo e mantém suspensão de multa da União, visando negociação de dívidas",
    summary: "O Ministro Dias Toffoli, do Supremo Tribunal Federal (STF), prorrogou por mais seis meses a permanência do estado do Rio de Janeiro no Regime de Recuperação Fiscal (RRF). A decisão mantém a suspensão da multa da União e visa proporcionar tempo para que o estado negocie sua adesão a um novo programa de refinanciamento de dívidas com o governo federal.",
    content: "O Ministro Dias Toffoli, do STF, concedeu uma extensão de seis meses para a permanência do estado do Rio de Janeiro no Regime de Recuperação Fiscal. A medida, anunciada recentemente, visa dar continuidade ao processo de ajuste fiscal do estado, que enfrenta dificuldades financeiras crônicas. A prorrogação é considerada crucial para evitar um colapso nas contas estaduais e garantir a continuidade de serviços públicos essenciais.\n\nA decisão judicial também mantém a suspensão da multa imposta pela União, relacionada ao descumprimento de obrigações fiscais. Segundo o ministro, o prazo adicional permitirá que o governo estadual do Rio de Janeiro estabeleça negociações com o governo federal para a adesão a um novo programa de refinanciamento de dívidas, buscando uma solução de longo prazo para o passivo financeiro.\n\nSimultaneamente, o Governo do Rio de Janeiro tem apresentado ao STF planos de ação em outras áreas. Recentemente, foi divulgado que o estado submeteu um plano detalhado focado na reocupação de territórios. Embora esta ação não esteja diretamente ligada à prorrogação do RRF, ela reflete os esforços do estado em demonstrar capacidade de gestão e recuperação em diversas frentes.\n\nO Regime de Recuperação Fiscal é um instrumento legal que permite aos estados em grave desequilíbrio financeiro implementar medidas de ajuste fiscal rigorosas em troca da suspensão do pagamento de dívidas com a União. A prorrogação de Toffoli sinaliza a necessidade de continuidade do suporte federal enquanto o estado busca a estabilização de suas finanças.",
    category: "Política",
    date: "22/12/2025",
    imageUrl: "/images/noticias/rio_janeiro.jpg",
    hasLeftPerspective: true,
    leftPerspective: "As fontes de esquerda enfatizam a decisão do STF como um alívio temporário necessário para o estado, focando na suspensão da multa e na oportunidade de negociação com o governo federal para adesão a um novo programa de refinanciamento de dívidas, destacando a intervenção judicial como crucial para a estabilidade fiscal do RJ.",
    hasRightPerspective: true,
    rightPerspective: "As fontes de direita tendem a focar em ações de gestão e segurança pública do governo estadual, como a apresentação de planos para a reocupação de territórios ao STF. Essa perspectiva pode sugerir um foco maior nas medidas internas de recuperação e ordem, em paralelo à dependência do auxílio fiscal federal.",
    attentionPoints: ["As fontes de esquerda focam estritamente no aspecto financeiro e na decisão judicial (STF/Toffoli), omitindo outros planos de gestão do estado.", "As fontes de direita introduzem o tema da segurança/território, o que pode desviar o foco da crise fiscal central e da dependência do RRF.", "Ambas as perspectivas tendem a omitir detalhes sobre as condições e contrapartidas rigorosas que o RRF impõe ao estado, focando mais nos benefícios (suspensão de multa/prazo)."],
    sources: ["G1/Globo", "Revista Oeste"],
    hasBiasDetected: true
  },
  {
    id: "cenario-eleitoral-2026-discussoes-sobre-as-candida",
    title: "Cenário Eleitoral 2026: Discussões sobre as candidaturas de Zema e Flávio Bolsonaro",
    subtitle: "Articulações políticas e posicionamentos individuais marcam o debate sobre a chapa presidencial da direita",
    summary: "O cenário das eleições presidenciais de 2026 tem sido marcado por discussões sobre as possíveis candidaturas do governador Romeu Zema e do senador Flávio Bolsonaro. Há articulações em curso que sugerem uma possível chapa com Zema como vice de Flávio, embora o governador mineiro tenha reafirmado sua intenção de manter sua candidatura até o fim.",
    content: "As movimentações políticas visando as eleições presidenciais de 2026 continuam a gerar debates sobre a composição da chapa da direita. Segundo relatos de bastidores, o político Gilberto Kassab estaria articulando uma possível composição entre o governador de Minas Gerais, Romeu Zema (Novo), e o senador Flávio Bolsonaro (PL), sugerindo Zema como vice de Flávio. Tais articulações indicam um esforço para unificar forças dentro do espectro político conservador.\n\nEm contraste com as articulações de chapa, o governador Romeu Zema tem mantido uma postura de pré-candidato. Zema declarou publicamente que pretende manter sua candidatura à presidência até o final do processo eleitoral, mesmo diante da possibilidade de Flávio Bolsonaro também se candidatar ao cargo máximo do Executivo. O posicionamento de Zema sugere uma disposição em prosseguir com um projeto individual, independentemente dos arranjos propostos por outros líderes políticos.\n\nO desenvolvimento dessas candidaturas e as negociações de bastidores serão cruciais para definir a configuração final da disputa presidencial de 2026. A possibilidade de uma chapa unificada, como a articulada por Kassab, contrasta com a intenção declarada de Zema de seguir com sua candidatura, indicando um período de intensa negociação e definição estratégica entre os principais nomes da direita.",
    category: "Política",
    date: "22/12/2025",
    imageUrl: "/images/noticias/urna_eletronica.jpg",
    hasLeftPerspective: false,
    leftPerspective: null,
    hasRightPerspective: false,
    rightPerspective: null,
    attentionPoints: ["Notícia baseada apenas em fontes de direita. Não foi possível verificar cobertura do outro espectro político.", "As informações sobre as articulações de Kassab e os posicionamentos de Zema são provenientes de um único veículo de imprensa."],
    sources: ["Zema vice de Flávio Bolsonaro? Kassab articula nos bastidores (Brasil Paralelo)", "Zema diz que mantém candidatura até o fim, mesmo com a candidatura de Flávio Bolsonaro (Brasil Paralelo)"],
    hasBiasDetected: false
  },
  {
    id: "dolar-se-mantem-acima-de-r-550-e-bolsa-de-valores-",
    title: "Dólar se mantém acima de R$ 5,50 e Bolsa de Valores registra fechamento em alta",
    subtitle: "Movimentação do mercado financeiro é observada pelo terceiro dia consecutivo",
    summary: "O valor do dólar permaneceu acima da marca de R$ 5,50 pelo terceiro dia consecutivo. Em contraste, a Bolsa de Valores brasileira encerrou o pregão com valorização.",
    content: "O dólar comercial manteve sua cotação acima de R$ 5,50, consolidando esse patamar pelo terceiro dia útil seguido. A flutuação da moeda estrangeira é um indicador sensível às expectativas econômicas domésticas e internacionais, influenciando diversos setores da economia nacional.\n\nSimultaneamente, o mercado de ações apresentou um desempenho positivo. A Bolsa de Valores registrou um fechamento em alta, indicando um movimento de valorização dos ativos negociados. Esse comportamento ocorre em meio a um cenário de câmbio elevado.\n\nAnalistas de mercado monitoram a relação entre a estabilidade do dólar em patamares mais altos e o desempenho do mercado acionário, buscando compreender os fatores que impulsionam essa dinâmica. A alta da Bolsa pode refletir otimismo em setores específicos ou a busca por ativos de risco em um ambiente de incertezas.",
    category: "Economia",
    date: "22/12/2025",
    imageUrl: newsImages[9],
    hasLeftPerspective: false,
    leftPerspective: null,
    hasRightPerspective: false,
    rightPerspective: null,
    attentionPoints: ["Notícia baseada apenas em fontes de esquerda. Não foi possível verificar cobertura do outro espectro político."],
    sources: ["Dólar fica acima de R$ 5,50 pelo 3º dia consecutivo; Bolsa fecha em alta (UOL)"],
    hasBiasDetected: false
  },
  {
    id: "ministerio-da-justica-divulga-lista-de-criminosos-",
    title: "Ministério da Justiça divulga lista de criminosos mais procurados por estado",
    subtitle: "Iniciativa visa auxiliar na captura de indivíduos procurados por crimes graves em todo o país",
    summary: "O Ministério da Justiça lançou uma lista contendo os criminosos mais procurados em cada estado do Brasil. Os indivíduos listados são procurados por crimes como homicídio, tráfico de drogas, organização criminosa e roubo.",
    content: "O Ministério da Justiça e Segurança Pública (MJSP) lançou um site dedicado à divulgação dos criminosos mais procurados em cada unidade federativa do país. A iniciativa, implementada em dezembro, tem como objetivo fornecer informações detalhadas, incluindo fotos, para auxiliar as forças de segurança e a população na localização e captura desses indivíduos.\n\nOs perfis incluídos na lista são de pessoas procuradas por envolvimento em crimes considerados graves, que impactam diretamente a segurança pública. De acordo com as informações divulgadas, os principais delitos pelos quais os procurados respondem incluem homicídio, tráfico de drogas, participação em organização criminosa e roubo.\n\nA divulgação centralizada busca aumentar a visibilidade desses casos e promover a cooperação entre os diferentes órgãos de segurança estaduais e federais. O site funciona como um banco de dados acessível, padronizando a forma como essas informações são apresentadas ao público e às autoridades competentes.\n\nO lançamento da lista representa uma estratégia do MJSP para utilizar a tecnologia e a participação social como ferramentas no combate à criminalidade e na efetivação de mandados de prisão pendentes em todo o território nacional.",
    category: "Política",
    date: "22/12/2025",
    imageUrl: "/images/noticias/policia_federal.jpg",
    hasLeftPerspective: false,
    leftPerspective: null,
    hasRightPerspective: false,
    rightPerspective: null,
    attentionPoints: ["Notícia baseada apenas em fontes de esquerda (G1/Globo). Não foi possível verificar cobertura do outro espectro político, mas o conteúdo é estritamente factual sobre um anúncio governamental."],
    sources: ["Ministério da Justiça lança lista com os criminosos mais procurados de cada estado do país (G1/Globo)", "Mais procurados do Brasil respondem por homicídio, tráfico de drogas, organização criminosa e roubo (G1/Globo)"],
    hasBiasDetected: false
  },
  {
    id: "stf-decide-sobre-aposentadoria-integral-em-casos-d",
    title: "STF decide sobre aposentadoria integral em casos de doença grave não ocupacional",
    subtitle: "Supremo Tribunal Federal delibera sobre critérios para concessão de paridade e integralidade a servidores públicos",
    summary: "O Supremo Tribunal Federal (STF) decidiu recentemente sobre a concessão de aposentadoria integral a servidores públicos acometidos por doenças graves que não possuem relação direta com a atividade profissional. A decisão estabelece que a integralidade não será garantida automaticamente nesses casos, alinhando-se às regras previdenciárias vigentes.",
    content: "O Supremo Tribunal Federal (STF) se posicionou em relação à aposentadoria de servidores públicos que desenvolvem doenças graves não relacionadas ao trabalho. A Corte negou o direito à aposentadoria com proventos integrais e paridade para servidores que ingressaram no serviço público após a Emenda Constitucional nº 41/2003 e que não cumpriram os requisitos de transição estabelecidos. A integralidade e a paridade referem-se, respectivamente, ao direito de receber o último salário da ativa e ter os reajustes iguais aos dos servidores em atividade.\n\nA deliberação do STF foca na interpretação das normas previdenciárias que regem a aposentadoria por invalidez. Para servidores que entraram após a EC 41/2003, a regra geral é que os proventos sejam calculados com base na média das contribuições, e não pelo último salário, exceto em casos específicos de invalidez permanente decorrente de acidente de trabalho, moléstia profissional ou doença grave, contagiosa ou incurável, na forma da lei.\n\nA decisão sublinha a necessidade de aderência aos critérios estabelecidos pela legislação previdenciária e pelas emendas constitucionais que alteraram o sistema de previdência dos servidores. O entendimento do STF impacta diretamente a forma como as aposentadorias por invalidez de servidores públicos federais, estaduais e municipais serão concedidas, especialmente em relação ao cálculo dos proventos.\n\nEmbora a legislação preveja a aposentadoria integral em situações de invalidez por doença grave, a Corte enfatizou que a doença deve estar listada na lei e, no caso de servidores que não se enquadram nas regras de transição, a integralidade não é automática apenas pela gravidade da enfermidade não ocupacional.",
    category: "Política",
    date: "22/12/2025",
    imageUrl: "/images/noticias/stf_fachada.jpg",
    hasLeftPerspective: false,
    leftPerspective: null,
    hasRightPerspective: false,
    rightPerspective: null,
    attentionPoints: ["Notícia baseada apenas em fontes de esquerda. Não foi possível verificar cobertura do outro espectro político."],
    sources: ["STF nega aposentadoria integral à doença grave não ocupacional (UOL)"],
    hasBiasDetected: false
  },
];

export default newsArticles;
