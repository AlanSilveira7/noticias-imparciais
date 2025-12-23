# Contexto do Projeto: Notícias Imparciais

**Data:** 24 de dezembro de 2025  
**Status:** Site publicado e funcional

---

## 1. O Que É Este Projeto

O **Notícias Imparciais** é um portal de notícias sobre política e economia brasileiro que utiliza inteligência artificial para produzir conteúdo jornalístico imparcial. O diferencial do projeto é coletar notícias de fontes com diferentes vieses editoriais (esquerda e direita), analisar as abordagens e gerar uma versão neutra e factual dos acontecimentos.

### Proposta de Valor

> "Os fatos, sem filtro."

### URL do Site Publicado

O site está publicado na Manus no projeto **"Site de Notícias Imparciais"** (https://imparcial.manus.space/).

---

## 2. Objetivo do Negócio

O objetivo é criar um portal de notícias que gere receita passiva através de publicidade, permitindo ao dono gerenciá-lo em paralelo com seu emprego atual.

### Meta de Receita

**R$ 100/dia** (equivalente a R$ 3.000/mês)

### Premissas

- O negócio precisa rodar de forma automatizada
- Custo mínimo de operação (único investimento: assinatura Manus)
- Crescimento orgânico e progressivo

---

## 3. O Que Já Foi Desenvolvido

### 3.1. Identidade Visual

| Item | Status | Descrição |
| :--- | :---: | :--- |
| Nome | ✅ | Notícias Imparciais |
| Slogan | ✅ | "Os fatos, sem filtro." |
| Logotipo | ✅ | 3 versões (principal, alternativo, ícone) |
| Paleta de cores | ✅ | Navy Blue (#1A365D), Branco, Cinza |
| Domínio | ⏳ | noticiasimparciais.com.br (disponível, não registrado) |

### 3.2. Sistema de Coleta e Análise (Agente de IA)

O sistema coleta notícias de 4 fontes com vieses editoriais distintos:

| Fonte | Viés | Status |
| :--- | :--- | :---: |
| UOL | Esquerda | ✅ Funcional |
| G1/Globo | Esquerda | ✅ Funcional |
| Revista Oeste | Direita | ✅ Funcional |
| Brasil Paralelo | Direita | ✅ Funcional |

O sistema possui 3 módulos principais:

1. **Coletor** — Extrai notícias dos sites via navegador automatizado
2. **Analisador de Viés** — Identifica fatos, opiniões e vieses editoriais
3. **Sintetizador** — Gera versão imparcial da notícia

### 3.3. Website

| Característica | Descrição |
| :--- | :--- |
| Stack | React 19 + Tailwind CSS 4 + TypeScript |
| Design | Clean, estilo Globo.com, fundo branco |
| Páginas | Home, Artigo, Sobre, Busca, Política, Economia |
| Notícias | 12 notícias imparciais publicadas |
| Funcionalidades | Busca, categorias, widget de cotações, paginação |

### 3.4. Funcionalidades Especiais do Site

O site possui diferenciais que outros portais não têm:

| Funcionalidade | Descrição |
| :--- | :--- |
| Indicador de Viés | Badge que mostra quando viés foi detectado |
| "O Que Diz Cada Lado" | Seção que mostra perspectivas de esquerda e direita |
| Pontos de Atenção | Alertas sobre limitações ou vieses nas fontes |
| Fontes Consultadas | Transparência sobre de onde veio a informação |

---

## 4. Fluxo de Operação Atual

O ciclo de publicação de notícias funciona da seguinte forma:

```
1. COLETA
   Acessar UOL, G1, Revista Oeste, Brasil Paralelo
   Extrair manchetes, textos e links de Política e Economia
   
2. AGRUPAMENTO
   Identificar notícias sobre o mesmo tema
   Separar temas com cobertura múltipla (esquerda + direita)
   
3. ANÁLISE DE VIÉS
   Para cada tema com cobertura múltipla:
   - Identificar fatos objetivos
   - Identificar opiniões e ênfases de cada lado
   - Classificar viés (esquerda, direita, neutro)
   
4. SÍNTESE IMPARCIAL
   Gerar notícia neutra baseada nos fatos
   Incluir seção "O Que Diz Cada Lado"
   Adicionar "Pontos de Atenção" quando necessário
   
5. PUBLICAÇÃO
   Atualizar arquivo news.ts com as novas notícias
   Buscar imagens adequadas (bancos gratuitos ou domínio público)
   Publicar no site
```

---

## 5. Arquivos do Projeto (Incluídos no Pacote)

Todos os arquivos mencionados abaixo estão incluídos no arquivo compactado `PACOTE_NOTICIAS_IMPARCIAIS_COMPLETO.tar.gz`.

### 5.1. Código do Site

Pasta: `pacote_completo/site/`

```
site/
├── client/
│   ├── src/
│   │   ├── App.tsx              # Rotas
│   │   ├── index.css            # Estilos globais
│   │   ├── components/          # Header, Footer, etc.
│   │   ├── pages/               # Home, Article, About, etc.
│   │   └── data/news.ts         # Banco de notícias
│   └── public/images/           # Imagens do site
├── package.json
└── vite.config.ts
```

### 5.2. Scripts Python (Agente de IA)

Pasta: `pacote_completo/scraper/`

```
scraper/
├── coletor_noticias.py          # Coleta de notícias
├── analisador_vies.py           # Análise de viés com IA
├── sintetizador_imparcial.py    # Geração de notícias imparciais
├── gerar_noticias_lote.py       # Geração em lote
├── agrupar_temas.py             # Agrupamento por tema
└── converter_para_site.py       # Conversão para formato do site
```

### 5.3. Documentação Estratégica

Pasta: `pacote_completo/documentacao/`

```
documentacao/
├── plano_de_negocio_noticias_imparciais.md
├── roadmap_noticias_imparciais.md
├── PLANO_MONETIZACAO_NOTICIAS_IMPARCIAIS.md
└── PLANO_ACAO_OTIMIZADO.md
```

### 5.4. Assets de Design

Pasta: `pacote_completo/assets/`

```
assets/
├── logo_principal.png
├── logo_alternativo.png
├── logo_icone.png
└── identidade_visual.md
```

---

## 6. Status Atual do Roadmap

| Fase | Descrição | Status |
| :--- | :--- | :---: |
| Fase 1 | Fundação e Configuração (marca, logo, cores) | ✅ 100% |
| Fase 2 | Desenvolvimento do Agente de IA (scrapers, análise) | ✅ 100% |
| Fase 3 | Construção do Website MVP | ✅ 100% |
| Fase 4 | Lançamento e Operação | 🔄 33% |
| Fase 5 | Monetização | ⏳ 0% |

### O que falta para atingir a meta de R$ 100/dia:

- Cadastrar no Google AdSense
- Implementar espaços de anúncio no site
- Submeter ao Google News
- Estabelecer rotina de publicação diária (10 notícias/dia)
- Criar perfil no Instagram (@noticiasimparciais)
- Atingir 1.500 pageviews/dia

---

## 7. Problemas Identificados

### Problema 1: Complexidade e Consumo de Créditos

O projeto atingiu um nível de complexidade onde qualquer atividade consome muito tempo e muitos créditos da Manus. O contexto acumulado da tarefa ficou muito grande, tornando a operação ineficiente.

### Tentativa de Solução

Para resolver o Problema 1, foi feita uma tentativa de dividir o projeto em 5 agentes especializados (Administrador, Marketing Digital, Web Designer, Editor de Notícias e Social Media), cada um rodando em uma tarefa separada na Manus com contexto menor e mais focado.

### Problema 2: Isolamento entre Tarefas (derivado da tentativa de solução)

Ao tentar implementar a solução acima, descobriu-se que tarefas diferentes na Manus não compartilham arquivos entre si. Cada nova tarefa começa com um ambiente limpo, sem acesso aos arquivos desenvolvidos em tarefas anteriores. Isso inviabilizou a divisão em agentes especializados da forma como foi planejada.

---

## 8. Métricas para Sucesso

| Métrica | Atual | Meta (6 meses) |
| :--- | :---: | :---: |
| Pageviews/dia | ~0 | 1.500 |
| Notícias publicadas | 12 | 1.800+ |
| Receita/dia | R$ 0 | R$ 100 |
| Seguidores Instagram | 0 | 5.000 |

---

## 9. Informações Técnicas

### Stack do Site

- React 19
- Tailwind CSS 4
- TypeScript
- Vite
- Wouter (roteamento)
- shadcn/ui (componentes)

### APIs Utilizadas

- API de IA da Manus (para análise e síntese de notícias)

### Hospedagem

- Manus (projeto webdev)

---

## 10. Recursos

| Recurso | Informação |
| :--- | :--- |
| Projeto Manus | Site de Notícias Imparciais (Z6UNy9g27fUuce4V3gmoWi) |
| URL do Site | https://imparcial.manus.space/ |
| Domínio desejado | noticiasimparciais.com.br |
| Instagram planejado | @noticiasimparciais |

---

Este documento representa o estado atual do projeto em 24 de dezembro de 2025. Todos os arquivos funcionais estão incluídos no pacote anexo `PACOTE_NOTICIAS_IMPARCIAIS_COMPLETO.tar.gz`.
