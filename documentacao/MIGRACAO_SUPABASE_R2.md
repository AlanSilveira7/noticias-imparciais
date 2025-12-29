# Documentação da Migração - Notícias Imparciais

## Resumo da Migração

Este documento descreve a migração da arquitetura de dados do projeto Notícias Imparciais, que passou de um sistema baseado em arquivos estáticos para uma arquitetura profissional e escalável utilizando **Supabase** (banco de dados) e **Cloudflare R2** (armazenamento de imagens).

---

## Arquitetura Anterior

| Componente | Tecnologia | Limitações |
|------------|------------|------------|
| Armazenamento de notícias | Arquivo `news.ts` | Não escalável, requer deploy para atualizar |
| Armazenamento de imagens | Repositório Git | Aumenta tamanho do repositório, lento |
| Paginação | Simulada no frontend | Carrega todos os dados de uma vez |

---

## Nova Arquitetura

| Componente | Tecnologia | Benefícios |
|------------|------------|------------|
| Banco de dados | **Supabase** (PostgreSQL) | Escalável, API REST automática, atualizações em tempo real |
| Armazenamento de imagens | **Cloudflare R2** | CDN global, 10GB grátis/mês, zero egress fees |
| Paginação | Real (backend) | Carrega apenas dados necessários |

---

## Credenciais e Configurações

### Supabase

- **URL do Projeto:** `https://rlrnqrgempxjymhiisua.supabase.co`
- **Chave Anon (pública):** Configurada nas variáveis de ambiente do Vercel

### Cloudflare R2

- **Account ID:** `ec85f027ae9088cd81296ad023dcb4d1`
- **Bucket:** `noticias-imparciais-imagens`
- **URL Pública:** `https://pub-3140440bf76b4ff189659bf15abaa214.r2.dev`

### Variáveis de Ambiente (Vercel)

```
VITE_SUPABASE_URL=https://rlrnqrgempxjymhiisua.supabase.co
VITE_SUPABASE_ANON_KEY=<chave_configurada>
```

---

## Estrutura da Tabela `articles`

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| `id` | TEXT (PK) | Identificador único do artigo |
| `title` | TEXT | Título da notícia |
| `subtitle` | TEXT | Subtítulo/resumo curto |
| `summary` | TEXT | Resumo expandido |
| `content` | TEXT | Conteúdo completo |
| `category` | TEXT | Categoria (Política, Economia) |
| `date` | TEXT | Data de publicação |
| `image_url` | TEXT | URL da imagem no R2 |
| `has_left_perspective` | BOOLEAN | Possui perspectiva de esquerda |
| `left_perspective` | TEXT | Texto da perspectiva de esquerda |
| `has_right_perspective` | BOOLEAN | Possui perspectiva de direita |
| `right_perspective` | TEXT | Texto da perspectiva de direita |
| `attention_points` | JSONB | Lista de pontos de atenção |
| `sources` | JSONB | Lista de fontes consultadas |
| `has_bias_detected` | BOOLEAN | Viés detectado nas fontes |
| `version` | INTEGER | Versão do artigo |
| `created_at` | TIMESTAMPTZ | Data de criação |
| `updated_at` | TIMESTAMPTZ | Data de atualização |
| `related_news` | JSONB | IDs de notícias relacionadas |
| `original_id` | TEXT | ID original (se migrado) |

---

## Arquivos Modificados

### Frontend (React/TypeScript)

| Arquivo | Alteração |
|---------|-----------|
| `client/src/lib/supabase.ts` | **Novo** - Cliente Supabase e funções de busca |
| `client/src/pages/Home.tsx` | Refatorado para usar Supabase |
| `client/src/pages/Article.tsx` | Refatorado para usar Supabase |
| `client/src/pages/Politica.tsx` | Refatorado para usar Supabase |
| `client/src/pages/Economia.tsx` | Refatorado para usar Supabase |
| `client/src/pages/Search.tsx` | Refatorado para usar Supabase |

### Scripts Python

| Arquivo | Descrição |
|---------|-----------|
| `scripts/migrate_to_supabase.py` | Script de migração de dados do news.ts para Supabase |
| `scripts/upload_images_to_r2.py` | Script de upload de imagens para Cloudflare R2 |

---

## Funções Disponíveis no Cliente Supabase

```typescript
// Buscar todas as notícias
fetchAllArticles(): Promise<NewsArticleFrontend[]>

// Buscar notícias com paginação
fetchArticlesPaginated(page: number, pageSize: number): Promise<{ articles: NewsArticleFrontend[]; total: number }>

// Buscar notícia por ID
fetchArticleById(id: string): Promise<NewsArticleFrontend | null>

// Buscar notícias por categoria
fetchArticlesByCategory(category: string): Promise<NewsArticleFrontend[]>

// Buscar notícias por termo de pesquisa
searchArticles(searchTerm: string): Promise<NewsArticleFrontend[]>
```

---

## Testes Realizados

| Funcionalidade | Status |
|----------------|--------|
| Página inicial com notícias do Supabase | ✅ Funcionando |
| Imagens carregando do Cloudflare R2 | ✅ Funcionando |
| Paginação real (carregar mais) | ✅ Funcionando |
| Página de artigo individual | ✅ Funcionando |
| Página de categoria Política | ✅ Funcionando |
| Página de categoria Economia | ✅ Funcionando |
| Busca de notícias | ✅ Funcionando |
| Indicadores de viés | ✅ Funcionando |

---

## Próximos Passos (Opcionais)

1. **Remover arquivo `news.ts`** - Após confirmar que tudo está funcionando em produção por alguns dias
2. **Configurar RLS no Supabase** - Para maior segurança, habilitar Row Level Security
3. **Implementar cache** - Adicionar cache no frontend para reduzir requisições
4. **Monitoramento** - Configurar alertas no Supabase e Cloudflare

---

## Suporte

Para dúvidas ou problemas, consulte:
- [Documentação do Supabase](https://supabase.com/docs)
- [Documentação do Cloudflare R2](https://developers.cloudflare.com/r2/)

---

**Data da Migração:** 23 de dezembro de 2025
**Responsável:** Manus AI
