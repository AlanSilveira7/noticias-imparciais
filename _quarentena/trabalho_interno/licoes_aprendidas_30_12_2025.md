# Lições Aprendidas — Rotina de Atualização 30/12/2025

## Resumo do Dia

- **Notícias publicadas:** 30 (de 7 para 30)
- **Correções de imagem:** 6
- **Correções de selo/texto:** 14
- **Ciclos executados:** 4 (1+2+10+10)

---

## Erros Identificados e Corrigidos

### 1. Imagens com Marca D'Água

**Problema:** 6 imagens foram publicadas com marca d'água visível (principalmente "alamy")

**Notícias afetadas:**
- Mercado Reduz Projeção de Inflação (Banco Central)
- Correios Precisarão de R$ 8 Bilhões
- Aeronautas Aprovam Acordo (avião com URL visível)
- Calendário de Feriados 2026
- Espumante, Moscatel e Frisante
- Ibovespa Dispara 33%

**Lição:** Verificar VISUALMENTE cada imagem antes de usar, mesmo que venha de busca automática. Marcas d'água podem estar em cantos ou sobrepostas ao conteúdo.

**Ação preventiva:** Criar checklist de verificação de imagem antes da publicação.

---

### 2. Selo Incorreto (Viés Detectado sem Cobertura de Ambos os Lados)

**Problema:** Notícias receberam selo "Viés Detectado" mesmo quando apenas um lado político cobriu o tema.

**Notícias afetadas (7):**
- Estado de Saúde de Bolsonaro
- Desemprego Cai a 5,2%
- Mega da Virada Prêmio Recorde
- Meta Compra Manus
- Eduardo Bolsonaro passaporte
- Calendário de Feriados 2026
- Ibovespa Dispara 33%

**Lição:** O selo "Viés Detectado" só deve ser usado quando:
1. Ambos os lados (esquerda E direita) cobriram o tema
2. Há diferenças claras de perspectiva entre os lados

**Regra corrigida:**
| Cenário | Selo Correto |
|:---|:---:|
| Apenas fontes de esquerda | **Verificada** |
| Apenas fontes de direita | **Verificada** |
| Ambos os lados, perspectivas similares | **Verificada** |
| Ambos os lados, perspectivas diferentes | **Viés Detectado** |

---

### 3. Seção "Fontes de Direita" Vazia

**Problema:** 7 notícias foram publicadas com a seção "Fontes de direita" completamente vazia.

**Lição:** Quando não há cobertura de um dos lados, SEMPRE adicionar o texto padrão:
> "Não foi encontrada cobertura jornalística sobre este tema nos portais de [direita/esquerda] consultados."

---

### 4. Tempo Verbal Incorreto

**Problema:** A primeira notícia (Daniel Vorcaro) usou tempo verbal no passado para um evento que ainda iria acontecer.

**Lição:** Verificar a data/hora do evento antes de definir o tempo verbal:
- Evento futuro → Tempo presente/futuro ("colhe", "tem início", "será")
- Evento passado → Tempo passado ("colheu", "teve início", "foi")

---

### 5. Imagem Não Contextual

**Problema:** A primeira notícia usou imagem do Palácio do Planalto para uma notícia sobre depoimento na PF.

**Lição:** A imagem deve representar o tema específico da notícia:
- Depoimento na PF → Sede da Polícia Federal
- Votação no Congresso → Plenário da Câmara/Senado
- Estatais → Fachada da empresa específica (ex: Correios)

---

## Padrões de Qualidade — Notícia Exemplo (Estatais Federais)

### Estrutura Ideal

| Elemento | Padrão |
|:---|:---|
| **Título** | Factual + dado numérico concreto |
| **Subtítulo** | Contextualiza o dado principal |
| **Lead** | Responde O quê, Quando, Quanto, Fonte |
| **Corpo** | 3-4 parágrafos com contexto histórico e impacto |
| **Esquerda** | Perspectiva técnica/justificativa |
| **Direita** | Perspectiva crítica/comparativa |
| **Pontos de Atenção** | 2-3 itens objetivos |
| **Imagem** | Contextual, sem marca d'água |

### O Que Faz uma Notícia "Viés Detectado" de Qualidade

1. **Perspectivas claramente distintas** — O leitor consegue identificar facilmente a diferença de abordagem
2. **Sem julgamento** — Apresenta ambos os lados de forma neutra
3. **Contexto histórico** — Compara com dados anteriores
4. **Impacto explicado** — O leitor entende as consequências

---

## Checklist para Próximas Rotinas

### Antes de Publicar Cada Notícia

- [ ] Imagem verificada visualmente (sem marca d'água)
- [ ] Imagem é contextual ao tema específico
- [ ] Tempo verbal correto (verificar data/hora do evento)
- [ ] Seção "Fontes de esquerda" preenchida
- [ ] Seção "Fontes de direita" preenchida (ou texto padrão)
- [ ] Selo correto:
  - Verificada: apenas um lado cobriu OU perspectivas similares
  - Viés Detectado: ambos os lados com perspectivas diferentes
- [ ] Título com dado numérico (quando aplicável)
- [ ] Lead responde O quê, Quando, Quanto, Fonte

### Ao Final do Ciclo

- [ ] Verificar todas as notícias no site
- [ ] Confirmar que imagens estão carregando
- [ ] Confirmar que selos estão corretos
- [ ] Contar total de notícias publicadas

---

## Otimizações para Meta de 10 Notícias/Dia

### Fluxo Otimizado

1. **Coleta (30 min):** Acessar G1 e selecionar 10 notícias novas
2. **Busca (45 min):** Buscar cobertura nos 4 portais para cada tema
3. **Redação (60 min):** Processar e redigir as 10 notícias
4. **Imagens (30 min):** Selecionar e verificar imagens contextuais
5. **Publicação (15 min):** Executar script e verificar no site
6. **Validação (15 min):** Revisar todas as notícias publicadas

**Tempo estimado:** ~3 horas para 10 notícias

### Priorização de Temas

1. **Alta prioridade:** Temas com cobertura em ambos os lados (geram "Viés Detectado" de qualidade)
2. **Média prioridade:** Temas factuais importantes (economia, política)
3. **Baixa prioridade:** Temas de serviço/curiosidade (feriados, loteria)

### Acervo de Imagens

Manter acervo organizado por categoria:
- `economia/` — Banco Central, B3, dólar, empresas
- `politica/` — Congresso, STF, Planalto
- `seguranca/` — PF, polícias
- `saude/` — hospitais, equipamentos
- `legislativo/` — Câmara, Senado
