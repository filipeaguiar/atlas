## Why

O conteúdo aprovado hoje pode ser consultado apenas por meio do PDF incremental, o que dificulta navegação rápida, leitura em telas menores e acesso por links. Um site Hugo publicado no GitHub Pages oferece uma apresentação web contínua sem criar uma segunda seleção editorial nem expor fontes internas.

## What Changes

- Adicionar um site Hugo para o módulo completo dirigido ao Mestre.
- Materializar no site somente documentos declarados, em ordem, por `publicacao/manifest.yml` e aceitos pelas validações editoriais existentes.
- Gerar navegação por seções e capítulos, página inicial, metadados de versão e aviso de material em desenvolvimento.
- Copiar apenas recursos locais alcançáveis a partir dos documentos publicados e reescrever seus links para URLs seguras do site.
- Adicionar workflow do GitHub Actions para validação, build estrito do Hugo e implantação no GitHub Pages.
- Impedir que `desenvolvimento/`, `historico/`, `recuperacao/`, `referencias/`, stubs, saídas descartáveis ou qualquer fonte fora do manifesto sejam publicadas.
- Manter o PDF e o site como saídas diferentes da mesma seleção positiva, sem criar edição pública ou livro do jogador.

## Capabilities

### New Capabilities

- `site-hugo-do-mestre`: materialização e renderização navegável, em Hugo, do conteúdo aprovado do módulo do Mestre.
- `implantacao-github-pages`: build reproduzível e publicação segura do site pelo GitHub Actions no GitHub Pages do repositório.

### Modified Capabilities

Nenhuma.

## Impact

A mudança afeta o pipeline em `tools/`, acrescenta configuração, layouts e estilos do Hugo, cria uma saída web descartável e adiciona um workflow em `.github/workflows/`. Hugo Extended passa a ser requisito local e de CI. O repositório local será associado a `filipeaguiar/atlas`, cuja `main` divergente será substituída mediante autorização explícita. PDFs continuam apenas como saídas locais descartáveis e não serão publicados no Pages ou em releases.
