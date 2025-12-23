// Dados de notícias do portal Notícias Imparciais
// Atualizado em: 23/12/2025 10:50

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
  "bolsonaro-cancela-entrevista-e-tem-cirurgia-agenda": "/images/noticias/planalto.jpg",
  "ministro-moraes-e-banco-master-reunioes-e-question": "/images/noticias/stf_plenario.jpg",
  "general-heleno-inicia-cumprimento-de-prisao-domici": "/images/noticias/stf_fachada.jpg",
  "presidente-lula-assina-indulto-de-natal-excluindo-": "/images/noticias/planalto.jpg",
  "gustavo-feliciano-assume-ministerio-do-turismo-apo": "/images/noticias/congresso_nacional.jpg",
  "polemica-envolvendo-havaianas-gera-pedidos-de-boic": "/images/noticias/havaianas.jpg",
  "inflacao-registra-alta-em-2025-enquanto-mercado-aj": "/images/noticias/b3_touro.jpg",
  "governo-libera-saque-do-fgts-para-141-milhoes-de-t": "/images/noticias/banco_central.jpg",
  "eduardo-bolsonaro-pode-perder-passaporte-apos-cass": "/images/noticias/congresso_nacional.jpg",
};

// Função para obter imagem por ID
const getImageUrl = (id: string): string => newsImages[id] || "/images/noticias/stf_fachada.jpg";

export const newsArticles: NewsArticle[] = [
  {
    id: "bolsonaro-cancela-entrevista-e-tem-cirurgia-agenda",
    title: "Bolsonaro cancela entrevista e tem cirurgia agendada para o Natal",
    subtitle: "Defesa do ex-presidente solicita internação e procedimento cirúrgico; pedido de prisão domiciliar humanitária ainda não foi concedido",
    summary: "O ex-presidente Jair Bolsonaro cancelou uma entrevista prevista para esta semana alegando questões de saúde. Sua defesa solicitou que ele seja internado na quarta-feira (24) e submetido a uma cirurgia na quinta-feira (25), data do Natal, com a presença da esposa Michelle Bolsonaro como acompanhante.",
    content: "Jair Bolsonaro, ex-presidente do Brasil, cancelou uma entrevista que estava programada para esta semana, justificando motivos relacionados à sua saúde. A decisão foi confirmada por diferentes veículos de comunicação, que destacaram a preocupação da equipe médica e da defesa do político.\n\nA defesa de Bolsonaro entrou com um pedido para que ele seja internado já na quarta-feira (24) e realize uma cirurgia na quinta-feira (25), coincidindo com o feriado de Natal. A solicitação inclui a presença da esposa do ex-presidente, Michelle Bolsonaro, como acompanhante durante o procedimento.\n\nAlém disso, o Supremo Tribunal Federal (STF) tem analisado pedidos de prisão domiciliar humanitária para Bolsonaro, mas até o momento indicou que não deve conceder a medida em curto prazo, conforme declarações do ministro Alexandre de Moraes. O tribunal já concedeu esse benefício a outros casos, mas negou para o ex-presidente.\n\nO cenário político também envolve a análise separada dos casos de Bolsonaro e de outros generais pelo Superior Tribunal Militar (STM), enquanto o ex-presidente se prepara para sua primeira entrevista após a prisão, que foi adiada devido à questão de saúde.",
    category: "Política",
    date: "23/12/2025",
    imageUrl: "/images/noticias/planalto.jpg",
    hasLeftPerspective: true,
    leftPerspective: "Fontes de esquerda destacam o cancelamento da entrevista por questões de saúde e o pedido da defesa para internação e cirurgia no Natal, além da negativa do STF em conceder prisão domiciliar humanitária para Bolsonaro neste momento. Também enfatizam o contexto jurídico envolvendo o ex-presidente e a análise dos pedidos pelo tribunal.",
    hasRightPerspective: true,
    rightPerspective: "Fontes de direita confirmam o cancelamento da entrevista devido a questões de saúde e mencionam a expectativa de que Bolsonaro conceda sua primeira entrevista após a prisão em breve. Também ressaltam a análise separada dos casos pelo STM e o papel da família Bolsonaro em meio às movimentações políticas.",
    attentionPoints: ["As informações sobre a saúde de Bolsonaro são baseadas em comunicados da defesa e podem refletir interesses políticos.", "O pedido de prisão domiciliar humanitária está em análise e ainda não foi concedido, o que pode gerar interpretações divergentes.", "As fontes apresentam diferentes ênfases: veículos de esquerda focam no contexto jurídico e na negativa do STF, enquanto veículos de direita destacam a expectativa da entrevista e a movimentação política.", "A cobertura do tema envolve aspectos judiciais, de saúde e políticos, que podem ser explorados de formas distintas conforme o viés editorial."],
    sources: ["UOL", "G1/Globo", "Revista Oeste", "Brasil Paralelo"],
    hasBiasDetected: true
  },
  {
    id: "ministro-moraes-e-banco-master-reunioes-e-question",
    title: "Ministro Moraes e Banco Master: reuniões e questionamentos sobre o caso",
    subtitle: "Ministro do STF confirmou encontros com o Banco Central relacionados à Lei Magnitsky, enquanto investigações sobre o Banco Master avançam",
    summary: "O ministro Alexandre de Moraes, do Supremo Tribunal Federal (STF), confirmou ter realizado reuniões com o presidente do Banco Central (BC) para tratar da Lei Magnitsky. Paralelamente, o Banco Master está no centro de investigações que envolvem o BC e o Supremo, com processos em andamento e debates sobre a atuação das instituições, ocorridos em dezembro de 2025, no Brasil.",
    content: "O ministro Alexandre de Moraes confirmou que manteve encontros com o presidente do Banco Central para discutir aspectos relacionados à Lei Magnitsky, legislação que trata de sanções contra violações de direitos humanos e corrupção. Segundo Moraes, as reuniões tiveram como foco esse tema e não mencionaram diretamente o Banco Master.\n\nO Banco Master tem sido alvo de investigações que levantam questionamentos sobre sua atuação e relação com o mundo político. O banco teria ocupado espaço deixado por outras instituições, como a Odebrecht, segundo análises de especialistas. O Banco Central, por sua vez, informou estar pronto para prestar esclarecimentos ao STF sobre o caso, embora tenha decidido não divulgar notas públicas sobre diálogos envolvendo o assunto.\n\nNo âmbito institucional, tramita em sigilo um processo no Tribunal de Contas da União (TCU) que apura possível omissão do Banco Central em relação ao Banco Master. O STF também tem sido chamado a se posicionar sobre a defesa do banco, diante das investigações em curso.\n\nAlém disso, o ministro Moraes indicou que não há previsão para concessão de prisão domiciliar ao ex-presidente Jair Bolsonaro neste momento, em meio a outras decisões judiciais que envolvem figuras políticas relevantes.",
    category: "Política",
    date: "23/12/2025",
    imageUrl: "/images/noticias/stf_plenario.jpg",
    hasLeftPerspective: true,
    leftPerspective: "Fontes de esquerda destacam que Moraes confirmou reuniões com o Banco Central para tratar da Lei Magnitsky, mas sem citar diretamente o Banco Master. Também ressaltam que o banco teria assumido espaço político deixado pela Odebrecht e que há discussões sobre o papel do Supremo na defesa da instituição. Além disso, apontam que Moraes indicou que Bolsonaro não terá prisão domiciliar em breve.",
    hasRightPerspective: true,
    rightPerspective: "Fontes de direita enfatizam que o processo sobre possível omissão do Banco Central no caso Master tramita em sigilo no TCU e que o BC optou por não divulgar notas públicas sobre o diálogo envolvendo Moraes. Defensores do ministro, como Gilmar Mendes, sustentam sua atuação no caso. Também destacam que Moraes afirmou que as reuniões foram focadas na Lei Magnitsky e que o Banco Central está pronto para prestar esclarecimentos ao STF.",
    attentionPoints: ["As informações sobre as reuniões entre Moraes e o Banco Central são apresentadas com ênfases diferentes conforme a fonte, podendo influenciar a percepção do leitor.", "O sigilo em processos no TCU e a decisão do Banco Central de não divulgar notas públicas limitam o acesso a detalhes completos do caso.", "A associação do Banco Master a questões políticas pode ser interpretada de formas distintas, dependendo do viés editorial das fontes.", "Comentários sobre figuras políticas, como o ex-presidente Bolsonaro, aparecem no contexto, mas não estão diretamente ligados ao caso Banco Master, podendo gerar confusão."],
    sources: ["UOL", "G1/Globo", "Revista Oeste", "Brasil Paralelo"],
    hasBiasDetected: true
  },
  {
    id: "general-heleno-inicia-cumprimento-de-prisao-domici",
    title: "General Heleno inicia cumprimento de prisão domiciliar",
    subtitle: "Decisão judicial permite que o general cumpra pena em casa, gerando diferentes interpretações na mídia",
    summary: "O general Heleno começou a cumprir prisão domiciliar nesta semana, conforme decisão judicial. A medida foi concedida após análise do Supremo Tribunal Federal (STF) e tem gerado debates sobre critérios e precedentes para esse tipo de benefício no sistema prisional brasileiro.",
    content: "O general Heleno, figura conhecida no cenário político e militar, iniciou o cumprimento de sua pena em regime domiciliar. A decisão foi tomada por instância judicial competente, que avaliou as condições de saúde e outros fatores humanitários para conceder o benefício.\n\nDados do sistema prisional indicam que apenas 0,6% dos presos no Brasil cumprem pena em prisão domiciliar, o que torna essa medida relativamente rara. Antes do caso de Heleno, o STF havia concedido prisão domiciliar humanitária para 20 pessoas e negado para 17, incluindo o ex-presidente Bolsonaro.\n\nA decisão envolvendo Heleno ocorre em um contexto de debates sobre os critérios para concessão de prisão domiciliar, especialmente em casos que envolvem figuras públicas e militares. O Supremo Tribunal Federal tem sido o órgão responsável por analisar esses pedidos, considerando aspectos legais e humanitários.\n\nA medida foi comunicada oficialmente e já está em vigor, com o general cumprindo a pena em sua residência, conforme as condições estabelecidas pela justiça.",
    category: "Política",
    date: "23/12/2025",
    imageUrl: "/images/noticias/stf_fachada.jpg",
    hasLeftPerspective: true,
    leftPerspective: "Fontes de esquerda destacam que o STF tem sido criterioso na concessão de prisão domiciliar, concedendo o benefício para um número limitado de casos humanitários e negando para outros, incluindo figuras como Bolsonaro. Apontam que a prisão domiciliar é uma exceção no sistema prisional brasileiro, aplicada a apenas 0,6% dos detentos.",
    hasRightPerspective: true,
    rightPerspective: "Veículos de direita enfatizam que o general Heleno já começou a cumprir prisão domiciliar, apresentando a medida como uma vitória ou avanço no caso do militar. Destacam o início efetivo do cumprimento da pena em casa, sem aprofundar nos critérios ou comparações com outros casos.",
    attentionPoints: ["A concessão de prisão domiciliar é um tema sensível e pode ser interpretado de formas distintas conforme o viés político.", "Dados estatísticos sobre a aplicação da prisão domiciliar ajudam a contextualizar a raridade do benefício, mas podem ser usados para reforçar narrativas divergentes.", "É importante considerar que decisões judiciais são fundamentadas em critérios legais e humanitários, que nem sempre são detalhados na cobertura midiática.", "A cobertura pode variar em ênfase e tom, dependendo da orientação editorial das fontes consultadas."],
    sources: ["UOL", "G1/Globo", "Revista Oeste"],
    hasBiasDetected: true
  },
  {
    id: "presidente-lula-assina-indulto-de-natal-excluindo-",
    title: "Presidente Lula assina indulto de Natal excluindo condenados pelo 8 de janeiro",
    subtitle: "Medida de clemência foi publicada em dezembro de 2025, abrangendo presos comuns e excluindo delatores e envolvidos nos atos de 8 de janeiro",
    summary: "No dia 23 de dezembro de 2025, o presidente Luiz Inácio Lula da Silva assinou o indulto de Natal, uma medida que concede perdão parcial a determinados presos no Brasil. A decisão foi publicada oficialmente e exclui pessoas condenadas por participação nos eventos de 8 de janeiro, bem como delatores. O indulto é uma prática tradicional no país, concedida anualmente pelo chefe do Executivo.",
    content: "O indulto de Natal é uma prerrogativa do presidente da República que concede perdão total ou parcial a presos, reduzindo penas ou extinguindo-as, geralmente em datas comemorativas. Em 2025, o presidente Lula assinou o decreto que regulamenta o benefício, definindo os critérios para a concessão do indulto natalino.\n\nDe acordo com o decreto, presos condenados por crimes comuns que atendam aos requisitos estabelecidos poderão ser beneficiados. No entanto, o texto exclui explicitamente os condenados por participação nos atos de 8 de janeiro, data marcada por manifestações e invasões a prédios públicos em Brasília, bem como delatores, que também não terão direito ao benefício.\n\nA medida foi publicada em meio a discussões políticas e sociais sobre a abrangência do indulto e seu impacto na segurança pública e na Justiça. O governo ressaltou que a decisão segue critérios legais e técnicos, buscando equilibrar a concessão do benefício com a manutenção da ordem e da responsabilização dos crimes mais graves.\n\nAlém do indulto, outras questões relacionadas ao período natalino, como direitos trabalhistas para quem atua durante as festas de fim de ano, também foram tema de orientações divulgadas por órgãos oficiais.",
    category: "Política",
    date: "23/12/2025",
    imageUrl: "/images/noticias/planalto.jpg",
    hasLeftPerspective: true,
    leftPerspective: "Fontes alinhadas à esquerda destacam que o presidente Lula assinou o indulto de Natal conforme a tradição, ressaltando a exclusão dos presos envolvidos nos atos de 8 de janeiro e dos delatores. A medida é apresentada como um ato de clemência que respeita os critérios legais e não beneficia aqueles ligados a crimes graves ou políticos.",
    hasRightPerspective: true,
    rightPerspective: "Veículos de direita enfatizam a exclusão dos condenados pelo 8 de janeiro do indulto, interpretando a medida como uma forma de manter a responsabilização dos envolvidos nos eventos. Também ressaltam que o indulto não foi ampliado para beneficiar delatores, apontando para uma postura de rigor na aplicação da Justiça.",
    attentionPoints: ["O indulto é uma medida tradicional que pode gerar interpretações políticas divergentes.", "A exclusão de determinados grupos, como os condenados pelo 8 de janeiro, é destacada por diferentes fontes com ênfases distintas.", "Fontes de diferentes espectros políticos podem enfatizar aspectos específicos do indulto para apoiar suas narrativas.", "É importante considerar o texto oficial do decreto para compreender os critérios e limitações do benefício."],
    sources: ["UOL", "G1/Globo", "Revista Oeste"],
    hasBiasDetected: true
  },
  {
    id: "gustavo-feliciano-assume-ministerio-do-turismo-apo",
    title: "Gustavo Feliciano assume Ministério do Turismo após saída de Sabino",
    subtitle: "Presidente Lula empossa novo ministro do Turismo em cerimônia realizada em Brasília",
    summary: "Na terça-feira, 23 de dezembro de 2025, o presidente Luiz Inácio Lula da Silva deu posse a Gustavo Feliciano como novo ministro do Turismo, em cerimônia realizada no Palácio do Planalto, em Brasília, após a saída do ex-ministro Sabino.",
    content: "O presidente Lula oficializou a nomeação de Gustavo Feliciano para o comando do Ministério do Turismo, substituindo Sabino, que deixou o cargo recentemente. A cerimônia contou com a presença de autoridades e aliados políticos.\n\nGustavo Feliciano é aliado do deputado Motta, que recentemente afirmou ao presidente Lula que o Congresso Nacional não faltou ao governo, em meio a tensões políticas recentes. A nomeação foi vista como um movimento para fortalecer a base governista no Legislativo.\n\nA transição no Ministério do Turismo ocorre em um momento de atenção ao setor, que busca retomar o crescimento após os impactos da pandemia e desafios econômicos. O novo ministro terá como desafio implementar políticas para fomentar o turismo nacional.\n\nA saída de Sabino e a posse de Feliciano foram acompanhadas de diferentes interpretações na mídia, refletindo a polarização política existente no país.",
    category: "Política",
    date: "23/12/2025",
    imageUrl: "/images/noticias/congresso_nacional.jpg",
    hasLeftPerspective: true,
    leftPerspective: "Veículos de esquerda destacam a posse de Gustavo Feliciano como um ato de fortalecimento da base aliada do presidente Lula, ressaltando a importância do Congresso para o governo e a continuidade das políticas públicas no setor de turismo.",
    hasRightPerspective: true,
    rightPerspective: "Fontes de direita enfatizam a substituição de Sabino por Feliciano como uma mudança administrativa necessária, mencionando a transição como um fato político relevante, sem aprofundar em avaliações sobre o impacto das nomeações.",
    attentionPoints: ["As fontes apresentam diferentes ênfases na cobertura, com veículos de esquerda focando na articulação política e os de direita na mudança administrativa.", "Algumas manchetes utilizam termos como 'novela' ou 'rusgas', que podem sugerir conflitos internos, mas o conteúdo oficial destaca a normalidade do processo de posse.", "O leitor deve considerar que a polarização política pode influenciar a interpretação dos fatos apresentados nas diferentes fontes."],
    sources: ["UOL", "G1/Globo", "Revista Oeste"],
    hasBiasDetected: true
  },
  {
    id: "polemica-envolvendo-havaianas-gera-pedidos-de-boic",
    title: "Polêmica envolvendo Havaianas gera pedidos de boicote e movimenta diferentes grupos políticos",
    subtitle: "A marca Havaianas tem sido alvo de campanhas de boicote por parte de grupos políticos, com repercussões no mercado e na militância",
    summary: "Em dezembro de 2025, a marca brasileira Havaianas passou a ser foco de pedidos de boicote por políticos e grupos de diferentes espectros ideológicos, repercutindo em ações na bolsa e mobilização de militantes em redes sociais no Brasil.",
    content: "A campanha de boicote à Havaianas ganhou força após declarações e posicionamentos públicos que motivaram reações de políticos e grupos organizados. A empresa Alpargatas, responsável pela marca, registrou queda em suas ações na bolsa de valores em meio à repercussão do caso.\n\nDe um lado, políticos alinhados ao bolsonarismo utilizaram o episódio para mobilizar sua base de apoio, buscando reforçar a militância após recentes derrotas eleitorais. A iniciativa incluiu chamadas para o boicote como forma de protesto contra o que consideram posicionamentos contrários aos seus valores.\n\nPor outro lado, a polêmica também foi interpretada por grupos e veículos de direita como um exemplo de suposta influência da esquerda em marcas populares, citando episódios envolvendo personalidades públicas e a associação da marca a causas políticas.\n\nO debate em torno da Havaianas reflete a crescente interseção entre consumo, política e ativismo, com impactos tanto na percepção pública da marca quanto em seu desempenho econômico.",
    category: "Economia",
    date: "23/12/2025",
    imageUrl: "/images/noticias/havaianas.jpg",
    hasLeftPerspective: true,
    leftPerspective: "Fontes de esquerda destacam que o boicote à Havaianas é uma reação política promovida por grupos bolsonaristas para mobilizar militância após derrotas eleitorais, ressaltando que a iniciativa teve impacto na queda das ações da Alpargatas, mas questionam a efetividade do boicote no consumo geral.",
    hasRightPerspective: true,
    rightPerspective: "Fontes de direita interpretam a polêmica como um conflito ideológico, apontando que a marca e suas associações estariam alinhadas a causas de esquerda, e usam o episódio para criticar o que chamam de 'lacração' em produtos populares, destacando casos envolvendo figuras públicas como Fernanda Torres.",
    attentionPoints: ["As informações sobre o boicote são fortemente influenciadas por posicionamentos políticos, o que pode afetar a interpretação dos fatos.", "A queda nas ações da Alpargatas pode estar relacionada a múltiplos fatores econômicos além do boicote.", "O uso do episódio para mobilização política pode ampliar a polarização em torno de uma marca comercial.", "É importante considerar que campanhas de boicote nem sempre refletem mudanças significativas no comportamento do consumidor."],
    sources: ["UOL", "G1/Globo", "Revista Oeste"],
    hasBiasDetected: true
  },
  {
    id: "inflacao-registra-alta-em-2025-enquanto-mercado-aj",
    title: "Inflação registra alta em 2025 enquanto mercado ajusta previsões econômicas",
    subtitle: "Preços ao consumidor sobem em dezembro e no ano, enquanto mercado financeiro revisa projeções e despesas públicas crescem",
    summary: "Em dezembro de 2025, o índice de preços ao consumidor (IPCA-15) registrou alta de 0,25%, fechando o ano com aumento acumulado de 4,41% no Brasil. Ao mesmo tempo, o mercado financeiro reduziu pela sexta semana consecutiva a previsão de inflação para o próximo período, enquanto despesas públicas apresentaram crescimento acima da inflação. Esses dados foram divulgados em diferentes fontes nacionais, refletindo o cenário econômico atual.",
    content: "O Instituto Brasileiro de Geografia e Estatística (IBGE) divulgou que o IPCA-15, considerado uma prévia da inflação oficial, subiu 0,25% em dezembro de 2025. O índice acumulado no ano atingiu 4,41%, indicando um aumento nos preços ao consumidor ao longo do período.\n\nNo mercado financeiro, o relatório Focus, que reúne projeções de analistas, apontou uma redução na expectativa de inflação pela sexta semana consecutiva. Essa tendência sugere uma percepção de desaceleração da pressão inflacionária para os próximos meses.\n\nPor outro lado, dados sobre as despesas públicas indicam que os gastos do governo cresceram acima da inflação, o que tem gerado debates sobre a sustentabilidade fiscal e os impactos na economia. A análise desses indicadores é fundamental para compreender o cenário macroeconômico do país.\n\nNo ambiente financeiro, o dólar apresentou recuo, enquanto a bolsa de valores brasileira avançou, influenciada por indicadores econômicos nacionais e internacionais, como a prévia da inflação no Brasil e dados do Produto Interno Bruto (PIB) dos Estados Unidos.",
    category: "Economia",
    date: "23/12/2025",
    imageUrl: "/images/noticias/b3_touro.jpg",
    hasLeftPerspective: true,
    leftPerspective: "Fontes com viés progressista destacam a alta do IPCA-15 em dezembro e o acumulado anual como indicadores importantes do comportamento dos preços ao consumidor, ressaltando a influência desses dados no mercado financeiro, que reagiu com queda do dólar e alta da bolsa. Também mencionam ações políticas e econômicas que impactam o cenário, como movimentos de boicote e a dinâmica do mercado.",
    hasRightPerspective: true,
    rightPerspective: "Veículos com orientação conservadora enfatizam a redução contínua das projeções de inflação pelo mercado, interpretando isso como sinal de controle da pressão inflacionária. Além disso, apontam o crescimento das despesas públicas acima da inflação como um fator preocupante, associando-o à gestão fiscal do governo atual.",
    attentionPoints: ["As fontes apresentam diferentes ênfases nos dados econômicos, o que pode influenciar a interpretação do cenário.", "A redução das projeções de inflação pelo mercado não elimina a alta acumulada observada no IPCA-15 durante o ano.", "O crescimento das despesas públicas é apresentado com diferentes interpretações quanto ao seu impacto econômico.", "Movimentos políticos e econômicos, como boicotes ou ações governamentais, podem afetar indicadores financeiros e devem ser analisados com cautela."],
    sources: ["UOL", "G1/Globo", "Revista Oeste"],
    hasBiasDetected: true
  },
  {
    id: "governo-libera-saque-do-fgts-para-141-milhoes-de-t",
    title: "Governo libera saque do FGTS para 14,1 milhões de trabalhadores que aderiram ao saque-aniversário",
    subtitle: "Prazo para saque do abono salarial termina no dia 29; trabalhadores devem verificar direito ao benefício",
    summary: "O governo federal liberou o saque do Fundo de Garantia do Tempo de Serviço (FGTS) para 14,1 milhões de trabalhadores que optaram pelo saque-aniversário. O prazo para o saque do abono salarial, benefício relacionado ao PIS/Pasep, termina no dia 29 de dezembro. As informações são válidas para trabalhadores de todo o Brasil e envolvem procedimentos realizados por meio das plataformas oficiais do governo.",
    content: "O FGTS é um direito trabalhista que permite ao trabalhador acumular recursos durante o período de contrato de trabalho. Recentemente, o governo autorizou o saque do FGTS para os trabalhadores que aderiram ao chamado saque-aniversário, modalidade que permite a retirada anual de parte do saldo da conta do FGTS no mês do aniversário do trabalhador.\n\nSegundo dados oficiais, cerca de 14,1 milhões de trabalhadores estão aptos a realizar o saque neste momento. O valor disponível varia conforme o saldo acumulado na conta vinculada ao FGTS de cada trabalhador. A liberação do saque visa proporcionar maior liquidez e acesso a recursos financeiros para os beneficiários.\n\nAlém do FGTS, o prazo para o saque do abono salarial, benefício pago a trabalhadores que atendem a determinados critérios de renda e tempo de serviço, está se encerrando no dia 29 de dezembro. O abono é destinado a trabalhadores que tenham recebido até dois salários mínimos mensais em média no ano-base e que tenham exercido atividade remunerada por pelo menos 30 dias no ano anterior.\n\nOs trabalhadores interessados devem consultar os canais oficiais do governo, como o aplicativo FGTS e os sites da Caixa Econômica Federal, para verificar o direito ao saque e realizar os procedimentos necessários dentro dos prazos estabelecidos.",
    category: "Economia",
    date: "23/12/2025",
    imageUrl: "/images/noticias/banco_central.jpg",
    hasLeftPerspective: true,
    leftPerspective: "Fontes como UOL e G1 destacam a liberação do saque do FGTS como uma medida que beneficia milhões de trabalhadores, ressaltando a importância do acesso a esses recursos para a população de baixa e média renda. Também enfatizam o prazo final para o saque do abono salarial, orientando os trabalhadores a verificarem seus direitos e realizarem o saque dentro do prazo.",
    hasRightPerspective: false,
    rightPerspective: null,
    attentionPoints: ["As informações sobre o saque do FGTS e do abono salarial devem ser confirmadas nos canais oficiais para evitar golpes e fraudes.", "A adesão ao saque-aniversário implica em regras específicas que podem afetar o saldo disponível para saque em outras situações, como demissão sem justa causa.", "A ausência de notícias de fontes de direita pode indicar falta de cobertura ou posicionamento sobre o tema, o que deve ser considerado ao avaliar o panorama completo.", "O prazo para saque do abono salarial é uma informação sensível para trabalhadores que dependem desse benefício, sendo importante observar as datas para não perder o direito."],
    sources: ["UOL", "G1/Globo"],
    hasBiasDetected: false
  },
  {
    id: "eduardo-bolsonaro-pode-perder-passaporte-apos-cass",
    title: "Eduardo Bolsonaro pode perder passaporte após cassação de mandato",
    subtitle: "Possibilidade de cancelamento do passaporte brasileiro de Eduardo Bolsonaro é discutida após decisão sobre seu mandato parlamentar",
    summary: "Após a cassação do mandato de Eduardo Bolsonaro, deputado federal, surgiu a possibilidade de que ele possa perder o passaporte brasileiro. A situação está sendo analisada conforme as normas legais vigentes no Brasil.",
    content: "Eduardo Bolsonaro, deputado federal, teve seu mandato cassado recentemente, conforme informações divulgadas por fontes alinhadas à direita. Em decorrência dessa decisão, há discussões sobre a possibilidade de cancelamento de seu passaporte brasileiro.\n\nA legislação brasileira prevê que, em determinadas situações, a validade do passaporte pode ser afetada por questões relacionadas ao exercício de mandato parlamentar, embora não haja uma regra automática para a perda do documento em casos de cassação.\n\nAté o momento, não foram divulgadas informações oficiais por órgãos governamentais ou autoridades competentes confirmando a perda do passaporte de Eduardo Bolsonaro. A situação permanece em análise e pode depender de procedimentos administrativos futuros.\n\nNão foram encontradas reportagens ou posicionamentos de veículos de comunicação de esquerda sobre o tema, o que limita a compreensão completa das diferentes perspectivas sobre o assunto.",
    category: "Política",
    date: "23/12/2025",
    imageUrl: "/images/noticias/congresso_nacional.jpg",
    hasLeftPerspective: false,
    leftPerspective: null,
    hasRightPerspective: true,
    rightPerspective: "Fontes alinhadas à direita, como a Revista Oeste e Brasil Paralelo, noticiam que Eduardo Bolsonaro pode perder o passaporte brasileiro em decorrência da cassação de seu mandato, destacando a possibilidade como consequência da decisão.",
    attentionPoints: ["A ausência de reportagens em veículos de esquerda pode indicar falta de cobertura ou interesse no tema, o que limita a visão plural sobre o assunto.", "Fontes de direita apresentam a possibilidade de perda do passaporte como uma consequência direta da cassação, mas não há confirmação oficial até o momento.", "É importante considerar que a legislação sobre passaportes e mandatos parlamentares pode ser complexa e não necessariamente implica em cancelamento automático do documento.", "O leitor deve estar atento a possíveis interpretações parciais e aguardar posicionamentos oficiais para uma compreensão completa."],
    sources: ["Revista Oeste", "Brasil Paralelo"],
    hasBiasDetected: false
  }
];
