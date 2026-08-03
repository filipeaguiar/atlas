## Context

O repositório novo está vazio e `Atlas.bkp` contém o projeto anterior. A recuperação será seletiva. Chonkie será usado somente depois que um documento entrar na árvore atual e receber metadados editoriais aprovados.

## Goals / Non-Goals

**Goals:**
- fragmentar Markdown localmente e de modo reproduzível;
- preservar caminho, hash, front matter, audiência e cabeçalho em cada fragmento;
- impedir indexação da cópia de segurança e de áreas internas;
- manter o índice como saída descartável.

**Non-Goals:**
- copiar conteúdo de `Atlas.bkp`;
- decidir cânone ou proveniência;
- adicionar embeddings, RAG, servidor ou banco vetorial;
- publicar o índice ou usá-lo na geração do livro.

## Decisions

- Fixar `chonkie==1.7.0` e usar somente a instalação base.
- Usar `RecursiveChunker` com regras locais de Markdown, tokenizer por palavras e tamanho explícito; não baixar receitas remotas.
- Aceitar apenas Markdown sob `cenario/`, `campanha/`, `regras/` e `apendices/`, com `status: canon` e sem `publicar: false`.
- Separar audiências `publico` e `mestre`; a pública exclui `camada: mestre` e `conteudo_para_jogadores: false`.
- Produzir JSON determinístico com hashes e IDs de fragmento, sem data de geração.

## Risks / Trade-offs

- **Chonkie não conhece as regras editoriais** → o wrapper valida caminhos e front matter antes de chamá-lo.
- **Segredos podem entrar no índice público** → perfis separados e testes de isolamento.
- **Dependência excessiva para poucos arquivos** → instalação base, sem extras, e interface própria pequena.
- **Mudanças futuras no Chonkie** → versão fixada e lockfile.
