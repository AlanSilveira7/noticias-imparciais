# Documentação do Sistema de Imagens (v3.0)

**Data:** 29/12/2025  
**Versão:** 3.0 (com análise semântica e busca automática)

---

## 1. Visão Geral

O sistema de imagens foi reformulado para garantir que cada notícia tenha uma imagem contextual e de alta qualidade. Ele opera em três camadas: análise semântica, acervo local e busca automática online.

## 2. Lógica de Seleção (Três Camadas)

### Camada 1: Análise Semântica do Título

O script `analisador_contexto.py` analisa o título da notícia e classifica o contexto visual em uma de três categorias:

| Categoria | Descrição | Exemplo |
|:---|:---|:---|
| **Conceito/Símbolo** | Quando o tema é abstrato ou simbólico | "Mudanças no FGTS" → `carteira de trabalho` |
| **Instituição** | Quando o foco é uma entidade governamental ou corporativa | "Acareação no STF" → `plenário do STF` |
| **Pessoa** | Apenas quando a pessoa é o foco principal (saúde, prisão domiciliar) | "Bolsonaro passa por procedimento médico" → `foto do Bolsonaro` |

### Camada 2: Acervo Local (`acervo_temas/`)

Com base na análise semântica, o sistema busca uma imagem correspondente no acervo local. O acervo está organizado por categorias:

- `economia/`
- `executivo/`
- `judiciario/`
- `legislativo/`
- `pessoas/`
- `seguranca/`
- `eleicoes/`

### Camada 3: Busca Automática no Wikimedia Commons

Se nenhuma imagem adequada for encontrada no acervo local, o script `buscador_imagens_br.py` é ativado automaticamente:

1. **Busca:** Procura no Wikimedia Commons usando as palavras-chave da análise semântica.
2. **Validação:** Filtra os resultados para garantir:
   - **Resolução Mínima:** 1280px de largura.
   - **Licença Adequada:** Creative Commons (CC BY, CC BY-SA) ou Domínio Público (CC0).
   - **Sem Marca d'Água:** Imagens com marcas d'água visíveis são descartadas.
3. **Download e Adição ao Acervo:** A melhor imagem encontrada é baixada, adicionada à categoria correta no `acervo_temas/` e utilizada na publicação.

Se a busca online não retornar nenhuma imagem válida, o sistema utiliza uma imagem de fallback genérica da categoria (ex: `executivo/planalto_fachada_02.jpg`).

## 3. Como Adicionar Novas Imagens Manualmente

Se desejar melhorar a qualidade de uma imagem ou adicionar cobertura para um novo tema, siga estes passos:

1. **Encontre uma imagem de alta qualidade** (mínimo 1280px de largura) em fontes como Wikimedia Commons, Agência Brasil, etc.
2. **Verifique a licença** (deve ser Creative Commons ou domínio público).
3. **Salve a imagem** com um nome descritivo (ex: `sergio_moro_depoimento_01.jpg`).
4. **Adicione a imagem à pasta da categoria correspondente** em `acervo_temas/` (ex: `acervo_temas/pessoas/`).

O sistema detectará e utilizará a nova imagem automaticamente no próximo ciclo de publicação.

## 4. Padrões de Qualidade

| Padrão | Requisito |
|:---|:---|
| **Resolução Mínima** | 1280px de largura |
| **Licença** | Creative Commons ou Domínio Público |
| **Marca d'Água** | Não permitido |
| **Formato** | JPEG, PNG, WebP |

---

Este sistema garante um fluxo de trabalho autônomo e de alta qualidade, expandindo o acervo de imagens organicamente conforme a necessidade.
