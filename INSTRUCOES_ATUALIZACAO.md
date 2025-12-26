# Instruções de Atualização - Notícias Imparciais

**Autor:** Manus AI  
**Data:** 26/12/2025  
**Versão:** 2.0

## 1. Visão Geral do Fluxo

O sistema de atualização do portal Notícias Imparciais funciona em **3 etapas sequenciais**:

| Etapa | Script | Descrição |
|-------|--------|-----------|
| 1 | Coleta via Browser | Coleta notícias reais dos sites de notícias |
| 2 | `processar_noticias.py` | Analisa viés e gera notícias imparciais |
| 3 | `publicar_supabase.py` | Publica no banco de dados Supabase |

## 2. Etapa 1: Coleta de Notícias

A coleta de notícias é feita **manualmente via browser** pelo agente Manus. O agente deve:

1. Acessar cada fonte de notícias
2. Coletar os títulos, URLs e resumos das notícias mais recentes
3. Salvar em arquivos JSON no diretório `/home/ubuntu/noticias-imparciais/scraper/data/`

### Fontes Configuradas

**Fontes de Esquerda:**
- UOL: `https://noticias.uol.com.br/politica/`
- G1/Globo: `https://g1.globo.com/politica/`

**Fontes de Direita:**
- Revista Oeste: `https://revistaoeste.com/politica/`
- Brasil Paralelo: `https://www.brasilparalelo.com.br/noticias`

### Formato dos Arquivos de Coleta

Os arquivos devem ser salvos com os nomes:
- `uol_politica_novo.json`
- `globo_politica_novo.json`
- `oeste_politica_novo.json`
- `brasil_paralelo_politica_novo.json`

Formato JSON:
```json
[
  {
    "titulo": "Título da notícia",
    "url": "https://...",
    "resumo": "Resumo ou subtítulo",
    "data": "26/12/2025 14h30"
  }
]
```

## 3. Etapa 2: Processamento

Após a coleta, executar o script de processamento:

```bash
cd /home/ubuntu/noticias-imparciais/scraper
python3 processar_noticias.py
```

Este script:
- Carrega as notícias coletadas de todas as fontes
- Identifica temas comuns entre esquerda e direita
- Gera notícias imparciais usando IA
- Salva em `data/noticias_imparciais.json`

## 4. Etapa 3: Publicação

Após o processamento, publicar no Supabase:

```bash
cd /home/ubuntu/noticias-imparciais/scraper
python3 publicar_supabase.py
```

Este script:
- Lê as notícias imparciais geradas
- Verifica duplicatas no banco
- Seleciona imagens do acervo curado
- Faz upload das imagens para Cloudflare R2
- Publica no Supabase

## 5. Fluxo Completo (Resumo)

```bash
# 1. Coletar notícias via browser (manual)
# 2. Processar notícias
cd /home/ubuntu/noticias-imparciais/scraper
python3 processar_noticias.py

# 3. Publicar no Supabase
python3 publicar_supabase.py
```

## 6. Verificação Pós-Execução

Para verificar se as notícias foram publicadas corretamente:

```bash
cd /home/ubuntu/noticias-imparciais
python3 -c "
from dotenv import load_dotenv
from supabase import create_client
import os
load_dotenv()
supabase = create_client(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_SERVICE_KEY'))
response = supabase.table('articles').select('id', count='exact').execute()
print(f'Total de notícias: {response.count}')
"
```

## 7. Estrutura de Arquivos

```
/home/ubuntu/noticias-imparciais/
├── scraper/
│   ├── data/
│   │   ├── uol_politica_novo.json      # Notícias coletadas do UOL
│   │   ├── globo_politica_novo.json    # Notícias coletadas do G1
│   │   ├── oeste_politica_novo.json    # Notícias coletadas da Oeste
│   │   ├── brasil_paralelo_politica_novo.json  # Notícias do BP
│   │   └── noticias_imparciais.json    # Notícias processadas
│   ├── processar_noticias.py           # Script de processamento
│   ├── publicar_supabase.py            # Script de publicação
│   └── seletor_temas_v4.py             # Seletor de imagens
├── acervo_temas/                        # Imagens curadas por tema
└── .env                                 # Variáveis de ambiente
```

## 8. Troubleshooting

| Problema | Solução |
|----------|---------|
| "Nenhuma notícia encontrada" | Verificar se os arquivos `*_novo.json` existem em `scraper/data/` |
| "Duplicata - pulando" | Normal - a notícia já existe no banco |
| Erro de conexão Supabase | Verificar variáveis `SUPABASE_URL` e `SUPABASE_SERVICE_KEY` no `.env` |
| Erro de upload de imagem | Verificar variáveis `R2_*` no `.env` |

---

**IMPORTANTE:** Este sistema foi projetado para coletar notícias **reais** dos sites de notícias, não para gerar notícias fictícias. A etapa de coleta deve ser feita manualmente pelo agente acessando os sites reais.
