## ADDED Requirements

### Requirement: Mapa completo das posições da saga
O projeto SHALL manter um grafo Mermaid editorial com exatamente 23 posições de aventura, agrupadas em Arco I (1–6), Arco II (7–16) e Arco III (17–23), incluindo os Marcos entre os arcos.

#### Scenario: Contagem e agrupamento
- **WHEN** o mapa editorial é validado
- **THEN** todas as posições de 1 a 23 aparecem uma única vez e pertencem ao arco correto

### Requirement: Distinção de autoridade editorial
O mapa MUST distinguir visual e textualmente fatos fixos, consequências condicionais, variáveis do Pacote de Antagonista e lacunas editoriais.

#### Scenario: Posição ainda indefinida
- **WHEN** uma função de aventura ainda não foi aprovada
- **THEN** o nó correspondente é identificado como lacuna editorial e não recebe silenciosamente evento, antagonista ou resultado

#### Scenario: Elemento dependente do Pacote
- **WHEN** um nó depende de identidade, motivação, sinal, força, Frente ou contrajogo do Pacote
- **THEN** o elemento aparece como variável do Pacote, sem seleção padrão

### Requirement: Âncoras estruturais preservadas
O mapa SHALL preservar a abertura pelo Exame de Admissão, o encerramento do Arco I pela licença provisória, a segunda operação de captura na Aventura 14, suas consequências na Aventura 15, a conclusão do Arco II na Aventura 16 e o encerramento do legado na Aventura 23.

#### Scenario: Operação da Aventura 14
- **WHEN** a Aventura 14 é representada
- **THEN** o mapa fixa a ocorrência da segunda operação de captura e mantém a captura física como resultado condicional

#### Scenario: Encadeamento das Aventuras 14 a 16
- **WHEN** o trecho final do Arco II é consultado
- **THEN** o estado produzido na Aventura 14 alimenta a Aventura 15 e a Aventura 16 preserva sua função de encerramento institucional

### Requirement: Grafo não prescritivo
As arestas do mapa MUST representar sucessão editorial, dependência de informação, consequência ou Marco, e MUST NOT declarar uma sequência obrigatória de cenas ou um único resultado válido.

#### Scenario: Solução inesperada
- **WHEN** os personagens produzem um estado coerente não antecipado
- **THEN** a dependência seguinte pode receber esse estado sem exigir retorno a um caminho predefinido

### Requirement: Isolamento do planejamento
O grafo editorial SHALL permanecer em `desenvolvimento/` e MUST NOT ser selecionado pelo manifesto ou materializado no PDF.

#### Scenario: Geração do módulo
- **WHEN** o PDF do Mestre é gerado
- **THEN** o Mermaid editorial, sua legenda e suas lacunas não aparecem nos artefatos de publicação

### Requirement: Atualização incremental auditável
O mapa SHALL ser atualizado à medida que funções e aventuras forem aprovadas, preservando a diferença entre estado planejado, revisado e canônico.

#### Scenario: Aprovação de uma aventura
- **WHEN** uma aventura recebe aprovação explícita
- **THEN** sua posição pode deixar de ser lacuna, e a alteração correspondente é revisável no histórico do projeto
