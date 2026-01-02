# Módulo de Coleta de Notícias

**Projeto:** Axia News  
**Versão:** 2.0.0  
**Data:** 29/12/2025  
**Autor:** Manus AI

---

## Visão Geral

Este módulo é responsável pela coleta automatizada de notícias de múltiplos portais de notícias brasileiros. O objetivo é coletar notícias de fontes com diferentes vieses editoriais para posterior análise, comparação e síntese de conteúdo imparcial.

## Estrutura de Arquivos

```
scraper/
├── README.md                    # Esta documentação
├── processar_noticias.py          # Coleta e processa notícias
├── publicar_supabase.py     # Publica no Supabase
├── deduplicacao.py          # Módulo de deduplicação
├── similaridade.py          # Módulo de similaridade
├── analisador_contexto.py   # Análise semântica
├── buscador_imagens_br.py   # Busca imagens Wikimedia
└── data/                    # Dados de operação
```

## Fontes Configuradas

| Fonte | ID | Viés Editorial | Status |
|-------|-----|----------------|--------|
| UOL | `uol` | Esquerda | ✅ Ativo |
| G1/Globo | `globo` | Esquerda | ✅ Ativo |
| Revista Oeste | `oeste` | Direita | ✅ Ativo |
| Brasil Paralelo | `brasil_paralelo` | Direita | ✅ Ativo |

## Como Usar

### 1. Importação Básica

```python
from coletor_noticias import ColetorNoticias

# Inicializar o coletor
coletor = ColetorNoticias()

# Importar notícias de um arquivo JSON
coletor.importar_json("data/uol_politica.json", "uol", "politica")
coletor.importar_json("data/globo_politica.json", "globo", "politica")
```

### 2. Consultas

```python
# Buscar por fonte
noticias_uol = coletor.buscar_por_fonte("uol")

# Buscar por viés editorial
noticias_esquerda = coletor.buscar_por_vies("esquerda")
noticias_direita = coletor.buscar_por_vies("direita")

# Buscar por seção
noticias_politica = coletor.buscar_por_secao("politica")

# Buscar por termo no título
noticias_lula = coletor.buscar_por_termo("Lula")

# Buscar por data
noticias_hoje = coletor.buscar_por_data("2025-12-22")
```

### 3. Agrupamento por Tema

```python
# Agrupa notícias de diferentes fontes sobre o mesmo assunto
temas = coletor.agrupar_por_tema()

for tema, noticias in temas.items():
    print(f"{tema}: {len(noticias)} notícias")
```

### 4. Exportação para Análise de IA

```python
# Exporta em formato otimizado para o módulo de análise
arquivo = coletor.exportar_para_analise()
```

## Estrutura de Dados

### Notícia

```json
{
  "id": "news_1234567890",
  "fonte": "UOL",
  "fonte_id": "uol",
  "vies_editorial": "esquerda",
  "secao": "politica",
  "titulo": "Título da notícia",
  "url": "https://...",
  "resumo": "Resumo ou subtítulo",
  "texto_completo": null,
  "data_publicacao": "2025-12-22T19:04:00",
  "data_coleta": "2025-12-22T20:00:00"
}
```

### Exportação para Análise

```json
{
  "data_exportacao": "2025-12-22T20:00:00",
  "total_noticias": 18,
  "temas": {
    "Caso Ramagem": {
      "total": 5,
      "fontes_esquerda": [...],
      "fontes_direita": [...],
      "fontes_centro": [...]
    }
  }
}
```

## Coleta via Navegador (Manus)

Como os sites possuem proteções anti-bot, a coleta é feita via navegador automatizado. O processo recomendado é:

1. **Navegar** para a URL da seção desejada
2. **Executar JavaScript** para extrair os dados das notícias
3. **Salvar** os dados em arquivo JSON
4. **Importar** para o banco de dados usando `coletor.importar_json()`

### Exemplo de Script JavaScript para Extração

```javascript
const noticias = [];
document.querySelectorAll("a").forEach(link => {
    const href = link.href || "";
    const texto = link.innerText || "";
    
    if (href && texto && href.includes("noticia") && texto.length > 30) {
        noticias.push({
            titulo: texto.split("\n")[0].trim(),
            url: href,
            data: new Date().toISOString().split("T")[0],
            resumo: ""
        });
    }
});
JSON.stringify(noticias, null, 2);
```

## Próximos Passos

1. **Implementar scrapers para fontes de direita** (Revista Oeste, Brasil Paralelo)
2. **Automatizar ciclo noturno** de coleta
3. **Integrar com módulo de análise de viés** (Atividade 2.2)
4. **Adicionar extração de texto completo** das notícias

## Estatísticas Atuais

- **Total de notícias coletadas:** 38
- **Fontes ativas:** UOL, G1/Globo, Revista Oeste, Brasil Paralelo
- **Seções cobertas:** Política
- **Distribuição por viés:** 18 esquerda, 20 direita
- **Temas identificados:** Caso Ramagem, Caso Augusto Heleno, Ministro Moraes, Presidente Lula, Família Bolsonaro, etc.

---

*Documentação gerada automaticamente pelo Manus AI*
