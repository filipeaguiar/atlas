## Context

O projeto já possui uma fronteira editorial forte: `publicacao/manifest.yml` é a única lista positiva, `prepare_publication()` valida cânone e áreas proibidas, e `materialize_publication.py` copia somente documentos e recursos alcançáveis. A saída atual combina esses documentos para HTML de impressão e PDF. O novo site precisa reutilizar essa autoridade sem fazer Hugo ler diretamente toda a árvore do repositório.

O site continuará sendo o módulo completo do Mestre. GitHub Pages não fornece controle de acesso para o site estático comum; portanto, sua implantação torna publicamente acessíveis os segredos do Mestre que já estejam no manifesto. Imagens apenas aprovadas na curadoria continuam inelegíveis até serem promovidas para uma fonte publicável, referenciadas por ela e alcançadas pelo manifesto.

Hugo Extended 0.164.0 já está disponível localmente e o `gh` está autenticado como `filipeaguiar`. O repositório local não possui remoto. `filipeaguiar/atlas` já existe como repositório privado e divergente; foi aprovada explicitamente a substituição de sua `main` pelo estado e histórico do repositório local.

## Goals / Non-Goals

**Goals:**

- gerar um site navegável e responsivo a partir da mesma seleção positiva do PDF;
- preservar ordem, títulos, seções, idioma, versão e estado de desenvolvimento do manifesto;
- impedir publicação acidental de fontes internas ou não declaradas;
- oferecer build local reproduzível e implantação automática no GitHub Pages;
- funcionar tanto em domínio de usuário quanto em subdiretório de projeto, sem URL fixa no código.

**Non-Goals:**

- criar livro do jogador, edição pública separada ou filtragem de segredos do Mestre;
- transformar aprovação de curadoria de imagem em aprovação de publicação;
- editar conteúdo pelo Hugo ou duplicar manualmente capítulos em `content/`;
- hospedar busca com servidor, comentários, autenticação ou CMS;
- substituir o pipeline de PDF ou publicar PDFs no site, no artefato Pages ou em releases;

## Decisions

### Reutilizar o plano editorial existente

`tools/generate_site.py` chamará `prepare_publication()` em modo estrito e consumirá o mesmo `PublicationPlan` usado pelo PDF. Não haverá descoberta automática por diretório. Isso evita divergência entre produtos e mantém todas as recusas de front matter, caminho, link e recurso.

Alternativa considerada: apontar `contentDir` do Hugo para `cenario/`, `campanha/` e `regras/`. Foi rejeitada porque publicaria por presença, ignoraria a ordem positiva e aumentaria o risco de vazar arquivos não manifestados.

### Montar um projeto Hugo descartável

Arquivos autorais de apresentação ficarão em `publicacao/hugo/` — configuração-base, layouts, partials e assets. O gerador criará um projeto completo em `build/hugo/`, com `content/`, `static/recursos/` e dados editoriais derivados. Hugo produzirá o artefato final em `build/site/`. Ambas as árvores de `build/` serão descartáveis.

Cada seção terá uma página de lista e cada documento uma página própria, com pesos derivados da ordem do manifesto. A abertura alimentará a página inicial; seções vazias aparecerão como “Em preparação”. Links entre documentos declarados serão convertidos para URLs internas estáveis e recursos locais receberão nomes derivados de hash para evitar colisões.

Alternativa considerada: gerar um único HTML por meio do renderizador atual. Foi rejeitada porque perderia navegação própria, taxonomia de páginas e recursos nativos do Hugo.

### Tema próprio mínimo, sem módulo remoto

O site usará layouts e CSS locais, responsivos, com navegação lateral em telas largas e navegação compacta em telas pequenas. Não haverá tema Git submodule nem módulo baixado durante o build. Isso reduz dependências de rede e permite controlar a apresentação do conteúdo do Mestre.

### Base URL fornecida no build

A configuração não fixará proprietário ou nome do repositório. Localmente, o script aceitará `--base-url`; no workflow, `actions/configure-pages` fornecerá a URL efetiva e o build a passará ao Hugo. Todos os links e assets usarão mecanismos de URL do Hugo, permitindo Pages em subdiretório.

### Implantação oficial do GitHub Pages

`.github/workflows/pages.yml` executará em push para `main` e por acionamento manual. O job de build terá apenas permissão de leitura, instalará uma versão fixada do Hugo Extended, executará testes e build estrito e enviará exclusivamente `build/site/` por `actions/upload-pages-artifact`. Um job separado, com permissões `pages: write` e `id-token: write`, fará a implantação com `actions/deploy-pages` e ambiente `github-pages`.

A concorrência será limitada ao grupo `pages`, cancelando builds antigos sem interromper uma implantação já em andamento.

### Verificação negativa da saída

Além das validações de entrada, testes confirmarão que nenhum arquivo ou metadado da saída contém caminhos ou conteúdo vindo de `desenvolvimento/`, `historico/`, `recuperacao/`, `referencias/`, `openspec/`, `publicacao/stubs/` ou saídas descartáveis. O workflow nunca enviará a raiz do repositório como artefato Pages.

## Risks / Trade-offs

- **[Segredos do Mestre ficam publicamente acessíveis]** → Exibir claramente que o site é um módulo para o Mestre e exigir que somente conteúdo explicitamente manifestado seja publicado; não prometer controle de acesso.
- **[PDF e site renderizam Markdown de modo diferente]** → Compartilhar seleção, links e recursos, e testar estrutura e conteúdo essencial; aceitar diferenças tipográficas próprias de cada mídia.
- **[Mudança de versão do Hugo altera a saída]** → Fixar a versão no workflow e documentar a versão local suportada.
- **[Links relativos quebram em GitHub Pages de projeto]** → Construir com a URL retornada por `configure-pages` e testar uma base URL com subcaminho.
- **[Arquivos internos entram no artefato por configuração do Hugo]** → Gerar um source tree positivo dentro de `build/` e enviar somente `build/site/`.
- **[Repositório sem remoto impede implantação imediata]** → Manter build local funcional e tratar configuração do remoto/Pages como pré-condição operacional, não como motivo para enfraquecer o pipeline.

## Migration Plan

1. Implementar e validar localmente o materializador Hugo e o tema próprio.
2. Executar testes e build estrito com uma base URL de subdiretório.
3. Adicionar o workflow sem alterar o pipeline do PDF.
4. Associar `filipeaguiar/atlas` como remoto e substituir sua `main` pelo histórico local com proteção explícita contra envio de saídas descartáveis.
5. Selecionar “GitHub Actions” como origem do Pages nas configurações do repositório.
6. Acionar manualmente o primeiro deploy e revisar navegação, assets e ausência de áreas proibidas.
7. Em caso de problema, desabilitar Pages ou reverter o workflow; o PDF e as fontes permanecem inalterados.

## Open Questions

- O repositório permanece privado ou será tornado público? Se permanecer privado, a disponibilidade de GitHub Pages depende do plano da conta.
- Um domínio personalizado poderá ser configurado futuramente; não faz parte desta mudança.
