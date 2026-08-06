# Publicação incremental

`publicacao/manifest.yml` é a única lista positiva de documentos do livro. A presença de um arquivo canônico na árvore não o publica automaticamente.

O projeto produz somente o módulo completo destinado ao Mestre. Não existe perfil público ou livro do jogador. Handouts, quando aprovados, entram no próprio módulo na seção correspondente e são entregues aos jogadores apenas por decisão do Mestre.

A seção com `papel: abertura` é renderizada em uma coluna entre a capa e o sumário. Seções com `papel: conteudo` formam o corpo numerado; `papel: handouts` acrescenta orientação reservada ao Mestre antes de cada material entregável.

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

## Site Hugo do Mestre

O site usa exatamente a mesma seleção positiva do manifesto e exige **Hugo Extended 0.164.0**:

```bash
uv run python tools/generate_site.py
```

Para simular a URL do GitHub Pages do projeto:

```bash
uv run python tools/generate_site.py \
  --base-url https://filipeaguiar.github.io/atlas/
```

A saída fica em `build/site/`. O site é o módulo integral dirigido ao Mestre: quando implantado no GitHub Pages, seus segredos ficam publicamente acessíveis. Não existe filtragem automática para jogadores.

Aprovar uma imagem na curadoria não a publica. Ela só entra no site depois de ser promovida para uma raiz editorial permitida, referenciada por um documento manifestado e aceita pelo build estrito.

O workflow `.github/workflows/pages.yml` testa, gera e envia exclusivamente `build/site/` ao GitHub Pages. **Nenhum PDF é publicado.**

## Saídas descartáveis

- `publicacao/conteudo/`: fontes materializadas, sumário, Markdown combinado e HTML;
- `build/hugo/`: projeto Hugo materializado;
- `build/site/`: site estático gerado;
- `build/herdeiros-da-vanguarda-<versão>.pdf`: preview local do livro, nunca publicado pelo Pages;
- `build/relatorio-publicacao.json`: relatório do PDF;
- `build/relatorio-site.json`: relatório do site.

Nunca edite essas saídas manualmente.
