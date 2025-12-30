# Guia Rápido - Ciclo de Atualização Diário

**Para:** Agente Editor Chefe  
**Data:** 29/12/2025  
**Assunto:** Checklist e comandos para o ciclo de atualização diário.

---

## ✅ Checklist Pré-Execução

Antes de iniciar, garanta que seu ambiente está pronto:

| Verificação | Comando / Ação | Frequência |
|:---|:---|:---|
| **1. Repositório Atualizado** | `git pull origin main` | Diariamente |
| **2. Dependências Instaladas** | `pip install python-dotenv supabase boto3 requests openai` | Apenas uma vez |
| **3. Arquivo `.env` Configurado** | Verificar se o arquivo `.env` existe na raiz com as credenciais | Apenas uma vez |

---

## 🚀 Comandos do Ciclo Diário (2 Etapas)

Execute estes dois comandos em sequência para atualizar o site:

### Etapa 1: Coletar, Processar e Deduplicar Notícias

```bash
python3 scraper/processar_noticias.py
```

- **O que faz:** Coleta notícias dos 4 portais, analisa viés, gera versões imparciais e **aplica deduplicação inteligente automaticamente**.
- **Duração:** ~1-2 minutos.

### Etapa 2: Publicar no Banco de Dados

```bash
python3 scraper/publicar_supabase.py
```

- **O que faz:** Publica no Supabase com seleção inteligente de imagens (análise semântica + busca automática no Wikimedia Commons) e upload para Cloudflare R2.
- **Duração:** ~1-3 minutos (depende da busca de imagens).

---

## 📋 Premissas de Imagens

Todas as imagens devem atender aos seguintes padrões:

| Padrão | Requisito |
|:---|:---|
| **Resolução Mínima** | 1280px de largura |
| **Licença** | Creative Commons ou Domínio Público |
| **Marca d'Água** | Não permitido |
| **Formato** | JPEG, PNG, WebP |

---

## 💾 Salvar Alterações no GitHub (Opcional)

Após a publicação, salve as alterações no repositório:

```bash
git add .
git commit -m "Ciclo de notícias [DATA]"
git push origin main
```

---

## 📊 KPIs Esperados

| Métrica | Meta |
|---------|------|
| Notícias publicadas | 10/dia |
| Índice de imparcialidade | 100% |
| Taxa de sucesso do ciclo | > 95% |
| Resolução de imagens | ≥ 1280px |

---

## ❓ Troubleshooting

### Erro: `ModuleNotFoundError`

**Problema:** Faltam dependências Python.
**Solução:** Execute `pip install python-dotenv supabase boto3 requests openai`.

### Erro: `supabase.client.ClientOptionsError` ou `botocore.exceptions.NoCredentialsError`

**Problema:** Credenciais não encontradas.
**Solução:** Verifique se o arquivo `.env` existe na raiz do projeto e contém todas as variáveis necessárias (Supabase e R2).

### Erro: Imagem errada ou genérica

**Problema:** A análise semântica pode não ter identificado o tema corretamente, ou a busca online não encontrou imagem adequada.
**Solução:** Você pode adicionar uma imagem manualmente ao acervo (`acervo_temas/`) na categoria correta. O sistema a utilizará na próxima vez.

### Erro: Notícias duplicadas

**Problema:** A deduplicação não identificou a similaridade.
**Solução:** Verifique se o histórico do Supabase está sendo carregado corretamente. O limiar de similaridade é 85%.

---

Este fluxo é simples e robusto. Se tiver qualquer dúvida, consulte a documentação completa ou o Desenvolvedor Backend.
