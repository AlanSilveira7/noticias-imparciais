# Pasta de Quarentena

**Data de criação:** 29/12/2025  
**Prazo para exclusão definitiva:** 05/01/2026 (1 semana)

## Propósito

Esta pasta contém arquivos identificados como sujeira/resíduos de desenvolvimento que foram movidos para cá antes da exclusão definitiva. Se nenhum arquivo for necessário durante o período de quarentena, toda a pasta pode ser excluída.

## Conteúdo

### 📁 cache_python/
Cache de compilação Python (`__pycache__`). Pode ser excluído imediatamente.

### 📁 scripts_obsoletos/
Scripts substituídos por versões mais recentes:
- `publicar_supabase_v2.py` → substituído por `publicar_supabase.py` (v2.0)
- `seletor_imagens.py` → substituído por `analisador_contexto.py`
- `seletor_imagens_v2.py` → substituído por `analisador_contexto.py`
- `seletor_temas_v4.py` → substituído por `analisador_contexto.py`
- `expansor_acervo.py` → substituído por `expansor_acervo_integrado.py`
- `news.ts` → site agora usa Supabase diretamente

### 📁 scripts_manutencao/
Scripts de uso único para manutenção/limpeza:
- `verificar_imagens_hoje.py`
- `verificar_noticias_hoje.py`
- `limpar_acervo.py`
- `limpar_imagens_r2.py`
- `limpar_noticias_antigas.py`
- `atualizar_imagens_noticias.py`
- `atualizar_imagens_semantico.py`
- `verificador_cobertura.py`

### 📁 logs_temporarios/
Logs e dados de execuções anteriores:
- `logs_cobertura/`
- `logs_busca/`
- `logs_expansao/`
- `requisicoes_imagens/`
- `noticias_para_analise_*.json`
- `verificacao_imagens.json`

### 📁 imagens_site_antigas/
Imagens que estavam no frontend antes da migração para R2:
- `public_noticias/` - 12 imagens
- `dist_noticias/` - 12 imagens (cópia do build)

### 📁 documentacao_revisar/
Documentação possivelmente desatualizada:
- `INTEGRACAO_UNSPLASH.md` - Integração desativada
- `PROMPT_AUDITORIA.md`
- `analise_comparativa.md`
- `analise_estrutura.md`

## Ação Após Quarentena

Se nenhum arquivo for necessário até **05/01/2026**, execute:
```bash
rm -rf _quarentena/
```
