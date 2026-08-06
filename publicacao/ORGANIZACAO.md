# Regras de Publicação e Materializador

Este arquivo define como o conteúdo é processado para a publicação do livro/módulo.

## O Materializador
- O Materializador é um script que compila as fontes no produto final.
- Ele **deve recusar terminantemente** fontes originadas de diretórios de uso interno, como `desenvolvimento/`, `historico/`, `recuperacao/` e `publicacao/stubs/`.

## Manifesto de Publicação
- A pasta `publicacao/fontes/` contém apenas adaptações editoriais aprovadas e deve rastrear suas fontes canônicas.
- Um arquivo só entra no produto publicado **quando e somente quando** o arquivo `publicacao/manifest.yml` o declara explicitamente.
- Arquivos que possuírem a flag (frontmatter) `publicar: false` serão sumariamente ignorados.
- Stubs (rascunhos) nunca entram na publicação. Devem migrar para a árvore canônica (`campanha/aventuras/`) quando aprovados, antes de serem inseridos no manifesto.
