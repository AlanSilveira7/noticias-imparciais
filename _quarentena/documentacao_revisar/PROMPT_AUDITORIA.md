# Prompt de Auditoria - Projeto Notícias Imparciais

**Objetivo:** Este prompt deve ser usado pelo agente que idealizou o projeto para auditar os scripts atualmente ativos e validar se as premissas e conceitos originais continuam sendo respeitados.

---

## PROMPT PARA O AGENTE AUDITOR

```
# TAREFA: Auditoria de Conformidade - Projeto Notícias Imparciais

## CONTEXTO

Você é o agente que idealizou o projeto "Notícias Imparciais". Seu objetivo era criar um portal de notícias que:

1. **Coletasse notícias reais** de fontes com diferentes vieses editoriais (esquerda e direita)
2. **Analisasse o viés** de cada fonte de forma transparente
3. **Gerasse versões imparciais** das notícias, apresentando os fatos sem filtro
4. **Mostrasse ao leitor** as diferentes perspectivas de cada lado
5. **Usasse imagens de alta qualidade**, contextuais e brasileiras

O projeto passou por melhorias de infraestrutura para escalabilidade. Sua missão agora é **auditar os scripts ativos** para garantir que a essência e as premissas originais foram preservadas.

---

## INSTRUÇÕES DE AUDITORIA

### PASSO 1: Clone o Repositório
```bash
gh repo clone AlanSilveira7/noticias-imparciais
cd noticias-imparciais
```

### PASSO 2: Analise os Scripts Principais

Você deve ler e analisar os seguintes arquivos no diretório `scraper/`:

| Script | Função | O que verificar |
|--------|--------|-----------------|
| `processar_noticias.py` | Processa notícias coletadas e gera versões imparciais | A lógica de identificação de temas e geração de notícias imparciais está correta? O prompt enviado à IA respeita a imparcialidade? |
| `publicar_supabase.py` | Publica notícias no banco de dados | A lógica de detecção de viés (`has_bias_detected`) está correta? Só marca TRUE quando AMBAS as perspectivas existem? |
| `seletor_temas_v4.py` | Seleciona imagens do acervo curado | A lógica de seleção prioriza TEMA sobre PESSOA? Diferencia quando a pessoa É o tema vs. realiza ação institucional? |
| `sintetizador_imparcial.py` | Gera notícias imparciais a partir da análise de viés | O prompt de geração respeita a imparcialidade? Apresenta ambos os lados de forma equilibrada? |
| `analisador_vies.py` | Analisa o viés de cada notícia | A análise identifica corretamente fatos objetivos, linguagem carregada e omissões? |

### PASSO 3: Verifique o Acervo de Imagens

```bash
ls -la acervo_temas/
```

Verifique se:
- As imagens são organizadas por TEMA (judiciario, legislativo, executivo, economia, etc.)
- Existe um diretório `pessoas/` para fotos de pessoas específicas
- As imagens são de alta qualidade e sem marcas d'água

### PASSO 4: Analise uma Amostra de Notícias no Banco

Execute o seguinte comando para ver as notícias publicadas:

```bash
cd noticias-imparciais
python3 -c "
from dotenv import load_dotenv
from supabase import create_client
import os
load_dotenv()
supabase = create_client(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_SERVICE_KEY'))
response = supabase.table('articles').select('title, has_bias_detected, has_left_perspective, has_right_perspective, left_perspective, right_perspective').limit(5).execute()
for art in response.data:
    print('='*60)
    print(f'TÍTULO: {art[\"title\"]}')
    print(f'Viés Detectado: {art[\"has_bias_detected\"]}')
    print(f'Perspectiva Esquerda: {art[\"has_left_perspective\"]}')
    print(f'Perspectiva Direita: {art[\"has_right_perspective\"]}')
    if art['left_perspective']:
        print(f'Esquerda: {art[\"left_perspective\"][:100]}...')
    if art['right_perspective']:
        print(f'Direita: {art[\"right_perspective\"][:100]}...')
"
```

---

## CHECKLIST DE VALIDAÇÃO

Após a análise, responda às seguintes perguntas:

### Premissa 1: Imparcialidade
- [ ] Os prompts enviados à IA instruem claramente para gerar conteúdo imparcial?
- [ ] A estrutura da notícia apresenta ambos os lados de forma equilibrada?
- [ ] A seção "O que diz cada lado" está presente e bem implementada?

### Premissa 2: Coleta de Notícias Reais
- [ ] O sistema coleta notícias REAIS dos sites (não gera notícias fictícias)?
- [ ] As fontes de esquerda (UOL, G1) e direita (Oeste, Brasil Paralelo) estão configuradas?

### Premissa 3: Detecção de Viés
- [ ] O campo `has_bias_detected` só é TRUE quando AMBAS as perspectivas existem?
- [ ] Perspectivas vazias ou genéricas ("não há informações") são tratadas como FALSE?

### Premissa 4: Qualidade de Imagens
- [ ] O acervo contém imagens brasileiras e contextuais?
- [ ] A lógica de seleção prioriza TEMA sobre PESSOA?
- [ ] Imagens de pessoas só são usadas quando a pessoa É o tema da notícia?

### Premissa 5: Transparência
- [ ] As fontes consultadas são listadas em cada notícia?
- [ ] Os pontos de atenção alertam o leitor sobre possíveis vieses?

---

## FORMATO DO RELATÓRIO DE AUDITORIA

Ao final da auditoria, gere um relatório no seguinte formato:

```markdown
# Relatório de Auditoria - Notícias Imparciais

**Data:** [DATA]
**Auditor:** [NOME DO AGENTE]

## Resultado Geral
[APROVADO / APROVADO COM RESSALVAS / REPROVADO]

## Análise por Premissa

### 1. Imparcialidade
[Análise detalhada]
**Status:** [OK / ATENÇÃO / CRÍTICO]

### 2. Coleta de Notícias Reais
[Análise detalhada]
**Status:** [OK / ATENÇÃO / CRÍTICO]

### 3. Detecção de Viés
[Análise detalhada]
**Status:** [OK / ATENÇÃO / CRÍTICO]

### 4. Qualidade de Imagens
[Análise detalhada]
**Status:** [OK / ATENÇÃO / CRÍTICO]

### 5. Transparência
[Análise detalhada]
**Status:** [OK / ATENÇÃO / CRÍTICO]

## Recomendações
[Lista de recomendações, se houver]

## Conclusão
[Parecer final sobre a conformidade do projeto com as premissas originais]
```

---

## OBSERVAÇÕES IMPORTANTES

1. **Não altere nenhum código** durante a auditoria - apenas leia e analise
2. **Documente evidências** para cada conclusão (trechos de código, exemplos de notícias)
3. **Seja crítico mas justo** - o objetivo é garantir a qualidade, não encontrar problemas
4. **Considere o contexto** - algumas mudanças podem ter sido necessárias para escalabilidade

---

*Este prompt foi criado para garantir a continuidade e integridade do projeto Notícias Imparciais.*
```
