## Context

A árvore contém fontes canônicas em reconstrução, documentos mecânicos ainda sem metadados, referências externas protegidas e saídas derivadas. O progresso precisa ser visível em PDF sem enfraquecer a regra de publicação por lista positiva. O único leitor-alvo do módulo é o Mestre; materiais para jogadores aparecem como handouts dentro do livro e só são entregues por decisão do Mestre.

O ambiente possui Google Chrome, mas não Pandoc, LaTeX ou Typst. O projeto já usa Python com `uv`, PyYAML e saídas ignoradas em `build/` e `publicacao/conteudo/`.

## Goals / Non-Goals

**Goals:**
- produzir um PDF legível em qualquer estágio da reconstrução;
- selecionar e ordenar fontes por manifesto explícito;
- validar metadados, caminhos, links e isolamento editorial;
- criar capa, sumário navegável, hierarquia visual e numeração;
- incorporar handouts numa seção do módulo;
- registrar exatamente o que entrou em cada versão.

**Non-Goals:**
- gerar edição pública ou livro do jogador;
- descobrir e publicar arquivos automaticamente;
- transformar rascunhos ou referências em conteúdo;
- escrever ou revisar o conteúdo dos capítulos;
- extrair handouts automaticamente como produtos separados;
- produzir o acabamento gráfico definitivo da edição comercial.

## Decisions

### 1. Manifesto positivo e versionado

`publicacao/manifest.yml` declarará título, subtítulo, versão, idioma, nome-base da saída e seções ordenadas. Cada documento terá `origem`, e opcionalmente `titulo` e `papel`. Somente caminhos declarados serão considerados.

Fontes devem permanecer em `cenario/`, `campanha/`, `regras/`, `apendices/` ou adaptações aprovadas em `publicacao/fontes/`. O materializador recusará `referencias/`, `desenvolvimento/`, `historico/`, `recuperacao/`, `publicacao/stubs/`, `publicacao/conteudo/`, `build/` e caminhos externos.

**Alternativa rejeitada:** descobrir todos os arquivos com `status: canon`. Existência física não equivale a decisão de publicação.

### 2. Elegibilidade validada antes da cópia

Cada fonte deverá possuir front matter válido, `status: canon`, `publicar` diferente de `false`, identificador e título. O destino materializado será derivado do caminho de origem, evitando destinos arbitrários e colisões. Hashes SHA-256 serão registrados.

Arquivos ausentes, duplicados, inelegíveis ou fora das raízes permitidas sempre interrompem o build. Links locais quebrados serão avisos no modo incremental e erros no modo estrito.

### 3. Pipeline Markdown → HTML → PDF

O materializador copiará fontes elegíveis para `publicacao/conteudo/`, removerá front matter da versão renderizada e produzirá um documento combinado. A biblioteca Python-Markdown, com tabelas, listas e código, gerará HTML sem acessar rede. Um template e CSS próprios fornecerão capa, sumário, cabeçalhos, blocos do Mestre, tabelas e quebras de página.

O Chrome headless imprimirá o HTML em PDF. O executável será encontrado por `CHROME_BIN` ou caminhos conhecidos. Falta do navegador produzirá erro acionável.

**Alternativa rejeitada:** adicionar Pandoc ou uma distribuição LaTeX. Nenhuma está instalada e ambas ampliariam o ambiente antes de validar o fluxo editorial.

### 4. Um único livro para o Mestre

Não haverá parâmetro de audiência nem PDF público. Todo o conteúdo do manifesto pertence ao livro do Mestre. Marcações como `camada: mestre` continuam úteis para indicar conhecimento, não para criar outra edição.

O nome do PDF combinará nome-base e versão saneada, por exemplo `herdeiros-da-vanguarda-0.1.0-dev.1.pdf`.

### 5. Handouts dentro do módulo

Handouts canônicos viverão em `apendices/handouts/` e serão declarados numa seção `papel: handouts`. O front matter armazenará orientação do Mestre, condição de entrega e aquilo que o material revela; o corpo será a página entregável.

No PDF, cada handout receberá primeiro uma caixa de orientação do Mestre e, após quebra de página, a parte entregável isolada. O gerador não criará automaticamente arquivos separados.

### 6. Modos incremental e estrito

O modo incremental é o padrão para acompanhar progresso. Ele permite links a capítulos ainda indisponíveis, registra cada pendência no relatório e marca a edição como desenvolvimento na capa. Isso não permite fontes inelegíveis ou ausentes no próprio manifesto.

`--strict` transforma links e recursos locais ausentes em erros e será obrigatório para uma release final. O relatório indicará o modo usado.

### 7. Relatório rastreável

`build/relatorio-publicacao.json` registrará versão, modo, Chrome, documentos e hashes, ordem, avisos, recursos, HTML e PDF produzidos e um digest do conjunto de entradas. Data operacional poderá aparecer no relatório, mas não será usada como autoridade editorial.

## Risks / Trade-offs

- **Chrome pode variar a paginação entre versões** → registrar versão do navegador e tratar o PDF como preview incremental.
- **Links quebrados podem esconder lacunas** → relatório explícito e modo estrito obrigatório para release.
- **Handout pode carregar instrução do Mestre na página entregável** → separar metadados de orientação e corpo por quebra controlada.
- **Conteúdo não revisado pode parecer pronto por estar diagramado** → capa e rodapé identificam versões `dev` como desenvolvimento.
- **Markdown complexo pode renderizar de forma inconsistente** → limitar extensões, criar fixtures e validar tabelas, imagens e quebras.
- **Fontes externas podem vazar** → allowlist de raízes e testes negativos para `referencias/` e áreas internas.
