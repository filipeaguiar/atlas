## Why

O projeto precisa de versões incrementais do livro para acompanhar organização, volume, navegação e qualidade visual enquanto o conteúdo é reconstruído. A publicação deve permanecer um único módulo direcionado ao Mestre, sem criar edição pública ou incluir automaticamente tudo que existe na árvore.

## What Changes

- Criar `publicacao/manifest.yml` como lista positiva e ordenada das fontes do livro.
- Materializar somente documentos canônicos, aprovados e publicáveis em uma área descartável.
- Gerar HTML paginado e PDF com Google Chrome headless, capa, sumário, seções, estilos e numeração.
- Produzir versões incrementais identificadas pelo número declarado no manifesto.
- Incluir handouts dentro do próprio módulo, em seção específica e com páginas entregáveis separadas das instruções do Mestre.
- Oferecer modo incremental, que registra links ou elementos ainda indisponíveis, e modo estrito para releases sem pendências.
- Gerar relatório com documentos, hashes, avisos, erros, ferramenta e arquivos resultantes.
- Recusar referências externas, áreas internas, stubs, saídas derivadas e qualquer fonte não declarada.
- Não gerar PDF público, livro de jogador ou handout independente automaticamente.

## Capabilities

### New Capabilities
- `manifesto-do-livro-do-mestre`: define seleção positiva, ordem, seções, versão e regras de elegibilidade do conteúdo publicado.
- `pdf-incremental-do-mestre`: materializa o módulo, renderiza HTML/PDF incremental e incorpora handouts sob controle do Mestre.

### Modified Capabilities

## Impact

A mudança adiciona manifesto, materializador, gerador de PDF, template, CSS, dependência de renderização Markdown, testes e documentação. As saídas ficam em `publicacao/conteudo/` e `build/`. O Google Chrome local é a única dependência de sistema. Nenhum livro em `referencias/` ou índice Chonkie participa da publicação.
