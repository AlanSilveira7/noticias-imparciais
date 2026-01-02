# Roadmap de Implementação: Axia News

**Objetivo:** Detalhar o passo a passo das atividades necessárias para desenvolver, lançar e monetizar o portal "Axia News", atingindo a meta de R$ 100/dia de receita.

**Última atualização:** 23 de dezembro de 2025

---

## Fase 1: Fundação e Configuração do Projeto ✅ CONCLUÍDA

O objetivo desta fase é estabelecer as bases do projeto, incluindo a identidade da marca e a estrutura técnica inicial.

| Atividade | Descrição | Status |
| :--- | :--- | :---: |
| **1.1. Definição da Marca e Domínio** | Brainstorming de nomes e verificação de disponibilidade de domínios. Escolhido: "Axia News" com domínio `axianews.com`. | ✅ Concluído |
| **1.2. Design do Logotipo** | Criado logotipo com símbolo de balança da justiça, versão principal, alternativa (monograma NI) e ícone para favicon/app. | ✅ Concluído |
| **1.3. Slogan da Marca** | Definido: "Os fatos, sem filtro." | ✅ Concluído |
| **1.4. Identidade Visual** | Paleta de cores (Navy Blue, Slate Gray, Off White), tipografia (Inter) e mockups de aplicação criados. | ✅ Concluído |

---

## Fase 2: Desenvolvimento do Agente de IA ✅ CONCLUÍDA

Esta é a fase mais crítica, onde o coração do negócio foi construído: o sistema de inteligência artificial para processamento das notícias.

| Atividade | Descrição | Status |
| :--- | :--- | :---: |
| **2.1. Módulo de Coleta (Scraper)** | Desenvolvido scraper para 4 fontes: UOL, G1/Globo (esquerda), Revista Oeste, Brasil Paralelo (direita). Coletadas 52 notícias. | ✅ Concluído |
| **2.2. Módulo de Análise de Viés (IA)** | Criado `analisador_vies.py` que identifica fatos, classifica viés, extrai ênfases e omissões. | ✅ Concluído |
| **2.3. Módulo de Síntese Imparcial (IA)** | Desenvolvido `sintetizador_imparcial.py` que gera notícias neutras com seções "O Que Diz Cada Lado" e "Pontos de Atenção". | ✅ Concluído |
| **2.4. Orquestrador do Agente** | Módulo `coletor_noticias.py` integra coleta, análise e síntese em fluxo único. | ✅ Concluído |
| **2.5. Testes e Validação** | Geradas 12 notícias imparciais completas sobre temas reais, validadas e refinadas. | ✅ Concluído |

---

## Fase 3: Construção da Plataforma - Website MVP ✅ CONCLUÍDA

Com o agente de IA validado, construímos a interface onde os leitores consumirão o conteúdo.

| Atividade | Descrição | Status |
| :--- | :--- | :---: |
| **3.1. Design da Interface (UI/UX)** | Layout clean estilo Globo.com: fundo branco, notícias com fotos e manchetes em destaque. | ✅ Concluído |
| **3.2. Desenvolvimento do Frontend** | Site desenvolvido em React + Tailwind CSS com páginas: Home, Artigo, Sobre, Busca, Política, Economia. | ✅ Concluído |
| **3.3. Estrutura de Dados** | Formato JSON definido para notícias com título, texto, análise de viés, perspectivas e fontes. | ✅ Concluído |
| **3.4. Integração Conteúdo-Site** | Site lê dados de notícias e exibe dinamicamente com componentes reutilizáveis. | ✅ Concluído |
| **3.5. Funcionalidades Avançadas** | Busca funcional, páginas de categoria, widget de cotações, notícias relacionadas, paginação. | ✅ Concluído |
| **3.6. Imagens Relevantes** | Imagens de bancos gratuitos e domínio público para cada notícia. | ✅ Concluído |

---

## Fase 4: Lançamento e Operação Inicial ✅ CONCLUÍDA

Nesta fase, o projeto foi colocado no ar e o ciclo de operação foi validado.

| Atividade | Descrição | Status |
| :--- | :--- | :---: |
| **4.1. Configuração da Automação** | Adiado para após validação de custos. | ⏸️ Pausado |
| **4.2. Registro do Domínio** | Adiado para após validação de viabilidade financeira. | ⏸️ Pausado |
| **4.3. Deploy do Website** | Site publicado no domínio Manus (*.manus.space). | ✅ Concluído |
| **4.4. Publicação das Primeiras Notícias** | 12 notícias imparciais publicadas no ciclo de teste. | ✅ Concluído |
| **4.5. Configuração de Analytics** | Analytics já integrado via Manus (Umami). | ✅ Concluído |
| **4.6. Criação do Perfil no Instagram** | Pendente para Fase 5. | ⏳ A Fazer |

---

## Fase 5: Monetização — Meta R$ 100/dia 🔄 EM ANDAMENTO

**Objetivo:** Implementar estratégias de monetização para atingir receita de R$ 100/dia (R$ 3.000/mês) em 6 meses.

### Etapa 5.1: Fundação da Monetização (Semanas 1-4)

| Atividade | Descrição | Status |
| :--- | :--- | :---: |
| **5.1.1. Cadastro no Google AdSense** | Criar conta, submeter site para aprovação (1-2 semanas). | ⏳ A Fazer |
| **5.1.2. Implementar espaços de anúncio** | Adicionar 3-4 posições de banner no site (header, sidebar, in-article). | ⏳ A Fazer |
| **5.1.3. Cadastro no Google News** | Submeter site ao Google News Publisher Center para indexação. | ⏳ A Fazer |
| **5.1.4. Otimização para Google Discover** | Configurar meta tags (max-image-preview:large), imagens 1200px+. | ⏳ A Fazer |
| **5.1.5. Criar sitemap de notícias** | Gerar sitemap XML específico para news. | ⏳ A Fazer |
| **5.1.6. Criar perfil no Instagram** | @axianews com bio, foto de perfil e identidade visual. | ⏳ A Fazer |
| **5.1.7. Criar canal no Telegram** | Canal para distribuição de manchetes diárias. | ⏳ A Fazer |
| **5.1.8. Criar página no APOIA.se** | Configurar planos de apoio (R$ 5, R$ 10, R$ 20/mês). | ⏳ A Fazer |
| **5.1.9. Estabelecer rotina de publicação** | Mínimo 10 notícias/dia, todos os dias. | ⏳ A Fazer |
| **5.1.10. Criar templates para Instagram** | Posts e stories padronizados com identidade visual. | ⏳ A Fazer |

### Etapa 5.2: Expansão de Canais (Semanas 5-8)

| Atividade | Descrição | Status |
| :--- | :--- | :---: |
| **5.2.1. Cadastro no MGID** | Mídia nativa para sites com menor volume de tráfego. | ⏳ A Fazer |
| **5.2.2. Implementar widget de mídia nativa** | Bloco "Leia também" no final das notícias. | ⏳ A Fazer |
| **5.2.3. Criar newsletter semanal** | Resumo das principais notícias da semana. | ⏳ A Fazer |
| **5.2.4. Criar grupo no WhatsApp** | Comunidade de leitores para engajamento. | ⏳ A Fazer |
| **5.2.5. Otimizar SEO das notícias** | Títulos, meta descriptions, URLs amigáveis. | ⏳ A Fazer |
| **5.2.6. Criar página "Anuncie"** | Mídia kit com preços, formatos e dados de audiência. | ⏳ A Fazer |
| **5.2.7. Prospectar anunciantes** | E-mails para empresas do nicho (tecnologia, educação, consultorias). | ⏳ A Fazer |
| **5.2.8. Analisar métricas** | Google Analytics, Search Console, ajustar estratégia. | ⏳ A Fazer |

### Etapa 5.3: Otimização e Escala (Semanas 9-12)

| Atividade | Descrição | Status |
| :--- | :--- | :---: |
| **5.3.1. Testar posições de anúncios** | A/B testing para maximizar CTR e receita. | ⏳ A Fazer |
| **5.3.2. Implementar links de afiliados** | Amazon, Hotmart, cursos relacionados. | ⏳ A Fazer |
| **5.3.3. Criar conteúdo evergreen** | Artigos de fundo sobre política e economia. | ⏳ A Fazer |
| **5.3.4. Expandir fontes de notícias** | Adicionar Folha, Estadão, Gazeta do Povo. | ⏳ A Fazer |
| **5.3.5. Automatizar publicação no Instagram** | Agendamento de posts via ferramentas. | ⏳ A Fazer |
| **5.3.6. Avaliar Taboola/Outbrain** | Se atingir 500k pageviews/mês. | ⏳ A Fazer |
| **5.3.7. Revisar e ajustar estratégia** | Análise de ROI por canal de receita. | ⏳ A Fazer |

### Etapa 5.4: Consolidação (Meses 4-6)

| Atividade | Descrição | Status |
| :--- | :--- | :---: |
| **5.4.1. Fechar primeiro anunciante direto** | Meta: R$ 500/mês em venda direta. | ⏳ A Fazer |
| **5.4.2. Atingir 500 seguidores no Instagram** | Crescimento orgânico consistente. | ⏳ A Fazer |
| **5.4.3. Atingir 30 apoiadores no APOIA.se** | Meta: R$ 300/mês em apoio recorrente. | ⏳ A Fazer |
| **5.4.4. Atingir 30.000 pageviews/mês** | Marco de audiência para monetização. | ⏳ A Fazer |
| **5.4.5. Atingir R$ 100/dia de receita** | META FINAL do plano de monetização. | ⏳ A Fazer |

---

## Resumo do Progresso

| Fase | Status | Progresso |
| :--- | :---: | :---: |
| Fase 1: Fundação e Configuração | ✅ Concluída | 4/4 (100%) |
| Fase 2: Desenvolvimento do Agente de IA | ✅ Concluída | 5/5 (100%) |
| Fase 3: Construção do Website MVP | ✅ Concluída | 6/6 (100%) |
| Fase 4: Lançamento e Operação | ✅ Concluída | 4/6 (67%) |
| Fase 5: Monetização | 🔄 Em Andamento | 0/24 (0%) |
| **TOTAL** | — | **19/45 (42%)** |

---

## Metas de Receita por Mês

| Mês | Pageviews/Dia | Receita/Dia | Receita/Mês | Status |
| :---: | :---: | :---: | :---: | :---: |
| Mês 1 | 50-100 | R$ 0-2 | R$ 0-50 | ⏳ |
| Mês 2 | 150-300 | R$ 5-10 | R$ 150-300 | ⏳ |
| Mês 3 | 400-600 | R$ 15-25 | R$ 450-750 | ⏳ |
| Mês 4 | 700-900 | R$ 30-50 | R$ 900-1.500 | ⏳ |
| Mês 5 | 1.000-1.200 | R$ 60-80 | R$ 1.800-2.400 | ⏳ |
| **Mês 6** | **1.250+** | **R$ 100** | **R$ 3.000** | 🎯 META |

---

## Próximas Atividades Prioritárias

1. **5.1.1. Cadastro no Google AdSense** — Iniciar processo de aprovação
2. **5.1.3. Cadastro no Google News** — Aumentar visibilidade
3. **5.1.6. Criar perfil no Instagram** — Estabelecer presença social
4. **5.1.9. Estabelecer rotina de publicação** — 10 notícias/dia

---

## Arquivos e Entregas Produzidos

### Documentação
- `/home/ubuntu/axia-news/documentacao/plano_de_negocio_axia_news.md` — Plano de negócio completo
- `/home/ubuntu/axia-news/documentacao/roadmap_axia_news.md` — Este roadmap
- `/home/ubuntu/axia-news/documentacao/PLANO_MONETIZACAO_AXIA_NEWS.md` — Plano detalhado de monetização

### Identidade Visual
- `/home/ubuntu/axia-news/assets/logo_principal.png`
- `/home/ubuntu/axia-news/assets/logo_alternativo.png`
- `/home/ubuntu/axia-news/assets/logo_icone.png`
- `/home/ubuntu/axia-news/assets/identidade_visual.md`

### Módulos de IA
- `/home/ubuntu/axia-news/scraper/coletor_noticias.py` — Módulo de coleta
- `/home/ubuntu/axia-news/scraper/analisador_vies.py` — Análise de viés
- `/home/ubuntu/axia-news/scraper/sintetizador_imparcial.py` — Síntese imparcial
- `/home/ubuntu/axia-news/scraper/gerar_noticias_lote.py` — Geração em lote

### Website
- `/home/ubuntu/axia-news/` — Projeto web completo (React + Tailwind)
