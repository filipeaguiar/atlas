# Herdeiros da Vanguarda

Nova árvore editorial da campanha, reconstruída gradualmente a partir de uma cópia de segurança somente leitura.

## Princípio de recuperação

`/home/filipe/Documentos/Projetos/Atlas.bkp` não é uma fonte ativa. Cada elemento recuperado deve ser examinado, incorporado individualmente e receber metadados de proveniência antes de ser tratado como conteúdo do projeto.

## Ambiente

```bash
uv sync --frozen
```

O projeto fixa **Chonkie 1.7.0** apenas para fragmentação local de Markdown. Não são instalados extras de embeddings, LLMs ou bancos vetoriais.

## Índice editorial

Índice público:

```bash
uv run python tools/build_retrieval_index.py --audience publico
```

Índice completo para o Mestre:

```bash
uv run python tools/build_retrieval_index.py --audience mestre
```

As saídas são geradas em `build/retrieval/` e não são versionadas. Somente arquivos Markdown nas raízes configuradas, com `status: canon` e sem `publicar: false`, podem ser processados.

O perfil público também exclui documentos com `camada: mestre` ou `conteudo_para_jogadores: false`. Chonkie não determina cânone nem recupera conteúdo ausente: ele apenas divide fontes já aprovadas para consulta posterior.

## Referências locais de regras

Os livros em `referencias/` permanecem fora do Git e da publicação. Para criar e consultar o índice local separado:

```bash
uv run python tools/index_references.py
uv run python tools/search_references.py "Ataque Especial"
```

Consulte [REFERENCIAS.md](REFERENCIAS.md) para limites de uso e proveniência.

## Testes

```bash
uv run pytest
openspec validate --all --strict --no-interactive
```
