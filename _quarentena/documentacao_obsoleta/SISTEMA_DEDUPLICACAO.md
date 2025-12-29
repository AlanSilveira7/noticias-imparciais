# Sistema de Deduplicação Inteligente

## Visão Geral

O sistema de deduplicação do Notícias Imparciais evita a publicação de notícias duplicadas e cria links entre notícias relacionadas, melhorando a experiência do usuário e o SEO do site.

---

## Como Funciona

### Fluxo de Processamento

```
Nova notícia gerada
       │
       ▼
┌─────────────────────────────────────┐
│  Calcular similaridade com          │
│  notícias dos últimos 2 dias        │
└─────────────────────────────────────┘
       │
       ├── Similaridade > 85% ──────► ATUALIZA notícia existente
       │                              (incrementa versão, atualiza conteúdo)
       │
       ├── Similaridade 50-85% ─────► PUBLICA como nova
       │                              (adiciona links para relacionadas)
       │
       └── Similaridade < 50% ──────► PUBLICA como nova
                                      (notícia completamente independente)
```

---

## Limiares de Similaridade

| Faixa | Classificação | Ação |
|:---:|:---|:---|
| **> 85%** | Duplicata | Atualiza a notícia existente |
| **50-85%** | Relacionada | Publica nova com links para relacionadas |
| **< 50%** | Nova | Publica como notícia independente |

---

## Algoritmo de Similaridade

O sistema combina dois métodos:

### 1. Similaridade de Sequência (60%)
- Usa o algoritmo `SequenceMatcher` do Python
- Captura a ordem das palavras
- Detecta títulos quase idênticos

### 2. Similaridade de Jaccard (40%)
- Baseado em palavras-chave
- Remove stopwords (palavras comuns)
- Detecta mesmo tema com palavras diferentes

### Fórmula Final
```
Similaridade = (Sequência × 0.6) + (Jaccard × 0.4)
```

---

## Novos Campos na Estrutura de Dados

| Campo | Tipo | Descrição |
|:---|:---:|:---|
| `version` | number | Versão da notícia (incrementa a cada atualização) |
| `createdAt` | string | Data de criação original |
| `updatedAt` | string | Data da última atualização (null se nunca atualizada) |
| `relatedNews` | string[] | IDs das notícias relacionadas |
| `originalId` | string | ID da notícia original (para desdobramentos) |

---

## Arquivos do Sistema

| Arquivo | Descrição |
|:---|:---|
| `scraper/similaridade.py` | Módulo de cálculo de similaridade |
| `scraper/deduplicacao.py` | Gerenciador de deduplicação |
| `scraper/atualizar_site.py` | Script principal (v2.0) |
| `scraper/data/historico_noticias_site.json` | Histórico completo |

---

## Uso no Site

### Indicador de Atualização
Quando uma notícia é atualizada, aparece um badge:
- **"Atualizada em DD/MM/YYYY"** - Indica que houve atualização
- **"v2", "v3"...** - Mostra a versão atual

### Notícias Relacionadas
No final de cada artigo, aparece uma seção:
- **"Notícias Relacionadas"** - Lista até 3 notícias sobre o mesmo tema

---

## Benefícios para SEO

1. **Evita conteúdo duplicado** - Google não penaliza
2. **URLs estáveis** - Notícias atualizadas mantêm a mesma URL
3. **Links internos** - Relacionadas criam estrutura de links
4. **Conteúdo "vivo"** - Atualizações mostram ao Google que o site é ativo

---

## Configuração

Os limiares podem ser ajustados no `GerenciadorDeduplicacao`:

```python
gerenciador = GerenciadorDeduplicacao(
    dias_comparacao=2,        # Quantos dias para trás comparar
    limiar_duplicata=0.85,    # Threshold para duplicata
    limiar_relacionada=0.50   # Threshold para relacionada
)
```

---

## Exemplos de Classificação

### Duplicata (>85%)
```
Título 1: "Bolsonaro cancela entrevista e tem cirurgia agendada para o Natal"
Título 2: "Bolsonaro cancela entrevista e tem cirurgia agendada no Natal"
Similaridade: 96% → ATUALIZA
```

### Relacionada (50-85%)
```
Título 1: "Bolsonaro cancela entrevista por cirurgia"
Título 2: "Ex-presidente Bolsonaro será operado no Natal"
Similaridade: 65% → PUBLICA COM LINK
```

### Nova (<50%)
```
Título 1: "Bolsonaro cancela entrevista"
Título 2: "Dólar fecha em alta nesta segunda"
Similaridade: 15% → PUBLICA INDEPENDENTE
```

---

## Manutenção

### Logs de Execução
O script gera logs detalhados:
```
[DEDUPLICAÇÃO] Processando 9 notícias...
    → 'Bolsonaro cancela entrevista...'
      Mais similar: 100.0% (duplicata)
      ✓ Atualizada para versão 2
```

### Estatísticas
Ao final, mostra resumo:
```
Estatísticas de deduplicação:
  - Notícias novas: 3
  - Notícias atualizadas: 5
  - Com relacionadas: 1
```
