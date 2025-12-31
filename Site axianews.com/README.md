# Axia News - Portal de Notícias

Site de notícias inspirado no layout do Globo.com, desenvolvido com React e Tailwind CSS.

## Tecnologias Utilizadas

- **React 19** com TypeScript
- **Vite** como bundler
- **Tailwind CSS 4** para estilização
- **shadcn/ui** como biblioteca de componentes
- **Wouter** para roteamento

## Estrutura do Projeto

```
client/
├── public/
│   └── images/          # Imagens estáticas
├── src/
│   ├── components/      # Componentes reutilizáveis
│   │   ├── Header.tsx   # Cabeçalho com logo e navegação
│   │   ├── Footer.tsx   # Rodapé simplificado
│   │   ├── NewsCard.tsx # Card de notícia
│   │   ├── SectionColumn.tsx # Coluna temática
│   │   └── MobileHeroSection.tsx # Hero para mobile
│   ├── pages/
│   │   └── Home.tsx     # Página principal
│   ├── App.tsx          # Roteamento e providers
│   └── index.css        # Estilos globais e variáveis
```

## Seções Temáticas

O site possui 3 seções temáticas com cores distintas:

- **Política** (Vermelho - #FF0000)
- **Economia** (Laranja - #FF6B00)
- **Tecnologia** (Verde - #00A859)

## Instalação

1. Instale as dependências:
```bash
pnpm install
```

2. Execute o servidor de desenvolvimento:
```bash
pnpm dev
```

3. Acesse `http://localhost:3000`

## Build para Produção

```bash
pnpm build
```

Os arquivos serão gerados na pasta `dist/`.

## Personalização

### Alterar o Logo
Edite o arquivo `client/src/components/Header.tsx` na seção do logo.

### Alterar Cores das Seções
Edite o arquivo `client/src/pages/Home.tsx` nas props `color` dos componentes `SectionColumn`.

### Adicionar Notícias
As notícias estão definidas como arrays no arquivo `client/src/pages/Home.tsx`. Substitua os dados mock por dados reais ou integre com uma API.

---

© 2025 Axia News. Todos os direitos reservados.
