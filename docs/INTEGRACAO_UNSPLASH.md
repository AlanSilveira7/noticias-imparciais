# Integração com Unsplash API - Notícias Imparciais

## Visão Geral

O portal Notícias Imparciais agora conta com integração automática com a API do Unsplash para buscar imagens profissionais e relevantes para cada notícia publicada. Esta integração resolve o problema de repetição de imagens e garante um acervo visual diversificado e de alta qualidade.

## Arquitetura da Solução

A integração é composta por dois módulos Python principais localizados em `/scraper/`:

| Módulo | Descrição |
|:---|:---|
| `unsplash_service.py` | Serviço de busca de imagens no Unsplash com extração inteligente de keywords |
| `processar_imagem_noticia.py` | Processador completo que busca, baixa, faz upload para R2 e atualiza o Supabase |

## Fluxo de Processamento

O sistema segue um fluxo automatizado em 5 etapas:

1. **Extração de Keywords**: O título da notícia é analisado para extrair palavras-chave relevantes. Termos em português são automaticamente traduzidos para inglês para melhorar os resultados de busca.

2. **Busca no Unsplash**: A API do Unsplash é consultada com as keywords extraídas. O sistema seleciona uma imagem de forma determinística (baseada em hash) para garantir consistência.

3. **Download da Imagem**: A imagem é baixada em resolução de 1080px (qualidade "regular" do Unsplash), ideal para uso em web.

4. **Upload para Cloudflare R2**: A imagem é enviada para o bucket R2 com um nome único baseado no título da notícia e ID do Unsplash.

5. **Atualização do Supabase**: A URL da nova imagem é salva no banco de dados, associada ao artigo correspondente.

## Configuração

### Variáveis de Ambiente

As seguintes variáveis devem estar configuradas no arquivo `.env`:

```env
# Credenciais Unsplash API
UNSPLASH_ACCESS_KEY=sua_access_key_aqui
UNSPLASH_SECRET_KEY=sua_secret_key_aqui
```

### Dependências Python

```bash
pip install requests python-dotenv boto3 supabase
```

## Uso

### Processar uma única notícia

```python
from processar_imagem_noticia import processar_imagem_para_noticia

resultado = processar_imagem_para_noticia(
    titulo="STF decide sobre aposentadoria integral",
    categoria="Política",
    article_id="uuid-do-artigo"  # Opcional
)

if resultado:
    print(f"URL da imagem: {resultado['url']}")
    print(f"Fotógrafo: {resultado['photographer']}")
```

### Atualizar todas as imagens do banco

```bash
cd /home/ubuntu/noticias-imparciais/scraper
python3 processar_imagem_noticia.py --atualizar-todas
```

### Testar o módulo Unsplash isoladamente

```bash
cd /home/ubuntu/noticias-imparciais/scraper
python3 unsplash_service.py
```

## Mapeamento de Termos

O sistema inclui um dicionário de tradução de termos políticos e econômicos brasileiros para inglês, garantindo melhores resultados de busca:

| Termo PT | Tradução EN |
|:---|:---|
| STF | supreme court justice |
| Congresso | congress parliament |
| Economia | economy finance |
| Dólar | dollar currency money |
| Brasília | brasilia brazil government |
| Inflação | inflation economy |

## Limites da API

O plano atual do Unsplash possui os seguintes limites:

| Tipo | Limite |
|:---|:---|
| Modo Demo | 50 requisições/hora |
| Modo Produção | 5.000 requisições/hora |

Para solicitar upgrade para produção, acesse: https://unsplash.com/oauth/applications

## Atribuição

De acordo com os termos do Unsplash, a atribuição ao fotógrafo é recomendada mas não obrigatória. O sistema armazena as informações do fotógrafo para uso futuro:

- `photographer`: Nome do fotógrafo
- `photographer_url`: Link para o perfil no Unsplash
- `unsplash_url`: Link para a foto original

## Resultados

Após a implementação, o portal passou de **12 imagens repetidas** para **21+ imagens únicas**, cada uma contextualmente relevante para sua notícia.

### Exemplos de Imagens Geradas

| Notícia | Imagem |
|:---|:---|
| Lula sanciona reajuste para servidores | Foto do Congresso Nacional por Gabriel Tiveron |
| Dólar se mantém acima de R$ 5,50 | Foto de notas de dólar por Eric Prouzet |
| Congresso aprova Orçamento da União | Foto de prédio governamental por Marius |

## Manutenção

O sistema foi projetado para ser executado automaticamente junto com o pipeline de geração de notícias. Para integrar com o fluxo existente, basta importar a função `processar_imagem_para_noticia` no script de publicação de notícias.

---

*Documentação criada em 26/12/2025*
*Portal Notícias Imparciais - Os fatos, sem filtro.*
