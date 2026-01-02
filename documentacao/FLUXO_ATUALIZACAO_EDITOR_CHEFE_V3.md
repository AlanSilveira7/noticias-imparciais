# Fluxo de Atualização Completo - Editor-Chefe (v3.0)

**Data:** 30/12/2025

---

## 1. Visão Geral do Ciclo

| Etapa | Responsável | Descrição |
|:---:|:---|:---|
| **0** | Editor-Chefe (manual) | Coletar notícias via navegador dos 4 portais |
| **1** | Script `processar_noticias.py` | Identificar temas, gerar notícias imparciais |
| **2** | Script `publicar_supabase.py` | Publicar no Supabase com imagens |

---

## 2. Etapa 0: Coleta

- **Portais:** UOL, G1, Revista Oeste, Brasil Paralelo
- **O que coletar:** Título, URL, Data, Resumo
- **Onde salvar:** Arquivos JSON na pasta `scraper/data/`

---

## 3. Etapa 1: Processamento

- **Comando:** `python3 scraper/processar_noticias.py`
- **O que faz:** Carrega os JSONs, identifica temas, gera notícias imparciais e salva em `noticias_processadas.json`.

---

## 4. Etapa 2: Publicação

- **Comando:** `python3 scraper/publicar_supabase.py`
- **O que faz:** Lê o JSON, seleciona imagem, faz upload e publica no Supabase.

---

## 5. Checklist de Qualidade (Antes de Publicar)

- [ ] Imagem verificada visualmente (sem marca d'água)
- [ ] Imagem é contextual ao tema específico
- [ ] Tempo verbal correto (verificar data/hora do evento)
- [ ] Seção "Fontes de esquerda" preenchida
- [ ] Seção "Fontes de direita" preenchida (ou texto padrão)
- [ ] Selo correto (Verificada ou Viés Detectado)
- [ ] Título com dado numérico (quando aplicável)
- [ ] Lead responde O quê, Quando, Quanto, Fonte

---

## 6. Verificação Pós-Publicação

- **Acessar:** https://axianews.com/
- **Verificar para cada notícia:** Título, conteúdo, tema único, imagem e perspectivas.

---

## 7. Erros Comuns e Como Evitar

| Erro | Como Evitar |
|:---|:---|
| Imagens com marca d'água | Verificar VISUALMENTE cada imagem antes de usar |
| Selo incorreto | Usar "Verificada" se apenas um lado cobriu ou se as perspectivas são similares |
| Seção vazia | Usar o texto padrão quando não há cobertura de um lado |
| Tempo verbal incorreto | Verificar data/hora do evento |
| Imagem não contextual | Usar imagem que representa o tema específico |

---

## 8. Troubleshooting

| Erro | Solução |
|:---|:---|
| `ModuleNotFoundError` | `pip install python-dotenv supabase boto3 requests openai` |
| Credenciais não encontradas | Verificar arquivo `.env` |
| Notícias duplicadas | Excluir manualmente do Supabase |

---

## 9. Fluxo Otimizado para 10 Notícias/Dia

| Etapa | Duração Estimada |
|:---|:---:|
| 1. Coleta (10 notícias) | 30 min |
| 2. Busca nos portais | 45 min |
| 3. Redação (10 notícias) | 60 min |
| 4. Seleção de imagens | 30 min |
| 5. Publicação e verificação | 15 min |
| 6. Validação final | 15 min |
| **Total** | **~3 horas** |
