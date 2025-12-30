# Análise de Melhorias — Briefing e Fluxo de Atualização

## Resumo da Análise

Após revisar os dois documentos atuais e compará-los com as lições aprendidas do dia 30/12/2025, identifiquei os seguintes pontos de melhoria:

---

## BRIEFING EDITOR CHEFE (v1.1)

### O que está BOM e deve ser mantido:
- Missão clara e bem definida
- Pilares filosóficos (Imparcialidade, Fatos, Transparência)
- Estrutura de fontes de notícias
- Configuração do ambiente (.env, dependências)

### O que está FALTANDO:
1. **Regra de Selos** — Não há orientação sobre quando usar "Verificada" vs "Viés Detectado"
2. **Texto padrão para seção vazia** — Não menciona o que fazer quando não há cobertura de um lado
3. **Verificação visual de imagens** — Não enfatiza a necessidade de verificar marca d'água
4. **Tempo verbal** — Não menciona a importância de verificar data/hora do evento
5. **Notícia exemplo** — Não há um padrão de qualidade a seguir

### O que está REDUNDANTE ou pode ser REMOVIDO:
1. Seção 8 "Lições Aprendidas" — Está incompleta e será substituída por regras mais claras
2. Seção 10 "Checklist Resumido" — Muito superficial, será movido para o Fluxo

### O que precisa ser ATUALIZADO:
1. Regras Invioláveis — Adicionar regras de selo e imagem
2. Sistema de Imagens — Adicionar verificação visual obrigatória

---

## FLUXO DE ATUALIZAÇÃO (v2.0)

### O que está BOM e deve ser mantido:
- Estrutura de 3 etapas (Coleta, Processamento, Publicação)
- Formato dos arquivos JSON
- Comandos de execução
- Troubleshooting

### O que está FALTANDO:
1. **Checklist de qualidade antes de publicar** — Verificação de imagem, selo, tempo verbal
2. **Regra de selo** — Quando usar Verificada vs Viés Detectado
3. **Texto padrão para seção vazia** — O que colocar quando não há cobertura de um lado
4. **Verificação de imagem** — Checklist visual antes de publicar
5. **Fluxo otimizado para 10 notícias/dia** — Tempo estimado por etapa
6. **Priorização de temas** — Quais temas priorizar

### O que está REDUNDANTE ou pode ser REMOVIDO:
1. Seção 2 "Regras Invioláveis" — Duplicada do Briefing, deve ficar apenas no Briefing
2. Seção 8 "Salvar no GitHub" — Opcional e não essencial para o fluxo

### O que precisa ser ATUALIZADO:
1. Etapa de Verificação — Adicionar checklist detalhado
2. Adicionar seção de "Erros Comuns e Como Evitar"

---

## PROPOSTA DE REORGANIZAÇÃO

### BRIEFING (Contexto + Premissas)
- Missão e Pilares
- Regras Invioláveis (incluindo selos e imagens)
- Fontes de Notícias
- Configuração do Ambiente
- Notícia Exemplo (padrão de qualidade)

### FLUXO (Passo a Passo + Checklists)
- Visão Geral do Ciclo
- Etapa 0: Coleta
- Etapa 1: Processamento
- Etapa 2: Publicação
- Checklist de Qualidade (NOVO)
- Verificação Pós-Publicação
- Erros Comuns e Como Evitar (NOVO)
- Troubleshooting
