## Context

`referencias/` contém conversões locais completas de 3DeT Victory e Ferozes e Furiosos. Esses arquivos são material externo protegido por direitos autorais, sem front matter e com marcas de página por quebra de formulário. O indexador editorial atual exige `status: canon` e, corretamente, não os processa.

## Goals / Non-Goals

**Goals:**
- pesquisar termos e regras localmente;
- preservar livro, edição, hash, offsets e página aproximada;
- limitar resultados a pequenos trechos para consulta;
- manter isolamento absoluto do cânone e da publicação.

**Non-Goals:**
- publicar ou versionar os livros;
- transformar referências em cânone;
- fornecer cópias extensas do texto;
- implementar busca semântica ou embeddings;
- corrigir automaticamente o OCR.

## Decisions

- Manter um catálogo rastreado em `config/references.yml`; somente arquivos listados podem ser indexados.
- Fragmentar texto bruto com `RecursiveChunker`, tokenizer por palavras e regras locais de parágrafo e sentença.
- Calcular página aproximada contando caracteres `\f` antes do início do fragmento; quando não houver marcadores, registrar `null`.
- Armazenar fragmentos em `build/retrieval/referencias.sqlite` usando FTS5 `unicode61 remove_diacritics 2` e ranking BM25.
- Limitar número de resultados e tamanho dos trechos exibidos pela CLI.
- Fixar caminhos dentro da raiz atual, impedir links simbólicos externos e manter `referencias/*.md` no `.gitignore`.

## Risks / Trade-offs

- **OCR reduz qualidade da busca** → busca textual tolera acentos e sempre mostra fonte e posição para conferência.
- **Página aproximada pode divergir do impresso** → rotular como aproximada e conservar offsets exatos.
- **Trechos protegidos podem ser copiados em excesso** → limites conservadores de resultados e snippets; índice permanece local.
- **Resultado pode ser tratado como regra canônica** → metadados e documentação declaram `autoridade: referencia-externa`.
