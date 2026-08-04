# Referências locais de regras

Os arquivos em `referencias/` são cópias locais de obras externas protegidas por direitos autorais. Eles não são fontes editoriais do módulo, não definem o cânone de **Herdeiros da Vanguarda** e nunca entram no manifesto ou no PDF.

Os livros Markdown são ignorados pelo Git. Somente o catálogo `config/references.yml`, que contém metadados e caminhos esperados, é versionado.

## Criar o índice

```bash
uv run python tools/index_references.py
```

A saída local fica em `build/retrieval/referencias.sqlite` e também é ignorada.

## Pesquisar

```bash
uv run python tools/search_references.py "Ataque Especial"
uv run python tools/search_references.py "Ganho Perda" --limit 8
```

Cada resultado informa obra, edição, página aproximada e offsets da conversão. A página é estimada pelas quebras presentes no arquivo e deve ser conferida na obra original.

Resultados servem para consulta mecânica. Não copie passagens automaticamente para o módulo e não trate uma referência externa como fato do cenário.
