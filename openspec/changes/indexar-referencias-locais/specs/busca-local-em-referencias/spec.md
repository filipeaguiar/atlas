## ADDED Requirements

### Requirement: Somente referências catalogadas são indexadas
O sistema MUST processar apenas arquivos explicitamente declarados no catálogo de referências e localizados dentro de `referencias/` na raiz atual.

#### Scenario: Livro presente e catalogado
- **WHEN** um arquivo coincide com uma entrada válida do catálogo
- **THEN** ele pode ser fragmentado com seu título, edição e identificador declarados

#### Scenario: Caminho externo ou não catalogado
- **WHEN** uma entrada sai da raiz, usa link externo ou um livro não consta no catálogo
- **THEN** o sistema recusa a indexação e identifica o caminho problemático

### Requirement: Chonkie produz fragmentos rastreáveis
Cada fragmento MUST preservar identificador do livro, hash da fonte, offsets, contagem de palavras e página aproximada quando houver marcadores de página.

#### Scenario: Fonte inalterada
- **WHEN** o mesmo catálogo e os mesmos livros são reindexados
- **THEN** os identificadores e metadados dos fragmentos permanecem determinísticos

#### Scenario: Livro sem marca de página
- **WHEN** a conversão não contém caracteres de quebra de formulário
- **THEN** o fragmento mantém offsets exatos e registra página aproximada como nula

### Requirement: Busca textual local retorna citações limitadas
O sistema MUST consultar o índice com SQLite FTS5, ordenar resultados por relevância e exibir somente trechos limitados acompanhados de fonte e localização.

#### Scenario: Termo encontrado
- **WHEN** o usuário pesquisa uma regra presente no índice
- **THEN** recebe título, edição, página aproximada, offsets e um pequeno trecho destacado

#### Scenario: Limites solicitados acima do máximo
- **WHEN** uma consulta pede resultados ou trechos acima dos limites seguros
- **THEN** a ferramenta aplica os máximos configurados ou recusa o valor

### Requirement: Referências permanecem fora do produto
Livros, fragmentos e banco de busca MUST NOT entrar no Git, no manifesto ou no PDF do módulo.

#### Scenario: Repositório e publicação
- **WHEN** o índice é gerado
- **THEN** somente arquivos ignorados sob `build/retrieval/` são criados e nenhuma fonte editorial é alterada

### Requirement: Resultado não concede autoridade canônica
A interface MUST identificar resultados como `referencia-externa` e MUST NOT apresentá-los como fato do cenário ou texto publicável.

#### Scenario: Regra localizada
- **WHEN** uma busca encontra uma passagem mecânica
- **THEN** a saída orienta a conferência na obra e não altera fontes editoriais
