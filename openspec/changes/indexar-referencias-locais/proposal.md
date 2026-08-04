## Why

Os livros locais em `referencias/` são necessários para conferir regras de 3DeT Victory, mas são extensos, possuem OCR imperfeito e não podem ser confundidos com cânone ou material publicável. É necessário permitir busca rápida e rastreável sem versionar, publicar ou copiar automaticamente seu conteúdo para o módulo.

## What Changes

- Catalogar explicitamente referências locais por título, edição e caminho esperado.
- Usar Chonkie para fragmentar os livros sem exigir front matter editorial.
- Criar um índice SQLite FTS5 separado dos índices canônicos.
- Oferecer busca textual local com ranking, trechos limitados, caminho, hash e página aproximada.
- Manter livros e índice fora do Git e do manifesto de publicação.
- Recusar caminhos externos, fontes não catalogadas e saídas fora de `build/retrieval/`.

## Capabilities

### New Capabilities
- `busca-local-em-referencias`: indexa e consulta livros de referência locais sem lhes conceder autoridade canônica ou publicabilidade.

### Modified Capabilities
- `indexacao-editorial-local`: esclarece que o índice editorial e o índice de referências possuem entradas, metadados e finalidades separadas.

## Impact

A mudança adiciona catálogo rastreado, scripts de indexação e busca, testes e regras de exclusão no Git. Reutiliza Chonkie 1.7.0 e a biblioteca SQLite do Python, sem embeddings, banco externo ou serviços de rede.
