## ADDED Requirements

### Requirement: Manifesto é a única seleção positiva do livro
O sistema MUST incluir somente documentos declarados em `publicacao/manifest.yml` e MUST preservar a ordem de seções e documentos ali definida.

#### Scenario: Arquivo canônico não declarado
- **WHEN** um documento elegível existe na árvore mas não aparece no manifesto
- **THEN** ele não é materializado nem incluído no PDF

#### Scenario: Documento declarado duas vezes
- **WHEN** a mesma origem aparece mais de uma vez
- **THEN** a validação falha antes da materialização

### Requirement: Manifesto identifica a versão incremental
O manifesto MUST declarar título, versão, idioma e nome-base de saída suficientes para identificar o artefato.

#### Scenario: Build de desenvolvimento
- **WHEN** a versão é `0.1.0-dev.1`
- **THEN** o PDF e o relatório utilizam essa versão e a capa indica que o material está em desenvolvimento

#### Scenario: Versão ou nome inseguro
- **WHEN** um valor produziria caminho externo ou nome de arquivo inválido
- **THEN** o sistema recusa o manifesto

### Requirement: Fontes publicadas são elegíveis e confinadas
Cada origem MUST permanecer numa raiz editorial permitida, possuir front matter válido, `status: canon`, identificador e título, e MUST NOT declarar `publicar: false`.

#### Scenario: Referência externa declarada
- **WHEN** o manifesto aponta para `referencias/` ou para outro caminho proibido
- **THEN** a validação falha e nenhum produto é gerado

#### Scenario: Marcador ou rascunho declarado
- **WHEN** uma origem é pendente, stub, não publicável ou não possui metadados
- **THEN** a validação falha e identifica o arquivo

### Requirement: Publicação possui apenas audiência do Mestre
O manifesto MUST representar um único módulo dirigido ao Mestre e MUST NOT definir perfil público, livro do jogador ou seleção automática por audiência.

#### Scenario: Conteúdo secreto declarado
- **WHEN** um capítulo `camada: mestre` está no manifesto
- **THEN** ele entra no mesmo livro principal sem criar artefato público alternativo

### Requirement: Handouts pertencem a uma seção do módulo
Todo handout publicado MUST estar declarado em seção apropriada do manifesto e MUST permanecer dentro do PDF do Mestre.

#### Scenario: Handout disponível
- **WHEN** um documento de `apendices/handouts/` é declarado na seção de handouts
- **THEN** ele aparece no sumário e no corpo do mesmo módulo

#### Scenario: Handout não declarado
- **WHEN** um handout existe mas não aparece no manifesto
- **THEN** ele não é incluído nem exportado separadamente
