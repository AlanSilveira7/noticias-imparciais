# Configuração do utilitário de cache R2

O utilitário `atualizar_cache_r2.py` lê quatro variáveis do ambiente do processo:
`R2_ACCOUNT_ID`, `R2_ACCESS_KEY_ID`, `R2_SECRET_ACCESS_KEY` e `R2_BUCKET_NAME`.
O arquivo `.env.example` documenta seus nomes e não contém valores reais.
Este script não carrega um arquivo `.env` automaticamente.

Configure os valores no gerenciador de segredos do ambiente de execução.
Não os coloque em commits, comandos compartilhados, exemplos, logs ou mensagens.
O acesso deve ser restrito ao bucket necessário.

Importar o módulo não cria um cliente. Executar sem configuração completa falha
antes da criação do cliente, informando somente os nomes das variáveis ausentes.

O script altera os metadados dos objetos em `noticias/imagens/`.
A revisão desta configuração não exige executá-lo contra o bucket real.
A remoção de valores do código não revoga credenciais antigas nem altera o histórico Git.

Teste local sem rede e sem credenciais reais:

```bash
python3 -m unittest discover -s tests -p 'test_configuracao_r2.py' -v
```
