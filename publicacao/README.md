# Publicação incremental

`publicacao/manifest.yml` é a única lista positiva de documentos do livro. A presença de um arquivo canônico na árvore não o publica automaticamente.

O projeto produz somente o módulo completo destinado ao Mestre. Não existe perfil público ou livro do jogador. Handouts, quando aprovados, entram no próprio módulo na seção correspondente e são entregues aos jogadores apenas por decisão do Mestre.

## Build incremental

```bash
uv run python tools/generate_pdf.py
```

Links para capítulos ainda ausentes são registrados como avisos em `build/relatorio-publicacao.json`.

## Build estrito

```bash
uv run python tools/generate_pdf.py --strict
```

O modo estrito falha se houver links ou recursos locais ausentes e deve ser usado para releases finais.

## Saídas descartáveis

- `publicacao/conteudo/`: fontes materializadas, sumário, Markdown combinado e HTML;
- `build/herdeiros-da-vanguarda-<versão>.pdf`: preview do livro;
- `build/relatorio-publicacao.json`: fontes, hashes, avisos e ferramenta utilizada.

Nunca edite essas saídas manualmente.
